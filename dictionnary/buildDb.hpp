#pragma once

#include <vector>
#include <array>
#include <iostream>
#include <iostream>
#include <fstream>
#include <cwchar>
#include <locale>
#include <codecvt>

#include "MyCppLib/MyCppLib.hpp"
using namespace Printer;

enum Type{
    CONSONANT,
    VOWEL
};

namespace ipapronunciation
{
    static constexpr std::array<const wchar_t, 23> consonantFirstChars = {L'b', L'd', L'f', L'g', L'h', L'k', L'l', L'm', L'n', L'ŋ', L'p', L'r', L's', L'ʃ', L't', L'θ', L'ð', L'v', L'w', L'ʍ', L'j', L'z', L'ʒ'};
    static constexpr std::array<const wchar_t, 13> vowelFirstChars = {L'æ', L'e', L'ɑ', L'ɛ', L'ɔ', L'i', L'ə', L'ɜ', L'a', L'ɒ', L'o', L'u', L'ʊ'};

    static bool isConsonant(const wchar_t c) {
        for (auto &cons : consonantFirstChars) {
            if (c == cons) {
                return true;
            }
        }
        return false;
    }
    static bool isVowel(const wchar_t c) {
        for (auto &vowel : vowelFirstChars) {
            if (c == vowel) {
                return true;
            }
        }
        return false;
    }
};

class Token
{
private:
    Type findType(const wchar_t c) {
        if(ipapronunciation::isConsonant(c))
            return CONSONANT;
        return VOWEL;
    }
    size_t findPhonemeStart(const std::wstring my_string) {
        size_t len = my_string.length();
        size_t i = len -1;
        const Type type = findType(my_string[i]);
        if(type == CONSONANT){
            while(i > -1 && ipapronunciation::isConsonant(my_string[i]))
                i--;
        }
        else{
            while(i > -1 && ipapronunciation::isVowel(my_string[i]))
                i--;
        }
        return i+1;
    }
    void fetchIpaPronunciations(const std::vector<std::string> &strings_pronunciation)
    {
        for (const std::string& str_pronunciation : strings_pronunciation) {
            std::wstring my_wstring(str_pronunciation.begin(), str_pronunciation.end());
            std::wcout << "wstring: " << my_wstring << std::endl;
            std::vector<std::wstring> phoneme_list;
            while(my_wstring.size()) {
                size_t start = findPhonemeStart(my_wstring);
                std::wstring phoneme = my_wstring.substr(start);
                my_wstring[start] = 0;
                phoneme_list.push_back(phoneme);
            }
            rev_ipa_pronunciations.push_back(phoneme_list);
            Logger::winfo("rev ipa: ", rev_ipa_pronunciations);
        }
    }

public:
    std::string word;
    std::vector<std::vector<std::wstring>> rev_ipa_pronunciations;
    Token(std::string &line)
    {
        removeAll(line, "/,");
        std::vector<std::string> line_split = split<std::vector>(line, WHITE_SPACES);
        word = line_split[0];
        const std::vector<std::string> strings_pronunciation(line_split.begin() + 1, line_split.end());
        fetchIpaPronunciations(strings_pronunciation);
    };
    ~Token() {};
};

// std:ostream& operator<<()
