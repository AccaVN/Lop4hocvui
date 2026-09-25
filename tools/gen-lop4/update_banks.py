"""Cập nhật ngân hàng câu hỏi lớp 4 vào public/index.html.
Cách chạy (trong thư mục tools/gen-lop4):  python3 update_banks.py
Sửa câu hỏi: m4a.py, m4b.py (Toán), tv4a–tv4d.py (Tiếng Việt), en4.py (English) rồi chạy lại lệnh trên.
Kiểm tra đáp án Toán: python3 check_m4.py"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from m4b import build as build_math
from tvbank4 import build_tv
from en4 import build_en
from common import R
J = lambda o: json.dumps(o, ensure_ascii=False, separators=(',', ':'))
P = os.path.join(HERE, '..', '..', 'public', 'index.html')
mb, meta = build_math()
R.seed(4202609); tvu, tvb = build_tv()
R.seed(4202610); enu, enb = build_en()
L = open(P, encoding='utf-8').read().split('\n')
def setline(prefix, new):
    idx = [i for i, l in enumerate(L) if l.startswith(prefix)]
    assert len(idx) == 1, (prefix, idx)
    changed = L[idx[0]] != new
    L[idx[0]] = new
    print(('ĐỔI  ' if changed else 'giữ  ') + prefix)
setline('const MATH_BANK=', 'const MATH_BANK=' + J(mb) + ';')
setline('const EN_UNITS=', 'const EN_UNITS=' + J(enu) + ';')
setline('const EN_BANK=', 'const EN_BANK=' + J(enb) + ';')
setline('const TV_UNITS=', 'const TV_UNITS=' + J(tvu) + ';')
setline('const TV_BANK=', 'const TV_BANK=' + J(tvb) + ';')
setline('const WEEKS=', 'const WEEKS=' + J(meta) + ';')
open(P, 'w', encoding='utf-8').write('\n'.join(L))
