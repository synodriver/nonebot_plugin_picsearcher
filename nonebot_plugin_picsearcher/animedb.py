"""
Copyright (c) 2008-2023 synodriver <diguohuangjiajinweijun@gmail.com>
"""
import io
from typing import List, Tuple

import aiohttp
import httpx
import nonebot
from lxml.html import fromstring
from nonebot.adapters.onebot.v11 import MessageSegment

# from .formdata import FormData

try:
    from .proxy import proxy
except ImportError:
    proxy = None

headers = {
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    # "Content-Type": "multipart/form-data; boundary=WebAppBoundary",
    "cache-control": "no-cache",
    "origin": "https://ai.animedb.cn",
    "pragma": "no-cache",
    "referer": "https://ai.animedb.cn/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
}


async def get_pic_from_url(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp1:
            content = await resp1.read()
    async with httpx.AsyncClient() as session:
        resp = await session.post(
            "https://aiapiv2.animedb.cn/ai/api/detect?force_one=1&model=anime",  # fuck fuck fuck, only httpx can pass waf
            files={"image": ("test.png", content, "image/png")},
            headers=headers,
        )
        return resp.json()


async def get_des(url: str):
    image_data: dict = await get_pic_from_url(url)
    if not image_data:
        msg: str = "找不到高相似度的"
        yield msg
        return
    for pic in image_data["data"][0]["char"]:
        msg = MessageSegment.text(f"动漫名:{pic['cartoonname']}，人物:{pic['name']}, ")
        yield msg


if __name__ == "__main__":
    import asyncio

    async def main():
        async for msg in get_des(
            "https://camo.githubusercontent.com/28b2b0fabbeedcc3e4cb7a38a1c4c1b63099248265abbcb1b0de5195dbb44892/68747470733a2f2f692e70697869762e6361742f696d672d6f726967696e616c2f696d672f323031392f30382f30372f30302f31332f33372f37363131363734325f70302e706e67"
        ):
            print(msg)

    asyncio.run(main())  # todo fix
