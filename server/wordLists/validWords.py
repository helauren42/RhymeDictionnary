from const import PROJECT_DIR

words_list_file = PROJECT_DIR + "CMUdict/files/cmudict-0.7b"
dest = PROJECT_DIR + "server/words_list.txt"

words = []

def create():
    with open(words_list_file, "r") as file:
        lines = file.readlines()
        for line in lines:
            word = line.split()[0].strip()
            if word is not None and len(word) > 0:
                words.append(word)
    with open(dest, "w") as file:
        for word in words:
            file.write(word + "\n")

def get() -> list[str]:
    return words

if __name__ == "__main__":
    create()
    get()

