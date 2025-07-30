#include <iostream>
#include "node.h"

using namespace std;

int main()
{
    cout << "Testing Node class..." << endl;

    // Create nodes
    Node root(U'\0', false);
    Node* a = new Node(U'a', false);
    Node* b = new Node(U'b', false);
    Node* c = new Node(U'ث', true);

    // Add children
    root.add_child(a);
    a->add_child(b);
    b->add_child(c);

    // Print node information
    cout << "Root node children: " << root.get_children().size() << ", is word: " << root.get_is_word() << endl;
    cout << "Node 'a' children: " << a->get_children().size() << ", is word: " << a->get_is_word() << endl;
    cout << "Node 'b' children: " << b->get_children().size() << ", is word: " << b->get_is_word() << endl;
    cout << "Node 'c' children: " << c->get_children().size() << ", is word: " << c->get_is_word() << endl;

    // Clean up dynamically allocated memory
    delete a;
    delete b;
    delete c;

    cout << "Test complete." << endl;
    return 0;
}
