"""감항 1단 상황보고 조각(frag_ga1.html)을 /report/ 와 / (접수 안내) 두 페이지에 넣는다.

사용: python3 tools/build_ga1.py <저장소 경로> <비밀번호 파일>
- <priv>…</priv> 부분은 페이지에 이미 쓰인 SALT로 PBKDF2(SHA-256, 300,000회) + AES-GCM 암호화해 잠금 처리.
- 비밀번호는 기존 잠금 하나를 풀어 맞는지 먼저 확인한다.
"""
import base64, os, re, sys
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

repo, pwfile = sys.argv[1], sys.argv[2]
pw = open(pwfile, encoding='utf-8').read().strip()
rp = os.path.join(repo, 'report/index.html')
ip = os.path.join(repo, 'index.html')
frag = open(os.path.join(repo, 'tools/frag_ga1.html'), encoding='utf-8').read().rstrip('\n')
rep = open(rp, encoding='utf-8').read()
idx = open(ip, encoding='utf-8').read()

salt = base64.b64decode(re.search(r"SALT='([^']+)'", rep).group(1))
key = PBKDF2HMAC(hashes.SHA256(), 32, salt, 300000).derive(pw.encode())
g = AESGCM(key)
m = re.search(r'data-iv="([^"]+)" data-ct="([^"]+)"', rep)
try:
    g.decrypt(base64.b64decode(m.group(1)), base64.b64decode(m.group(2)), None)
except Exception:
    sys.exit('비밀번호가 기존 잠금과 맞지 않습니다.')

LOCK = ('<span class="lock" role="button" tabindex="0" aria-label="비밀번호를 입력하면 볼 수 있는 내용" '
        'data-iv="{iv}" data-ct="{ct}"><span class="pill">🔒 비밀번호 입력</span><span class="bar"></span></span>')

def enc(h):
    def f(mm):
        iv = os.urandom(12)
        ct = g.encrypt(iv, mm.group(1).encode(), None)
        return LOCK.format(iv=base64.b64encode(iv).decode(), ct=base64.b64encode(ct).decode())
    return re.sub(r'<priv>(.*?)</priv>', f, h, flags=re.S)

# 1) 상황보고 페이지: p3(감항 1단) 패널 교체 + 접수 현황
pat = re.compile(r'(<div class="panel" id="p3"[^>]*>\s*<div class="group">감항</div>\n).*?(\n    </div>\n\n    <div class="panel" id="p4")', re.S)
assert pat.search(rep), 'report p3 not found'
rep = pat.sub(lambda mm: mm.group(1) + enc(frag) + mm.group(2), rep, count=1)
rep = rep.replace('<b>감항 1단</b><span class="wait">접수 중</span>', '<b>감항 1단</b><span class="ok">접수</span>')

# 2) 접수 안내 페이지: 참고 탭에 감항 1단 추가 (곤1, 곤2, 감1, 감2)
if 'aria-controls="p4"' not in idx:
    idx = idx.replace('aria-controls="p3" id="t3">감항 2단</button>',
                      'aria-controls="p3" id="t3">감항 1단</button>\n      '
                      '<button role="tab" aria-selected="false" aria-controls="p4" id="t4">감항 2단</button>')
    idx = idx.replace('<div class="panel" id="p3" role="tabpanel" aria-labelledby="t3" hidden>',
                      '<div class="panel" id="p4" role="tabpanel" aria-labelledby="t4" hidden>')
    i = idx.find('<div class="panel" id="p4"')
    idx = (idx[:i] + '<div class="panel" id="p3" role="tabpanel" aria-labelledby="t3" hidden>\n'
           + enc(frag) + '\n    </div>\n\n    ' + idx[i:])
else:
    pat2 = re.compile(r'(<div class="panel" id="p3"[^>]*>\n).*?(\n    </div>\n\n    <div class="panel" id="p4")', re.S)
    idx = pat2.sub(lambda mm: mm.group(1) + enc(frag) + mm.group(2), idx, count=1)
idx = idx.replace('먼저 보내주신 곤항 1·2단, 감항 2단의 상황보고', '먼저 보내주신 곤항 1·2단, 감항 1·2단의 상황보고')

open(rp, 'w', encoding='utf-8').write(rep)
open(ip, 'w', encoding='utf-8').write(idx)
print('ok')
