#include "builder.hpp"
#include <fstream>
#include <string>

#include "../MyCppLib/Logger/Logger.hpp"
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
  vector<Token> tokens;
  Logger::setLogger("logger/logger.log", Logger::INFO, true);
  Connector connector;
  const vector<string> lines = readLines();
  for (auto &line : lines) {
    auto split_line = split<vector>(line, WHITE_SPACES);
    if (split_line.empty() || split_line.size() < 2)
      continue;
    const Token &token = TokenMaker::makeToken(split_line);
    // tokens.push_back(token);
    const string query = DatabaseHandler::buildQuery(token);
    connector.makeQuery(query);
    // connector.makeQuery("SELECT * FROM dict");
  }
  Logger::debug(tokens);
  Logger::info("the end");
  return 0;
}
