from typing import List, TypeVar
import os.path

from graia.application.event.messages import FriendMessage, GroupMessage, TempMessage

AnyMessage = TypeVar('AnyMessage', GroupMessage, FriendMessage, TempMessage)

def createFiles(files: List[str]) -> None:
    for file in files:
        if not os.path.exists(file):
            with open(file, 'w') as f:
                f.write('')