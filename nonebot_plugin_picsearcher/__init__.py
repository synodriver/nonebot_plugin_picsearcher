# -*- coding: utf-8 -*-
import traceback

from aiohttp.client_exceptions import ClientError
from nonebot.plugin import on_command
from nonebot.rule import to_me
from nonebot.adapters.cqhttp import Bot, Event, Message

from .ex import get_des as get_des_ex
from .iqdb import get_des as get_des_iqdb
from .saucenao import get_des as get_des_sau
from .ascii2d import get_des as get_des_asc
from .trace import get_des as get_des_trace


async def get_des(url: str, mode: str):
    """
    :param url: 图片链接
    :param mode: 图源
    :return:
    """
    if mode == "iqdb":
        async for msg in get_des_iqdb(url):
            yield msg
    elif mode == "ex":
        async for msg in get_des_ex(url):
            yield msg
    elif mode == "trace":
        async for msg in get_des_trace(url):
            yield msg
    elif mode.startswith("asc"):
        async for msg in get_des_asc(url):
            yield msg
    else:
        async for msg in get_des_sau(url):
            yield msg


setu = on_command("搜图", aliases={"search"}, rule=to_me())


@setu.handle()
async def handle_first_receive(bot: Bot, event: Event, state: dict):
    msg = event.message
    if msg:
        state["setu"] = msg
    pass


@setu.got("mod", prompt="从哪里查找呢? ex/nao/trace/iqdb/ascii2d")
async def get_func(bot: Bot, event: Event, state: dict):
    pass


@setu.got("setu", prompt="图呢？")
async def get_setu(bot: Bot, event: Event, state: dict):
    """
    发现没有的时候要发问
    :return:
    """
    msg: Message = Message(state["setu"])
    mod: str = state["mod"]  # 模式
    try:
        if msg[0].type == "image":
            await bot.send(event=event, message="正在处理图片")
            url = msg[0].data["url"]  # 图片链接
            async for msg in get_des(url, mod):
                await bot.send(event=event, message=msg)
            # image_data: List[Tuple] = await get_pic_from_url(url)
            await setu.finish("hso")
        else:
            await setu.reject("这不是图,重来!")
    except (IndexError, ClientError):
        await bot.send(event, traceback.format_exc())
        await setu.finish("参数错误")
