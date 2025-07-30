import pytest
from kws_decoder import Trie


def test_trie_persian():
    trie = Trie()
    trie.add_word("مادرید")

    assert trie.has_word("مادرید") is True
    assert trie.has_word("مادر") is False
    assert trie.is_promising("مادر") is True
    assert trie.is_promising("مار") is False


def test_trie_english():
    trie = Trie()
    trie.add_word("hello")

    assert trie.has_word("hello") is True
    assert trie.has_word("hell") is False
    assert trie.is_promising("hell") is True
    assert trie.is_promising("her") is False
