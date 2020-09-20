'''
 _   _   _____   __  __ 
| \ | | | ____| |  \/  |
|  \| | |  _|   | |\/| |
| |\  | | |___  | |  | |
|_| \_| |_____| |_|  |_|

  Not Enough Messages
    更好的消息解析器
需配合 Graia Framework 使用


Usage:
``` python
from graiaX.nem import NEM

...

@bcc.receiver(GroupMessage)
async def group_message_listener(app: GraiaMiraiApplication, group: Group, _gm: GroupMessage):
    nem = NEM(_gm)
    await app.sendGroupMessage(group, MessageChain.create([Plain(nem.plain_message)]))

...
```
'''

from .filters import Filters
from .nem import NEM
from .permission import Permission
