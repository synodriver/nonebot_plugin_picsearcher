# -*- coding: utf-8 -*-
from typing import List, Tuple
from urllib.parse import urljoin

import aiohttp
from lxml.html import fromstring
from nonebot.adapters.onebot.v11 import MessageSegment

try:
    from .proxy import proxy
except ImportError:
    proxy = None

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Origin": "https://ascii2d.net",
    "Referer": "https://ascii2d.net/",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
}


def parse_html(html: str):
    selector = fromstring(html)
    for tag in selector.xpath(
        '//div[@class="container"]/div[@class="row"]/div/div[@class="row item-box"]'
    )[1:5]:
        if pic_url := tag.xpath('./div/img[@loading="lazy"]/@src'):  # 缩略图url
            pic_url = urljoin("https://ascii2d.net/", pic_url[0])
        if description := tag.xpath("./div/div/h6/a[1]/text()"):  # 名字
            description = description[0]
        if author := tag.xpath("./div/div/h6/a[2]/text()"):  # 作者
            author = author[0]
        if origin_url := tag.xpath("./div/div/h6/a[1]/@href"):  # 原图地址
            origin_url = origin_url[0]
        if author_url := tag.xpath("./div/div/h6/a[2]/@href"):  # 作者地址
            author_url = author_url[0]
        yield pic_url, description, author, origin_url, author_url

    pass


async def get_pic_from_url(url: str):
    real_url = "https://ascii2d.net/search/uri"

    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://ascii2d.net/", headers=headers, proxy=proxy
        ) as resp1:
            html1 = await resp1.text()
        selector = fromstring(html1)
        authenticity_token = selector.xpath('//meta[@name="csrf-token"]')[0].attrib[
            "content"
        ]
        post_data = {
            "utf8": "✓",
            "authenticity_token": authenticity_token,
            "uri": url,
            "search": "",
        }
        async with session.post(
            real_url, data=post_data, proxy=proxy, headers=headers
        ) as resp:
            html: str = await resp.text()
        return [i for i in parse_html(html)]


async def get_des(url: str):
    image_data: List[Tuple] = await get_pic_from_url(url)
    if not image_data:
        msg: str = "找不到高相似度的"
        yield msg
        return
    for pic in image_data:
        msg = MessageSegment.image(file=pic[0]) + "\n"
        for i in pic[1:]:
            msg = msg + f"{i}\n"
        yield msg


if __name__ == "__main__":

    async def main():
        async for msg in get_des(
            "https://camo.githubusercontent.com/28b2b0fabbeedcc3e4cb7a38a1c4c1b63099248265abbcb1b0de5195dbb44892/68747470733a2f2f692e70697869762e6361742f696d672d6f726967696e616c2f696d672f323031392f30382f30372f30302f31332f33372f37363131363734325f70302e706e67"
        ):
            print(msg)

    import asyncio

    asyncio.run(main())
