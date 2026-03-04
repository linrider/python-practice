import sys
from collections import Counter

def read_file(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        raise SystemExit(f"File not found: {path}")

def count_lines(text: str) -> int:
    return len(text.splitlines())


def count_words(text: str) -> int:
    return len(text.lower().split())


def top_words(text: str, n: int=10) -> list[tuple[str, int]]:
    words = text.lower().split()
    counter = Counter(words)
    return counter.most_common(n)


def main():
    if len(sys.argv) < 2:
        print("Usage: python word_stats.py <file>")
        sys.exit(1)
        
    raw_text = read_file(sys.argv[1])
    print(f"Lines: {count_lines(raw_text)}")
    print(f"Words: {count_words(raw_text)}")
    topwords = top_words(raw_text)
    print("\nTop words:")
    for word, count in topwords:
        print(f"{word}: {count}")


if __name__ == "__main__":
    main()