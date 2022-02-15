# -*- coding: utf-8 -*-
import traceback
from typing import Dict
import json

from aiohttp.client_exceptions import ClientError

from nonebot.params import State, ArgPlainText, Arg, CommandArg
from nonebot.plugin import on_command, on_message
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, GroupMessageEvent, PrivateMessageEvent, Message
from nonebot.typing import T_State
from nonebot.utils import DataclassEncoder

from .ex import get_des as get_des_ex
from .iqdb import get_des as get_des_iqdb
from .saucenao import get_des as get_des_sau
from .ascii2d import get_des as get_des_asc
from .trace import get_des as get_des_trace
from .yandex import get_des as get_des_yandex

from .utils import limiter


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
    elif mode == "yandex":
        async for msg in get_des_yandex(url):
            yield msg
    elif mode.startswith("asc"):
        async for msg in get_des_asc(url):
            yield msg
    else:
        async for msg in get_des_sau(url):
            yield msg


setu = on_command("搜图", aliases={"search"}, rule=to_me())


@setu.handle()
async def handle_first_receive(event: MessageEvent, state: T_State = State(), setu: Message = CommandArg()):
    if setu:
        state["setu"] = setu


@setu.got("mod", prompt="从哪里查找呢? ex/nao/trace/iqdb/ascii2d")
async def get_func():
    pass


@setu.got("setu", prompt="图呢？")
async def get_setu(bot: Bot,
                   event: MessageEvent,
                   mod: str = ArgPlainText("mod"),
                   msg: Message = Arg("setu")):
    """
    发现没有的时候要发问
    :return:
    """
    try:
        if msg[0].type == "image":
            await bot.send(event=event, message="正在处理图片")
            url = msg[0].data["url"]  # 图片链接
            if not getattr(bot.config, "risk_control", None) or isinstance(event, PrivateMessageEvent):  # 安全模式
                async for msg in limiter(get_des(url, mod), getattr(bot.config, "search_limit", None) or 2):
                    await bot.send(event=event, message=msg)
            else:
                msgs: Message = sum(
                    [msg if isinstance(msg, Message) else Message(msg) async for msg in get_des(url, mod)])
                dict_data = json.loads(json.dumps(msgs, cls=DataclassEncoder))
                await bot.send_group_forward_msg(group_id=event.group_id,
                                                 messages=[
                                                     {
                                                         "type": "node",
                                                         "data": {
                                                             "name": event.sender.nickname,
                                                             "uin": event.user_id,
                                                             "content": [
                                                                 content
                                                             ]
                                                         }
                                                     }
                                                     for content in dict_data
                                                 ]
                                                 )

            # image_data: List[Tuple] = await get_pic_from_url(url)
            await setu.finish("hso")
        else:
            await setu.reject("这不是图,重来!")
    except (IndexError, ClientError):
        await bot.send(event, traceback.format_exc())
        await setu.finish("参数错误")


pic_map: Dict[str, str] = {}  # 保存这个群的上一张色图 {"123456":"http://xxx"}


async def check_pic(bot: Bot, event: MessageEvent, state: T_State = State()) -> bool:
    if isinstance(event, MessageEvent):
        for msg in event.message:
            if msg.type == "image":
                url: str = msg.data["url"]
                state["url"] = url
                return True
        return False


notice_pic = on_message(check_pic)


@notice_pic.handle()
async def handle_pic(event: GroupMessageEvent, state: T_State = State()):
    try:
        group_id: str = str(event.group_id)
        pic_map.update({group_id: state["url"]})
    except AttributeError:
        pass


previous = on_command("上一张图是什么", aliases={"上一张", "这是什么"})


@previous.handle()
async def handle_previous(bot: Bot, event: GroupMessageEvent):
    await bot.send(event=event, message="processing...")
    try:
        url: str = pic_map[str(event.group_id)]
        if not getattr(bot.config, "risk_control", None):  # 安全模式
            async for msg in limiter(get_des(url, "nao"), getattr(bot.config, "search_limit", None) or 2):
                await bot.send(event=event, message=msg)
        else:
            msgs: Message = sum(
                [msg if isinstance(msg, Message) else Message(msg) async for msg in get_des(url, "nao")])
            dict_data = json.loads(json.dumps(msgs, cls=DataclassEncoder))
            await bot.send_group_forward_msg(group_id=event.group_id,
                                             messages=[
                                                 {
                                                     "type": "node",
                                                     "data": {
                                                         "name": event.sender.nickname,
                                                         "uin": event.user_id,
                                                         "content": [
                                                             content
                                                         ]
                                                     }
                                                 }
                                                 for content in dict_data
                                             ]
                                             )
    except (IndexError, ClientError):
        await bot.send(event, traceback.format_exc())
        await previous.finish("参数错误")
    except KeyError:
        await previous.finish("没有图啊QAQ")
