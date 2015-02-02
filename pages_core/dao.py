# coding: utf-8

from .models import Page
from .strings.parse_strings import translit


def get_pages_by_title(*titles):
    """
    Вернуть страницы по названиям.

    @rtype: dict
    """
    return {
        page.title: page for page in
        Page.objects.filter(title__in=titles)
    }


def get_pages_by_urls(*urls):
    """
    @rtype: dict
    """
    return {
        page.title: page for page in
        Page.objects.filter(title__in=urls)
    }


def new_url_for(title):
    """
    Вернуть какой-нибудь URL, которого еще нет в базе.

    @rtype: basestring
    """
    translitted_title = translit(title).lower()
    url = translitted_title
    cnt = 1
    while True:
        try:
            Page.objects.get(url=url)
            url = u'%s_%s' % (translitted_title, cnt)
            cnt += 1
        except Page.DoesNotExist:
            break
    return url


def create_page(body, title, formatted_body):
    """
    Записать страницу в базу.

    Используйте create_page из logic.

    @rtype: Page
    """
    page = Page(
        body=body,
        title=title,
        formatted_body=formatted_body,
        url=new_url_for(title)
    )
    page.save()
    return page


def update_page(page, title, body, formatted_body):
    """
    Обновить страницу в базе.

    @rtype: Page
    """
    page.body = body
    page.title = title
    page.formatted_body = formatted_body
    page.save()
