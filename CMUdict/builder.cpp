#include "builder.hpp"
#include <fstream>
#include <string>

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
    for (auto &character : buffer) {
      if (character == '(' || character == ')' ||
          (character >= 48 && character <= 57))
        continue;
      line += character;
    }
    lines.push_back(line);
  };
  // for (auto line : lines) {
  //   cout << line << endl;
  // }
  return lines;
}

int main() {
  vector<Token> tokens;
  const vector<string> lines = readLines();
  for (auto &line : lines) {
    auto split_line = split<vector>(line, WHITE_SPACES);
    Printer::stdOut(split_line);
    if (split_line.empty() || split_line.size() < 2)
      continue;
    const Token &token = TokenMaker::makeToken(split_line);
    tokens.push_back(token);
  }
  Printer::stdOut(tokens);
  return 0;
}
