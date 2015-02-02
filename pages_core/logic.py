# coding: utf-8

from .dao import (
    get_pages_by_title, get_pages_by_urls, create_page as dao_create_page,
    update_page as dao_update_page
)
from .strings import parse_markup


def get_page_by_title(title):
    """

    @rtype: Page|None
    """
    return get_pages_by_title(title).get(title)


def get_page_by_url(url):
    """
    @rtype: Page|None
    """
    return get_pages_by_urls(url).get(url)


def create_page(title, body):
    """
    Создать страницу.

    @rtype: Page
    """
    formatted_body = parse_markup(
        body, title
    )
    return dao_create_page(
        body=body,
        title=title,
        formatted_body=formatted_body
    )


def update_page(page, title, body):
    """
    @type: page
    """
    return dao_update_page(
        page,
        title=title, body=body,
        formatted_body=parse_markup(body, title)
    )
