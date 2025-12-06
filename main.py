import json
import os


def load_vocab(vocabulary_path):
    if os.path.isfile(vocabulary_path):
        with open(vocabulary_path, "r", encoding="utf-8") as f:
            voc = json.load(f)
        print(f"✅ Loaded vocab size: {len(voc)}")
        return voc
    else:
        print("❌ Vocab file not found. Please train first.")
        return None


def encode(text, voc):
    chars = list(text)
    i = 0
    while True:
        merged = False
        for pair in [chars[j] + chars[j + 1] for j in range(len(chars) - 1)]:
            if pair in voc:
                # merge the first valid pair found
                new_chars = []
                skip = False
                for j in range(len(chars)):
                    if skip:
                        skip = False
                        continue
                    if j < len(chars) - 1 and chars[j] + chars[j + 1] == pair:
                        new_chars.append(pair)
                        skip = True
                    else:
                        new_chars.append(chars[j])
                chars = new_chars
                merged = True
                break
        if not merged:
            break

    deconstructed = [ch if ch in voc else "[UNK]" for ch in chars]
    token_to_id = {tok: i for i, tok in enumerate(voc)}
    tokens = [token_to_id.get(ch, token_to_id["[UNK]"]) for ch in deconstructed]

    return deconstructed, tokens


def decode(tokens, voc):
    id_to_token = {i: tok for i, tok in enumerate(voc)}
    decoded_tokens = [id_to_token.get(tok, "[UNK]") for tok in tokens]
    return "".join(decoded_tokens)


if __name__ == "__main__":
    voc = load_vocab("/home/sebastien/Documents/bpe/Vocabs/Vocab_of_candide.json") # put your voacabs path here

    while True:
        print("##NOTE##\n tous est permis")
        user_input = str(input("-> "))
        if user_input != "q":
            deconstucted, tokens = encode(user_input, voc)
            decoded = decode(tokens, voc)
            print(f"deconstructed: {deconstucted}")
            print(f"Tokens: {tokens}")
            print(f"Decoded: {decoded}")
            print("-----------------------------")
        else:
            break
