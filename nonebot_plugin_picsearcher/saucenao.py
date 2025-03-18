# -*- coding: utf-8 -*-
import io
from typing import List, Tuple

import aiohttp,httpx
from lxml.html import fromstring
from nonebot.adapters.onebot.v11 import MessageSegment

# from aiohttp import FormData
try:
    from .proxy import proxy
except ImportError:
    proxy = None  # test case

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Host": "saucenao.com",
    "Origin": "https://saucenao.com",
    "Referer": "https://saucenao.com/",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
}


def parse_html(html: str):
    """
    解析nao返回的html
    :param html:
    :return:
    """
    selector = fromstring(html)
    for tag in selector.xpath('//div[@class="result"]/table'):
        pic_url = tag.xpath("./tr/td/div/a/img/@src")
        if pic_url:
            pic_url = pic_url[0]
        else:
            pic_url = None  # 相似度
        xsd: List[str] = tag.xpath(
            './tr/td[@class="resulttablecontent"]/div[@class="resultmatchinfo"]/div[@class="resultsimilarityinfo"]/text()'
        )
        if xsd:
            xsd = xsd[0]
        else:
            xsd = "没有写"  # 相似度
        title: List[str] = tag.xpath(
            './tr/td[@class="resulttablecontent"]/div[@class="resultcontent"]/div[@class="resulttitle"]/strong/text()'
        )
        if title:
            title = title[0]
        else:
            title = "没有写"  # 标题
        # pixiv id
        pixiv_id: List[str] = tag.xpath(
            './tr/td[@class="resulttablecontent"]/div[@class="resultcontent"]/div[@class="resultcontentcolumn"]/a[1]/@href'
        )
        if pixiv_id:
            pixiv_id = pixiv_id[0]
        else:
            pixiv_id = "没有说"
        member: List[str] = tag.xpath(
            './tr/td[@class="resulttablecontent"]/div[@class="resultcontent"]/div[@class="resultcontentcolumn"]/a[2]/@href'
        )
        if member:
            member = member[0]
        else:
            member = "没有说"
        yield pic_url, xsd, title, pixiv_id, member


async def get_pic_from_url(url: str):
    """
    从url搜图
    :param url:
    :return:
    """
    async with aiohttp.ClientSession() as session:
        async with httpx.AsyncClient(verify=True) as client:
            response = await client.get(url)
            content = io.BytesIO(response.content)
        data = aiohttp.FormData()  # boundary="----WebKitFormBoundaryPpuR3EZ1Ap2pXv8W"
        data.add_field(
            name="file", value=content, content_type="image/png", filename="blob"
        )
        async with session.post(
            "https://saucenao.com/search.php", data=data, headers=headers, proxy=proxy
        ) as res:
            html = await res.text()
            image_data = [each for each in parse_html(html)]
    return image_data


async def get_des(url: str):
    image_data: List[Tuple] = await get_pic_from_url(url)
    if not image_data:
        msg: str = "找不到高相似度的"
        yield msg
        return
    for pic in image_data:
        msg = (
            MessageSegment.image(file=pic[0])
            + f"\n相似度:{pic[1]}\n标题:{pic[2]}\npixivid:{pic[3]}\nmember:{pic[4]}\n"
        )
        yield msg


if __name__ == "__main__":

    async def main():
        async for msg in get_des(
            "https://camo.githubusercontent.com/28b2b0fabbeedcc3e4cb7a38a1c4c1b63099248265abbcb1b0de5195dbb44892/68747470733a2f2f692e70697869762e6361742f696d672d6f726967696e616c2f696d672f323031392f30382f30372f30302f31332f33372f37363131363734325f70302e706e67"
        ):
            print(msg)

    import asyncio

    asyncio.run(main())
