from _typeshed import StrPath
from typing import List, Optional, Union

from graia.application.message.elements.internal import At, Image


class Command(object):
    '''指令相关

    `cmd` 为指令，
    `args` 为参数，
    `argsList` 为参数列表，
    '''
    cmd: Optional[str]
    args: Optional[str]
    argsList: Optional[List[str]]


class AtList(List[At]):
    '''
    At 的增强版，允许你更方便地操作 At 列表
    AtList 本身也是一个列表，因此可以使用大部分的 list 特性
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

    def __init__(self, atList: List[At]) -> None:
        self.ints = [i.target for i in atList]
        super().__init__(atList)

    def __contains__(self, at: Union[At, int]) -> bool:
        return self.__getTarget(at) in self.ints

    def append(self, at: Union[At, int]) -> None:
        if isinstance(at, At):
            atObj = at
        elif isinstance(at, int):
            atObj =  At(at)
        else:
            raise TypeError('Must be Union[At, int]')
        super().append(atObj)

    def __set(self, l: List[At]) -> None:
        '''
        内部函数，用于更新 AtList
        '''
        self.__init__(l)

    def get(self, at: Union[At, int]) -> At:
        '''
        根据 QQ 号或 `At` 对象获取 `At` 对象本身
        '''
        target = self.__getTarget(at)
        ats: List[At] = self.copy()
        for i in ats:
            if i.target == target:
                return i
        else:
            return None

    def __del(self, at: Union[At, int]) -> None:
        '''
        内部函数，用于删除 `AtList` 中的某一项
        '''
        target = self.__getTarget(at)
        ats = self.copy()
        for i in range(len(ats)):
            if ats[i].target == target:
                del ats[i]
                self.__set(ats)
                break

    def delete(self, at: Union[At, int]) -> None:
        '''
        根据传入的 QQ 号或 `At` 对象删除 `AtList` 中的所有匹配项
        '''
        while self.__contains__(at):
            self.__del(at)


class ImagePro(Image):
    async def save2file(self, filepath: StrPath) -> None:
        imageBytes = await self.http_to_bytes()
        with open(filepath, 'wb') as f:
            f.write(imageBytes)
