from selfstorage.settings import SHORTIO_DOMAIN, SHORTIO_TOKEN, SHORTIO_URL
from short_io_api_client import AuthenticatedClient
from short_io_api_client.api.link_management import post_links
from short_io_api_client.api.link_queries import get_links_by_original_url
from short_io_api_client.models import PostLinksBody


def create_short_link(long_url: str):
    """Создание короткой ссылкию."""

    client = AuthenticatedClient(
        base_url=SHORTIO_URL,
        token=SHORTIO_TOKEN,
    )
    body = PostLinksBody(
        original_url=long_url,
        domain=SHORTIO_DOMAIN,
    )
    with client as c:
        result = post_links.sync(client=c, body=body)
    if getattr(result, 'shortURL', None):
        print('result.shortURL', result.shortURL)
        return result.shortURL
    else:
        raise ValueError(f'Ошибка Short.io: {result}')


def get_clicks(long_url: str):
    """Получение кликов."""

    client = AuthenticatedClient(
        base_url=SHORTIO_URL,
        token=SHORTIO_TOKEN
    )
    with client as c:
        result = get_links_by_original_url.sync(
            client=c,
            domain=SHORTIO_DOMAIN,
            original_url=long_url,
        )
    if getattr(result, 'links', None) and len(result.links) > 0:
        return result.links[0].clicks or 0
    return 0
