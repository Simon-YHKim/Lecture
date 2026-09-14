"""Build scripts, audio timelines and offline decks from private narration plans.

Use `jobs` before speak_clone.py; use `assemble` after synthesis. This deliberately
does not publish files or alter the approved lecture scripts.
"""
import argparse
import hashlib
import html
import json
import math
from pathlib import Path
import re
import sys
import wave

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / 'part'))
from prepare_narrated import read_json, write_json, standalone
import tts_jobs

FPS = 30
SR = 24000


def digest(path):
    with Path(path).open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def make_jobs(work, lang):
    from selfstudy_voice_text import slide_narration, pronunciation
    lessons, pronunciations = [], {}
    for row in read_json(work / ('projects-%s.json' % lang)):
        plan = read_json(row['plan'])
        source = read_json(row['source'])
        jobs = []
        for slide in plan['slides']:
            if slide['audio']['mode'] == 'reuse':
                continue
            text = slide_narration(slide, source, lang)
            if not text or text == '—':
                raise ValueError('Empty narration: ' + slide['sceneId'])
            slide['notes'] = text
            parts = []
            for number, chunk in enumerate(tts_jobs.chunks_of(text, lang), 1):
                tone = tts_jobs.tone_of(chunk, lang, 'sourceStep' in slide)
                parts.append({'n':number, 'text':chunk, 'tone':tone, 'mood':tts_jobs.MOOD[tone]})
                identity = '%s/%s#%02d' % (row['slug'], slide['sceneId'], number)
                spoken = pronunciation(chunk, lang)
                if spoken != chunk:
                    pronunciations[identity] = spoken
            jobs.append({'key':slide['sceneId'], 'chars':len(text), 'chunks':parts})
            slide['audio']['chunks'] = parts
        lessons.append({'slug':row['slug'], 'jobs':jobs})
        write_json(row['plan'], plan)
    doc = {'schemaVersion':1, 'lang':lang, 'language':'Korean' if lang=='ko' else 'English',
           'moods':sorted(set(tts_jobs.MOOD.values())), 'lessons':lessons}
    write_json(work / ('jobs-%s.json' % lang), doc)
    write_json(work / ('pronunciations-%s.json' % lang), pronunciations)
    print(json.dumps({'lang':lang, 'slides':sum(len(l['jobs']) for l in lessons),
                      'chunks':sum(len(j['chunks']) for l in lessons for j in l['jobs']),
                      'characters':sum(j['chars'] for l in lessons for j in l['jobs'])}), flush=True)


def wav_data(path):
    with wave.open(str(path), 'rb') as f:
        if (f.getframerate(),f.getnchannels(),f.getsampwidth()) != (SR,1,2):
            raise ValueError('Expected native 24kHz mono PCM16: ' + str(path))
        return f.readframes(f.getnframes())


def silence(seconds):
    return bytes(round(seconds*SR)*2)


