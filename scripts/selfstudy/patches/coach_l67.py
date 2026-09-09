# -*- coding: utf-8 -*-
"""치수 차시와 편집 차시에 도면과 코치 마크를 넣는다.

검수 메모 18: "치수 차시는 도면 띄우고 코치마크로 위치 알려주는게 전체적으로
빠져있음." 치수는 어느 점 두 개를 집느냐가 값을 정한다. 어느 점인지 안 보이면
따라 할 수가 없다.

좌표는 도면에서 읽은 값이지 짐작이 아니다. 원점은 베이스 왼쪽 아래 구석,
x 오른쪽, y 위다 — scripts/part/edu_ib_02.py 와 같은 기준이다.

    python coach_l67.py [--dry]
"""
import io
import json
import os
import sys
# 저장소 뿌리에서 상대로 잡는다 — 남의 컴퓨터에서도 돌아가야 한다.
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


SRC = os.path.join(REPO, 'scripts', 'selfstudy', 'source')

BOSS = (60.0, 62.0)
FC_R, FC_L = (107.86, 26.0), (12.14, 26.0)      # 필렛 중심 — 사이가 참고 치수 95.7
TAP = 15.556                                     # 피치원 반지름 22 를 45도로 나눈 값


def sp(x, y, snap, ko, en):
    return {'x': x, 'y': y, 'snap': snap, 'hover': {'ko': ko, 'en': en}}


L7 = {
 6: ('profile', [
    sp(0, 0, 'end', '왼쪽 아래 구석 — 120 과 90 둘 다 여기서 시작',
       'Lower-left corner - both the 120 and the 90 start here'),
    sp(120, 0, 'end', '오른쪽 아래 구석 — 120 의 반대쪽 점',
       'Lower-right corner - the far point of the 120'),
    sp(60, 90, 'qua', '보스 맨 위 — 90 의 위쪽 점입니다. 사분점 표식을 보고 누르세요',
       'Top of the boss - the upper point of the 90. Wait for the quadrant marker')]),
 7: ('bossc', [
    sp(0, 0, 'end', '왼쪽 아래 구석 — 16 과 60 · 62 의 공통 기준점',
       'Lower-left corner - the datum for the 16 and for 60, 62'),
    sp(0, 16, 'end', '왼쪽 세로변 끝 — 베이스 높이 16 의 위쪽 점',
       'Top of the left edge - the upper point of the 16'),
    sp(BOSS[0], BOSS[1], 'cen', '보스 중심 — 60 과 62 가 만나는 자리. 중심 표식이에요',
       'Boss center - where the 60 and the 62 meet. The center marker')]),
 8: ('slot', [
    sp(0, 0, 'end', '왼쪽 아래 구석 — 29 와 8 을 여기서 잽니다',
       'Lower-left corner - the 29 and the 8 are measured from here'),
    sp(29, 8, 'cen', '왼쪽 장공의 왼쪽 끝원 중심 — 29 와 8 이 만나는 자리',
       'Center of the left slot left end - where the 29 and the 8 meet'),
    sp(79, 8, 'cen', '오른쪽 장공의 왼쪽 끝원 중심 — 여기까지가 50',
       'Center of the right slot left end - the 50 ends here')]),
 9: ('neck', [
    sp(20, 16, 'int', '왼쪽 라운드가 베이스 윗면에 닿는 자리 — 80 의 왼쪽 점',
       'Where the left fillet meets the base top - the left point of the 80'),
    sp(100, 16, 'int', '오른쪽 라운드가 닿는 자리 — 80 의 오른쪽 점',
       'Where the right fillet meets - the right point of the 80')]),
 10: ('bore', [
    sp(BOSS[0], BOSS[1], 'cen', '보스 중심 — 지름은 원을 클릭하면 중심을 알아서 잡습니다',
       'Boss center - a diameter picks the center itself when you click the circle'),
    sp(BOSS[0] - 12.5, BOSS[1], 'qua', '축 구멍 둘레 — 여기를 클릭하면 Ø25 입니다',
       'The bore edge - click here for the Ø25'),
    sp(BOSS[0] - 28, BOSS[1], 'qua', '보스 둘레 — 여기를 클릭하면 Ø56 입니다',
       'The boss edge - click here for the Ø56')]),
 11: ('fillet', [
    sp(FC_L[0] + 10, FC_L[1], 'nea', '왼쪽 라운드 — 호를 클릭하면 R10 입니다',
       'The left fillet - click the arc for the R10'),
    sp(FC_R[0] - 10, FC_R[1], 'nea', '오른쪽 라운드 — 같은 값이라 2-R10 으로 묶어 적습니다',
       'The right fillet - the same value, so they are written together as 2-R10'),
    sp(29, 13, 'nea', '장공 끝의 둥근 부분 — 여기가 R5 입니다',
       'The rounded end of the slot - this is the R5')]),
 13: ('basehl', [
    sp(5, 16, 'end', '왼쪽 모따기 — 경사선 자체를 클릭합니다',
       'The left chamfer - click the sloped edge itself'),
    sp(115, 16, 'end', '오른쪽 모따기 — 같은 값이라 2-C5 로 묶습니다',
       'The right chamfer - the same value, written together as 2-C5')]),
 14: ('tap', [
    sp(BOSS[0] - TAP, BOSS[1] + TAP, 'cen', '왼쪽 위 탭 — 네 개가 같은 값이라 4-M5 로 묶습니다',
       'The top-left tapped hole - all four are the same, so 4-M5'),
    sp(BOSS[0] + TAP, BOSS[1] + TAP, 'cen', '오른쪽 위 탭 — 지시선은 하나만 뺍니다',
       'The top-right tapped hole - only one leader is drawn')]),
 15: ('filletc', [
    sp(FC_L[0], FC_L[1], 'cen', '왼쪽 필렛 중심 — 여기 높이가 26 입니다',
       'The left fillet center - this height is the 26'),
    sp(FC_R[0], FC_R[1], 'cen', '오른쪽 필렛 중심 — 두 중심 사이가 참고 치수 (95.7)',
       'The right fillet center - between the two is the reference (95.7)')]),
}

