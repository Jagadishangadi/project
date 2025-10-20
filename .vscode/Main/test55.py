from __future__ import annotations
import sys
import argparse
from collections import Counter
from typing import Iterable, Tuple, List

#!/usr/bin/env python3
"""
Simple text statistics tool.

Usage:
    python test55.py path/to/file.txt
If no file is provided, reads from standard input.
Prints lines, words, characters and top 5 most common words.
"""


def read_lines_from_file(path: str) -> Iterable[str]:
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            yield line


def read_lines_from_stdin() -> Iterable[str]:
    for line in sys.stdin:
        yield line


def tokenize(line: str) -> List[str]:
    # Simple tokenizer: split on whitespace and strip punctuation
    return [
        token.strip(".,!?:;\"'()[]{}<>").lower()
        for token in line.split()
        if token.strip(".,!?:;\"'()[]{}<>")
    ]


def text_stats(lines: Iterable[str]) -> Tuple[int, int, int, Counter]:
    line_count = 0
    word_count = 0
    char_count = 0
    counter: Counter = Counter()

    for line in lines:
        line_count += 1
        char_count += len(line)
        tokens = tokenize(line)
        word_count += len(tokens)
        counter.update(tokens)

    return line_count, word_count, char_count, counter


def print_stats(line_count: int, word_count: int, char_count: int, counter: Counter) -> None:
    print(f"Lines: {line_count}")
    print(f"Words: {word_count}")
    print(f"Characters: {char_count}")
    print("Top 5 words:")
    for word, cnt in counter.most_common(5):
        print(f"  {word!r}: {cnt}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Simple text statistics")
    parser.add_argument("path", nargs="?",
                        help="Path to text file. If omitted, read from stdin.")
    return parser


def main(argv: List[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.path:
        lines = read_lines_from_file(args.path)
    else:
        if sys.stdin.isatty():
            print(
                "Reading from stdin. Type/paste text and press Ctrl-D (Unix) or Ctrl-Z (Windows) to end.")
        lines = read_lines_from_stdin()

    line_count, word_count, char_count, counter = text_stats(lines)
    print_stats(line_count, word_count, char_count, counter)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
