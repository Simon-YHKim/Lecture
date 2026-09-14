"""Export the actual self-study deck states to narrated 1080p MP4s.

The HyperFrames slideshow player is used for deterministic per-slide stills.
FFmpeg holds each still for its measured narration beat; a slideshow is never
passed directly to `hyperframes render`, which would render only its first root.
"""
import argparse
import json
from pathlib import Path
import subprocess
import sys

from prepare_narrated import read_json, write_json
from narrated_delivery import digest

VIDEO_FILTER='fps=30'


def concat_text(shots):
    # Give the sparse still timestamps the same time base as the output.
    return ('ffconcat version 1.0\n'+''.join(
        'file %s\noption framerate 30\nduration %.9f\n'%(quote_concat(s['imagePath']),s['duration']) for s in shots)
        +'file '+quote_concat(shots[-1]['imagePath'])+'\noption framerate 30\n')


def validate_video_timing(probe,duration):
    video=next(s for s in probe['streams'] if s['codec_type']=='video')
    audio=next(s for s in probe['streams'] if s['codec_type']=='audio')
    frames=round(duration*30)
    if (int(video['nb_frames'])!=frames or abs(float(video['duration'])-duration)>.001
            or abs(float(video.get('start_time',0)))>.001):
        raise ValueError('Video track does not cover the scheduled frames')
    if abs(float(audio['duration'])-duration)>.05 or abs(float(probe['format']['duration'])-duration)>.05:
        raise ValueError('Audio/container duration mismatch')
    return {'frames':frames,'videoSeconds':float(video['duration']),'audioSeconds':float(audio['duration'])}


def capture(work, lang, lesson=None):
    from playwright.sync_api import sync_playwright
    records=[]
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True)
        page=browser.new_page(viewport={'width':1920,'height':1080},device_scale_factor=1)
        errors,requests=[],[]
        page.on('pageerror',lambda err: errors.append(str(err)))
        page.on('request',lambda req: requests.append(req.url) if req.url.startswith(('http:','https:')) else None)
        for path in sorted((work/'assembled'/lang).glob('L*.json')):
            row=read_json(path)
            if lesson and row['lesson']!=lesson: continue
            output=work/'images'/lang/('L%02d'%row['lesson'])
            output.mkdir(parents=True,exist_ok=True)
            source=Path(row['package'])/(row['stem']+'.html')
            errors.clear(); requests.clear()
            page.goto(source.as_uri(),wait_until='load')
            page.evaluate('document.fonts.ready')
            page.wait_for_function('typeof window.__deckGo === "function"')
            page.add_style_tag(content='''#bar,#note,#full-script{display:none!important}
                #stage{inset:0!important;width:1920px!important;height:1080px!important;transition:none!important}
                #stage [data-composition-id]{box-shadow:none!important}''')
            page.evaluate('window.__deckFit()')
            for shot in row['shots']:
                details=page.evaluate('''s=>{window.__deckGo(s.slide);window.__deckFit();
                    let el=document.querySelector('[data-composition-id="'+s.scene+'"]');
                    let tl=window.__timelines[s.scene];if(!tl)throw Error('Missing timeline '+s.scene);
                    tl.pause().time(Math.min(s.state,tl.duration()));
                    let rect=el.getBoundingClientRect();
                    return {text:el.innerText.length,film:!!el.querySelector('.film'),
                            width:rect.width,height:rect.height,left:rect.left,top:rect.top};}''',shot)
                if details['film'] or details['text']<8 or abs(details['width']-1920)>1 or abs(details['height']-1080)>1:
                    raise ValueError('Invalid self-study frame '+str(details))
                image=output/shot['image']
                page.screenshot(path=str(image),animations='allow')
                shot['imageSha256']=digest(image)
                shot['imagePath']=str(image)
            if errors or requests: raise ValueError({'runtimeErrors':errors,'networkRequests':requests})
            row['deckSha256']=digest(source)
            write_json(path,row)
            records.append({'lang':lang,'lesson':row['lesson'],'slides':row['slides'],'shots':len(row['shots']),
                            'offline':True,'runtimeErrors':errors,'deckSha256':row['deckSha256']})
            print(json.dumps(records[-1]),flush=True)
        browser.close()
    write_json(work/('capture-%s%s.json'%(lang,'-%02d'%lesson if lesson else '')),records)


def quote_concat(path):
    return "'"+str(Path(path).resolve()).replace('\\','/').replace("'", "'\\''")+"'"


def render(work,lang,lesson=None):
    results=[]
    for path in sorted((work/'assembled'/lang).glob('L*.json')):
        row=read_json(path)
        if lesson and row['lesson']!=lesson: continue
        base=work/'encode'/lang/('L%02d'%row['lesson'])
        base.mkdir(parents=True,exist_ok=True)
        shots=row['shots']
        for shot in shots:
            if digest(shot['imagePath'])!=shot['imageSha256']:raise ValueError('Changed captured frame')
        concat=base/'images.ffconcat'
        concat.write_bytes(concat_text(shots).encode())
        package=Path(row['package'])
        dest=package/(row['stem']+'.mp4')
        if dest.exists(): raise FileExistsError('Keep delivered video; use a new private output for revisions: '+str(dest))
        pending=base/'video.pending.mp4'
        log=base/'ffmpeg.log'
        args=['ffmpeg','-hide_banner','-nostdin','-y','-f','concat','-safe','0','-i',str(concat),
              '-i',row['audio'],'-i',str(package/(row['stem']+'.vtt')),
              '-map','0:v:0','-map','1:a:0','-map','2:s:0',
              # Expand sparse stills before output truncation; output -r alone
              # can end early when the final still has a long hold.
              '-vf',VIDEO_FILTER,'-r','30','-fps_mode','cfr','-t','%.9f'%row['duration'],
              '-c:v','h264_nvenc','-preset','p5','-rc','vbr','-cq','18','-b:v','0','-pix_fmt','yuv420p',
              '-c:a','aac','-b:a','160k','-c:s','mov_text','-metadata:s:s:0','language='+('kor' if lang=='ko' else 'eng'),
              '-metadata','title='+row['stem'],'-movflags','+faststart',str(pending)]
        with log.open('w',encoding='utf-8') as f:
            subprocess.run(args,stdout=f,stderr=subprocess.STDOUT,check=True)
        probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(pending)],text=True,encoding='utf-8'))
        video=next(s for s in probe['streams'] if s['codec_type']=='video')
        if (video['width'],video['height'],video['r_frame_rate'])!=(1920,1080,'30/1'):
            raise ValueError('Unexpected video format')
        validate_video_timing(probe,row['duration'])
        pending.rename(dest)
        result={'lang':lang,'lesson':row['lesson'],'slides':row['slides'],'shots':len(shots),
                'file':str(dest),'duration':row['duration'],'bytes':dest.stat().st_size,'sha256':digest(dest)}
        write_json(base/'render.json',result)
        results.append(result)
        print(json.dumps(result),flush=True)
    return results


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('command',choices=['capture','render'])
    ap.add_argument('--work',type=Path,required=True)
    ap.add_argument('--lang',choices=['ko','en'],required=True)
    ap.add_argument('--lesson',type=int)
    a=ap.parse_args()
    (capture if a.command=='capture' else render)(a.work,a.lang,a.lesson)
