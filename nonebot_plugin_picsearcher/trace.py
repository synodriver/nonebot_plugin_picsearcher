# -*- coding: utf-8 -*-
import io
from copy import deepcopy
from base64 import b64encode
from typing import List, Tuple

import aiohttp
from nonebot.adapters.cqhttp import MessageSegment

header = {':authority': 'trace.moe',
          ':method': 'POST',
          "host": "trace.moe",
          ':path': '/search',
          ':scheme': 'https',
          'accept': '*/*',
          'accept-encoding': 'gzip, deflate',
          'accept-language': 'zh-CN,zh;q=0.9',
          "cache-control": "no-cache",
          'content-type': 'multipart/form-data; boundary=----WebKitFormBoundaryAyWVOEnpliN09xxB',
          'origin': 'https://trace.moe',
          'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'same-origin',
          'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/84.0.4147.105 Safari/537.36',
          'x-requested-with': 'XMLHttpRequest'}


async def parse_json(session: aiohttp.ClientSession, data: dict):
    count = 0
    for i in data["docs"]:
        similarity = 100 - i["diff"]
        anilist_id = i["anilist_id"]
        from_ = i["from"]
        to = i["to"]
        file = i["file"]  # 这个用得到
        t = i["t"]
        is_adult = i["is_adult"]
        tokenthumb = i["tokenthumb"]
        header_new = deepcopy(header)
        del header_new[":path"]
        del header_new["content-type"]
        header_new[":method"] = 'GET'
        header_new["accept"] = "image/webp,image/apng,image/*,*/*;q=0.8"
        header_new["sec-fetch-dest"] = "image"
        header_new["sec-fetch-mode"] = "no-cors"
        async with session.get("https://trace.moe/thumbnail.php?",
                               params={"anilist_id": anilist_id, "file": file, "t": t, "token": tokenthumb}) as resp:
            pic = "base64://" + b64encode(await resp.read()).decode()
        yield pic, similarity, file, is_adult, from_, to
        count += 1
        if count > 4:
            break


async def get_pic_from_url(url: str):
    """
    从url搜图
    :param url:
    :return:
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            content = io.BytesIO(await resp.read())
        # with open("F:\elu.PNG", "rb") as f:
        #     content = io.BytesIO(f.read())
        data = aiohttp.FormData(boundary="----WebKitFormBoundaryAyWVOEnpliN09xxB")
        data.add_field(name="image", value=content, content_type="image/jpeg",
                       filename="blob")
        data.add_field(name="filter", value="")
        data.add_field(name="trial", value="0")
        async with session.post("https://trace.moe/search", data=data, headers=header) as res:
            data: dict = await res.json()
            image_data = [each async for each in parse_json(session, data)]
    return image_data


async def get_des(url: str):
    image_data: List[Tuple] = await get_pic_from_url(url)
    if not image_data:
        msg: str = "找不到高相似度的"
        yield msg
        return
    for pic in image_data:
        msg = MessageSegment.image(
            file=pic[0]) + f"\n相似度:{pic[1]}%\n标题:{pic[2]}\nR18:{pic[3]}\n开始时间:{pic[4]}s\n结束时间{pic[5]}s"
        yield msg
    pass


if __name__ == "__main__":
    import asyncio

    asyncio.run(get_pic_from_url(
        "https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1606681978562&di=6d6c90aef5ff1f9f8915bbc2e18e3c98&imgtype=0&src=http%3A%2F%2Fc-ssl.duitang.com%2Fuploads%2Fblog%2F202011%2F15%2F20201115190356_c5b95.thumb.1000_0.jpg"))
