from const import PROJECT_DIR

words_list_file = PROJECT_DIR + "dictionnary/files/en_US.txt"
dest = PROJECT_DIR + "server/words_list.txt"

words = []

def create():
    with open(words_list_file, "r") as file:
        lines = file.readlines()
        for line in lines:
            words.append(line.split()[0].strip())

    with open(dest, "w") as file:
        for word in words:
            file.write(word + "\n")

def get() -> list[str]:
    return words

if __name__ == "__main__":
    create()
    get()
