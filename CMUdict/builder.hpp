#include "../MyCppLib/MyCppLib.hpp"

#include <array>
#include <iostream>
#include <ostream>
#include <string>
#include <vector>

using namespace std;
using namespace Printer;

class Token {
public:
  const std::string word;
  const vector<string> phonemes;
  const unsigned int syllables;

  Token(const string &_word, const vector<string> &_phonemes,
        const int &_syllables)
      : word(_word), phonemes(_phonemes), syllables(_syllables) {};
  const std::string stringify() const {
    std::string ret;
    ret += "\nword: " + word + "\n";
    ret += "phonemes: " + std::string("\n");
    for (auto &phoneme : phonemes) {
      ret += phoneme + " ";
    }
    ret += "\n";
    ret += "syllables: " + to_string(syllables);
    ret += "\n";
    return ret;
  }
};

ostream &operator<<(ostream &lhs, const Token &token) {
  lhs << token.stringify();
  return lhs;
}

struct TokenMaker {
  static constexpr array<const char *, 15> vowels = {
      "AA", "AE", "AH", "AO", "AW", "AY", "EH", "ER",
      "EY", "IH", "IY", "OY", "OW", "UH", "UW"};
  static inline bool isVowel(const std::string &phoneme) {
    for (auto &vowel : vowels) {
      if (phoneme == vowel)
        return true;
    }
    return false;
  }
  static Token makeToken(const vector<string> &split_line) {
    const string &word = split_line[0];
    vector<std::string> phonemes;
    for (int i = 0; i < split_line.size(); i++) {
      phonemes.push_back(split_line[i]);
    }
    const unsigned int &syllable_count = TokenMaker::countSyllables(phonemes);
    return Token(word, phonemes, syllable_count);
  }
  static unsigned int countSyllables(const vector<string> &phonemes) {
    unsigned int count = 0;
    for (auto &phoneme : phonemes) {
      if (TokenMaker::isVowel(phoneme)) {
        count++;
      }
    }
    return count;
  }
};
