#ifndef TRIE_H
#define TRIE_H

#include <string>

#include "node.h"

using namespace std;

class Trie
{
    Node *root;

    public:
        Trie();
        ~Trie();

        void add_word(u32string);
        bool has_word(u32string);
        bool is_promising(u32string);

    private:
        Node* get_root();
        Node* inspect_children(Node*, char32_t);
        Node* traverse(u32string);
};

#endif
