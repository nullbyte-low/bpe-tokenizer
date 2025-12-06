import json
import os
from collections import defaultdict


def init_voc(corpus):
    return sorted(set([char for sen in corpus for char in sen]))

def save_voc(vocab_path, voc):
    with open(vocab_path, "w", encoding="utf-8") as f:
        json.dump(voc, f, ensure_ascii=False, indent=2)
    print(f"Vocab saved: {vocab_path}")

def data_process(path):
    if not path:
        print("Need path.")
        return []
    else:
        with open(path, "r") as f:
            corpus = f.readlines()
    return corpus


def check_vocab(path):
    filename = os.path.basename(path)
    book_name = filename[:-4] + ".json"

    book_name = book_name.replace(" ", "_")
    vocab_path = "/home/sebastien/Documents/bpe/Vocabs/Vocab_of_"
    vocab_path += book_name

    print(vocab_path)
    if os.path.isfile(vocab_path):
        print(f"✅ Voc has been found. Please heed to the Tokenizer for usage.")
        return True, vocab_path
    else:
        print("❌ Vocab file not found. Please train first.")
        return False, vocab_path


def segmentation_of_word_plus_enhancement(corpus):
    tokens = []
    for texte in corpus:
        texte = texte.strip()
        words = texte.split(" ")
        for i, word in enumerate(words):
            if i == len(words) - 1:
                tokens.append(word)
                break
            word += " "
            tokens.append(word)
    return tokens


def words_frequency_plus_mapper_and_global_freq(tokens):
    word_freqs = defaultdict(int)
    for token in tokens:
        word_freqs[token] += 1
    Mapper = {}
    for word, n in word_freqs.items():
        char = list(word)
        temp = {
            "n": n,
            "p": [char[i] + char[i + 1] for i in range(len(char) - 1)],
            "m": list(word),
        }

        Mapper[word] = temp

    global_freq = defaultdict(int)
    for temp in Mapper.values():
        for pair in temp["p"]:
            global_freq[pair] += temp["n"]

    return Mapper, global_freq


def merge_pair(chars, pair):
    new_split = []
    i = 0
    while i < len(chars):
        if i < len(chars) - 1 and chars[i] + chars[i + 1] == pair:
            new_split.append(pair)
            i += 2
        else:
            new_split.append(chars[i])
            i += 1
    return new_split


def pruning_of_pair_with_n_than_1(global_freq):
    pairs_with_less_than_one = []
    for pair, n in global_freq.items():
        if n <= 1:
            pairs_with_less_than_one.append(pair)

    for pair in pairs_with_less_than_one:
        global_freq.pop(pair, None)
    return global_freq


def local_updater_using_occurance(Mapper, global_freq, highest_freq, voc):
    occurance = {}
    for word in Mapper.keys():
        for pairs in Mapper[word]["p"]:
            if highest_freq == pairs:
                occurance[word] = Mapper[word]["n"]

    for word, n in occurance.items():
        old_pair = Mapper[word]["p"]
        old_merge = Mapper[word]["m"]
        merged = merge_pair(old_merge, highest_freq)
        new_pairs = [merged[i] + merged[i + 1] for i in range(len(merged) - 1)]
        Mapper[word]["p"] = new_pairs
        Mapper[word]["m"] = merged

        for pair in old_pair:
            if pair in new_pairs:
                continue
            else:
                global_freq[pair] = max(0, global_freq.get(pair, 0) - n)

        for new_pair in new_pairs:
            global_freq[new_pair] += n

    voc.append(highest_freq)
    global_freq.pop(highest_freq)
    return Mapper, global_freq, voc


def train(condition, vocab_path, path):
    vocab_size = int(input("Vocab size: "))
    if condition:
        print("Can't train, there's already a vocab for this corpus.\n")
    else:
        corpus = data_process(path)
        voc = init_voc(corpus)
        tokens = segmentation_of_word_plus_enhancement(corpus)
        Mapper, global_freq = words_frequency_plus_mapper_and_global_freq(tokens)

        step = 0

        while len(voc) < vocab_size:
            if not global_freq:
                print("No more pairs to merge — cannot reach target vocab size.")
                save_voc(vocab_path, voc)
                break

            highest_freq = max(global_freq, key=global_freq.get)
            Mapper, global_freq, voc = local_updater_using_occurance(
                Mapper, global_freq, highest_freq, voc
            )
            global_freq = pruning_of_pair_with_n_than_1(global_freq)
            step += 1
            if step % 100 == 0:
                print(f"Step {step}: merged '{highest_freq}', vocab size = {len(voc)}")
        print("Training Finished.\n")
        voc.append("[UNK]")
        save_voc(vocab_path, voc)
        


if __name__ == "__main__":
    path = str(input("PATH: "))
    condition, vocab_path = check_vocab(path)
    train(condition, vocab_path, path)
