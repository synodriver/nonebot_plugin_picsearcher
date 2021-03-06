# -*- coding: utf-8 -*-
from typing import List, Tuple

from lxml.html import fromstring
import aiohttp
from nonebot.adapters.cqhttp import MessageSegment

"""
http://yandex.com/clck/jsredir?from=yandex.com%3Bimages%2Fsearch%3Bimages%3B%3B&text=&etext=9185.K4iyzsNBG9xrJrSJCUTF4i-XPMAfmBQYR_Igss1ESRc.65568e796f3375fae39da91273ae8a1a82410929&uuid=&state=iric5OQ0sS2054x1_o8yG9mmGMT8WeQxqpuwa4Ft4KVzd9aE_Y4Dfw,,&data=eEwyM2lDYU9Gd1VROE1ZMXhZYkJTYW5fZC1TWjIzaFh5TmR1Z09fQm5DdDB3bFJSSUpVdUxfZmUzcVhfaXhTN1BCU2dINGxmdkY4NFVNcHYyUmw0emFKT2pnOWJoVmlPVzAzX1FIbWh6aXVFV3F0YWFaMGdxeGFtY2dxTzFZZl9VY1huZmlLaGVGOFZleUthZXBlM1pxUGM2elVDLXdvZEo3OGJwdVFqYmVkTDJxWElHSzFZR2NVQUhVcTdzelJwSXlrTjhlS0txdHpYY1RMMHRLOU5HSTYtT0VDb0hpdll6YjVYRXNVcUhCRFJaeDExNTQwZlhMdjh4M2YtTVFUbVJ5ZzBxMTVJcG9DNW51UWhvRzE0WjlFS19uS0VUZWhNRGxOZWlPUkFlRUUs&sign=7ba9ee25d3716868ec8464fb766c9e25&keyno=IMGS_0&b64e=2&l10n=en
"""
def parse_html(html: str):
    selector = fromstring(html)

    pass


async def get_pic_from_url(url: str):
    real_url = f"https://yandex.com/images/search?rpt=imageview&url={url}"
    async with aiohttp.ClientSession() as session:
        async with session.get(real_url) as resp:
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
