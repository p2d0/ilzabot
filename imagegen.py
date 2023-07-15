#!/usr/bin/env python3
from EdgeGPT.ImageGen import ImageGenAsync
from BingImageCreator import HEADERS
import aiohttp
import asyncio
import json
from aiohttp_socks import ProxyType, ProxyConnector, ChainProxyConnector

class ImageGenAsyncWithProxy(ImageGenAsync):
    """
    Image generation by Microsoft Bing with SOCKS5 proxy support
    Parameters:
        auth_cookie: str
        proxy_url: str (optional)
    """

    def __init__(self, cookie_path: str, proxy_url: str = None, quiet: bool = False) -> None:
        with open(cookie_path, "r", encoding="utf8") as f:
            auth_cookie = f.read()
            cookie_json = json.loads(auth_cookie)

        cookies = {}
        for cookie in cookie_json:
            cookies[cookie["name"]] = cookie["value"]
        print(cookies)
        self.quiet = quiet;
        print(cookie)
        if proxy_url:
            connector = ProxyConnector.from_url(proxy_url)
            self.session = aiohttp.ClientSession(headers=HEADERS, cookies=cookies, connector=connector,trust_env=True)
        else:
            self.session = aiohttp.ClientSession(headers=HEADERS, cookies=cookies,trust_env=True)

async def async_image_gen(prompt):
    async with ImageGenAsyncWithProxy("./cookie.json","socks5://192.168.31.27:8093") as image_generator:
        return await image_generator.get_images(prompt)

if __name__ == '__main__':
    asyncio.run(async_image_gen("kek"))
