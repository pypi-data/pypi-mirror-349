# Keyword Spotting Decoder

This repository provides a high-performance implementation of a Keyword Spotting (KWS) decoder in C++, designed to accelerate decoding in Python via pybind11.

KWS is essentially a streamlined beam search algorithm that looks for specified keywords directly in the output of an acoustic model (AM).  For example, consider the output from an acoustic model for the WAV file "tests/data/George_crop2.wav", where the speaker says:
"AT ANY SECOND AND JUST GO AND THEN WATCH EVERYBODY'S MOUTH DROP I WILL NOT BE OVER"

![Sample acoustic model output](tests/data/output.png)

The image above shows the first few timesteps of the acoustic model's output for the given text (for clarity).

There are two main approaches to searching for specific keywords in audio:
1. **Transcribe the entire audio**: Convert all spoken words to text, then search for your keywords in the transcription.
2. **Direct keyword search in the acoustic model output**: Search for keywords directly in the AM output.

The first approach is prone to errors due to the influence of the language model (LM) during ASR decoding. The LM may alter the output to form more probable sentences, potentially causing actual spoken keywords to be missed or replaced with other words.

KWS addresses this issue by searching for your desired keywords directly in the acoustic model output, bypassing the language model and reducing the chance of missing keywords.

## Installation

The module is available on PyPI. You can install it with:

```bash
pip install kws-decoder
```

## Usage example

the following code shows a simple example that this module could be used:

```python
import numpy as np
from kws_decoder import KWSDecoder

labels = ["-", "|", "A", "B"]
blank_index = 0
decoder = KWSDecoder(labels, blank_index)

# you can set/get decoder parameters using setter/getter functions
decoder.set_beam_width(128)
decoder.set_beta(1.05)

# don't forget to add keywords to the decoder
keywords = ["AA", "AB"]
decoder.add_words(keywords)

# create a dummy am output
logits = np.random.randn(1000, 4).astype(np.float32)
exp_logits = np.exp(logits - logits.max(axis=1, keepdims=True))
probs = exp_logits / exp_logits.sum(axis=1, keepdims=True)

# then you can search through AM output
decoder.search(probs)
```

## Algorithm hyper parameters

Here is the list of the most important and influential parameters of the decoder:

`beam_width`: Number of candidate sequences (beams) kept at each decoding step. Larger values can improve accuracy at the cost of more computation and time.

`beta`: Longer keywords naturally receive lower scores because more probabilities (each 0–1) are multiplied together. `beta` compensates for this length penalty: the score of a keyword is `p(keyword) × beta^len(keyword).`

`min_keyword_score`: Minimum score a keyword must reach to be accepted as detected. Any (partial or complete) keyword below this threshold is pruned from the beam.

`max_gap`: Maximum allowed gap, in timesteps, between successive detections of the same keyword. If two detections end within `max_gap`, they are merged into one occurrence whose score is the maximum of the two.

`min_clip`: Floor value applied to every character probability to prevent underflow and improve numerical stability, increasing algorithm robustness. Note that setting this value too high increases the likelihood of false alarms.

`top_n`: At each timestep only the top_n most-probable characters are expanded, limiting the branching factor of the beam search. It must be less than or equal to the number of characters.


### (Optional) Run Sample Python Implementation Codes

The original code was developed in Python. To run the original implementation, install the package with:

```bash
pip install kws-decoder[ext]
```

This command installs `pygtrie`, `torch`, and `tqdm`, which are necessary to run the original implementation of the beam search algorithm. After installing the dependencies, you can run the script with the original Python implementation located in the test folder, specifically "beam_search.py".


# Testing

After installing the module, you can run unit tests using `pytest`:

```bash
pytest
```

It runs two tests written in Persian and English to ensure everything works as expected.
