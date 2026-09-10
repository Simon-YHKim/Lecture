# -*- coding: utf-8 -*-
"""코치 마크 번호를 조작 줄에 연결한다.

검수 요청 (전 차시 공통 4)

    코치마크는 도면 아래에 중복으로 설명할 필요가 없다. 좌측 설명란 text에 이와
    관련된 내용이 있기 때문이다. 다만 내용은 조금 다듬을 필요가 있으며, 코치마크
    숫자와 대조할수 있게 표현해야 한다.

도면 아래 캡션을 없애려면 **어느 조작 줄이 어느 자리인지** 자료에 있어야 한다.
글자 유사도로 맞춰 보니 141자리 중 67이 어긋나서, 사람이 읽고 정한 값을 여기 둔다.

한 줄이 여러 자리를 아우르는 데가 있다. 「같은 방법으로 세 개를 더 그립니다」 같은
줄이 그렇다. 그때는 번호를 여럿 단다.

    python scripts/patches/p12_spot_links.py [--dry-run]

`check-editions.py` 가 자리마다 집이 있는지 센다. 빠지면 그 번호는 도면에만 뜨고
설명이 없어진다 — 캡션을 없앤 뒤에는 그것이 바로 결함이다.
"""
import io
import json
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = os.path.join(ROOT, "scripts", "selfstudy", "source")

# 차시 → 단계 → {조작 줄 번호: 자리 번호(또는 여럿)}
LINKS = {
    2: {
        11: {1: 1, 2: 2, 5: 3},
        12: {2: 1, 5: [2, 3, 4]},
        13: {1: 1, 8: 2},
        15: {5: 1, 9: 2},
    },
    3: {
        3: {3: [1, 2]},
        4: {2: 1, 13: 2, 16: 3},
        5: {1: 1},
        7: {4: 1},
        8: {9: 1},
        10: {3: 1},
        11: {1: [1, 2, 3]},
        12: {2: 1, 8: 2},
        13: {2: 1, 6: 2},
    },
    4: {
        2: {4: 1},
        3: {5: 1, 6: 2},
        4: {3: 1},
        5: {2: 1},
        6: {3: 1},
        8: {1: 1, 14: 2},
        9: {2: 1, 3: 2},
        10: {2: 1, 3: 2},
        11: {3: 1, 5: 2},
        12: {2: 1},
        13: {4: 1, 5: 2},
        15: {1: [1, 2], 3: 3, 5: 4},
    },
    5: {
        4: {2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 7},
        5: {2: 1, 5: 2, 8: 3, 11: 4},
        6: {2: 1, 3: 2, 4: 3, 7: 4},
        7: {2: 1, 3: 2, 4: 3, 5: 4, 7: 5},
        8: {3: 1, 7: 2, 10: 3, 11: 4},
        9: {2: 1, 4: 2, 5: 3, 6: 4, 7: 5},
        10: {2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6},
        11: {3: 1, 4: 2, 9: 3, 15: 4},
        12: {3: 1, 4: 2, 7: [3, 4]},
        13: {3: 1, 4: 2, 7: [3, 4]},
        14: {3: 2, 4: 1, 7: 3, 8: 4},
        15: {3: 1, 6: 2, 11: 3, 12: 4},
        16: {3: 1, 4: 2, 7: [3, 4], 11: 5},
    },
    6: {
        5: {2: [1, 2]},
        6: {1: 2, 2: 1},
        9: {1: 1, 2: 2},
        10: {1: 1, 4: 2},
        14: {0: 1},
    },
    7: {
        6: {0: [1, 2], 1: 3},
        7: {0: [1, 2], 1: 3},
        8: {0: [1, 2], 2: 3},
        9: {0: [1, 2]},
        10: {0: [1, 2], 5: 3},
        11: {0: [1, 2], 3: 3},
        12: {7: 1},
        13: {0: 1, 2: 2},
        14: {0: [1, 2]},
        15: {2: [1, 2]},
    },
}


def main():
    dry = "--dry-run" in sys.argv
    bad, done = [], 0
    for no, steps in sorted(LINKS.items()):
        path = os.path.join(SRC, "lesson-%02d.json" % no)
        doc = json.load(io.open(path, encoding="utf-8"))
        seen = set()
        for sec in doc.get("sections", []):
            for blk in sec.get("blocks", []):
                if blk.get("type") != "steps":
                    continue
                for st in blk.get("items", []):
                    plan = steps.get(st.get("n"))
                    if not plan:
                        continue
                    seen.add(st["n"])
                    acts = st.get("actions", [])
                    nspot = len(st.get("spots") or [])
                    covered = set()
                    for ai, spot in plan.items():
                        if ai >= len(acts):
                            bad.append("%d차시 %d단계 — 조작 줄 a%d 이 없다" % (no, st["n"], ai))
                            continue
                        acts[ai]["spot"] = spot
                        covered |= set(spot if isinstance(spot, list) else [spot])
                        done += 1
                    miss = set(range(1, nspot + 1)) - covered
                    if miss:
                        bad.append("%d차시 %d단계 — 집 없는 자리 %s"
                                   % (no, st["n"], sorted(miss)))
                    extra = covered - set(range(1, nspot + 1))
                    if extra:
                        bad.append("%d차시 %d단계 — 없는 자리를 가리킴 %s"
                                   % (no, st["n"], sorted(extra)))
        missing = set(steps) - seen
        if missing:
            bad.append("%d차시 — 없는 단계 번호 %s" % (no, sorted(missing)))
        if not dry and not bad:
            with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
                json.dump(doc, fh, ensure_ascii=False, indent=1)
                fh.write("\n")
        print("  %s %d차시 — 조작 줄 %d개에 번호"
              % ("·" if dry else "✓", no, sum(1 for _ in steps.values())))
    if bad:
        print("\n어긋난 곳 %d건 — 아무것도 쓰지 않았다\n" % len(bad))
        for b in bad:
            print("  ✗", b)
        return 1
    print("\n%s연결 %d곳" % ("--dry-run — " if dry else "", done))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
