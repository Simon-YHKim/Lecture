"""Build a fully offline review player for eight verified lesson downloads."""
import argparse
import hashlib
import json
from pathlib import Path

from narrated_delivery import digest
from prepare_narrated import read_json

HERE=Path(__file__).resolve().parent


def review_data(work,lang,complete=True):
    lessons=[]
    for path in sorted((work/'assembled'/lang).glob('L*.json')):
        row=read_json(path)
        validation=work/'validation'/lang/path.name
        if not validation.exists():continue
        valid=read_json(validation)
        folder=Path(row['package']);stem=row['stem']
        if not valid['ok'] or valid.get('validationVersion')!=2 or valid['planSha256']!=digest(path):raise ValueError('Unverified assembly')
        if valid['sha256']!=digest(folder/(stem+'.mp4')):raise ValueError('Video changed after verification')
        if row['deckSha256']!=digest(folder/(stem+'.html')):raise ValueError('Deck changed after capture')
        source=read_json(row['source'])
        lessons.append({'number':row['lesson'],'title':source['title'][lang],
                        'duration':row['duration'],'video':stem+'.mp4','slides':stem+'.html',
                        'videoSha256':valid['sha256'],'deckSha256':row['deckSha256'],
                        'cues':[{k:c[k] for k in ['start','end','text','slide']} for c in row['cues']]})
    if complete and [l['number'] for l in lessons]!=list(range(1,9)):
        raise ValueError('All eight verified lessons are required')
    if not lessons:raise ValueError('No verified lesson')
    review_id=hashlib.sha256(json.dumps(lessons,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
    return {'language':lang,'reviewId':review_id,'complete':complete,'lessons':lessons}


def document(data):
    raw=(HERE/'assets/narrated_review.html').read_text(encoding='utf-8')
    serialized=json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')
    return raw.replace('__LANG__',data['language']).replace('__DATA__',serialized)


def build(work,lang):
    data=review_data(work,lang)
    target=work/'packages'/lang/('START_REVIEW_%s.html'%lang.upper())
    target.write_bytes(document(data).encode('utf-8'))
    return target


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--work',type=Path,required=True)
    ap.add_argument('--lang',choices=['ko','en'],required=True)
    a=ap.parse_args();print(build(a.work,a.lang))
