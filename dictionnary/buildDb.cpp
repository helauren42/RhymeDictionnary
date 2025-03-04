#include "buildDb.hpp"

#define FILE "files/en_US.txt"

int main(int ac, char **av) {
    (void)ac;
    (void)av;
    // setlocale(LC_ALL, "");
    std::locale::global(std::locale("en_US.UTF-8"));
    Logger::setLogger("logger/logger.log", Logger::DEBUG, true);
    std::wifstream readFile(FILE);
    if(!readFile) {
        stdErr("Error reading file");
        Logger::debug("Error reading file");
    }
    std::wstring line;
    while(getline(readFile, line)) {
        // stdOut("line: ", line);
        Token token = Token(line);
    }
    return 0;
}
