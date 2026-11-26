"""12월 상황보고(/report/)를 접수 안내(/)와 같은 형식(번호 붙은 절 + 맺음 상자)으로 바꾼다.

사용: python3 -I tools/restyle_report_2612.py <저장소 경로>
- 1 접수 현황 / 2 항단 상황보고(탭) / 3 지난달 항단 상황보고(11월 링크) / 맺음 상자
- 탭·접수 현황 내용은 그대로 옮긴다(이미 채운 탭도 유지).
"""
import os, re, sys

repo = sys.argv[1]
p = os.path.join(repo, 'report', 'index.html')
s = open(p, encoding='utf-8').read()

if 'id="sec-status"' in s:
    print('already'); sys.exit()

def grab(pat):
    m = re.search(pat, s, re.S); assert m, pat[:50]; return m.group(0)

status = grab(r'  <div class="status">.*?</div>\n  </div>')
tabsec = grab(r'  <section>\s*<div class="tabs".*?</section>')
tabs_inner = re.search(r'<section>(.*)</section>', tabsec, re.S).group(1)
old_body = grab(r'  <div class="status">.*?<footer>')

new_body = f'''  <section id="sec-status">
    <h2><span class="num">1</span>접수 현황</h2>
{status}
    <p class="note">상황보고가 들어오는 대로 '접수'로 바꾸고 아래 탭에 담습니다.</p>
  </section>

  <section>
    <h2><span class="num">2</span>항단 상황보고</h2>{tabs_inner}</section>

  <section>
    <h2><span class="num">3</span>지난달 항단 상황보고</h2>
    <p>11월 정단회에서 나눈 곤항 1·2단, 감항 1·2단의 상황보고를 참고로 보실 수 있습니다.</p>
    <a class="linkcard" href="../2611/report/"><div><b>11월 정단회 상황보고 보기</b><span>곤항 1·2단, 감항 1·2단</span></div><span class="arr">›</span></a>
  </section>

  <div class="closing">
    <p>바쁘신 가운데 늘 항단을 살펴 주셔서 감사드립니다.<br>각 항단의 소식이 모여 정단회가 더 풍성해질 수 있도록 함께해 주시면 고맙겠습니다.</p>
  </div>

  <footer>'''
s = s.replace(old_body, new_body, 1)
# 절 제목 아래 여백 맞춤
s = s.replace('.status{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin:0 0 6px}',
              '.status{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin:0}')
# 첫 절은 헤더 바로 아래라 위 여백을 줄인다
s = s.replace('</style>', '  #sec-status h2{margin-top:0}\n</style>', 1)
open(p, 'w', encoding='utf-8').write(s)
print('ok')
