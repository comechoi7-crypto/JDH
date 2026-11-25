"""12월 정단회 접수 안내(/)·상황보고(/report/) 첫 페이지를 만든다.

사용: python3 -I tools/build_2612_init.py <저장소 경로>
- 11월 페이지(index.html, report/, jaryojip/, img/)를 2611/ 에 그대로 복사해 보관한다.
- 루트 접수 안내와 상황보고를 12월(건항 1·2단, 태항 1·2단) 내용으로 바꾼다.
- 자료집(/jaryojip/)은 12월 자료집이 나올 때까지 그대로 둔다.
"""
import os, re, shutil, sys

repo = sys.argv[1]
J = lambda *p: os.path.join(repo, *p)

# 1) 11월 보관
arc = J('2611')
if not os.path.exists(arc):
    os.makedirs(arc)
    shutil.copy2(J('index.html'), J('2611', 'index.html'))
    for d in ('report', 'jaryojip', 'img'):
        shutil.copytree(J(d), J('2611', d))

TEAMS = [('건항', '건항 1단'), ('건항', '건항 2단'), ('태항', '태항 1단'), ('태항', '태항 2단')]

def sub1(pat, rep, s, flags=re.S):
    out, n = re.subn(pat, rep, s, count=1, flags=flags)
    assert n == 1, pat[:60]
    return out

# 2) 접수 안내
idx = open(J('2611', 'index.html'), encoding='utf-8').read()
idx = idx.replace('11월 정단회 상황보고 안내', '12월 정단회 상황보고 안내')
idx = idx.replace('<meta property="og:image" content="img/gh1-12.jpg">',
                  '<meta property="og:image" content="jaryojip/emblem.png">')
idx = sub1(r'<p class="lead">.*?</p>',
           '<p class="lead">12월 정단회에서는 건항 1·2단, 태항 1·2단의 항단 상황보고가 있습니다. '
           '발표하실 내용을 미리 보내주시면 정단회 자료에 담아 함께 공유드릴 수 있도록 하겠습니다.</p>', idx)
sec2 = '''<section>
    <h2><span class="num">2</span>지난달 항단 상황보고</h2>
    <p>형식은 자유롭게 정해 주시면 됩니다. 11월 정단회에서 나눈 곤항 1·2단, 감항 1·2단의 상황보고를 참고로 보실 수 있습니다.</p>
    <a class="linkcard" href="2611/report/"><div><b>11월 정단회 상황보고 보기</b><span>곤항 1·2단, 감항 1·2단</span></div><span class="arr">›</span></a>
  </section>'''
idx = sub1(r'<section>\s*<h2><span class="num">2</span>.*?</section>', sec2, idx)
# linkcard 스타일(상황보고 페이지와 같게)
rep_css = open(J('2611', 'report', 'index.html'), encoding='utf-8').read()
lc = ''.join(re.findall(r'  \.linkcard[^\n]*\n', rep_css))
if '.linkcard{' not in idx:
    idx = idx.replace('</style>', lc + '</style>', 1)
open(J('index.html'), 'w', encoding='utf-8').write(idx)

# 3) 상황보고
rep = rep_css
rep = rep.replace('원기111년 11월 정단회 상황보고', '원기111년 12월 정단회 상황보고')
rep = rep.replace('<meta property="og:description" content="곤항 1·2단, 감항 1·2단 상황보고">',
                  '<meta property="og:description" content="건항 1·2단, 태항 1·2단 상황보고">')
rep = rep.replace('<meta property="og:image" content="../img/gh1-12.jpg">',
                  '<meta property="og:image" content="../jaryojip/emblem.png">')
rep = rep.replace('<h1>원기111년 11월 정단회<br>상황보고</h1>', '<h1>원기111년 12월 정단회<br>상황보고</h1>')
rep = sub1(r'<p class="lead">.*?</p>',
           '<p class="lead">건항 1·2단, 태항 1·2단에서 보내주시는 상황보고를 모으고 있습니다.</p>', rep)
status = '<div class="status">\n' + ''.join(
    f'    <div class="st"><b>{n}</b><span class="wait">접수 중</span></div>\n' for _, n in TEAMS) + '  </div>'
rep = sub1(r'<div class="status">.*?</div>\n  </div>', status, rep)
tabs = '\n'.join(
    f'      <button role="tab" aria-selected="{"true" if i == 1 else "false"}" aria-controls="p{i}" id="t{i}">{n}</button>'
    for i, (_, n) in enumerate(TEAMS, 1))
panels = '\n\n'.join(
    f'''    <div class="panel" id="p{i}" role="tabpanel" aria-labelledby="t{i}"{"" if i == 1 else " hidden"}>
      <div class="group">{g}</div>
      <div class="pending"><b>{n} 상황보고</b>보내주시는 대로 이곳에 담아 함께 나누겠습니다.</div>
    </div>''' for i, (g, n) in enumerate(TEAMS, 1))
sect = f'''<section>
    <div class="tabs" role="tablist">
{tabs}
    </div>

{panels}
  </section>'''
rep = sub1(r'<section>\s*<div class="tabs".*?</section>', sect, rep)
# 12월 자료집이 나오기 전이므로 자료집 버튼은 뺀다(자료집 게시 때 다시 넣음)
rep = sub1(r'\s*<a class="linkcard"[^\n]*</a>\n', '\n', rep)
open(J('report', 'index.html'), 'w', encoding='utf-8').write(rep)
print('ok')
