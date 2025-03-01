#include "buildDb.hpp"

#define FILE "files/en_US.txt"

int main(int ac, char **av) {
    (void)ac;
    (void)av;
    Logger::setLogger("logger/logger.log", Logger::DEBUG, true);
    std::ifstream readFile(FILE);
    if(!readFile) {
        stdErr("Error reading file");
        Logger::debug("Error reading file");
    }
    std::string line;
    while(getline(readFile, line)) {
        Token token = Token(line);
    }
    return 0;
}
