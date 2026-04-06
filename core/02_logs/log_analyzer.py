from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path

def analyze_log(path: Path) -> Counter:
    counter = Counter()
    
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            
            level = line.split()[0]
            counter[level] += 1
        
    return counter

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="log_analyzer",
        description="Count log levels in a log file.",
    )
    parser.add_argument("file", type=Path, help="Path to log file")
    parser.add_argument("--level", type=str, help="Show only selected log level (e.g. INFO, ERROR, WARNING)")
    return parser

def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    
    counts = analyze_log(args.file)
    args.level = args.level.upper()
    if args.level:
        print(f"{args.level}: {counts.get(args.level, 0)}")
    else:
        for level, count in counts.items():
            print(f"{level}: {count}")
        
        
if __name__ == "__main__":
    main()