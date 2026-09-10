#!/bin/sh
# prepare_scene_checks.py 가 쪼개 놓은 장면을 하나씩 검사하고 한 줄로 요약한다.
#
# 검사 하나가 크롬을 띄우므로 71장면을 한 번에 돌리면 메모리가 모자란다 —
# 실제로 두 번 끊겼다. 이미 ok:true 인 장면은 건너뛰므로 끊긴 자리에서 그대로
# 이어 돌리면 된다.
#
#     sh scripts/part/run_scene_checks.sh <장면 폴더> <이름표>
SCENES="$1"
LABEL="$2"
FAIL=0
TOTAL=0
for d in "$SCENES"/*/; do
  name=$(basename "$d")
  [ -f "$d/index.html" ] || continue
  TOTAL=$((TOTAL+1))
  out="$d/check.json"
  if [ -f "$out" ] && grep -q '"ok": true' "$out" 2>/dev/null; then
    printf '%-14s %-34s %s\n' "$LABEL" "$name" "OK (skipped)"
    continue
  fi
  npx --yes hyperframes@0.8.33 check "$d" --json --at-transitions > "$out" 2>&1
  res=$(PYTHONIOENCODING=utf-8 python - "$out" <<'PY'
import json, sys
raw = open(sys.argv[1], encoding='utf-8', errors='replace').read()
i = raw.find('{')
if i < 0:
    print('NOJSON ' + raw[:120].replace('\n', ' '))
    raise SystemExit
d = json.loads(raw[i:])
bad = []
for k in ('lint', 'runtime', 'layout', 'motion', 'contrast'):
    s = d.get(k) or {}
    if s.get('errorCount'):
        bad.append('%s e=%d' % (k, s['errorCount']))
        for f in (s.get('findings') or []):
            if f.get('severity') == 'error':
                bad.append('   %s %s %s' % (k, f.get('selector'), f.get('message', '')[:110]))
print(('OK' if d.get('ok') else 'FAIL') + (' | ' + ' | '.join(bad) if bad else ''))
PY
)
  case "$res" in
    OK*) ;;
    *) FAIL=$((FAIL+1)) ;;
  esac
  printf '%-14s %-34s %s\n' "$LABEL" "$name" "$res"
done
printf '%-14s scenes=%d failed=%d\n' "$LABEL" "$TOTAL" "$FAIL"
