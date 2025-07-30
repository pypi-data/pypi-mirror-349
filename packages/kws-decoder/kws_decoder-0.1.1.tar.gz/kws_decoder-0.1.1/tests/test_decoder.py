import json
from pathlib import Path

import torch
import pytest

from kws_decoder import KWSDecoder
from beam_search import prefix_beam_search

RESOURCES = Path(__file__).parent / "data"


def filter_results(results, threshold=0.15):
    """
    Filter the results to only include high probable keywords.
    """
    tmp = {
        k: [occ for occ in v if occ["score"] > threshold] for k, v in results.items()
    }
    return {k: v for k, v in tmp.items() if v}


@pytest.mark.parametrize(
    "lang, label_file, data_file, keywords",
    [
        (
            "ENGLISH",
            "labels.json",
            "output.pth",
            ["think", "sport", "cheat", "kids", "remember"],
        ),
        (
            "PERSIAN",
            "fa_labels.json",
            "fa_output.pth",
            ["پادشاه", "پرگار", "ارادت", "جلال", "عظمت", "طالبی"],
        ),
    ],
)
def test_kws_decoder(lang, label_file, data_file, keywords):
    label_path = RESOURCES / label_file
    data_path = RESOURCES / data_file

    with open(label_path, encoding="utf-8") as f:
        labels = json.load(f)

    data = torch.load(data_path, weights_only=True)
    data = data.squeeze().numpy()

    if lang == "ENGLISH":
        keywords = [word.upper() for word in keywords]

    ref_results = prefix_beam_search(labels, 0, data, keywords)
    ref_results = filter_results(ref_results)

    decoder = KWSDecoder(labels, 0)
    decoder.add_words(keywords)
    results = decoder.search(data)
    results = filter_results(results)

    # Compare keys
    assert set(ref_results.keys()) == set(results.keys())
    for k, values in ref_results.items():
        assert len(values) == len(results[k])

    # Optionally, compare the results more deeply
    # For demonstration, just print results
    print(f"\n########## {lang} ##########")
    print("Reference result:")
    print(json.dumps(ref_results, indent=4, ensure_ascii=False))
    print("C++ result:")
    print(json.dumps(results, indent=4, ensure_ascii=False))
