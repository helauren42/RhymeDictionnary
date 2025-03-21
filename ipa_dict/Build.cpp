#include "Build.hpp"
#include "Connector.hpp"

struct PATHS {
    static const std::string ProjectDir;
    static const std::string DictText;
    static const std::string Database;
};

const std::string PATHS::ProjectDir = "/home/henri/Projects/RhymeDictionnary/";
const std::string PATHS::DictText = PATHS::ProjectDir + "dictionnary/files/en_US.txt";
const std::string PATHS::Database = PATHS::ProjectDir + "db";

int main(int ac, char **av) {
    (void)ac;
    (void)av;
    std::locale::global(std::locale("en_US.UTF-8"));
    Logger::setLogger(PATHS::ProjectDir + "dictionnary/logger/logger.log", Logger::INFO, true);
    Connector connector;
    std::wifstream readFile(PATHS::DictText);
    if(!readFile) {
        stdErr("Error reading file: " + PATHS::DictText);
        Logger::debug("Error reading file" + PATHS::DictText);
        return 1;
    }
    std::wstring line;
    std::list<Token> tokens;
    while(getline(readFile, line)) {
        Token token = Token(line);
        // Logger::winfo(token);
        connector.addToken(token);
        // tokens.push_back(token);
    }
    return 0;
}
