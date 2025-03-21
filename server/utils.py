from typing import Optional
from const import PROJECT_DIR

PATH = PROJECT_DIR + "secrets/secrets.txt"

def fetchAccountInfo(find: str) -> Optional[str]:
    with open(PATH, "r") as file:
        lines = file.readlines()
        for line in lines:
            split_line = line.strip().split("=")
            if split_line[0] == find:
                return split_line[1]
    return None

