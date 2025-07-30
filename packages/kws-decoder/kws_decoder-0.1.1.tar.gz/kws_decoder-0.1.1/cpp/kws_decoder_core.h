#ifndef KWS_DECODER_CORE_H
#define KWS_DECODER_CORE_H

#include <vector>

#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>
#include <tuple>

#include "trie.h"

using namespace std;
namespace py = pybind11;

class KWSDecoder
{
    Trie trie;
    vector<char32_t> alphabet;
    int blank_index;
    int alphabet_size;
    long unsigned int beam_width = 64;
    float beta = 1.2;
    float min_keyword_score = 0.0001;
    int max_gap = 3;
    float min_clip = .01;
    int top_n = 25;

    public:
        KWSDecoder(vector<char32_t>, int);

        void add_words(vector<u32string>);
        map<u32string, vector<map<u32string, float>>> search(py::array_t<float>);

        // Getters
        vector<char32_t> get_alphabet();
        int get_blank_index();
        int get_alphabet_size();
        long unsigned int get_beam_width();
        float get_beta();
        float get_min_keyword_score();
        int get_max_gap();
        float get_min_clip();
        int get_top_n();

        // Setters
        void set_alphabet(vector<char32_t>&);
        void set_blank_index(int);
        void set_alphabet_size(int);
        void set_beam_width(long unsigned int);
        void set_beta(float);
        void set_min_keyword_score(float);
        void set_max_gap(int);
        void set_min_clip(float);
        void set_top_n(int);

    private:
        tuple<vector<int>, vector<vector<float>>> collapse(py::array_t<float>);
};

#endif
