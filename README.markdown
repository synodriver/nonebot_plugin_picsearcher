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

由于[exhentai](https://exhentai.org)的接口需要cookie~~以及fq~~，因此需要在配置文件
中加入如下选项，没有设置COOKIE时会回退到eh~~有些loli本就搜不到了~~
```
EX_COOKIE=XXXXX
PROXY=XXXX  # type: str e.g. PROXY=http://127.0.0.1:8889
SEARCH_LIMIT=2  # 搜索限制 防刷屏
RISK_CONTROL=true # 风控模式 启动后会使用合并转发 只有gocq有实现
RECORD_PRIORITY=99 # 记录上一张图片matcher的优先级，与 上一张 命令有关
```

## 更新日志
- v0.1.4
    - 修复了formdata手动改库的问题，改为就地hook aiohttp
    - yandex搜图
  
- v0.1.5rc1
    - 加入可选的`search_limit`配置项，确认一次搜索的显示结果数量，默认`2`
    - 加入可选的`proxy`选项

- v0.1.6rc1
    - 手残的代价（

- v0.1.6rc2
    - 支持nb2.beta1， 需要onebot adapter

- v0.1.7
    - 支持beta2


## 下一阶段目标

- Yandex? Maybe


## 特别感谢

- [Mrs4s / go-cqhttp](https://github.com/Mrs4s/go-cqhttp)
- [nonebot / nonebot2](https://github.com/nonebot/nonebot2)

## 优化建议

可以来抓更多网站的接口or汇报bug or pr
![](https://i.pixiv.cat/img-original/img/2019/08/07/00/13/37/76116742_p0.png "呐呐呐,来pr的话~就给大哥哥透噢")
