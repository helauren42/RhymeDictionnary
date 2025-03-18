#include "../MyCppLib/Logger/Logger.hpp"

#include <array>
#include <iostream>
#include <ostream>
#include <string>
#include <vector>

using namespace std;
using namespace Printer;

struct Token {
  const std::string word;
  const vector<string> phonemes;
  const string phonemes_str;
  const unsigned int syllables;

  Token(const string &_word, const vector<string> &_phonemes,
        const string &_phonemes_str, const int &_syllables)
      : word(_word), phonemes(_phonemes), phonemes_str(_phonemes_str),
        syllables(_syllables) {};
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

struct DatabaseHandler {
  static void addTokenToDb(const Token &token) {
    std::string query = "INSERT INTO dict(word, phonemes, syllables)";
    std::string values = "VALUES('" + token.word + "', '" + token.phonemes_str +
                         "', " + to_string(token.syllables) + ")";
    query += values;
    // makeValuesStr(token.word, token.phonemes, token.syllables);
    Logger::info("makeing query: ", query);
  }
  //
  // template <typename... Args>
  // static std::string makeValuesStr(const Args &...args) {
  //   stringstream ret("VALUES(");
  //   while (sizeof...(args) > 0) {
  //     cout << std::string(args...) << endl;
  //     ret << std::string(args...);
  //   }
  //   return ret.str();
  // }
};

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
    std::string phonemes_str;
    for (unsigned int i = 0; i < split_line.size(); i++) {
      phonemes.push_back(split_line[i]);
      phonemes_str += split_line[i];
      if (i < split_line.size() - 1) {
        phonemes_str += " ";
      }
    }
    const unsigned int &syllable_count = TokenMaker::countSyllables(phonemes);
    return Token(word, phonemes, phonemes_str, syllable_count);
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
