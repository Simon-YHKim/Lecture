"""Package only verified, authorized self-study downloads; never publish them.

The private work directory can contain references, WAVs and ASR. No directory
walk is used for delivery: each public filename is explicitly selected.
"""
import argparse
from datetime import datetime, timezone, timedelta
import html
import json
from pathlib import Path
import re
import shutil
import zipfile

from build_narrated_review import document, review_data
from narrated_delivery import digest
from prepare_narrated import write_json

EXTENSIONS = ('.html', '.mp4', '.md', '.vtt', '.srt')


def clock(seconds):
    seconds = round(seconds)
    return '%d:%02d' % (seconds // 60, seconds % 60)


def selected_files(folder, lang):
    """Select 40 exact names, excluding samples, source audio and other files."""
    return [folder / ('AutoCAD_%s_L%02d_SELFSTUDY%s' % (lang.upper(), n, ext))
            for n in range(1, 9) for ext in EXTENSIONS]


def file_record(path):
    return {'file': path.name, 'bytes': path.stat().st_size, 'sha256': digest(path)}


def checksums(paths):
    return ''.join('%s  %s\n' % (digest(p), p.name) for p in sorted(paths))


def validate_text(path):
    if path.suffix == '.mp4':
        return
    text = path.read_text(encoding='utf-8')
    # Block machine-local paths and separate private assets. Public scripts and
    # captions are authorized release downloads, never Git source artifacts.
    patterns = [r'(?i)file://', r'(?i)[A-Z]:[\\/](?:Users|Lecture|Temp)[\\/]',
                r'(?i)(?:AppData[\\/]|local-materials[\\/])',
                r'(?i)["\'][^"\'\n]*\.(?:wav|flac|safetensors|woff2?)["\']',
                r'(?i)\b(?:github_pat_|ghp_|sk-proj-|dcap_)[A-Za-z0-9_-]{16,}']
    if any(re.search(pattern, text) for pattern in patterns):
        raise ValueError('Private path or asset in ' + path.name)


def readme(data):
    lang = data['language']
    name = 'START_REVIEW_%s.html' % lang.upper()
    if lang == 'ko':
        text = f'''# AutoCAD 자습 강의 검수본

전체 ZIP을 압축 해제한 뒤 `{name}`을 Chrome 또는 Edge에서 여세요.
차시를 고르고 대본을 클릭하면 해당 영상 시간으로 이동합니다.
`이 부분의 슬라이드 열기`로 같은 화면을 확인할 수 있습니다.
의견을 저장한 뒤 `의견 JSON 내보내기`로 검수 결과를 전달하세요.
의견은 브라우저에 저장되며 자동 전송되지 않습니다.

각 차시는 대본이 통합된 HTML 슬라이드, 그 슬라이드 화면과 강사 복제
음성으로 만든 MP4, 대본 MD, VTT/SRT 자막으로 구성됩니다.
영상은 1920×1080, 30fps이며 음성은 원래 속도 1.00×입니다.
실습은 도해와 단계별 슬라이드로 설명합니다. 실제 AutoCAD 조작 녹화는
포함하지 않습니다. 사람의 전체 청취 및 AutoCAD 실습 검수는 남아 있습니다.

슬라이드와 검수 페이지는 압축 해제 후 인터넷 없이 사용할 수 있습니다.
영상만 받으려면 MP4를 여세요. 자막은 MP4 내장 자막 또는 VTT를 사용하세요.
일부 외부 SRT 재생기는 AutoCAD 자리표시 `<>`를 숨길 수 있습니다.
HTML의 발표자 대본과 전체 대본은 해당 자습 영상의 낭독 내용입니다.
언어별 차시 8개를 아래에서 확인하세요.

| 차시 | 제목 | 영상 길이 | 슬라이드 |
|---|---|---:|---|
'''
    else:
        text = f'''# AutoCAD self-study review edition

Extract the entire ZIP, then open `{name}` in Chrome or Edge.
Select a lesson and click its script to seek the video. Use `Open matching slide`
to see the corresponding slide. Save feedback at the current time, then export
the feedback JSON for your reviewer. Feedback stays in the browser and is not
sent automatically.

Each lesson includes an HTML slide deck with its script, an MP4 showing those
slides with cloned instructor narration, a Markdown script, and VTT/SRT captions.
Videos are 1920×1080 at 30fps. Narration retains its native 1.00× speed.
Practice is explained through diagrams and step-by-step slides. These are not
AutoCAD screen recordings. Full human listening and hands-on validation remain
pending.

The slides and review player work offline after extraction. Open an MP4 for video
playback alone. Use the MP4 subtitle track or VTT captions; some external SRT
players can hide the AutoCAD `<>` placeholder. Presenter notes and the full script
inside each deck correspond to the narration of that self-study video.
All eight lessons are listed below.

| Lesson | Title | Video duration | Slides |
|---|---|---:|---|
'''
    for row in data['lessons']:
        text += '| %d | %s | %s | [%s](%s) |\n' % (
            row['number'], row['title'], clock(row['duration']), row['slides'], row['slides'])
    return text


def guide(manifest, tag):
    url = 'https://github.com/Simon-YHKim/Lecture/releases/download/' + tag + '/'
    tables = []
    for lang in ['ko', 'en']:
        rows = []
        for lesson in manifest['editions'][lang]['lessons']:
            stem = 'AutoCAD_%s_L%02d_SELFSTUDY' % (lang.upper(), lesson['number'])
            links = ' · '.join('<a href="%s%s%s">%s</a>' % (url, stem, ext, label)
                               for ext, label in [('.html', 'HTML'), ('.mp4', 'MP4')])
            rows.append('<tr><td>%d</td><td>%s</td><td>%d</td><td>%s</td><td>%s</td></tr>' % (
                lesson['number'], html.escape(lesson['title']), lesson['slides'],
                clock(lesson['duration']), links))
        tables.append('<section lang="%s"><h2>%s</h2><p><a href="%sAutoCAD_%s_SELFSTUDY.zip">%s</a></p>'
                      '<table><thead><tr><th>№</th><th>Title / 제목</th><th>Slides / 장</th>'
                      '<th>Time / 길이</th><th>Download</th></tr></thead><tbody>%s</tbody></table></section>' % (
                          lang, '한국어' if lang == 'ko' else 'English', url, lang.upper(),
                          '전체 ZIP 다운로드' if lang == 'ko' else 'Download complete ZIP', ''.join(rows)))
    return '''<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width">
<title>AutoCAD · 자습 강의 다운로드 / Self-study downloads</title><style>
:root{color-scheme:light dark;--accent:#b80046;--text:#222;--muted:#666}
@media(prefers-color-scheme:dark){:root{--accent:#ff86b2;--text:#eee;--muted:#bbb}}
body{max-width:1050px;margin:40px auto;padding:0 24px;font:16px/1.6 system-ui,sans-serif;color:var(--text)}
a{color:var(--accent)}:focus-visible{outline:3px solid var(--accent)}.cards{display:flex;gap:20px;flex-wrap:wrap}
.card{border:1px solid var(--muted);padding:20px;flex:1;min-width:180px}.card strong{font-size:28px;color:var(--accent)}
table{border-collapse:collapse;width:100%%}th,td{text-align:left;padding:10px;border-bottom:1px solid var(--muted)}
section,details{margin-top:30px}summary{cursor:pointer}small{color:var(--muted)}</style>
<h1>AutoCAD 자습 강의 · Self-study course</h1>
<p>차시별 자습 슬라이드에 대본을 통합하고 같은 화면에 강사 복제 음성을 넣은 검수본입니다.<br>
Review edition: per-lesson self-study slides with integrated scripts and matching videos narrated in the cloned instructor voice.</p>
<div class="cards"><div class="card">HTML 슬라이드 / decks<br><strong>16</strong></div>
<div class="card">MP4 영상 / videos<br><strong>16</strong></div><div class="card">자동 영상 검사 / automated checks<br><strong>16 / 16</strong></div></div>
<p><b>ZIP 전체 압축 해제 → START_REVIEW_KO.html 또는 START_REVIEW_EN.html 열기</b><br>
Extract the whole ZIP → open START_REVIEW_KO.html or START_REVIEW_EN.html.</p>
<p>대본 클릭으로 영상 이동 · 해당 슬라이드 열기 · 시간별 의견 JSON 저장<br>
Click the script to seek · open the matching slide · export timestamped feedback JSON</p>
%s
<details><summary>검증과 검수 상태 / Validation and review status</summary>
<p>모든 MP4의 전체 디코딩, 자막 문자·시간, 원본 음성과 인코딩 음성의 표본, 모든 출력 화면을 확인했습니다.
사람의 전체 청취와 실제 AutoCAD 실행 검수는 남아 있습니다.<br>
Every MP4 passed full decoding, subtitle text/timing checks, audio samples against source PCM, and all captured slide-state comparisons.
Full human listening and hands-on AutoCAD validation remain pending.</p>
<p>실습 내용은 도해와 단계별 슬라이드입니다. 실제 AutoCAD 조작 녹화는 포함하지 않습니다.<br>
Practice uses diagrams and step-by-step slides; it does not include AutoCAD screen recordings.</p>
<p>1920×1080 · 30fps · H.264/AAC · native 1.00× narration · embedded subtitles.
자막은 MP4 내장 또는 VTT를 권장합니다. / Use embedded subtitles or VTT to preserve the literal &lt;&gt; placeholder.</p></details>
<details><summary>파일 검증 / File integrity</summary><p>release-manifest.json과 SHA256SUMS.txt에 파일 크기와 SHA-256을 기록했습니다.<br>
File sizes and SHA-256 checksums are recorded in release-manifest.json and SHA256SUMS.txt.</p></details>
<p><small>%s · %s</small></p></html>''' % (''.join(tables), html.escape(tag), manifest['generatedKST'])


def package(work, output, source_commit, tag):
    if not re.fullmatch('[a-f0-9]{40}', source_commit):
        raise ValueError('A full source commit SHA is required')
    if not re.fullmatch(r'autocad-[0-9.]+-selfstudy-review\.[0-9]+', tag):
        raise ValueError('Unexpected release tag')
    if output.exists():
        raise FileExistsError('Use a fresh output directory; existing releases are preserved')
    editions = {lang: review_data(work, lang) for lang in ['ko', 'en']}
    selected = {lang: selected_files(work/'packages'/lang, lang) for lang in editions}
    # Validate everything before creating the new delivery directory.
    for paths in selected.values():
        for path in paths:
            if not path.is_file():
                raise FileNotFoundError(path.name)
            validate_text(path)
    manifest = {'schemaVersion': 1, 'tag': tag, 'sourceCommit': source_commit,
                'generatedKST': datetime.now(timezone(timedelta(hours=9))).strftime('%Y-%m-%d %H:%M:%S KST'),
                'scope': 'KO and EN each: eight HTML self-study decks and eight matching MP4 videos',
                'coreFileCount': 32, 'humanListeningPerformed': False, 'handsOnValidation': 'pending',
                'video': {'width': 1920, 'height': 1080, 'fps': 30, 'narrationSpeed': 1.0,
                          'practicePresentation': 'illustrated step-by-step slides'},
                'editions': {}, 'assets': []}
    for lang, data in editions.items():
        lessons = []
        for row in data['lessons']:
            validation = json.loads((work/'validation'/lang/('L%02d.json'%row['number'])).read_text())
            lessons.append({k: row[k] for k in ['number', 'title', 'duration', 'videoSha256', 'deckSha256']}
                           | {k: validation[k] for k in ['slides', 'shots', 'cues', 'fullDecode', 'literalCaptions']})
        manifest['editions'][lang] = {'duration': sum(r['duration'] for r in lessons), 'lessons': lessons}
    output.mkdir(parents=True)
    for lang, data in editions.items():
        folder = work/'packages'/lang
        player = folder/('START_REVIEW_%s.html'%lang.upper())
        player.write_bytes(document(data).encode('utf-8'))
        notes = folder/'README.md'; notes.write_bytes(readme(data).encode('utf-8'))
        entries = selected[lang] + [player, notes]
        local_manifest = folder/'release-manifest.json'
        write_json(local_manifest, {k: v for k, v in manifest.items() if k != 'assets'}
                   | {'scope': lang.upper()+' package: eight HTML decks and eight matching MP4 videos',
                      'language': lang, 'coreFileCount': 16,
                      'editions': {lang: manifest['editions'][lang]},
                      'files': [file_record(p) for p in entries]})
        entries.append(local_manifest)
        sums = folder/'SHA256SUMS.txt'; sums.write_bytes(checksums(entries).encode('utf-8'))
        entries.append(sums)
        archive = output/('AutoCAD_%s_SELFSTUDY.zip'%lang.upper())
        with zipfile.ZipFile(archive, 'x', allowZip64=True) as z:
            for path in entries:
                z.write(path, path.name, compress_type=zipfile.ZIP_STORED if path.suffix=='.mp4' else zipfile.ZIP_DEFLATED)
        with zipfile.ZipFile(archive) as z:
            if z.testzip() is not None or set(z.namelist()) != {p.name for p in entries}:
                raise ValueError('ZIP verification failed')
        for path in selected[lang]:
            if path.suffix in ['.html', '.mp4']:
                shutil.copy2(path, output/path.name)
    overview = output/'REVIEW_GUIDE.html'; overview.write_bytes(guide(manifest, tag).encode('utf-8'))
    manifest['assets'] = [file_record(p) for p in sorted(output.iterdir())]
    write_json(output/'release-manifest.json', manifest)
    (output/'SHA256SUMS.txt').write_bytes(checksums(list(output.iterdir())).encode('utf-8'))
    return manifest


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--work', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--source-commit', required=True)
    ap.add_argument('--tag', required=True)
    a = ap.parse_args()
    result = package(a.work, a.out, a.source_commit, a.tag)
    print(json.dumps({'coreFiles': result['coreFileCount'], 'assets': len(result['assets'])+2}))
