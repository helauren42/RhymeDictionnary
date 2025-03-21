#include "../PATHS.hpp"

#include "../MyCppLib/Printer/Printer.hpp"
#include "../MyCppLib/Strings/Strings.hpp"
#include <cctype>
#include <fstream>
#include <iostream>
#include <vector>

using namespace std;

const std::string WORDS_LIST_FILE =
    std::string(PROJECT_DIR) + "CMUdict/files/cmudict-0.7b";
const std::string DEST =
    std::string(PROJECT_DIR) + "server/wordLists/CMU_english";

int main() {
  ifstream readFile(WORDS_LIST_FILE);
  Printer::setFout(DEST);
  if (!readFile) {
    cerr << "could not open file: " << WORDS_LIST_FILE << endl;
    return 1;
  }
  vector<string> lines;
  std::string buffer;
  while (getline(readFile, buffer)) {
    std::string line = buffer;
    lines.push_back(line);
    line = "";
  }
  for (auto line : lines) {
    vector<string> split_line = split<vector>(line, " ");
    string word;
    for (auto &character : split_line[0]) {
      if (character == '\'' || isalpha(character)) {
        word += character;
      }
    }
    Printer::Fout(word.c_str());
  }
  return 0;
}
