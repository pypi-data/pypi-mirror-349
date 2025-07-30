from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from django.test import RequestFactory
from django.utils.datastructures import MultiValueDict

from django_nextjs.app_settings import NEXTJS_SERVER_URL
from django_nextjs.render import _get_render_context, render_nextjs_page_to_string
from django_nextjs.views import nextjs_page


def test_get_render_context_empty_html():
    assert _get_render_context("") is None


def test_get_render_context_html_without_children():
    assert _get_render_context("<html></html>") is None


def test_get_render_context_html_with_empty_sections():
    assert _get_render_context("<html><head></head><body></body></html>") is None


def test_get_render_context_html_with_incomplete_sections():
    assert (
        _get_render_context(
            """<html><head></head><body><div id="__django_nextjs_body_begin"/>
            <div id="__django_nextjs_body_end"/></body></html>"""
        )
        is None
    )


def test_get_render_context_html_with_sections_and_content():
    html = """<html><head><link/></head><body id="__django_nextjs_body"><div id="__django_nextjs_body_begin"/><div id="__django_nextjs_body_end"/></body></html>"""
    expected_context = {
        "django_nextjs__": {
            "section1": "<html><head>",
            "section2": "<link/>",
            "section3": '</head><body id="__django_nextjs_body">',
            "section4": '<div id="__django_nextjs_body_begin"/>',
            "section5": '<div id="__django_nextjs_body_end"/></body></html>',
        }
    }
    assert _get_render_context(html) == expected_context

    context = {"extra_context": "content"}
    assert _get_render_context(html, context) == {**expected_context, **context}


@pytest.mark.asyncio
async def test_nextjs_page(rf: RequestFactory):
    path = "random/path"
    params = MultiValueDict({"name": ["Adrian", "Simon"], "position": ["Developer"]})
    request = rf.get(f"/{path}", data=params)
    nextjs_response = "<html><head></head><body></body></html>"

    with patch("aiohttp.ClientSession") as mock_session:
        with patch("aiohttp.ClientSession.get") as mock_get:
            mock_get.return_value.__aenter__.return_value.text = AsyncMock(return_value=nextjs_response)
            mock_get.return_value.__aenter__.return_value.status = 200
            mock_get.return_value.__aenter__.return_value.headers = {"Location": "target_value", "unimportant": ""}
            mock_session.return_value.__aenter__ = AsyncMock(return_value=MagicMock(get=mock_get))

            http_response = await nextjs_page(allow_redirects=True, headers={"extra": "headers"})(request)

            assert http_response.content == nextjs_response.encode()
            assert http_response.status_code == 200
            assert http_response.has_header("Location")
            assert http_response.has_header("unimportant") is False

            # Arguments passed to aiohttp.ClientSession.get
            args, kwargs = mock_get.call_args
            url = args[0]
            assert url == f"{NEXTJS_SERVER_URL}/{path}"
            assert [(k, v) for k in params.keys() for v in params.getlist(k)] == kwargs["params"]
            assert kwargs["allow_redirects"] is True

        args, kwargs = mock_session.call_args
        assert "csrftoken" in kwargs["cookies"]
        assert kwargs["headers"]["user-agent"] == ""
        assert kwargs["headers"]["x-real-ip"] == "127.0.0.1"
        assert kwargs["headers"]["extra"] == "headers"


@pytest.mark.asyncio
async def test_set_csrftoken(rf: RequestFactory):
    def get_mock_request():
        return rf.get("/random/path")

    async def get_mock_response(request: RequestFactory):
        with patch("aiohttp.ClientSession") as mock_session:
            with patch("aiohttp.ClientSession.get") as mock_get:
                mock_get.return_value.__aenter__.return_value.text = AsyncMock(return_value="<html></html>")
                mock_get.return_value.__aenter__.return_value.status = 200
                mock_session.return_value.__aenter__ = AsyncMock(return_value=MagicMock(get=mock_get))
                return await nextjs_page(allow_redirects=True)(request), mock_session

    # User does not have csrftoken and django-nextjs is not configured to guarantee one
    with patch("django_nextjs.render.ENSURE_CSRF_TOKEN", False):
        http_request = get_mock_request()
        _, mock_session = await get_mock_response(http_request)
        args, kwargs = mock_session.call_args
        # This triggers CsrfViewMiddleware to call response.set_cookie with updated csrftoken value
        assert "CSRF_COOKIE_NEEDS_UPDATE" not in http_request.META
        assert "csrftoken" not in kwargs["cookies"]

    # User does not have csrftoken and django-nextjs is configured to guarantee one
    with patch("django_nextjs.render.ENSURE_CSRF_TOKEN", True):
        http_request = get_mock_request()
        _, mock_session = await get_mock_response(http_request)
        args, kwargs = mock_session.call_args
        assert "CSRF_COOKIE_NEEDS_UPDATE" in http_request.META
        assert "csrftoken" in kwargs["cookies"]

    # User has csrftoken and django-nextjs is not configured to guarantee one
    with patch("django_nextjs.render.ENSURE_CSRF_TOKEN", False):
        http_request = get_mock_request()
        http_request.COOKIES["csrftoken"] = "whatever"
        _, mock_session = await get_mock_response(http_request)
        args, kwargs = mock_session.call_args
        assert "CSRF_COOKIE_NEEDS_UPDATE" not in http_request.META
        assert "csrftoken" in kwargs["cookies"]

    # User has csrftoken and django-nextjs is configured to guarantee one
    with patch("django_nextjs.render.ENSURE_CSRF_TOKEN", True):
        http_request = get_mock_request()
        http_request.COOKIES["csrftoken"] = "whatever"
        _, mock_session = await get_mock_response(http_request)
        args, kwargs = mock_session.call_args
        assert "CSRF_COOKIE_NEEDS_UPDATE" not in http_request.META
        assert "csrftoken" in kwargs["cookies"]


@pytest.mark.asyncio
async def test_render_nextjs_page_to_string(rf: RequestFactory):
    request = rf.get(f"/random/path")
    nextjs_response = """<html><head><link/></head><body id="__django_nextjs_body"><div id="__django_nextjs_body_begin"/><div id="__django_nextjs_body_end"/></body></html>"""

    with patch("aiohttp.ClientSession") as mock_session:
        with patch("aiohttp.ClientSession.get") as mock_get:
            mock_get.return_value.__aenter__.return_value.text = AsyncMock(return_value=nextjs_response)
            mock_session.return_value.__aenter__ = AsyncMock(return_value=MagicMock(get=mock_get))

            response_text = await render_nextjs_page_to_string(request, template_name="custom_document.html")
            assert "before_head" in response_text
            assert "after_head" in response_text
