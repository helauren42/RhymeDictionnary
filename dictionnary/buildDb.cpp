#include "buildDb.hpp"
// #include <cppconn/driver.h>

#define FILE "files/en_US.txt"

int main(int ac, char **av) {
    (void)ac;
    (void)av;
    // setlocale(LC_ALL, "");
    std::locale::global(std::locale("en_US.UTF-8"));
    Logger::setLogger("logger/logger.log", Logger::INFO, true);
    std::wifstream readFile(FILE);
    if(!readFile) {
        stdErr("Error reading file");
        Logger::debug("Error reading file");
        return 1;
    }
    std::wstring line;
    std::list<Token> tokens;
    while(getline(readFile, line)) {
        Token token = Token(line);
        tokens.push_back(token);
    }
    return 0;
}
