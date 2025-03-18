#include "builder.hpp"
#include <fstream>
#include <string>

#define READFILE "files/cmudict-0.7b"

vector<string> readLines() {
  ifstream readStream(READFILE);
  if (!readStream.is_open()) {
    WPrinter::stdErr("could not read file: ", READFILE);
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
  for (auto line : lines) {
    cout << line << endl;
  }
  return lines;
}

int main() {
  const vector<string> lines = readLines();
  return 0;
}
