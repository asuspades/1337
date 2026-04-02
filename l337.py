#!/usr/bin/env python3
# l337.py — Multi-Mode Text & Word Toolkit
# License: MIT

"""
Modes:
  --encode     Encode stdin into l337
  --pairs      Generate word pairs from dictionary

Examples:
  echo "hello" | python l337.py --encode
  python l337.py --pairs
"""

import argparse
import string
import sys
import os
import json
import csv

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────

WORD_LIST_PATH = os.getenv("WORD_LIST_PATH", "./words.txt")

ALLOWED_LETTERS = set('OIREASGTBD')

LETTER_TO_NUM = {
    'O': '0', 'I': '1', 'R': '2', 'E': '3',
    'A': '4', 'S': '5', 'G': '6', 'T': '7',
    'B': '8', 'D': '9'
}

# ─────────────────────────────────────────────
# L337 ENCODER
# ─────────────────────────────────────────────

CHAR_MAP = {
    string.printable[10]: string.printable[4],
    string.printable[11]: string.printable[8],
    string.printable[37]: string.printable[8],
    string.printable[12]: string.printable[69],
    string.printable[13]: string.printable[9],
    string.printable[14]: string.printable[3],
    string.printable[15]: string.printable[76],
    string.printable[41]: string.printable[76],
    string.printable[16]: string.printable[6],
    string.printable[17]: string.printable[64],
    string.printable[18]: string.printable[62],
    string.printable[19]: string.printable[78],
    string.printable[45]: string.printable[78],
    string.printable[20]: string.printable[79],
    string.printable[46]: string.printable[79],
    string.printable[21]: string.printable[1],
    string.printable[22]: string.printable[74],
    string.printable[23]: string.printable[67],
    string.printable[24]: string.printable[0],
    string.printable[25]: string.printable[81],
    string.printable[26]: string.printable[68],
    string.printable[52]: string.printable[68],
    string.printable[27]: string.printable[2],
    string.printable[28]: string.printable[5],
    string.printable[29]: string.printable[7],
    string.printable[30]: string.printable[63],
    string.printable[31]: string.printable[89],
    string.printable[57]: string.printable[89],
    string.printable[32]: string.printable[85],
    string.printable[58]: string.printable[85],
    string.printable[33]: string.printable[71],
    string.printable[59]: string.printable[71],
    string.printable[34]: string.printable[66],
    string.printable[60]: string.printable[66],
    string.printable[35]: string.printable[93],
    string.printable[61]: string.printable[93],
    string.printable[36]: string.printable[83],
    string.printable[38]: string.printable[84],
    string.printable[39]: string.printable[70],
    string.printable[40]: string.printable[80],
    string.printable[42]: string.printable[73],
    string.printable[43]: string.printable[92],
    string.printable[44]: string.printable[77],
    string.printable[47]: string.printable[91],
    string.printable[48]: string.printable[90],
    string.printable[49]: string.printable[87],
    string.printable[50]: string.printable[75],
    string.printable[51]: string.printable[86],
    string.printable[53]: string.printable[82],
    string.printable[54]: string.printable[65],
    string.printable[55]: string.printable[72],
    string.printable[56]: string.printable[88],
}

def encode(text):
    return ''.join(CHAR_MAP.get(c, c) for c in text)

def encode_mode():
    for line in sys.stdin:
        print(encode(line.rstrip("\n")))

# ─────────────────────────────────────────────
# WORD PAIRS MODE
# ─────────────────────────────────────────────

def load_words(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Word list not found: {path}")
    with open(path) as f:
        return [w.strip().upper() for w in f if w.strip().isalpha()]

def word_to_num(word):
    return ''.join(LETTER_TO_NUM.get(l, '') for l in word)

def filter_valid(words):
    return {
        w: True for w in words
        if all(l in ALLOWED_LETTERS for l in w)
    }

def find_pairs(valid):
    nums = {w: word_to_num(w) for w in valid}
    words = list(nums.keys())
    pairs = []

    for i, w1 in enumerate(words):
        for w2 in words[i+1:]:
            if nums[w1] and nums[w2]:
                pairs.append((w1, w2, nums[w1] + nums[w2]))

    return pairs

def pairs_mode():
    words = load_words(WORD_LIST_PATH)
    valid = filter_valid(words)

    with open("valid_words.json", "w") as f:
        json.dump(valid, f, indent=2)

    pairs = find_pairs(valid)

    with open("valid_pairs.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Word1", "Word2", "CombinedTranslation"])
        writer.writerows(pairs)

    print(f"{len(valid)} valid words")
    print(f"{len(pairs)} pairs generated")

# ─────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="l337 toolkit")

    parser.add_argument("--encode", action="store_true", help="Encode stdin")
    parser.add_argument("--pairs", action="store_true", help="Generate word pairs")

    args = parser.parse_args()

    if args.encode:
        encode_mode()
    elif args.pairs:
        pairs_mode()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
