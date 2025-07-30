#include <iostream>
#include <locale>
#include <codecvt>

#include "trie.h"

using namespace std;

// Utility function to convert std::u32string to std::string (UTF-8)
string to_utf8(const u32string& str) {
    wstring_convert<codecvt_utf8<char32_t>, char32_t> convert;
    return convert.to_bytes(str);
}

int main()
{
    Trie trie;

    // Test the Trie
    cout << "start of test" << endl;
    cout << "has مادر: " << trie.has_word(U"مادر") << endl << endl;
    cout << "has مادرید: " << trie.has_word(U"مادرید") << endl;
    cout << "adding madrid" << endl;
    trie.add_word(U"مادرید");
    cout << "has مادر: " << trie.has_word(U"مادر") << endl;
    cout << "has مادرید: " << trie.has_word(U"مادرید") << endl;
    cout << "is promising مادر: " << trie.is_promising(U"مادر") << endl;
    cout << "is promising مادرید: " << trie.is_promising(U"مادرید") << endl;
    return 0;
}
