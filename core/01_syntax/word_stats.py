from __future__ import annotations

import argparse
import string
from collections import Counter
from pathlib import Path


def read_file(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError as e:
        raise SystemExit(f"File not found: {path}") from e
    except IsADirectoryError as e:
        raise SystemExit(f"Expected a file but got a directory: {path}") from e


def normalize_text(text: str, min_length: int) -> list[str]:
    """
    Lowercase + remove punctuation + split into words.
    """
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    words = text.split()
    return [word for word in words if len(word) >= min_length]


def count_lines(text: str) -> int:
    return len(text.splitlines())


def count_words(words: list[str]) -> int:
    return len(words)


def top_words(words: list[str], n: int) -> list[tuple[str, int]]:
    return Counter(words).most_common(n)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="word_stats",
        description="Count lines, words, and top frequent words in a text file.",
    )
    parser.add_argument("file", type=Path, help="Path to the input text file")
    parser.add_argument("--top", "-t", type=int, default=10, help="How many top words to show (default: 10)")
    parser.add_argument("--min-length", "-l", type=int, default=3, help="The minimal length of words for processing (default: 3)")
    parser.add_argument("--output", "-o", type=Path, help="Write result to file instead of stdout")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.top <= 0:
        raise SystemExit("--top must be a positive integer")

    raw_text = read_file(args.file)
    words = normalize_text(raw_text, args.min_length)

    result_lines = [
        f"Lines: {count_lines(raw_text)}",
        f"Words: {count_words(words)}",
        "",
        "Top words:"
    ]

    for word, count in top_words(words, args.top):
        result_lines.append(f"{word}: {count}")

    result = "\n".join(result_lines)
    
    if args.output:
        args.output.write_text(result, encoding="utf-8")
        print(f"Saved result to {args.output}")
    else:
        print(result)
    
if __name__ == "__main__":
    main()