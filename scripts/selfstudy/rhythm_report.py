"""Report Korean sentence rhythm without grading a long book by raw TTR.

The global unique-ending/sentence ratio shrinks when text is repeated or grows
longer. Keep it visible for comparison, and also report fixed 20-sentence windows
and consecutive identical final words. These are editorial signals, not an AI
detector or a reason to change the meaning of a sentence.
"""
import argparse
import collections
import json
from pathlib import Path
import re
import statistics
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'part'))
import beats
import tone_check


def prose(path):
    if Path(path).suffix == '.json':
        fields = []
        tone_check.walk(json.loads(Path(path).read_text(encoding='utf-8')), fields)
        return [text for _, text in fields]
    return [re.sub(r'^\s*\([^)]*\)\s*', '', text)
            for paragraphs in beats.parse_script(path).values() for _, text in paragraphs]


def measure(texts, window=20):
    endings, words, lengths = [], [], []
    counts = collections.Counter()
    for text in texts:
        for sentence, core in tone_check.sentences(text):
            kind = tone_check.classify(core)
            counts[kind] += 1
            if kind not in ('hap', 'hae', 'muneo'):
                continue
            word = re.search(r'([가-힣]+)$', core)[1]
            # Match Humanize KR's current two-syllable ending key. Its docstring
            # says 1–3, but _ENDING_FINAL_RE actually captures two syllables.
            endings.append(word[-2:])
            words.append(word)
            lengths.append(len(sentence))
    ratios = [len(set(endings[i:i + window])) / window
              for i in range(len(endings) - window + 1)]
    longest = run = 0
    previous = None
    for word in words:
        run = run + 1 if word == previous else 1
        longest = max(longest, run)
        previous = word
    graded = counts['hap'] + counts['hae']
    return {
        'sentences': len(endings), 'formalPercent': round(100 * counts['hap'] / graded, 1) if graded else 0,
        'informalPercent': round(100 * counts['hae'] / graded, 1) if graded else 0,
        'plainStyleSentences': counts['muneo'],
        'globalEndingRatio': round(len(set(endings)) / len(endings), 4) if endings else 0,
        'windowSize': window, 'windowCount': len(ratios),
        'windowEndingRatioMean': round(statistics.mean(ratios), 4) if ratios else None,
        'windowEndingRatioMin': round(min(ratios), 4) if ratios else None,
        'longestRepeatedFinalWord': longest,
        'meanSentenceCharacters': round(statistics.mean(lengths), 1) if lengths else 0,
        'over40Characters': sum(n > 40 for n in lengths),
        'mostCommonFinalWords': words and collections.Counter(words).most_common(5) or [],
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('files', nargs='+', type=Path)
    ap.add_argument('--window', type=int, default=20)
    args = ap.parse_args()
    if args.window < 2:
        ap.error('--window must be at least 2')
    for path in args.files:
        print(json.dumps({'file': path.as_posix(), **measure(prose(path), args.window)}, ensure_ascii=False))


if __name__ == '__main__':
    main()
