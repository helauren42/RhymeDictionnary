#include "builder.hpp"
#include <fstream>
#include <string>
#include <vector>

#include "../MyCppLib/Logger/Logger.hpp"
#include "../MyCppLib/Strings/Strings.hpp"
#include "connector.hpp"

#define READFILE "files/cmudict-0.7b"

unsigned int count_syllables(const vector<string> &phonemes) {
  unsigned int count = 0;
  for (auto &phoneme : phonemes) {
    if (TokenMaker::isVowel(phoneme)) {
      count++;
    }
  }
  return count;
};

vector<string> readLines() {
  ifstream readStream(READFILE);
  if (!readStream.is_open()) {
    Printer::stdErr("could not read file: ", READFILE);
  }
  std::string buffer;
  vector<std::string> lines;
  while (getline(readStream, buffer)) {
    std::string line;
    unsigned int word_end = buffer.find_first_of(" ");
    for (unsigned int i = 0; buffer[i]; i++) {
      const char character = buffer[i];
      if (i > word_end) {
        if (character == '\'')
          continue;
      }
      if (character == '(' || character == ')' ||
          (character >= 48 && character <= 57))
        continue;
      line += character;
    }
    lines.push_back(line);
  };
  return lines;
}

int main() {
  std::vector<string> valid10k = DatabaseHandler::makeValid10k();
  vector<Token> tokens;
  Logger::setLogger("logger/logger.log", Logger::INFO, true);
  Connector connector;
  const vector<string> lines = readLines();
  for (auto &line : lines) {
    Logger::fatal("1: ", line);
    auto split_line = split<std::vector>(line, WHITE_SPACES);
    Logger::fatal("2 split line size: ", split_line.size());
    if (split_line.empty() || split_line.size() < 2)
      continue;
    Logger::fatal("2.2");
    const Token &token = TokenMaker::makeToken(split_line);
    Logger::fatal("3: ", token.phonemes.size());
    if (token.phonemes.size() < 2)
      continue;
    string query = DatabaseHandler::insertToBigDictQuery(token);
    connector.makeQuery(query);
    query = DatabaseHandler::insertToSmallDictQuery(token, valid10k);
    if (query.size() > 0)
      connector.makeQuery(query);
    Logger::fatal("4");
  }
  Logger::info("the end");
  return 0;
}
