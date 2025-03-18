import pymysql

PROJECT_DIR = "/home/henri/Projects/RhymeDictionnary/"
USER = ""
PWD = ""
HOST = "localhost"
CHARSET='utf8mb4'

try:
    with open(PROJECT_DIR + "secrets/secrets.txt") as file:
        lines = file.readlines()
        USER = lines[0].split("=")[1].strip()
        PWD = lines[1].split("=")[1].strip()

    connection = pymysql.connect(
        host=HOST,
        user=USER,
        password=PWD,
        charset=CHARSET
    )

    with connection.cursor() as cursor:
        cursor.execute("USE rd")
        cursor.execute("DROP table dict")
        cursor.close()
except Exception as e:
    print(e)