L6 = {
 5: ('profile', [
    sp(20, 16, 'int', '라운드가 베이스 윗면에 닿는 자리 — 여기 너머로 삐져나온 선을 자릅니다',
       'Where the fillet meets the base top - trim what runs past here'),
    sp(100, 16, 'int', '반대쪽도 같은 자리에서 자릅니다',
       'Trim at the matching point on the other side')]),
 6: ('basehl', [
    sp(0, 0, 'end', '베이스 왼쪽 아래 — 모자란 선은 여기까지 늘립니다',
       'Base lower left - extend a short line to here'),
    sp(120, 0, 'end', '베이스 오른쪽 아래 — 경계로 쓸 변입니다',
       'Base lower right - the edge you use as the boundary')]),
 9: ('slot', [
    sp(29, 8, 'cen', '왼쪽 장공 중심 — 왼쪽 끝에서 여기까지가 29 여야 합니다',
       'Left slot center - 29 from the left edge'),
    sp(91, 8, 'cen', '오른쪽 장공의 오른쪽 끝 — 오른쪽 끝에서 여기까지도 29 여야 대칭입니다',
       'Right end of the right slot - 29 from the right edge if it is symmetric')]),
 14: ('slotc', [
    sp(29, 8, 'cen', '장공 중심선 — 점과 선의 간격이 눈에 보이는지 봅니다',
       'A slot centerline - check the dash and dot actually read')]),
}


def main(dry=False):
    n = 0
    for les, table in ((6, L6), (7, L7)):
        p = os.path.join(SRC, 'lesson-%02d.json' % les)
        d = json.load(io.open(p, encoding='utf-8'))
        for s in d['sections']:
            for blk in s.get('blocks', []):
                if blk.get('type') != 'steps':
                    continue
                for st in blk['items']:
                    got = table.get(st['n'])
                    if not got:
                        continue
                    feat, spots = got
                    st['feature'] = feat
                    st['spots'] = spots
                    n += 1
        if not dry:
            io.open(p, 'w', encoding='utf-8', newline='\n').write(
                json.dumps(d, ensure_ascii=False, indent=1))
        print('%d차시 단계 %d개에 도면·코치 마크' % (les, len(table)))
    print('합계 %d단계' % n)
    return 0


if __name__ == '__main__':
    sys.exit(main('--dry' in sys.argv))
