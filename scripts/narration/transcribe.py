"""Transcribe a private narration recording into a word-level transcript.

The transcript is intentionally a private artifact: it carries the spoken text of
a recording that never leaves the approved private storage location. The guard
blocks transcript paths inside this repository. Write the output next to the
recording, outside the public working tree.

Only the numbers-only derivative produced by align.py may be published.

Usage:
    python scripts/narration/transcribe.py <audio> <output-json> [--model large-v3]
"""

import argparse
import json
import sys
import time


def parse_args(argv):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("audio", help="path to the narration recording")
    parser.add_argument("output", help="path to write the word-level transcript JSON")
    parser.add_argument("--model", default="large-v3", help="Whisper model size")
    parser.add_argument("--device", default="cuda", help="ctranslate2 device")
    parser.add_argument("--compute-type", default="float16", help="ctranslate2 compute type")
    parser.add_argument("--language", default="ko", help="spoken language code")
    parser.add_argument("--beam-size", type=int, default=5, help="decoder beam size")
    parser.add_argument(
        "--initial-prompt",
        default=None,
        help=(
            "optional decoding context. Canonical identifiers are recovered by "
            "align.py, not by the decoder, so this only nudges ordinary wording."
        ),
    )
    return parser.parse_args(argv)


def main(argv):
    args = parse_args(argv)

    from faster_whisper import WhisperModel

    model = WhisperModel(args.model, device=args.device, compute_type=args.compute_type)

    started = time.time()
    segments, info = model.transcribe(
        args.audio,
        language=args.language,
        word_timestamps=True,
        vad_filter=True,
        beam_size=args.beam_size,
        initial_prompt=args.initial_prompt,
    )

    collected = []
    for segment in segments:
        collected.append(
            {
                "start": round(segment.start, 3),
                "end": round(segment.end, 3),
                "text": segment.text.strip(),
                "words": [
                    {
                        "word": word.word,
                        "start": round(word.start, 3),
                        "end": round(word.end, 3),
                    }
                    for word in (segment.words or [])
                ],
            }
        )
    elapsed = time.time() - started

    word_count = sum(len(segment["words"]) for segment in collected)
    result = {
        "schemaVersion": 1,
        "model": args.model,
        "language": info.language,
        "languageProbability": round(info.language_probability, 4),
        "audioSeconds": round(info.duration, 3),
        "segmentCount": len(collected),
        "wordCount": word_count,
        "segments": collected,
    }

    with open(args.output, "w", encoding="utf-8") as handle:
        json.dump(result, handle, ensure_ascii=False, indent=2)

    print(f"model         : {args.model}")
    print(f"audio seconds : {result['audioSeconds']}")
    print(f"language      : {info.language} (p={result['languageProbability']})")
    print(f"transcribe    : {elapsed:.1f}s ({info.duration / elapsed:.1f}x realtime)")
    print(f"segments      : {len(collected)}")
    print(f"words         : {word_count}")
    print(f"written       : {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
