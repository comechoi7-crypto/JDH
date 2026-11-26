"""12월 상황보고(/report/)에 접수 안내(/)의 '이런 소식을 담아 주시면 됩니다'·'보내주시는 방법' 절을 넣고 번호를 다시 매긴다.

사용: python3 -I tools/report_add_guide_2612.py <저장소 경로>  (restyle_report_2612.py 다음에 실행)
순서: 1 이런 소식 / 2 접수 현황 / 3 항단 상황보고 / 4 지난달 항단 상황보고 / 5 보내주시는 방법
"""
import os, re, sys
repo = sys.argv[1]
idx = open(os.path.join(repo, 'index.html'), encoding='utf-8').read()
p = os.path.join(repo, 'report', 'index.html')
s = open(p, encoding='utf-8').read()
if '이런 소식을 담아 주시면 됩니다' in s:
    print('already'); sys.exit()
secs = re.findall(r'  <section>\s*<h2><span class="num">\d</span>.*?</section>', idx, re.S)
topics = next(x for x in secs if '이런 소식을' in x)
how = next(x for x in secs if '보내주시는 방법' in x)
num = lambda sec, n: re.sub(r'<span class="num">\d</span>', f'<span class="num">{n}</span>', sec, count=1)
# 기존 번호 1·2·3 → 2·3·4 (뒤에서부터)
for a, b in (('3', '4'), ('2', '3'), ('1', '2')):
    s = s.replace(f'<span class="num">{a}</span>', f'<span class="num">{b}</span>', 1)
s = s.replace('  <section id="sec-status">', num(topics, 1).replace('<section>', '<section id="sec-topics">', 1) + '\n\n  <section id="sec-status">', 1)
# 지난달 절 뒤, 맺음 상자 앞에 보내주시는 방법
s = s.replace('\n\n  <div class="closing">', '\n\n' + num(how, 5) + '\n\n  <div class="closing">', 1)
# 첫 절 위 여백: 이제 소식 절이 맨 앞
s = s.replace('#sec-status h2{margin-top:0}', '#sec-topics h2{margin-top:0}')
open(p, 'w', encoding='utf-8').write(s); print('ok')
