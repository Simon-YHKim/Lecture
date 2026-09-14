"""Narration of canonical self-study actions, with separate TTS pronunciation.

Display text preserves CAD literals. No drawing values or procedures are derived
here: all teaching content comes from the selected source slide and lesson.
"""
import html
import re


def clean(text):
    # Strip actual HTML before decoding entities, preserving literal <> input.
    text=re.sub(r'<(?:br|/p|/div)\s*/?>',' ',text,flags=re.I)
    text=re.sub(r'</?(?:p|div|span|b|strong|em|i|code|kbd|small|br|ul|li|ol|sup|sub)(?:\s[^>]*|\s*/?)>','',text,flags=re.I)
    text=html.unescape(text)
    text=re.sub(r'\*\*([^*]+)\*\*',r'\1',text).replace('`','')
    text=re.sub(r'\[(?:차분하게|짚어주듯|힘주어|또박또박|묻듯이|주의를 주듯|가볍게|따뜻하게|calm|pointing|emphatic|measured|asking|cautionary|light|warm)\]\s*','',text)
    return re.sub(r'\s+',' ',text).strip()


def localized(value,lang):
    if isinstance(value,dict):
        if lang not in value: raise ValueError('Missing '+lang+' source text')
        return clean(value[lang])
    return clean(value or '')


def sentence(text):
    return text if not text or text[-1] in '.?!。' else text+'.'


def slide_narration(slide,lesson,lang):
    if lang not in ('ko','en'):raise ValueError('Unsupported language')
    if 'sourceStep' not in slide:
        text=clean(slide['notes'])
        if not text or text=='—':raise ValueError('Empty slide narration')
        if lang=='en' and re.search('[가-힣]',text):raise ValueError('Korean text in English narration')
        return sentence(text)
    candidates=[step for section in lesson['sections'] for block in section.get('blocks',[])
                if block.get('type')=='steps' for step in block['items'] if step['n']==slide['sourceStep']]
    if len(candidates)!=1:raise ValueError('Ambiguous source step')
    step=candidates[0];actions=step.get('actions',[]);indices=slide['sourceActions']
    if not indices or indices!=list(range(indices[0],indices[-1]+1)) or indices[0]<1 or indices[-1]>len(actions):
        raise ValueError('Invalid split action indices')
    pieces=[]
    if indices[0]==1:pieces.append(localized(step.get('title'),lang))
    for index in indices:
        action=actions[index-1]
        typed=localized(action.get('type'),lang)
        # Canonical builder uses `type` for literal keystrokes, including dict
        # values where English file names differ from the Korean edition.
        description=localized(action.get('do'),lang)
        # A is an option; the article "a" is not. Likewise 0 is not the 0 in
        # 0.5, and 35 is not -35. Deduplicate only an exact input token.
        present=bool(typed and re.search(r'(?<![A-Za-z0-9_@+\-.,−])'+re.escape(typed)+
                                        r'(?![A-Za-z0-9_]|[.,]\d)',description))
        if typed and not present:
            kind=action.get('kind','type')
            if re.match(r'^(?:을|를|로|으로)\s',description) and lang=='ko':
                pieces.append(typed+description)
                continue
            if kind=='key':
                pieces.append(('%s 키를 누릅니다.' if lang=='ko' else 'Press %s.')%typed)
                if lang=='en' and description.startswith('clears '):description='This '+description
            elif kind=='click':
                if lang=='en' and re.match(r'^(?:and|from)\b',description):
                    pieces.append('Select %s %s'%(typed,description))
                    continue
                pieces.append(('%s 항목을 선택합니다.' if lang=='ko' else 'Select %s.')%typed)
            elif kind=='alt':
                pieces.append(('필요할 때 사용할 명령은 %s입니다.' if lang=='ko' else 'The optional command is %s.')%typed)
            else:
                pieces.append(('입력값은 %s입니다.' if lang=='ko' else 'Enter %s.')%typed)
        if description:pieces.append(description)
        if not typed and not description:raise ValueError('Action has no narration')
    if indices[-1]==len(actions) and step.get('expect'):
        pieces.append(localized(step['expect'],lang))
    if indices[0]==1 and step.get('why'):
        pieces.append(localized(step['why'],lang))
    if indices[-1]==len(actions) and step.get('pitfall'):
        pieces.append(localized(step['pitfall'],lang))
    result=' '.join(sentence(p) for p in pieces if p)
    if lang=='en' and re.search('[가-힣]',result):raise ValueError('Korean text in English narration')
    return result


KO_LETTERS=dict(zip('ABCDEFGHIJKLMNOPQRSTUVWXYZ',
    ['에이','비','씨','디','이','에프','지','에이치','아이','제이','케이','엘','엠','엔','오','피','큐','알','에스','티','유','브이','더블유','엑스','와이','제드']))
