import re
from typing import List

from graia.application.entry import Group, GroupMessage
from graia.broadcast.exceptions import ExecutionStop
from graia.broadcast.builtin.decoraters import Depend

from .nem import NEM


class Filter(object):
    '''
    NEM 消息过滤器，作为 `headless_decoraters` 使用

    请查看源码以了解所有可用的过滤器
    '''
    @staticmethod
    def exceptGroups(group_list: List[int]):
        '''在指定群聊内禁用'''
        def wrapper(group: Group):
            if group.id in group_list:
                raise ExecutionStop()
        return Depend(wrapper)

    @staticmethod
    def inGroups(group_list: List[int]):
        '''仅在指定群聊内启用'''
        def wrapper(group: Group):
            if not group.id in group_list:
                raise ExecutionStop()
        return Depend(wrapper)

    @staticmethod
    def adminOnly():
        '''仅管理员'''
        def wrapper(gm: GroupMessage):
            nem = NEM(gm)
            if not nem.permission.isAdmin():
                raise ExecutionStop()
        return Depend(wrapper)

    @staticmethod
    def onCommand(command_name: str):
        '''在特定指令时执行

        Args:
            command_name: 指令名称（不带标识符）'''
        def wrapper(gm: GroupMessage):
            nem = NEM(gm, '&')
            if nem.permission.isBlocked():
                raise ExecutionStop()
            if not nem.plain_message:
                raise ExecutionStop()
            if nem.Command.cmd != command_name:
                raise ExecutionStop()
        return Depend(wrapper)

    @staticmethod
    def onWord(word: str):
        '''在消息中有特定文字时执行，已弃用，使用 `onWords` 代替

        Args:
            word: 文字'''
        def wrapper(gm: GroupMessage):
            nem = NEM(gm, '&')
            if nem.permission.isBlocked():
                raise ExecutionStop()
            if not nem.plain_message:
                raise ExecutionStop()
            if not word in nem.plain_message:
                raise ExecutionStop()
        return Depend(wrapper)

    @staticmethod
    def onWords(words_list: List[str]):
        '''在消息中有特定文字时执行

        Args:
            words_list: 关键字列表'''
        def wrapper(gm: GroupMessage):
            nem = NEM(gm, '&')
            if nem.permission.isBlocked():
                raise ExecutionStop()
            inList = False
            if not nem.plain_message:
                raise ExecutionStop()
            for word in words_list:
                if word in nem.plain_message:
                    inList = True
                    break
            if not inList:
                raise ExecutionStop()
        return Depend(wrapper)

    @staticmethod
    def onMatch(pattern: str):
        '''在消息匹配正则表达式时执行

        Args:
            pattern: 正则表达式（必须为 str）'''
        def wrapper(gm: GroupMessage):
            nem = NEM(gm, '&')
            if nem.permission.isBlocked():
                raise ExecutionStop()
            if not nem.plain_message:
                raise ExecutionStop()
            if not re.match(pattern, nem.plain_message):
                raise ExecutionStop()
        return Depend(wrapper)

    @staticmethod
    def onMatchs(pattern_list: List[str]):
        '''在消息匹配正则表达式列表中的任何一项时执行

        Args:
            pattern_list: 正则表达式列表'''
        def wrapper(gm: GroupMessage):
            nem = NEM(gm, '&')
            if nem.permission.isBlocked():
                raise ExecutionStop()
            if not nem.plain_message:
                raise ExecutionStop()
            matched: bool = False
            for p in pattern_list:
                if re.match(p, nem.plain_message):
                    matched = True
                    break
            if not matched:
                raise ExecutionStop()
        return Depend(wrapper)
