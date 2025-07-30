#include <iostream>
#include <map>
#include <locale>
#include <codecvt>

#include "counter.h"

using namespace std;

// Utility function to convert std::u32string to std::string (UTF-8)
string to_utf8(const u32string str) {
    wstring_convert<codecvt_utf8<char32_t>, char32_t> convert;
    return convert.to_bytes(str);
}

int main()
{
    Counter counter1, counter2;

    counter1.set_item(U"a", 1.);
    counter1.set_item(U"ب", 2.);
    counter2.set_item(U"a", 3.);

    Counter result = counter1 + counter2;

    // Method 1: Print the counter using an iterator
    map<u32string, float> counter = result.get_counter();
    for (map<u32string, float>::iterator i = counter.begin(); i != counter.end(); i++)
    {
        cout << "key: " << to_utf8(i->first) << ", value: " << i->second << endl;
    }

    cout << "end of program" << endl;
    return 0;
}
