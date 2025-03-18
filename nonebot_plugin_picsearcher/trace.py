import io
from base64 import b64encode
from copy import deepcopy
from typing import List, Tuple

import aiohttp,httpx
from nonebot.adapters.onebot.v11 import MessageSegment

# from .formdata import FormData
try:
    from .proxy import proxy
except ImportError:
    proxy = None


headers = {
    ":authority": "api.trace.moe",
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9",
    # "content-type": "multipart/form-data; boundary=----WebKitFormBoundary9cyjY8YBBN8SGdG4",
    "origin": "https://trace.moe",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/84.0.4147.105 Safari/537.36",
}


async def parse_json(session: aiohttp.ClientSession, data: dict):
    count = 0
    ret = []
    for i in data["result"]:
        anilist: int = i["anilist"]
        # title: dict = i["anilist"]["title"]  todo 没了
        similarity = i["similarity"]
        from_ = i["from"]
        to = i["to"]
        file = i["filename"]
        # is_adult = i["anilist"]["isAdult"]  todo
        episode = i["episode"]  #
        ret.append(
            {
                "anilist": anilist,
                "similarity": similarity,
                "from": from_,
                "to": to,
                "filename": file,
                "episode": episode,
                "image": i["image"],
                "video": i["video"],
            }
        )

    async with session.post(
        "https://trace.moe/anilist",
        headers=headers,
        json={
            "query": "query ($ids: [Int]) {\n            Page(page: 1, perPage: 50) {\n              media(id_in: $ids, type: ANIME) {\n                id\n                title {\n                  native\n                  romaji\n                  english\n                }\n                type\n                format\n                status\n                startDate {\n                  year\n                  month\n                  day\n                }\n                endDate {\n                  year\n                  month\n                  day\n                }\n                season\n                episodes\n                duration\n                source\n                coverImage {\n                  large\n                  medium\n                }\n                bannerImage\n                genres\n                synonyms\n                studios {\n                  edges {\n                    isMain\n                    node {\n                      id\n                      name\n                      siteUrl\n                    }\n                  }\n                }\n                isAdult\n                externalLinks {\n                  id\n                  url\n                  site\n                }\n                siteUrl\n              }\n            }\n          }\n          ",
            "variables": {"ids": [i["anilist"] for i in ret]},
        },
        proxy=proxy,
    ) as resp:
        d = await resp.json()
        for index, i in enumerate(d["data"]["Page"]["media"]):
            title = i["title"]["native"]
            is_adult = i["isAdult"]
            ret[index]["title"] = title
            ret[index]["is_adult"] = is_adult

    # header_new = deepcopy(header)
    # del header_new["content-type"]
    # header_new[":method"] = 'GET'
    # header_new["accept"] = "image/webp,image/apng,image/*,*/*;q=0.8"
    # header_new["sec-fetch-dest"] = "image"
    # header_new["sec-fetch-mode"] = "no-cors"
    # async with session.get(i["image"], headers=header_new) as resp:
    #     pic = "base64://" + b64encode(await resp.read()).decode()
    for i in ret:
        yield i["image"], i["similarity"], i["filename"], i["is_adult"], i["from"], i[
            "to"
        ], i["title"], i["episode"]
        count += 1
        if count > 4:
            break


# POST https://api.trace.moe/search?cutBorders=1&anilistID=
async def get_pic_from_url(url: str):
    """
    从url搜图
    :param url:
    :return:
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            async with httpx.AsyncClient(verify=True) as client:
                response = await client.get(url)
                content = io.BytesIO(response.content)
        # with open("F:\elu.PNG", "rb") as f:
        #     content = io.BytesIO(f.read())
        data = aiohttp.FormData()  # boundary="----WebKitFormBoundary9cyjY8YBBN8SGdG4"
        data.add_field(
            name="image", value=content, content_type="image/jpeg", filename="blob"
        )
        # data.add_field(name="filter", value="")
        # data.add_field(name="trial", value="0")
        async with session.post(
            "https://api.trace.moe/search?cutBorders=1&anilistID=",
            data=data,
            headers=headers,
            proxy=proxy,
        ) as res:
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
        msg = (
            MessageSegment.image(file=pic[0])
            + f"\n相似度:{pic[1]}%\n标题:{pic[6]['native'] + ' ' + pic[6]}\n第{pic[7]}集\nR18:{pic[3]}\n开始时间:{pic[4]}s\n结束时间{pic[5]}s"
        )
        yield msg
    pass


if __name__ == "__main__":
    import asyncio

    async def main():
        async for msg in get_des(
            "https://camo.githubusercontent.com/28b2b0fabbeedcc3e4cb7a38a1c4c1b63099248265abbcb1b0de5195dbb44892/68747470733a2f2f692e70697869762e6361742f696d672d6f726967696e616c2f696d672f323031392f30382f30372f30302f31332f33372f37363131363734325f70302e706e67"
        ):
            print(msg)

    asyncio.run(main())  # todo fix