KO_COMMANDS={'OPEN':'오픈','CLOSE':'클로즈','SAVEAS':'세이브 애즈','LINE':'라인','PLINE':'피라인',
    'CIRCLE':'서클','ARC':'아크','OFFSET':'오프셋','TRIM':'트림','EXTEND':'익스텐드','ERASE':'이레이즈',
    'MOVE':'무브','COPY':'카피','MIRROR':'미러','ROTATE':'로테이트','FILLET':'필렛','CHAMFER':'챔퍼',
    'ARRAYPOLAR':'어레이 폴라','DIMLINEAR':'딤 리니어','DIMALIGNED':'딤 얼라인드',
    'DIMDIAMETER':'딤 다이어미터','DIMRADIUS':'딤 레이디우스','DIMANGULAR':'딤 앵귤러',
    'DIMSTYLE':'딤 스타일','DIMTEDIT':'딤 티 에디트','DIMEDIT':'딤 에디트','DIM':'딤',
    'LAYER':'레이어','LINETYPE':'라인 타입','LTSCALE':'엘 티 스케일','OSNAP':'오스냅',
    'ORTHO':'오쏘','XLINE':'엑스 라인','QSELECT':'퀵 셀렉트','PLOT':'플롯','ZOOM':'줌',
    'UNITS':'유닛츠','LIMITS':'리미츠','MTEXT':'엠 텍스트','TEXT':'텍스트','REGEN':'리젠',
    'Enter':'엔터','Ctrl':'컨트롤','Esc':'이스케이프','Tab':'탭','Shift':'시프트'}


def pronunciation(text,lang):
    text=clean(text)
    ko=lang=='ko'
    if ko:
        # Dimension callouts mix Latin letters and digits; leaving R5 to a
        # multilingual model can turn the radius into a different number.
        text=re.sub(r'(?<![A-Za-z0-9_])R(?=\d)','반지름 ',text)
        text=re.sub(r'(?<![A-Za-z0-9_])M(?=\d)','엠 ',text)
        text=re.sub(r'(?<![A-Za-z0-9_])H(?=\d)','에이치 ',text)
        text=re.sub(r'acadiso\.dwt','아카드 아이소 닷 디 더블유 티',text,flags=re.I)
    text=re.sub(r'%%([cCdDpP])',lambda m:('퍼센트 두 개, '+KO_LETTERS[m[1].upper()]) if ko
                else 'percent sign, percent sign, '+m[1].upper(),text)
    text=text.replace('<>','측정값 자리표시 꺾쇠' if ko else 'the measured value placeholder, less than sign then greater than sign')
    for symbol,k,e in [('Ø','지름 ','diameter '),('ø','지름 ','diameter '),('±','플러스 마이너스 ','plus or minus '),
                        ('°','도',' degrees'),('×',' 곱하기 ',' times '),('÷',' 나누기 ',' divided by '),
                        ('−',' 빼기 ',' minus ')]:
        text=text.replace(symbol,k if ko else e)
    text=re.sub(r'(?<=\d)\s+/\s+(?=\d)',' 나누기 ' if ko else ' divided by ',text)
    text=re.sub(r'(?<=\d)\s+-\s+(?=\d)',' 빼기 ' if ko else ' minus ',text)
    text=re.sub(r'@(?=[-+\d])','골뱅이 ' if ko else 'at sign ',text)
    text=re.sub(r'(?<![A-Za-z0-9_])-(?=\d)','마이너스 ' if ko else 'minus ',text)
    text=re.sub(r'(?<![A-Za-z0-9_])\+(?=\d)','플러스 ' if ko else 'plus ',text)
    text=re.sub(r'(?<=\d)\.(?=\d)',' 점 ' if ko else ' point ',text)
    text=text.replace('<',' 왼쪽 꺾쇠 ' if ko else ' less than sign ').replace('>',' 오른쪽 꺾쇠 ' if ko else ' greater than sign ')
    text=re.sub(r'(?<=\d),(?=\d|minus|마이너스)',' 쉼표 ' if ko else ' comma ',text)
    text=re.sub(r'(?<=\d)\s*\+\s*(?=\d)',' 더하기 ' if ko else ' plus ',text)
    if ko:
        pattern=r'(?<![A-Za-z0-9_])('+ '|'.join(sorted(map(re.escape,KO_COMMANDS),key=len,reverse=True)) +r')(?![A-Za-z0-9_])'
        text=re.sub(pattern,lambda m:KO_COMMANDS[m[0]],text)
        text=re.sub(r'(?<![A-Za-z0-9_])F(\d{1,2})(?![A-Za-z0-9_])',r'에프 \1',text)
        text=re.sub(r'(?<![A-Za-z0-9_])([A-Z]{1,3})(?![A-Za-z0-9_])',lambda m:' '.join(KO_LETTERS[c] for c in m[0]),text)
    else:
        text=re.sub(r'\bZ\b','Zed',text)
        text=re.sub(r'(?<![A-Za-z0-9_])F(\d{1,2})(?![A-Za-z0-9_])',r'F \1',text)
        text=re.sub(r'\bdiameter\s+diameter\b','diameter',text,flags=re.I)
    return re.sub(r'\s+',' ',text).strip()
