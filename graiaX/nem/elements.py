from typing import List, Optional, Union

from graia.application.message.elements.internal import At


class Command(object):
    '''指令相关

        `cmd` 为指令，
        `args` 为参数，
        `argsList` 为参数列表，
        '''
    cmd: Optional[str]
    args: Optional[str]
    argsList: Optional[List[str]]


class AtPro(list):
    '''更好的 At'''
    ats: List[At]
    ints: List[int]

    def __new__(self, atList: List[At]) -> None:
        self.ats = atList
        self.ints = [i.target for i in atList]
        return atList

    def __contains__(self, targetAt: Union[At, int]) -> bool:
        if isinstance(targetAt, At):
            target = targetAt.target
        elif isinstance(targetAt, int):
            target = targetAt
        else:
            raise TypeError('Param \'targetAt\' must be Union[At, int]')
        return target in self.ints

    def __getitem__(self, key: int) -> Optional[At]:
        for i in self.ats:
            if i.target == key:
                return i
        else:
            return None
    
    def __delitem__(self, key: int) -> None:
        pass  # TODO
