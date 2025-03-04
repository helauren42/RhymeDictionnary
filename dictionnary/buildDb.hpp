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
using namespace WPrinter;

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
        int i = len -1;
        const Type type = findType(my_string[i]);
        if(type == CONSONANT)
            while(i > 1 && ipapronunciation::isConsonant(my_string[i]))
                i--;
        else
            while(i > 1 && ipapronunciation::isVowel(my_string[i]))
                i--;
        return i;
    }
    void fetchIpaPronunciations(const std::vector<std::wstring> &strings_pronunciation)
    {
        for (std::wstring pronun : strings_pronunciation) {
            // std::wcout << "str : " << str_pronunciation << std::endl;
            std::vector<std::wstring> phoneme_list;
            while(pronun.size()) {
                // Logger::wdebug("pronun: ", pronun);
                size_t start = findPhonemeStart(pronun);
                // Logger::wdebug("start: ", start);
                std::wstring phoneme = pronun.substr(start);
                // Logger::wdebug("phoneme: \'", phoneme, "\'");
                if(phoneme.size() == 0)
                    continue;
                phoneme_list.push_back(phoneme);
                // Logger::wdebug("phoneme list: ", phoneme_list);
                pronun = pronun.substr(0, start);
            }
            rev_ipa_pronunciations.push_back(phoneme_list);
            Logger::winfo("rev ipa: ", rev_ipa_pronunciations);
        }
    }

public:
    std::wstring word;
    std::vector<std::vector<std::wstring>> rev_ipa_pronunciations;
    Token(std::wstring &line)
    {
        Logger::wdebug("before: ", line);
        line = wremoveAll(line, L"/ˌ,ˈ");
        Logger::wdebug("after: ", line);
        std::vector<std::wstring> line_split = wsplit<std::vector>(line, L" \t\n\r\v\f\u00A0\u200B");
        word = line_split[0];
        const std::vector<std::wstring> strings_pronunciation(line_split.begin() + 1, line_split.end());
        fetchIpaPronunciations(strings_pronunciation);
    };
    ~Token() {};
};

std::wstring& operator<<(std::wstring& lhs, const Token& token) {
    lhs += L"word: " + token.word + L"\n";
    for(auto& pronun : token.rev_ipa_pronunciations){
        lhs += L"ipa: [ ";
        for(auto& phoneme : pronun){
            lhs += phoneme + L' ';
        }
        lhs += L"]";
    }
    return lhs;
}
