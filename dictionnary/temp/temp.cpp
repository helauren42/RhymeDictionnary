#include <iostream>
#include "./utfcpp/source/utf8.h"
#include "../MyCppLib/WPrinter/WPrinter.hpp"
#include <cwchar>
#include <locale>
#include <codecvt>

int main() {
    setlocale(LC_ALL, "");
    std::string utf8_str = "æβγ";
    std::wstring test = L"æβγ";
    std::wcout << test << std::endl;
    // std::string utf8_str = "ævg";
    auto it = utf8::iterator<std::string::iterator>(utf8_str.begin(), utf8_str.begin(), utf8_str.end());
    auto end = utf8::iterator<std::string::iterator>(utf8_str.end(), utf8_str.begin(), utf8_str.end());

    // WPrinter::stdOut("");
    for (; it != end; ++it) {
        char32_t codepoint = *it; // Get Unicode codepoint
        std::wcout << codepoint << std::endl;
        std::wcout << "\'" << static_cast<wchar_t>(codepoint) << "\'" << std::endl; // May not work on Windows
        std::wcout << "--------" << std::endl;
        // WPrinter::stdOut("anything");
        WPrinter::stdOut("codepoint: ", codepoint, ", char: ", static_cast<wchar_t>(codepoint));
        std::wcout << "--------" << std::endl;
    }
}

