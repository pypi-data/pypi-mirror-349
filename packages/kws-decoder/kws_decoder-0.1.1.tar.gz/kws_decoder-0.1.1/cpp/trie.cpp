#include <iostream>
#include <vector>

#include "trie.h"

using namespace std;

Trie::Trie()
{
    root = new Node();
}

Node* Trie::get_root()
{
    return root;
}

Trie::~Trie()
{
    delete root;
}

Node* Trie::inspect_children(Node* node, char32_t ch)
{
    vector<Node*> children = node->get_children();
    for (long unsigned int i = 0; i < children.size(); i++)
    {
        // cout<<"child: "<<i<<", char: "<<node->get_child(i)->get_char()<<endl;
        if (children[i]->get_char() == ch)
        {
            // cout<<"@inspect return: "<<i<<endl;
            return children[i];
        }
    }
    return get_root();
}

void Trie::add_word(u32string word)
{
    // cout<<"@add_word: "<<word<<endl;
    Node *tmp;
    Node *current_node = get_root();
    for (long unsigned int i = 0; i < word.length(); i++)
    {
        tmp = inspect_children(current_node, word[i]);
        // cout<<"node char: "<<current_node->get_char()<<", char: "<<word[i]<<", result: "<<the_child<<endl;
        if (tmp == get_root())
        {
            tmp = new Node(char32_t(word[i]), false);
            // cout<<"######### "<<tmp->get_char()<<" #########"<<endl;
            current_node->add_child(tmp);
            // cout<<"######### "<<tmp->get_char()<<" #########"<<endl;
        }
        current_node = tmp;
    }
    current_node->set_is_word(true);
}

Node* Trie::traverse(u32string word)
{
    Node* tmp;
    Node *current_node = get_root();
    for (long unsigned int i = 0; i < word.length(); i++)
    {
        tmp = inspect_children(current_node, word[i]);
        if (tmp == get_root())
        {
            return get_root();
        }
        current_node = tmp;
    }
    return current_node;
}

bool Trie::has_word(u32string word)
{
    Node* result = traverse(word);
    if (result == get_root())
    {
        return false;
    }
    return result->get_is_word();
}

bool Trie::is_promising(u32string word)
{
    Node* result = traverse(word);
    if (result == get_root())
    {
        return false;
    }
    return true;
}
