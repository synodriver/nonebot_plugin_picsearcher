# nonebot_plugin_picsearcher
[![pypi](https://img.shields.io/pypi/v/nonebot-plugin-picsearcher.svg)](https://pypi.org/project/nonebot_plugin_picsearcher/) 
![implementation](https://img.shields.io/pypi/implementation/nonebot-plugin-picsearcher)
![wheel](https://img.shields.io/pypi/wheel/nonebot-plugin-picsearcher)
![python](https://img.shields.io/pypi/pyversions/nonebot-plugin-picsearcher)
[![license](https://img.shields.io/github/license/synodriver/nonebot_plugin_picsearcher.svg)](https://raw.githubusercontent.com/synodriver/nonebot_plugin_picsearcher/main/LICENSE)

- 基于[nonebot2](https://github.com/nonebot/nonebot2)

## 功能

- 从各个接口查找色图来源,目前支持ascii2d exhentai iqdb saucenao trace.moe

## 开始使用

~~建议~~必须使用 pip

- 通过 pip 从 [PyPI](https://pypi.org/project/nonebot_plugin_picsearcher/) 安装

``` {.sourceCode .bash}
pip install nonebot-plugin-picsearcher
```

- 在 nonebot2 项目中设置 load_plugin()

``` {.sourceCode .python}
nonebot.load_plugin('nonebot_plugin_picsearcher')
```

- 参照下文在 nonebot2 项目的环境文件 .env.\* 中添加配置项
- 使用时at搜图即可

## 配置项

由于[exhentai](https://exhentai.org)的接口需要cookie,因此需要在配置文件
中加入如下选项
```
EX_COOKIE=XXXXX
```

## 特别注意
- 由于aiohttp的某些神奇实现,默认的FormData类需要被稍微*调教*一下
``` {.sourceCode .python}
# 在\site-packages\aiohttp\formdata.py
class FormData:
    """Helper class for multipart/form-data and
    application/x-www-form-urlencoded body generation."""

    def __init__(self, fields:
                 Iterable[Any]=(),
                 quote_fields: bool=True,
                 charset: Optional[str]=None,
                 boundary: Optional[str]=None) -> None:
        self._writer = multipart.MultipartWriter('form-data', boundary=boundary)
        self._fields = []  # type: List[Any]
        self._is_multipart = False
        self._quote_fields = quote_fields
        self._charset = charset
```
- 以上,给他加一个参数(该操作不会影响其他包 ~~纯粹是 [aiolibs](https://github.com/aio-libs) 的人懒~~)

## 不魔改aiohttp会怎样?

那得问问那些网站愿不愿意了()

## 特别感谢

- [Mrs4s / go-cqhttp](https://github.com/Mrs4s/go-cqhttp)
- [nonebot / nonebot2](https://github.com/nonebot/nonebot2)

## 优化建议

可以来抓更多网站的接口or汇报bug or pr
![](https://i.pixiv.cat/img-original/img/2019/08/07/00/13/37/76116742_p0.png "呐呐呐,来pr的话~就给大哥哥透噢")