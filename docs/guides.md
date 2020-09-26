# 快速上手

## 前言

!> 我们假设你已按照 mirai & Graia Framework 的文档正确地进行了配置

!> **注意！** 如果你在使用过程中出现错误，应先检查是否真的为 `graiax-nem` 的错误。如果是，请在我们的 [GitHub Issues](https://github.com/jinzhijie/graiax-nem/issues) 处报告你遇到的错误，我们会尽快处理。如果不是，请去相应的项目报告问题。

## 安装

请查看此处 → [安装](README.md#安装)

## 使用

```python:14,23
# bot.py
import asyncio

from graia.application import GraiaMiraiApplication, Session
from graia.application.event.messages import GroupMessage
from graia.application.group import Group
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import Plain
from graia.broadcast import Broadcast

from graiax.nem import NEM
from graiax.nem.filters import Filters

BOTQQ = 10102233

loop = asyncio.get_event_loop()

bcc = Broadcast(loop=loop)
app = GraiaMiraiApplication(
    broadcast=bcc,
    connect_info=Session(
        host="http://localhost:8080",
        authKey="mirai-api-http-auth-key",
        account=BOTQQ,
        websocket=True
    )
)


@bcc.receiver(GroupMessage, headless_decoraters=[Filters.onAt(BOTQQ)])
async def nem_example(app: GraiaMiraiApplication, group: Group, _gm: GroupMessage):
    nem = NEM(_gm)
    await app.sendGroupMessage(group, MessageChain.create([Plain('YES!')]), quote=nem.source)


app.launch_blocking()
```

?> 别忘了修改 `BOTQQ` 和 `authKey` 的值

运行代码，终端输出：

```bash
[root@localhost]$ python3 bot.py
[2020-09-26 15:47:02,929][INFO]: launching app...
[2020-09-26 15:47:02,960][INFO]: using websocket to receive event
[2020-09-26 15:47:02,964][INFO]: event reveiver running...
```

现在你可以在群里 @ 你的 bot 来测试了

