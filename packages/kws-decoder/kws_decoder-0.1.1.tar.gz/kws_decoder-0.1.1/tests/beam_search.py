import json
from collections import defaultdict, Counter

import numpy as np
import torch
from pygtrie import CharTrie
from tqdm import tqdm


def prefix_beam_search(
    alphabet,
    blank_index,
    ctc,
    keywords,
    beam_width=16,
    beta=1.02,
    min_keyword_score=0.001,
    max_gap=25,
    clip_char_prob=0.01,
):
    trie = CharTrie()
    for word in keywords:
        trie[word] = True

    result = defaultdict(list)

    # STEP 1: Initiliazation
    O = ""
    Pb, Pnb = defaultdict(Counter), defaultdict(Counter)
    Pb[-1][O] = 1
    Pnb[-1][O] = 0
    A_prev = [O]
    # END: STEP 1

    # STEP 2: Iterations and pruning
    ctc = ctc.clip(clip_char_prob)
    for t in range(ctc.shape[0]):
        # print(f'timestep: {t}, hyp len: {len(A_prev)}')
        # pruned_alphabet = [alphabet[i] for i in np.where(ctc[t] > prune)[0]]
        for l in A_prev:
            for c in alphabet:
                c_ix = alphabet.index(c)
                # END: STEP 2

                # STEP 3: “Extending” with a blank
                if c_ix == blank_index:
                    Pb[t][l] += ctc[t][blank_index] * (Pb[t - 1][l] + Pnb[t - 1][l])
                # END: STEP 3

                # STEP 4: Extending with the end character
                else:
                    l_plus = l + c
                    if len(l) > 0 and c == l[-1]:
                        Pnb[t][l_plus] += ctc[t][c_ix] * Pb[t - 1][l]
                        Pnb[t][l] += ctc[t][c_ix] * Pnb[t - 1][l]
                    # END: STEP 4

                    # STEP 5: Extending with any other non-blank character and LM constraints
                    else:
                        Pnb[t][l_plus] += ctc[t][c_ix] * (Pb[t - 1][l] + Pnb[t - 1][l])
                    # END: STEP 5

                    # STEP 6: Make use of discarded prefixes
                    if l_plus not in A_prev:
                        Pb[t][l_plus] += ctc[t][blank_index] * (
                            Pb[t - 1][l_plus] + Pnb[t - 1][l_plus]
                        )
                        Pnb[t][l_plus] += ctc[t][c_ix] * Pnb[t - 1][l_plus]
                    # END: STEP 6

        # STEP 7: Select most probable prefixes
        A_next = Pb[t] + Pnb[t]
        sorted_items = sorted(
            A_next.items(), key=lambda x: x[1] * (beta ** len(x[0])), reverse=True
        )
        A_prev = []
        has_empty_string = False
        for prefix, prob in sorted_items:
            score = prob * beta ** len(prefix)
            if score < min_keyword_score:
                break
            if len(A_prev) >= beam_width:
                break
            if prefix == O:
                has_empty_string = True
            num_nodes = trie.has_node(prefix)
            if num_nodes == 0:
                continue
            elif num_nodes == 2:
                A_prev.append(prefix)
            # 1, 3
            else:
                if len(result[prefix]):
                    if t * 0.02 - result[prefix][-1]["end"] < max_gap * 0.02:
                        if result[prefix][-1]["score"] < score:
                            result[prefix].pop()
                            result[prefix].append({"end": t * 0.02, "score": score})
                    else:
                        result[prefix].append({"end": t * 0.02, "score": score})
                else:
                    result[prefix].append({"end": t * 0.02, "score": score})
                A_prev.append(prefix)
        # END: STEP 7
        if not has_empty_string:
            A_prev.append("")
        Pb[t][O] = 1
        Pnb[t][O] = 0
        # print(f'timestep: {t}\nA_prev length: {len(A_prev)}\n{A_prev}\n')
    return result
