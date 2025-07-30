#include <iostream>

#include "node.h"

using namespace std;

Node::Node()
{
    ch = '@';
    is_word = false;
    std::vector<Node*> children;
    // cout<<"@node end of simple instructor"<<endl;
    // cout<<ch<<endl;
    // cout<<is_word;
    // cout<<&children;
    // cout<<endl<<"----------"<<endl;
}

Node::Node(char32_t init_ch, bool init_is_word)
{
    ch = init_ch;
    is_word = init_is_word;
    std::vector<Node*> children;
    // cout<<"@node end of complex instructor"<<endl;
}

vector<Node*> Node::get_children()
{
    return children;
}

void Node::add_child(Node *node)
{
    children.push_back(node);
    // cout<<"num childs: "<<children.size()<<endl;
}

char32_t Node::get_char()
{
    return ch;
}

bool Node::get_is_word()
{
    return is_word;
}

void Node::set_is_word(bool value)
{
    is_word = value;
}
