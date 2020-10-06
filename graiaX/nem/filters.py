import re
from typing import Callable, List

from graia.application.entry import Group, GroupMessage
from graia.application.event.messages import FriendMessage
from graia.broadcast.exceptions import ExecutionStop
from graia.broadcast.builtin.decoraters import Depend

from .nem import NEM


class FrontFilters(object):
    '''过滤器的前置修饰器，无法直接使用'''
    @staticmethod
    def requirePlain(func: Callable[[GroupMessage], Callable]):
        def wrapper(gm: GroupMessage):
            nem = NEM(gm)
            if not nem.plain_message:
                raise ExecutionStop()
            return func(gm)
        return wrapper

    @staticmethod
    def requireNotBanned(func: Callable[[GroupMessage], Callable]):
        def wrapper(gm: GroupMessage):
            nem = NEM(gm)
            if nem.permission.isBlocked():
                raise ExecutionStop()
            return func(gm)
        return wrapper

    @staticmethod
    def depend(func: Callable) -> Depend:
        def wrapper(*args, **kwargs):
            return Depend(func(*args, **kwargs))
        return wrapper


class GroupFilters(object):
    '''
    Group 消息过滤器，作为 `headless_decoraters` 使用

    请查看源码以了解所有可用的过滤器
    '''

    # GroupMessage
    @staticmethod
    @FrontFilters.depend
    def exceptGroups(group_list: List[int]) -> Callable:
        '''在指定群聊内禁用'''
        def wrapper(group: Group):
            if group.id in group_list:
                raise ExecutionStop()
        return wrapper

    @staticmethod
    @FrontFilters.depend
    def inGroups(group_list: List[int]) -> Depend:
        '''仅在指定群聊内启用'''
        def wrapper(group: Group):
            if not group.id in group_list:
                raise ExecutionStop()
        return wrapper

    @staticmethod
    @FrontFilters.depend
    def adminOnly() -> Depend:
        '''仅管理员'''
        def wrapper(gm: GroupMessage):
            nem = NEM(gm)
            if not nem.permission.isAdmin():
                raise ExecutionStop()
        return wrapper

    @staticmethod
    @FrontFilters.depend
    def onCommand(command_name: str) -> Depend:
        '''在特定指令时执行

        Args:
            command_name: 指令名称（不带标识符）'''
        @FrontFilters.requirePlain
        @FrontFilters.requireNotBanned
        def wrapper(gm: GroupMessage):
            nem = NEM(gm)
            if nem.Command.cmd != command_name:
                raise ExecutionStop()
        return wrapper
    
    @staticmethod
    @FrontFilters.depend
    def onAt(qq: int) -> Depend:
        '''当 `qq` 在群内被 At 时执行

        Args:
            qq: QQ 号'''
        @FrontFilters.requireNotBanned
        def wrapper(gm: GroupMessage):
            nem = NEM(gm)
            if not qq in nem.at:
                raise ExecutionStop()
        return wrapper

    @staticmethod
    @FrontFilters.depend
    def onWord(word: str) -> Depend:
        '''在消息中有特定文字时执行

        Args:
            word: 文字'''
        @FrontFilters.requirePlain
        @FrontFilters.requireNotBanned
        def wrapper(gm: GroupMessage):
            nem = NEM(gm)
            if not word in nem.plain_message:
                raise ExecutionStop()
        return wrapper

    @staticmethod
    @FrontFilters.depend
    def onWords(words_list: List[str]) -> Depend:
        '''在消息中有特定文字时执行

        Args:
            words_list: 关键字列表'''
        @FrontFilters.requirePlain
        @FrontFilters.requireNotBanned
        def wrapper(gm: GroupMessage):
            nem = NEM(gm)
            inList = False
            for word in words_list:
                if word in nem.plain_message:
                    inList = True
                    break
            if not inList:
                raise ExecutionStop()
        return wrapper

    @staticmethod
    @FrontFilters.depend
    def onMatch(pattern: str) -> Depend:
        '''在消息匹配正则表达式时执行

        Args:
            pattern: 正则表达式（必须为 str）'''
        @FrontFilters.requirePlain
        @FrontFilters.requireNotBanned
        def wrapper(gm: GroupMessage):
            nem = NEM(gm)
            if not re.match(pattern, nem.plain_message):
                raise ExecutionStop()
        return wrapper

    @staticmethod
    @FrontFilters.depend
    def onMatchs(pattern_list: List[str]) -> Depend:
        '''在消息匹配正则表达式列表中的任何一项时执行

        Args:
            pattern_list: 正则表达式列表'''
        @FrontFilters.requirePlain
        @FrontFilters.requireNotBanned
        def wrapper(gm: GroupMessage):
            nem = NEM(gm)
            matched: bool = False
            for p in pattern_list:
                if re.match(p, nem.plain_message):
                    matched = True
                    break
            if not matched:
                raise ExecutionStop()
        return wrapper


class FriendFilters(object):
    @staticmethod
    @FrontFilters.depend
    def onFriend(qq: int) -> Depend:
        def wrapper(fm: FriendMessage):
            if fm.sender.id != qq:
                raise ExecutionStop()
        return wrapper
