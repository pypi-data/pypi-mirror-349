#ifndef NODE_H
#define NODE_H

#include <vector>

using namespace std;

class Node
{
    bool is_word;
    char32_t ch;
    vector<Node*> children;

    public:
        Node();
        Node(char32_t, bool);

        vector<Node*> get_children();
        void add_child(Node*);
        char32_t get_char();
        bool get_is_word();
        void set_is_word(bool);
};

#endif
