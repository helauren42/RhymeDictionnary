import mariadb
import sys
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

try:
    conn_params = {
        'user' : f"{fetchAccountInfo('DB_USER')}",
        'password' : f"{fetchAccountInfo('DB_PASSWORD')}",
        'host' : "127.0.0.1",
        'port' : 3306,
        'database' : "rd"
    }

    connection = mariadb.connect(**conn_params)
    cursor = connection.cursor()
except Exception as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

