import asyncio
from .proxies import PROXY_LIST
from .proxies.connections import check_host, check_address


__all__ = ["PROXY_LIST", "check_host", "check_address"]


async def proxy_list():
    proxies = []
    for proxy in PROXY_LIST:
        p = await proxy().get_list()
        try:
            proxies = proxies + p
        except TypeError:
            continue
    return proxies


def get_proxies():
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(proxy_list())
