import asyncio

from aiohttp import ClientSession

import requests


async def requests_func():
    response = await requests.get("url", verify=False)


with ClientSession as Session:
    asyncio.gather(requests_func())