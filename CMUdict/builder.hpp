#include "../MyCppLib/Logger/Logger.hpp"

#include <algorithm>
#include <array>
#include <cctype>
#include <exception>
#include <fstream>
#include <iostream>
#include <ostream>
#include <stdexcept>
#include <string>
#include <vector>

#include "../MyCppLib/Strings/Strings.hpp"
#define VALID_10K_FILE "./files/google-10000-english.txt"

using namespace std;
using namespace Printer;

struct Token {
  const std::string word;
  const vector<string> phonemes;
  const string phonemes_str;
  const string vowel_str;
  const string consonant_str;
  const unsigned int syllables;

  Token(const string &_word, const vector<string> &_phonemes,
        const string &_phonemes_str, const string& _vowel_str, const string& _consonant_str, const int &_syllables)
      : word(_word), phonemes(_phonemes), phonemes_str(_phonemes_str), vowel_str(_vowel_str), consonant_str(_consonant_str),
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
    const string &preword = split_line[0];
    string word;
    for (auto &character : preword) {
      if (character == '\'') {
        word += "\\'";
      } else
        word += character;
    }
    vector<std::string> phonemes;
    std::string phonemes_str;
    std::string vowel_str;
    std::string consonant_str;
    unsigned int i = 1;
    while(i < split_line.size()) {
      if(isVowel(split_line[i])) {
        phonemes.push_back(split_line[i]);
        phonemes_str = split_line[i] + " " + phonemes_str;
        vowel_str = split_line[i] + " " + vowel_str;
        i++;
      }
      else {
        std::string consonant = "";
        while(i < split_line.size() && !isVowel(split_line[i])) {
          consonant += split_line[i];
          i++;
        }
        phonemes_str = consonant + " " + phonemes_str;
        consonant_str = consonant + " " + consonant_str;
      }
    }
    vowel_str = rstrip(vowel_str);
    consonant_str = rstrip(consonant_str);
    phonemes_str = rstrip(phonemes_str);
    const unsigned int &syllable_count = TokenMaker::countSyllables(phonemes);
    return Token(word, phonemes, phonemes_str, vowel_str, consonant_str, syllable_count);
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

struct DatabaseHandler {
    static vector<string> makeValid10k(){
        vector<string> ret;
        ifstream readfile(VALID_10K_FILE);
        if(!readfile){
            throw runtime_error(std::string("Can't read file:") + VALID_10K_FILE);
        }
        string buffer;
        while(getline(readfile, buffer)){
            string uppercase;
            for(unsigned int i = 0; i < buffer.size(); i++)
                uppercase += toupper(buffer[i]);
            ret.push_back(uppercase);
        }
        std::sort(ret.begin(), ret.end());
        return ret;
    }
    static string insertToSmallDictQuery(const Token& token, vector<string>& valid10k){
        for(vector<string>::iterator it = valid10k.begin(); it != valid10k.end(); it++){
            if(*it == token.word){
                std::string query = "INSERT INTO smallDict(word, phonemes, vowels, consonants, syllables)";
                const std::string values = "VALUES('" + token.word + "', '" + token.phonemes_str +
                                     "', '" + token.vowel_str + "', '" + token.consonant_str + "', " + to_string(token.syllables) + ")";
                query += values;
                valid10k.erase(it);
                return query;
            }
        }
        return "";
    }
    static string insertToBigDictQuery(const Token &token) {
    std::string query = "INSERT INTO bigDict(word, phonemes, vowels, consonants, syllables)";

    std::string values = "VALUES('" + token.word + "', '" + token.phonemes_str +
                         "', '" + token.vowel_str + "', '" + token.consonant_str + "', " + to_string(token.syllables) + ")";
    query += values;
    return query;
  }
};
