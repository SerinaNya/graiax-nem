from typing import List
import os.path

def createFiles(files: List[str]) -> None:
    for file in files:
        if not os.path.exists(file):
            with open(file, 'w') as f:
                f.write('')