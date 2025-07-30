#include <vector>

#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>

#include "trie.h"
#include "kws_decoder_core.h"

namespace py = pybind11;

PYBIND11_MODULE(kws_decoder, m)
{
    m.doc() = "Keyword Spotting Decoder Module"; // Module description

    py::class_<Trie>(m, "Trie")
        .def(py::init<>(), "Initialize an empty Trie.")
        .def("add_word", &Trie::add_word, "Add a word to the Trie.")
        .def("has_word", &Trie::has_word, "Check if a word exists in the Trie.")
        .def("is_promising", &Trie::is_promising, "Check if a prefix is promising in the Trie.");

    py::class_<KWSDecoder>(m, "KWSDecoder", "Keyword Spotting Decoder class.")
        .def(py::init<vector<char32_t>, int>(),
             py::arg("alphabet"), py::arg("blank_index"),
             "Initialize the KWSDecoder with an alphabet and blank index.")
        .def("add_words", &KWSDecoder::add_words,
             py::arg("words"),
             "Add a list of words to the decoder.")
        .def("search", &KWSDecoder::search,
             py::arg("probs"),
             "Perform a search on the given probability array.")
        // getters
        .def("get_blank_index", &KWSDecoder::get_blank_index, "Get the blank index.")
        .def("get_alphabet_size", &KWSDecoder::get_alphabet_size, "Get the size of the alphabet.")
        .def("get_beam_width", &KWSDecoder::get_beam_width, "Get the beam width.")
        .def("get_beta", &KWSDecoder::get_beta, "Get the beta value.")
        .def("get_min_keyword_score", &KWSDecoder::get_min_keyword_score, "Get the minimum keyword score.")
        .def("get_max_gap", &KWSDecoder::get_max_gap, "Get the maximum gap allowed.")
        .def("get_min_clip", &KWSDecoder::get_min_clip, "Get the minimum clip value.")
        .def("get_top_n", &KWSDecoder::get_top_n, "Get the top N results.")
        // setters
        .def("set_blank_index", &KWSDecoder::set_blank_index,
             py::arg("blank_index"),
             "Set the blank index.")
        .def("set_alphabet_size", &KWSDecoder::set_alphabet_size,
             py::arg("alphabet_size"),
             "Set the size of the alphabet.")
        .def("set_beam_width", &KWSDecoder::set_beam_width,
             py::arg("beam_width"),
             "Set the beam width.")
        .def("set_beta", &KWSDecoder::set_beta,
             py::arg("beta"),
             "Set the beta value.")
        .def("set_min_keyword_score", &KWSDecoder::set_min_keyword_score,
             py::arg("min_keyword_score"),
             "Set the minimum keyword score.")
        .def("set_max_gap", &KWSDecoder::set_max_gap,
             py::arg("max_gap"),
             "Set the maximum gap allowed.")
        .def("set_min_clip", &KWSDecoder::set_min_clip,
             py::arg("min_clip"),
             "Set the minimum clip value.")
        .def("set_top_n", &KWSDecoder::set_top_n,
             py::arg("top_n"),
             "Set the top N results.");
}
