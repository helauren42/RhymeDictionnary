#pragma once

#include <vector>
#include <array>
#include <iostream>
#include <iostream>
#include <fstream>

#include "MyCppLib/MyCppLib.hpp"
using namespace Printer;

struct ipapronunciation
{
    static constexpr std::array<std::string_view, 25> consonants = {
        "b", "d", "dʒ", "f", "g", "h", "k", "l", "m", "n", "ŋ", "p", "r", "s", 
        "ʃ", "t", "tʃ", "θ", "ð", "v", "w", "ʍ", "j", "z", "ʒ"
    };
    
    static constexpr std::array<std::string_view, 20> vowels = {
        "æ", "eɪ", "ɑ", "ɛər", "ɔ", "ɛ", "i", "ɪər", "ər", "ɜr", "ɪ", 
        "aɪ", "ɒ", "oʊ", "u", "ʊ", "ɔɪ", "aʊ", "ʌ", "ə"
    };
};

class Token {
    private:
        // void fetchIpaPronunciations(){
        //     rev_ipa_pronunciations = 
        // };
    public:
        std::string word;
        std::vector<std::string> parsed_pronunciations;
        std::vector<std::vector<std::string>> rev_ipa_pronunciations;
        Token(std::string& line) {
            removeAll(line, "/,");
            std::vector<std::string>line_split = split<std::vector>(line, " ");
            word = line_split[0];
            parsed_pronunciations.assign(line_split.begin()+1, line_split.end());
        };
        ~Token(){};
};
