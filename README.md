This is a solid, clean implementation of the Byte-Pair Encoding (BPE) algorithm in Python\! The separation of the training logic (`BPE.py`) and the usage logic (`main.py`) is excellent.

I'll provide the requested **`README.md`** file, which explains the project structure, how to run the code, and how the BPE process works.

-----

# 📚 BPE Text Tokenizer

A complete, from-scratch implementation of the Byte-Pair Encoding (BPE) algorithm for text tokenization and vocabulary building, written in Python.

## 🌟 Features

  * **Training (`BPE.py`):** Builds a custom BPE vocabulary from a provided corpus up to a specified size.
  * **Encoding (`main.py`):** Tokenizes new text using the trained vocabulary by iteratively merging known pairs.
  * **Decoding (`main.py`):** Reconstructs text from token IDs.
  * **Persistent Vocab:** Saves and loads the vocabulary in JSON format for re-use.
  * **Out-of-Vocabulary (OOV) Handling:** Uses an `[UNK]` token for unknown characters/sequences.

## 📂 Project Structure

```
BPE_project/
├── BOOKS/                      # Your training corpus files (e.g., 'candide.txt')
├── Vocabs/                     # Directory where the trained vocabularies are saved
│   └── Vocab_of_candide.json   # Example saved vocabulary
├── BPE.py                      # Training script for building the BPE vocabulary
├── main.py                     # Encoding and decoding script using a trained vocabulary
├── .gitignore                  # Should exclude __pycache__ and sensitive files
└── README.md                   # This file
```


## 🚀 Getting Started

### 1\. Training the Vocabulary (`BPE.py`)

Run the training script first to generate the vocabulary file that the `main.py` encoder will use.

1.  **Run the script:**

    ```bash
    python BPE.py
    ```

2.  **Provide the Input Path:** The script will prompt you for the path to your training corpus (e.g., a large text file).

    ```
    PATH: BOOKS/candide.txt
    ```

3.  **Set the Vocab Size:** The script will ask for the target size of the final vocabulary.

    ```
    Vocab size: 1000
    ```

4.  **Output:** The script will save the final vocabulary (containing all characters and learned merged tokens) to the `Vocabs/` directory, for example: `/home/sebastien/Documents/bpe/Vocabs/Vocab_of_candide.json`.

### 2\. Encoding and Decoding (`main.py`)

The main script is ready to use the trained vocabulary to tokenize new input.

1.  **Configure the path:** Before running, ensure the line in `main.py` points to your newly created vocabulary file:

    ```python
    voc = load_vocab("/home/sebastien/Documents/bpe/Vocabs/Vocab_of_candide.json") # <--- UPDATE THIS PATH
    ```

2.  **Run the script:**

    ```bash
    python main.py
    ```

3.  **Test the Encoder/Decoder:** Enter any text when prompted.

    **Example Run:**

    ```
    -> it's amazing how bird fly
    deconstructed: ['it', "'", 's ', 'am', 'az', 'ing ', 'how ', 'bi', 'rd', ' ', 'fl', 'y']
    Tokens: [12637, 16, 20833, 3642, 4786, 12287, 11653, 4989, 19552, 1, 10438, 25121]
    Decoded: it's amazing how bird fly
    -----------------------------
    ```

## 🧠 BPE Algorithm Overview

The BPE algorithm works by iteratively replacing the most frequent pair of adjacent characters/tokens in a text with a single, new, merged token.

### Core Steps

1.  **Initialization:** The vocabulary starts with all unique characters found in the corpus.
2.  **Frequency Analysis:** All adjacent pairs of tokens are counted across the entire corpus.
3.  **Merge Rule:** The pair with the **highest frequency** is selected.
4.  **Merging:** All occurrences of the selected pair are replaced by a single, new token (e.g., `['t', 'h']` becomes `['th']`).
5.  **Iteration:** The new token is added to the vocabulary, the old tokens are removed (if no longer used as singles), and the process repeats until the target vocabulary size is reached.

This process ensures that the most common multi-character sequences (like "the", "ing", "tion") are represented by single tokens, significantly reducing the total length of the tokenized sequence.