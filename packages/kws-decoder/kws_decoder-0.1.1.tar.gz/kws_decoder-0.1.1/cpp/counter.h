#ifndef COUNTER_H
#define COUNTER_H

#include <map>
#include <vector>

using namespace std;

class Counter
{
    map<u32string, float> counter;

    public:
        map<u32string, float> get_counter();
        void set_item(u32string, float);
        float get_value(u32string);
        void accumulate_prob(u32string, float);
        vector<u32string> get_keys();
        vector<float> get_normalized_probs(float beta);
        float get_normalized_prob(float beta, u32string key);
        Counter operator+(Counter);
        float operator[](u32string);
        void clear();
};

#endif
