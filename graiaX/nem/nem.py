from typing import List, Optional, Tuple, Union

from graia.application.entry import (At, GroupMessage, MessageChain, Plain,
                                     Quote, Source)
from graia.application.event.messages import FriendMessage
from graia.application.friend import Friend
from graia.application.group import Member
from graia.application.message.elements.internal import Image

from .elements import AtList, ImagePro
from .permission import Permission


class NEM(object):
    '''
    Not Enough Messages -- 更好的消息解析器

    示例：
    ``` python
    @bcc.receiver(GroupMessage)
    async def group_message_listener(app: GraiaMiraiApplication, group: Group, _gm: GroupMessage):
        nem = NEM(_gm)
        await app.sendGroupMessage(group, MessageChain.create([Plain(nem.plain_message)]))
    ```

    属性解释：（带 `*` 号的表示此项有可能为 `None`）
    - `nem.permission` 为消息发送者的 `Permission` 对象
    - `nem.chain` 为原消息链（`MessageChain`）
    - `nem.sender` 为消息发送者的 `Member` 或 `Friend` 实例
    - `nem.sender_id` 为消息发送者的 QQ 号
    - `nem.source` 为原消息链的 `Source`，可用于回复
    - `nem.at` *为消息中所有的 `At` 列表，使用了 `AtList` 拥有特殊功能
    - `nem.images` *为 `ImagePro` 列表
    - `nem.plain_message` *为所有的 `Plain` 拼接而成的字符串
    - `nem.plain_message_source` *为被回复的消息中所有的 `Plain` 拼接而成的字符串
    '''
    _commandSymbol: str = '&'
    chain: MessageChain
    sender: Union[Member, Friend]
    sender_id: int
    plain_message: Optional[str]
    plain_message_source: Optional[str]
    source: Source
    at: AtList
    images: List[ImagePro]
    permission: Permission

    class Command(object):
        '''指令相关

        `cmd` 为指令，
        `args` 为参数，
        `argsList` 为参数列表，
        '''
        cmd: Optional[str]
        args: Optional[str]
        argsList: Optional[List[str]]

    def __init__(self, _message: Union[GroupMessage, FriendMessage], _command_symbol: str = None) -> None:
        '''
        初始化 NEM 解析器

        Args:
            _message: `Message` 对象
            _command_symbol: 指令标识符，默认为 `'&'`
        '''
        self._commandSymbol = self._commandSymbol or _command_symbol
        self.chain = _message.messageChain
        self.sender = _message.sender
        self.sender_id = _message.sender.id
        self.plain_message = self._getPlainMessage(self.chain)
        self.at = self._getAt()
        self.Command.cmd, self.Command.args, self.Command.argsList = self._getCommand()
        self.plain_message_source = self._getQuotePlainMessage()
        self.source = self._getSource()
        self.images = self._makeImageProList()
        self.permission = Permission(self.sender_id)

    @staticmethod
    def _getPlainMessage(_messagechain: MessageChain) -> Optional[str]:
        if Plain in _messagechain:
            _text = str()
            for _i in _messagechain[Plain]:
                i_text: str = _i.text
                if not i_text.strip().isspace():
                    _text = f'{_text} {i_text}'
            return _text.strip()
        else:
            return None

    def _getAt(self) -> AtList:
        atList = self.chain[At]
        return AtList(atList)

    def _getQuotePlainMessage(self) -> Optional[str]:
        if Quote in self.chain:
            _quote_message: Quote = self.chain[Quote][0]
            _origin_messagechain: MessageChain = _quote_message.origin
            _plain_message = self._getPlainMessage(_origin_messagechain)
            return _plain_message
        else:
            return None

    def _getSource(self) -> Source:
        return self.chain[Source][0]

    def makeMessageBody(self, plain_message: str) -> str:
        '''
        帮助你实现更好的指令解析，适用于一些消息转发机器人的特殊处理

        继承 `NEM` 类并重写这个函数以实现此功能
        '''
        return plain_message  # 不作操作，原样返回

    def _getCommand(self) -> Tuple[Optional[str], Optional[str], Optional[List[str]]]:
        if not self.plain_message:
            return None, None, None
        if self._commandSymbol in self.plain_message:
            _message_body: str = self.makeMessageBody(self.plain_message)
            _splited_message: list = _message_body.split(' ', 1)
            _command: str = _splited_message[0]
            _args: Optional[str] = _splited_message[1] if len(
                _splited_message) > 1 else None
            _argsList: Optional[List[str]] = _args.split() if _args else None
            cmd: str = _command.replace(
                self._commandSymbol, '')  # 只留下命令主体而不考虑命令标识符
            return cmd, _args, _argsList
        else:
            return None, None, None

    def _makeImageProList(self) -> Optional[List[ImagePro]]:
        if not Image in self.chain:
            return None
        images = self.chain[Image]
        return [ImagePro(i) for i in images]
