#include <map>
#include <vector>
#include <set>
#include <cmath>
#include <locale>
#include <codecvt>
#include <iostream>

#include "counter.h"

using namespace std;

map<u32string, float> Counter::get_counter()
{
    return counter;
}

void Counter::set_item(u32string prefix, float prob)
{
    counter[prefix] = prob;
}

float Counter::get_value(u32string prefix)
{
    return counter[prefix];
}

void Counter::accumulate_prob(u32string prefix, float prob)
{
    counter[prefix] += prob;
}

vector<u32string> Counter::get_keys()
{
    vector<u32string> result;
    for(map<u32string, float>::iterator i = counter.begin(); i != counter.end(); i++)
    {
        result.push_back(i->first);
    }
    return result;
}

float Counter::get_normalized_prob(float beta, u32string key)
{
    // return counter[key] * pow(beta, wstring_convert<codecvt_utf8<char32_t>, char32_t>{}.from_bytes(key).size());
    return counter[key] * pow(beta, key.size());
}

vector<float> Counter::get_normalized_probs(float beta)
{
    vector<float> result;
    for(map<u32string, float>::iterator i = counter.begin(); i != counter.end(); i++)
    {
        result.push_back(i->second * pow(beta, wstring_convert<codecvt_utf8<char32_t>, char32_t>{}.from_bytes(i->first.length()).size()));
    }
    return result;
}

Counter Counter::operator+(Counter operand)
{
    set<u32string> keys;
    for (u32string key : get_keys())
    {
        keys.insert(key);
    }
    for (u32string key : operand.get_keys())
    {
        keys.insert(key);
    }

    Counter result;
    for (u32string key : keys)
    {
        result.set_item(key, counter[key] + operand[key]);
    }
    return result;
}

float Counter::operator[](u32string prefix)
{
    return counter[prefix];
}

void Counter::clear()
{
    counter.clear();
}
