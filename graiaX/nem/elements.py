from typing import Iterator, List, Optional, Union

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
    '''
    At 的增强版，允许你更方便地操作 At 列表
    '''
    ints: List[int]

    @staticmethod
    def __getTarget(at: Union[At, int]) -> Optional[int]:
        if isinstance(at, At):
            return at.target
        elif isinstance(at, int):
            return at
        else:
            raise TypeError('Must be Union[At, int]')

    def __set(self, l: List[At]) -> None:
        self.__init__(l)

    def __init__(self, atList: List[At]) -> None:
        self.ints = [i.target for i in atList]
        super().__init__(atList)

    def __contains__(self, at: Union[At, int]) -> bool:
        return self.__getTarget(at) in self.ints

    def __iter__(self) -> Iterator[At]:
        return super().__iter__()

    def get(self, at: Union[At, int]) -> Optional[At]:
        target = self.__getTarget(at)
        ats: List[At] = self.copy()
        for i in ats:
            if i.target == target:
                return i
        else:
            return None

    def __del(self, at: Union[At, int]) -> None:
        target = self.__getTarget(at)
        ats = self.copy()
        for i in range(len(ats)):
            if ats[i].target == target:
                del ats[i]
                self.__set(ats)
                break

    def delete(self, at: Union[At, int]) -> None:
        while self.__contains__(at):
            self.__del(at)
