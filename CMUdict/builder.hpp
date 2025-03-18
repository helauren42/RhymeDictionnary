#include "../MyCppLib/MyCppLib.hpp"

#include <array>
#include <iostream>
#include <vector>

#define FILE "files/cmudict-0.7b"

using namespace std;

class Token {
private:
  const std::string word;
  const vector<string> phonemes;
  const unsigned int syllables;

public:
  Token(const string &_word, const vector<string> &_phonemes,
        const int &_syllables)
      : word(_word), phonemes(_phonemes), syllables(_syllables) {};
};

struct Builder {
  static constexpr array<const char *, 13> vowels = {
      "AA", "AE", "AH", "AO", "AW", "AY", "EH",
      "ER", "EY", "IH", "IY", "UH", "UW"};
  bool isVowel(const std::string &phoneme) {
    for (auto &vowel : vowels) {
      if (phoneme == vowel)
        return true;
    }
    return false;
  }

  vector<string> getPhonemes(const std::string &line) {
    return split<vector>(line);
  }

  unsigned int count_syllables(const vector<string> &phonemes) {
    for (auto &phoneme : phonemes) {
      unsigned int count = 0;
      if (isVowel(phoneme)) {
        count++;
      }
      return count;
    }
  }
};
