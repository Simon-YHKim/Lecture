"""Verify exported slide videos against captured pixels and native source PCM."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import io
import json
from pathlib import Path
import re
import subprocess

import numpy as np
from PIL import Image
from scipy.signal import correlate

from prepare_narrated import read_json, write_json
from narrated_delivery import digest, wav_data, SR, timestamp
from render_narrated import validate_video_timing

VALIDATION_VERSION=2


def run(args):
    return subprocess.run(args,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True).stdout


def verify(work,lang,lesson=None):
    results=[]
    for path in sorted((work/'assembled'/lang).glob('L*.json')):
        row=read_json(path)
        if lesson and row['lesson']!=lesson:continue
        video=Path(row['package'])/(row['stem']+'.mp4')
        if digest(Path(row['package'])/(row['stem']+'.html'))!=row['deckSha256']:
            raise ValueError('Deck changed after its pictures were captured')
        sha=digest(video)
        target=work/'validation'/lang/('L%02d.json'%row['lesson'])
        if target.exists():
            old=read_json(target)
            if old.get('ok') and old.get('validationVersion')==VALIDATION_VERSION and old['sha256']==sha and old['planSha256']==digest(path):
                results.append(old);continue
        probe=json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(video)]))
        timing=validate_video_timing(probe,row['duration'])
        run(['ffmpeg','-nostdin','-v','error','-xerror','-i',str(video),'-map','0:v:0','-map','0:a:0','-f','null','-'])
        srt=run(['ffmpeg','-nostdin','-v','error','-i',str(video),'-map','0:s:0','-f','srt','-']).decode('utf-8-sig')
        blocks=re.split(r'\n\s*\n',srt.replace('\r\n','\n').strip())
        text=[' '.join(b.splitlines()[2:]).strip() for b in blocks]
        times=re.findall(r'^([0-9:,]+) --> ([0-9:,]+)',srt,re.M)
        expected=[(timestamp(c['start'],','),timestamp(c['end'],',')) for c in row['cues']]
        if text!=[c['text'] for c in row['cues']] or times!=expected:
            raise ValueError('Subtitle text or timing changed: '+row['stem'])
        actual=np.frombuffer(run(['ffmpeg','-nostdin','-v','error','-i',str(video),'-map','0:a:0',
                                  '-ac','1','-ar',str(SR),'-f','f32le','-']),dtype='<f4').astype(np.float64)
        checks=[]
        for item in row['provenance']:
            if digest(item['source'])!=item['sha256']: raise ValueError('Changed voice source')
            source=np.frombuffer(wav_data(item['source']),dtype='<i2').astype(np.float64)/32768
            if len(source)<SR//10:raise ValueError('Voice source has fewer than 100 ms of samples')
            # Short keystrokes and numbers can legitimately last < 1 second.
            # Compare their complete PCM instead of rounding their length to 0.
            count=min(2*SR,len(source))
            window=SR//4; windows=len(source)//window
            span=max(1,count//window)
            if windows>=span:
                energies=(source[:windows*window].reshape(windows,window)**2).mean(axis=1)
                offset=int(np.convolve(energies,np.ones(span),mode='valid').argmax())*window
                offset=min(offset,len(source)-count)
            else:offset=0
            reference=source[offset:offset+count]
            reference-=reference.mean()
            center=round(item['videoStart']*SR)+offset
            begin=max(0,center-480)
            observed=actual[begin:center+len(reference)+480]
            n=len(reference)
            sums=np.concatenate(([0.0],np.cumsum(observed)))
            squares=np.concatenate(([0.0],np.cumsum(observed*observed)))
            energy=squares[n:]-squares[:-n]-(sums[n:]-sums[:-n])**2/n
            similarity=correlate(observed,reference,mode='valid',method='fft')/np.maximum(
                np.sqrt(np.maximum(0,energy))*np.linalg.norm(reference),1e-12)
            best=int(similarity.argmax());score=float(similarity[best])
            if score<.95:raise ValueError('Source audio mismatch: '+str((item['scene'],score)))
            checks.append({'scene':item['scene'],'correlation':round(score,6),'offsetMs':round((begin+best-center)/SR*1000,3)})
        def visual(shot,at=None):
            if at is None:at=shot['start']+shot['duration']/2
            encoded=run(['ffmpeg','-nostdin','-v','error','-ss',str(at),'-i',str(video),'-frames:v','1',
                         '-vf','scale=480:270:flags=lanczos','-f','image2pipe','-vcodec','png','-'])
            if not encoded:raise ValueError('Missing video frame: '+str((row['stem'],shot['image'],at)))
            actual_image=np.asarray(Image.open(io.BytesIO(encoded)).convert('RGB')).astype(np.float32)
            source=Path(shot['imagePath'])
            if digest(source)!=shot['imageSha256']:raise ValueError('Changed reference picture')
            reference=np.asarray(Image.open(source).convert('RGB').resize((480,270),Image.Resampling.LANCZOS)).astype(np.float32)
            difference=np.abs(actual_image-reference)
            # Mean error plus the worst 30px tile catches missing words that a
            # mostly white page would hide in its global average.
            tiles=difference.reshape(9,30,16,30,3).mean(axis=(1,3,4))
            mean,worst=float(difference.mean()),float(tiles.max())
            if mean>3 or worst>15:raise ValueError('Encoded picture differs: '+str((row['stem'],shot['image'],mean,worst)))
            return {'image':shot['image'],'at':round(at,3),'meanError':round(mean,3),'worstTile':round(worst,3)}
        with ThreadPoolExecutor(max_workers=3) as pool:visuals=list(pool.map(visual,row['shots']))
        last_frame=visual(row['shots'][-1],(timing['frames']-1)/30)
        result={'lang':lang,'lesson':row['lesson'],'ok':True,'sha256':sha,'planSha256':digest(path),
                'validationVersion':VALIDATION_VERSION,'trackTiming':timing,'lastFrame':last_frame,
                'slides':row['slides'],'shots':len(row['shots']),'cues':len(row['cues']),
                'fullDecode':True,'literalCaptions':True,'audioSamples':checks,'visualSamples':visuals,
                'humanListeningPerformed':False}
        write_json(target,result);results.append(result)
        print(json.dumps({k:result[k] for k in ['lang','lesson','ok','slides','shots','cues']}),flush=True)
    return results


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--work',type=Path,required=True)
    ap.add_argument('--lang',choices=['ko','en'],required=True)
    ap.add_argument('--lesson',type=int)
    a=ap.parse_args();verify(a.work,a.lang,a.lesson)