def timestamp(seconds, separator='.'):
    ms = round(seconds*1000)
    return '%02d:%02d:%02d%s%03d' % (ms//3600000, ms//60000%60, ms//1000%60,separator,ms%1000)


def public_manifest(plan):
    # Audio paths and source provenance are private. The public island carries
    # displayed scripts, navigation and measured video bounds only.
    return {k: ([{a:b for a,b in s.items() if a!='audio'} for s in v] if k=='slides' else v)
            for k,v in plan.items()}


def capture_state(mode, start, fragments, authored_duration):
    if mode == 'generate':
        # Authored self-study slides have entrances only. A concept page may
        # reveal six cards/figures over six seconds; .85s shows only its first.
        return authored_duration
    state = max(start,fragments[0])+.7 if fragments else authored_duration*.65
    return min(state,authored_duration-.1)


def shot_starts(mode,fragments,seconds):
    if mode!='reuse':return [0.0]
    # The first early fragment is already visible in the initial still.
    # Every later fragment needs its own shot, including late/short beats.
    return sorted(set([0.0]+[x for i,x in enumerate(fragments)
                            if 0<x<seconds and (i>0 or x>2)]))


def assemble(work, lang, lesson_filter=None):
    import speak_clone
    done = speak_clone.load_done(str(work/'out'/lang/'done.jsonl'))
    pronunciations_path=work/('pronunciations-%s.json'%lang)
    pronunciations=read_json(pronunciations_path) if pronunciations_path.exists() else {}
    results = []
    for row in read_json(work / ('projects-%s.json' % lang)):
        if lesson_filter and row['lesson'] != lesson_filter:
            continue
        plan = read_json(row['plan'])
        if any(s['audio']['mode']=='generate' and 'chunks' not in s['audio'] for s in plan['slides']):
            raise ValueError('Run jobs first')
        stem = 'AutoCAD_%s_L%02d_SELFSTUDY' % (lang.upper(), row['lesson'])
        package = work / 'packages' / lang
        if (package/(stem+'.mp4')).exists():
            raise FileExistsError('Video already exists; create a new private revision before changing its deck or script')
        package.mkdir(parents=True, exist_ok=True)
        audio_path = work / 'audio' / lang / (stem + '.wav')
        audio_path.parent.mkdir(parents=True, exist_ok=True)
        shots, cues, provenance, script = [], [], [], []
        raw = Path(row['raw']).read_text(encoding='utf-8')
        clock = 0.0
        with wave.open(str(audio_path), 'wb') as output:
            output.setparams((1,2,SR,0,'NONE','not compressed'))
            for index, slide in enumerate(plan['slides']):
                a = slide['audio']
                local_cues = []
                if a['mode']=='reuse':
                    if digest(a['path']) != a['sha256']:
                        raise ValueError('Changed approved source audio: '+slide['sceneId'])
                    pcm = wav_data(a['path'])
                    if abs(len(pcm)/SR/2-a['duration'])>.002:
                        raise ValueError('Audio duration mismatch')
                    local_cues = a['cues']
                    provenance.append({'scene':slide['sceneId'], 'source':a['path'], 'sha256':a['sha256'],
                                       'videoStart':clock, 'sourceStart':0, 'seconds':len(pcm)/SR/2})
                else:
                    pcm = bytearray(silence(.35))
                    for chunk in a['chunks']:
                        identity='%s/%s#%02d'%(row['slug'],slide['sceneId'],chunk['n'])
                        record=done.get((row['slug'],slide['sceneId'],chunk['n']))
                        speech=pronunciations.get(identity,chunk['text'])
                        if (not record or record['sha']!=speak_clone.sha(chunk['text']) or
                            record.get('spokenSha',record['sha'])!=speak_clone.sha(speech)):
                            raise ValueError('Current narration has not been synthesized: '+identity)
                        path = work / 'out' / lang / row['slug'] / ('%s#%02d.wav' % (slide['sceneId'],chunk['n']))
                        data = wav_data(path)
                        start = len(pcm)/SR/2
                        pcm.extend(data)
                        end = len(pcm)/SR/2
                        local_cues.append({'start':start,'end':end,'text':chunk['text'],
                                           'key':'%s#%02d' % (slide['sceneId'],chunk['n'])})
                        provenance.append({'scene':slide['sceneId'], 'source':str(path), 'sha256':digest(path),
                                           'videoStart':clock+start,'sourceStart':0,'seconds':end-start})
                        pcm.extend(silence(.2))
                seconds = len(pcm)/SR/2
                duration = math.ceil((seconds+.8)*FPS)/FPS
                output.writeframes(pcm)
                output.writeframes(silence(duration-seconds))
                slide.update(videoStart=clock, videoEnd=clock+duration)
                cues.extend(dict(c, start=round(clock+c['start'],3),end=round(clock+c['end'],3),
                                 slide=index+1,scene=slide['sceneId']) for c in local_cues)
                # Original frame fragments carry measured narration beats. Each
                # still is held until the next beat, preserving focus changes.
                root = re.search(r'<[^>]+data-composition-id="'+re.escape(slide['sceneId'])+r'"[^>]*>', raw)
                if not root:
                    raise ValueError('Missing slide root')
                base = float(re.search(r'data-start="([\d.]+)"',root[0])[1])
                authored_duration = float(re.search(r'data-duration="([\d.]+)"',root[0])[1])
                fragments = [x-base for x in slide.get('fragments',[])]
                starts = shot_starts(a['mode'],fragments,seconds)
                for part,start in enumerate(starts):
                    end = starts[part+1] if part+1<len(starts) else duration
                    state = capture_state(a['mode'],start,fragments,authored_duration)
                    shots.append({'slide':index,'scene':slide['sceneId'],'state':state,
                                  'start':clock+start,'duration':end-start,
                                  'image':'%04d.png' % len(shots)})
                script.append('## %d · %s\n\n%s\n' % (index+1,slide['sceneId'],slide['notes']))
                clock += duration
        display = public_manifest(plan)
        display.update(videoFile=stem+'.mp4',duration=clock)
        script_text = '# %s\n\n%s' % (plan['lessons'][0]['title'],'\n'.join(script))
        document = standalone(raw,display,row['gsap'],script_text)
        # Keep a direct route from a slide to the same point in its paired MP4.
        video_button = '''<script>(function(){var b=document.createElement('button');b.type='button';
var m=JSON.parse(document.querySelector('script[type="application/hyperframes-slideshow+json"]').textContent);
b.textContent=m.language==='en'?'Matching video':'이 화면의 영상';b.onclick=function(){
var n=parseInt(location.hash.replace('#s',''),10)||1;window.open(m.videoFile+'#t='+m.slides[n-1].videoStart,'_blank','noopener');};
document.getElementById('bar').appendChild(b);})();</script>'''
        document=document.replace('</body>',video_button+'\n</body>')
        (package/(stem+'.html')).write_bytes(document.encode('utf-8'))
        (package/(stem+'.md')).write_bytes(script_text.encode('utf-8'))
        for ext,separator in [('srt',','),('vtt','.')]:
            content='WEBVTT\n\n' if ext=='vtt' else ''
            content+='\n\n'.join('%d\n%s --> %s\n%s' % (i,timestamp(c['start'],separator),timestamp(c['end'],separator),
                html.escape(c['text'],quote=False) if ext=='vtt' else c['text']) for i,c in enumerate(cues,1))+'\n'
            (package/(stem+'.'+ext)).write_bytes(content.encode('utf-8'))
        if any(a['end']>b['start']+.001 for a,b in zip(cues,cues[1:])):
            raise ValueError('Overlapping caption cues')
        result=dict(row,stem=stem,package=str(package),audio=str(audio_path),duration=clock,
                    shots=shots,cues=cues,provenance=provenance,slides=len(plan['slides']))
        write_json(work/'assembled'/lang/('L%02d.json'%row['lesson']),result)
        results.append({'lesson':row['lesson'],'slides':len(plan['slides']),'shots':len(shots),'duration':clock,'cues':len(cues)})
        print(json.dumps(results[-1]),flush=True)
    return results


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('command',choices=['jobs','assemble'])
    ap.add_argument('--work',type=Path,required=True)
    ap.add_argument('--lang',choices=['ko','en'],required=True)
    ap.add_argument('--lesson',type=int)
    a=ap.parse_args()
    if a.command=='jobs': make_jobs(a.work,a.lang)
    else: assemble(a.work,a.lang,a.lesson)
