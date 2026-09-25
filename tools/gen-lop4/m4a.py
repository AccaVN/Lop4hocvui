"""Toán 4 (Kết nối tri thức) — tiện ích + Chặng 1–4.
Mỗi hàm q_*() trả về một bộ sinh (hàm không đối số) tạo 1 câu hỏi."""
from fractions import Fraction as F
from math import gcd
from common import *

# ================= TIỆN ÍCH =================
DG = ['không', 'một', 'hai', 'ba', 'bốn', 'năm', 'sáu', 'bảy', 'tám', 'chín']
NAMES = ['Lan', 'Nam', 'Mai', 'Hùng', 'Hoa', 'Minh', 'An', 'Bình', 'Hà', 'Tú', 'Linh', 'Khôi', 'Vy', 'Phong']


def fmt(n):
    """Viết số theo SGK: nhóm 3 chữ số bằng dấu cách (từ 1 000 trở lên)."""
    n = int(n)
    if abs(n) < 1000:
        return str(n)
    s = str(abs(n)); out = ''
    while len(s) > 3:
        out = '\u00a0' + s[-3:] + out; s = s[:-3]   # dấu cách không ngắt dòng
    return ('-' if n < 0 else '') + s + out


def read2(n, full=False):
    """Đọc số 0..99. full=True: đọc trong nhóm 3 chữ số (có 'linh')."""
    if n < 10:
        return DG[n]
    t, u = divmod(n, 10)
    head = 'mười' if t == 1 else DG[t] + ' mươi'
    if u == 0:
        return head
    if u == 1 and t > 1: tail = 'mốt'
    elif u == 5: tail = 'lăm'
    elif u == 4 and t > 1: tail = 'tư'
    else: tail = DG[u]
    return head + ' ' + tail


def read3(n, lead):
    """Đọc nhóm 3 chữ số. lead=True nếu là nhóm đầu tiên (không đọc 'không trăm')."""
    h, r = divmod(n, 100)
    if lead and h == 0:
        return read2(r)
    s = DG[h] + ' trăm'
    if r == 0:
        return s
    if r < 10:
        return s + ' linh ' + DG[r]
    return s + ' ' + read2(r)


def readNum(n):
    if n == 0:
        return 'không'
    parts = []
    units = ['', 'nghìn', 'triệu', 'tỉ']
    grp = []
    while n > 0:
        grp.append(n % 1000); n //= 1000
    first = True
    for i in range(len(grp) - 1, -1, -1):
        g = grp[i]
        if g == 0 and not first:
            continue
        txt = read3(g, first)
        parts.append(txt + ((' ' + units[i]) if units[i] else ''))
        first = False
    return ' '.join(parts)


def near(n, lo, hi, k=2, cands=None):
    s = []
    for c in (cands or []) + [n + 1, n - 1, n + 10, n - 10, n + 100, n - 100, n + 1000, n - 1000, n + 2, n - 2]:
        if lo <= c <= hi and c != n and c not in s:
            s.append(c)
    return s[:k]


def sign(a, b): return '>' if a > b else '<' if a < b else '='
SIGN_FIX = ['>', '<', '=']


def vcalc(a, b, op):
    return f'<div class="vcalc"><span>{fmt(a)}</span><span><i>{op}</i>{fmt(b)}</span><span class="ln"></span><span>?</span></div>'


def cards(ds):
    return (f'<div class="g100" style="grid-template-columns:repeat({len(ds)},58px)">'
            + ''.join(f'<span>{d}</span>' for d in ds) + '</div>')


def BIG(s):
    """big + tự thu nhỏ chữ khi phép tính dài."""
    return {'big': s, 'bigSmall': True if len(s) > 13 else None}


def sol(lines, ans, unit=''):
    """Lời giải kiểu SGK."""
    u = f' {unit}' if unit else ''
    return 'Bài giải\n' + '\n'.join(lines) + f'\nĐáp số: {fmt(ans) if isinstance(ans, int) else ans}{u}.'


def frac(fr):
    fr = F(fr)
    return str(fr.numerator) if fr.denominator == 1 else f'{fr.numerator}/{fr.denominator}'


def fr_wrong(ans, cands, k=2):
    """Chọn k phân số sai (khác giá trị với đáp án, không trùng chữ)."""
    out = []
    for c in cands:
        if c is None:
            continue
        if isinstance(c, tuple):
            n, d = c
            if d <= 0 or n < 0:
                continue
            txt = f'{n}/{d}' if d != 1 else str(n); val = F(n, d)
        else:
            val = F(c); txt = frac(val)
        if val == F(ans) or txt in out or txt == frac(ans):
            continue
        out.append(txt)
        if len(out) == k:
            break
    return out


# ---------- hình vẽ ----------
def angle_svg(deg, label=None, name='O'):
    """Góc đỉnh O, một cạnh nằm ngang sang phải."""
    import math
    cx, cy, L = 150, 120, 110
    if deg > 150:
        cx = 160
    a = math.radians(deg)
    x2, y2 = cx + L * math.cos(a), cy - L * math.sin(a)
    r = 26
    if deg == 90:
        arc = f'<path d="M{cx+18} {cy} L{cx+18} {cy-18} L{cx} {cy-18}" fill="none" stroke="#E11D48" stroke-width="2.5"/>'
    else:
        ax, ay = cx + r * math.cos(a), cy - r * math.sin(a)
        large = 1 if deg > 180 else 0
        arc = f'<path d="M{cx+r} {cy} A{r} {r} 0 {large} 0 {ax:.1f} {ay:.1f}" fill="none" stroke="#E11D48" stroke-width="2.5"/>'
    lab = ''
    if label:
        m = math.radians(deg / 2)
        lab = f'<text x="{cx + 52*math.cos(m):.1f}" y="{cy - 52*math.sin(m) + 6:.1f}" text-anchor="middle" font-size="18" font-weight="800" fill="#E11D48">{label}</text>'
    return (f'<svg class="geo" viewBox="0 0 300 150" style="max-width:300px" aria-hidden="true">'
            f'<line x1="{cx}" y1="{cy}" x2="{cx+L}" y2="{cy}" stroke="currentColor" stroke-width="3" stroke-linecap="round"/>'
            f'<line x1="{cx}" y1="{cy}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="currentColor" stroke-width="3" stroke-linecap="round"/>'
            f'{arc}{lab}<circle cx="{cx}" cy="{cy}" r="3.5" fill="currentColor"/>'
            f'<text x="{cx-8}" y="{cy+22}" font-size="17" font-weight="800" fill="currentColor">{name}</text></svg>')


def poly_svg(pts, labels, extra='', w=300, h=170):
    P = ' '.join(f'{x},{y}' for x, y in pts)
    s = f'<svg class="geo" viewBox="0 0 {w} {h}" style="max-width:{w}px" aria-hidden="true"><polygon points="{P}" fill="#DBEAFE" stroke="currentColor" stroke-width="3" stroke-linejoin="round"/>'
    cx = sum(p[0] for p in pts) / len(pts); cy = sum(p[1] for p in pts) / len(pts)
    for (x, y), l in zip(pts, labels):
        dx = -16 if x < cx else 8; dy = -6 if y < cy else 20
        s += f'<text x="{x+dx}" y="{y+dy}" font-size="17" font-weight="800" fill="currentColor">{l}</text>'
    return s + extra + '</svg>'


def rect_svg(labels=('A', 'B', 'C', 'D')):
    return poly_svg([(50, 30), (250, 30), (250, 140), (50, 140)], labels)


def lines_svg(kind):
    """kind: 'vg' vuông góc, 'ss' song song, 'cat' cắt nhau (không vuông góc), 'lech' không song song."""
    s = '<svg class="geo" viewBox="0 0 300 150" style="max-width:300px" aria-hidden="true"><g stroke="currentColor" stroke-width="3" stroke-linecap="round">'
    if kind == 'vg':
        s += '<line x1="40" y1="90" x2="260" y2="90"/><line x1="150" y1="15" x2="150" y2="140"/></g><path d="M150 72 L168 72 L168 90" fill="none" stroke="#E11D48" stroke-width="2.5"/>'
    elif kind == 'ss':
        s += '<line x1="30" y1="50" x2="270" y2="50"/><line x1="30" y1="110" x2="270" y2="110"/></g>'
    elif kind == 'cat':
        s += '<line x1="40" y1="120" x2="260" y2="40"/><line x1="60" y1="30" x2="250" y2="130"/></g>'
    else:
        s += '<line x1="30" y1="40" x2="270" y2="65"/><line x1="30" y1="120" x2="270" y2="95"/></g>'
    return s + '</svg>'


SHAPES = {
    'vuông': [(90, 20), (210, 20), (210, 140), (90, 140)],
    'chữ nhật': [(40, 35), (260, 35), (260, 135), (40, 135)],
    'bình hành': [(80, 30), (270, 30), (220, 135), (30, 135)],
    'thoi': [(150, 12), (240, 80), (150, 148), (60, 80)],
    'thang': [(100, 30), (200, 30), (270, 135), (30, 135)],
    'tam giác': [(150, 15), (265, 140), (35, 140)],
}


def shape_svg(k):
    return poly_svg(SHAPES[k], [''] * len(SHAPES[k]), w=300, h=160)


def frac_svg(n, d, kind=None):
    """Hình được chia d phần bằng nhau, tô màu n phần."""
    import math
    kind = kind or ('tron' if d <= 8 and R.random() < .5 else 'bang')
    if kind == 'tron':
        s = '<svg class="geo" viewBox="0 0 160 160" style="max-width:160px" aria-hidden="true">'
        for i in range(d):
            a1 = -math.pi / 2 + 2 * math.pi * i / d; a2 = -math.pi / 2 + 2 * math.pi * (i + 1) / d
            x1, y1 = 80 + 70 * math.cos(a1), 80 + 70 * math.sin(a1)
            x2, y2 = 80 + 70 * math.cos(a2), 80 + 70 * math.sin(a2)
            col = '#F59E0B' if i < n else '#FFFFFF'
            if d == 1:
                s += f'<circle cx="80" cy="80" r="70" fill="{col}" stroke="#334155" stroke-width="2.5"/>'
            else:
                s += f'<path d="M80 80 L{x1:.1f} {y1:.1f} A70 70 0 0 1 {x2:.1f} {y2:.1f} Z" fill="{col}" stroke="#334155" stroke-width="2.5"/>'
        return s + '</svg>'
    cols = d if d <= 10 else (d // 2 if d % 2 == 0 else d)
    rows = d // cols
    cw = min(40, 280 // cols); W = cw * cols; H = 44 * rows
    s = f'<svg class="geo" viewBox="0 0 {W+10} {H+10}" style="max-width:{W+10}px" aria-hidden="true">'
    for i in range(d):
        r_, c_ = divmod(i, cols)
        col = '#F59E0B' if i < n else '#FFFFFF'
        s += f'<rect x="{5+c_*cw}" y="{5+r_*44}" width="{cw}" height="44" fill="{col}" stroke="#334155" stroke-width="2.5"/>'
    return s + '</svg>'


def bar_svg(cats, vals, unit, step):
    """Biểu đồ cột đơn giản."""
    n = len(cats); top = max(vals); ymax = ((top + step - 1) // step) * step
    if ymax == top:
        ymax += step
    W = 70 + n * 62; H = 210; base = 175; hmax = 150
    s = f'<svg class="geo" viewBox="0 0 {W} {H}" style="max-width:{min(W, 420)}px" aria-hidden="true">'
    for v in range(0, ymax + 1, step):
        y = base - hmax * v / ymax
        s += f'<line x1="46" y1="{y:.1f}" x2="{W-8}" y2="{y:.1f}" stroke="#CBD5E1" stroke-width="1"/><text x="40" y="{y+5:.1f}" text-anchor="end" font-size="12" fill="currentColor">{v}</text>'
    COL = ['#3B82F6', '#F59E0B', '#10B981', '#EF4444', '#8B5CF6', '#EC4899']
    for i, (c, v) in enumerate(zip(cats, vals)):
        x = 60 + i * 62; h = hmax * v / ymax
        s += f'<rect x="{x}" y="{base-h:.1f}" width="38" height="{h:.1f}" rx="3" fill="{COL[i % 6]}"/>'
        s += f'<text x="{x+19}" y="{base+18}" text-anchor="middle" font-size="12" font-weight="700" fill="currentColor">{c}</text>'
    s += f'<line x1="46" y1="{base}" x2="{W-8}" y2="{base}" stroke="currentColor" stroke-width="2"/><line x1="46" y1="20" x2="46" y2="{base}" stroke="currentColor" stroke-width="2"/>'
    s += f'<text x="8" y="14" font-size="12" font-weight="700" fill="currentColor">{unit}</text>'
    return s + '</svg>'


def table_html(head, rows, caption=''):
    h = f'<table class="pg">{f"<caption>{caption}</caption>" if caption else ""}'
    h += '<tr>' + ''.join(f'<th>{x}</th>' for x in head) + '</tr>'
    for r in rows:
        h += '<tr>' + ''.join(f'<th>{x}</th>' for x in r) + '</tr>'
    return h + '</table>'


# ================= CHẶNG 1: ÔN TẬP VÀ BỔ SUNG =================
def q_doc5():
    def g():
        n = rnd(10001, 99999)
        if n % 1000 == 0:
            return None
        c = [n + 10000 if n < 90000 else n - 10000, int(str(n)[:2] + str(n)[3] + str(n)[2] + str(n)[4]) if str(n)[2] != str(n)[3] else None]
        c = [x for x in c if x and 10000 <= x <= 99999]
        if R.random() < .5:
            return mc('so', f'Số “{readNum(n)}” viết là:', fmt(n), [fmt(x) for x in near(n, 10000, 99999, 2, c)])
        return mc('so', f'Số {fmt(n)} đọc là:', readNum(n), [readNum(x) for x in near(n, 10000, 99999, 2, c)])
    return g


def q_cautao5():
    names = ['chục nghìn', 'nghìn', 'trăm', 'chục', 'đơn vị']
    def g():
        n = rnd(10000, 99999); s = str(n)
        r = R.random(); i = rnd(0, 4)
        if r < .35:
            d = [int(x) for x in s]
            parts = [d[j] * 10 ** (4 - j) for j in range(5) if d[j]]
            if len(parts) < 3:
                return None
            return inp('so', 'Viết số thích hợp:', n, **BIG(' + '.join(fmt(p) for p in parts) + ' = ?'),
                       explain=f'Cộng các giá trị theo hàng được {fmt(n)}.')
        if r < .7:
            if s[i] == '0':
                return None
            val = int(s[i]) * 10 ** (4 - i)
            return inp('so', f'Trong số {fmt(n)}, chữ số {s[i]} ở hàng {names[i]} có giá trị là bao nhiêu?', val,
                       explain=f'Chữ số {s[i]} ở hàng {names[i]} nên có giá trị {fmt(val)}.')
        if s.count(s[i]) > 1:
            return None
        opts = ['Hàng ' + x for x in names if x != names[i]]
        return mc('so', f'Chữ số {s[i]} trong số {fmt(n)} thuộc hàng nào?', 'Hàng ' + names[i], R.sample(opts, 2))
    return g


def q_cmp(lo, hi, same_len=True):
    def g():
        a = rnd(lo, hi)
        r = R.random()
        if r < .15:
            b = a
        elif r < .6 and same_len:
            s = list(str(a)); i = rnd(1, len(s) - 1); s[i] = str(rnd(0, 9)); b = int(''.join(s))
        else:
            b = rnd(lo, hi)
        if not (lo <= b <= hi):
            return None
        return mc('so', 'Chọn dấu thích hợp điền vào ô trống:', sign(a, b), [], fixed=SIGN_FIX, **BIG(f'{fmt(a)} ☐ {fmt(b)}'),
                  explain='So sánh từ hàng cao nhất (cùng số chữ số) hoặc số nào nhiều chữ số hơn thì lớn hơn.')
    return g


def q_sort(lo, hi, k=4):
    def g():
        base = rnd(lo, hi - 1000)
        xs = set()
        while len(xs) < k:
            xs.add(base + rnd(0, 999) * pick([1, 1, 10]) if base + 9990 <= hi else rnd(lo, hi))
        xs = [x for x in xs if lo <= x <= hi]
        if len(xs) < k:
            return None
        up = R.random() < .5
        ans = sorted(xs, reverse=not up)
        return ordq('so', f'Sắp xếp các số theo thứ tự {"từ bé đến lớn" if up else "từ lớn đến bé"}:', [fmt(x) for x in ans])
    return g


def q_maxmin(lo, hi):
    def g():
        xs = R.sample(range(lo, hi), 4); big = R.random() < .5
        a = max(xs) if big else min(xs)
        return mc('so', f'Số {"lớn" if big else "bé"} nhất trong các số sau là:', fmt(a), [fmt(x) for x in xs if x != a])
    return g


def q_lienke(lo, hi):
    def g():
        n = rnd(lo, hi)
        if R.random() < .5:
            return inp('so', f'Số liền sau của số {fmt(n)} là:', n + 1, explain=f'{fmt(n)} + 1 = {fmt(n+1)}')
        return inp('so', f'Số liền trước của số {fmt(n)} là:', n - 1, explain=f'{fmt(n)} − 1 = {fmt(n-1)}')
    return g


def roundto(n, p):
    return (n + p // 2) // p * p


HANG = {10: 'chục', 100: 'trăm', 1000: 'nghìn', 10000: 'chục nghìn', 100000: 'trăm nghìn', 1000000: 'triệu'}


def q_lamtron(ps, lo, hi):
    def g():
        p = pick(ps); n = rnd(lo, hi)
        if n % p == 0:
            return None
        a = roundto(n, p)
        lower = n // p * p
        wrong = [lower if a != lower else lower + p, a + p if a + p != (lower + p) else a - p]
        wrong = [w for w in wrong if w != a and w >= 0]
        dnext = HANG.get(p // 10, 'đơn vị') if p > 10 else 'đơn vị'
        return mc('so', f'Làm tròn số {fmt(n)} đến hàng {HANG[p]} ta được số nào?', fmt(a), [fmt(w) for w in wrong],
                  explain=f'Xét chữ số hàng {dnext}: bé hơn 5 thì làm tròn xuống, từ 5 trở lên thì làm tròn lên. Kết quả: {fmt(a)}.')
    return g


def q_congtru(lo, hi, vert=.35):
    def g():
        if R.random() < .5:
            a = rnd(lo, hi); b = rnd(lo // 2 if lo > 10 else 1, hi - a if hi - a > lo // 2 else lo)
            if a + b > hi * 1.2 or b <= 0:
                return None
            v = a + b; op = '+'
        else:
            a = rnd(lo, hi); b = rnd(max(1, lo // 3), a - 1); v = a - b; op = '−'
        if R.random() < vert:
            return inp('congtru', 'Đặt tính rồi tính:', v, visual=vcalc(a, b, op), explain=f'{fmt(a)} {op} {fmt(b)} = {fmt(v)}')
        return inp('congtru', 'Tính:', v, **BIG(f'{fmt(a)} {op} {fmt(b)} = ?'), explain=f'{fmt(a)} {op} {fmt(b)} = {fmt(v)}')
    return g


def q_nhanchia1(lo, hi):
    """Nhân, chia số nhiều chữ số với số có một chữ số (chia hết)."""
    def g():
        k = rnd(2, 9)
        if R.random() < .5:
            a = rnd(lo, hi // k); v = a * k
            if R.random() < .35:
                return inp('nhanchia', 'Đặt tính rồi tính:', v, visual=vcalc(a, k, '×'), explain=f'{fmt(a)} × {k} = {fmt(v)}')
            return inp('nhanchia', 'Tính:', v, **BIG(f'{fmt(a)} × {k} = ?'), explain=f'{fmt(a)} × {k} = {fmt(v)}')
        t = rnd(lo, hi // k); a = t * k
        return inp('nhanchia', 'Tính:', t, **BIG(f'{fmt(a)} : {k} = ?'), explain=f'{fmt(a)} : {k} = {fmt(t)} (vì {fmt(t)} × {k} = {fmt(a)})')
    return g


def q_bieuthuc(level=1):
    def g():
        r = rnd(0, 3)
        if r == 0:
            a = rnd(2000, 9000); b = rnd(2, 9); c = rnd(100, 900)
            v = a + b * c
            return inp('congtru', 'Tính giá trị của biểu thức:', v, **BIG(f'{fmt(a)} + {b} × {c} = ?'),
                       explain=f'Nhân trước, cộng sau: {b} × {c} = {b*c}; {fmt(a)} + {b*c} = {fmt(v)}.')
        if r == 1:
            k = rnd(2, 9); t = rnd(100, 2000); a = k * t; c = rnd(1, 900)
            if t <= c:
                return None
            v = a // k - c
            return inp('congtru', 'Tính giá trị của biểu thức:', v, **BIG(f'{fmt(a)} : {k} − {c} = ?'),
                       explain=f'Chia trước, trừ sau: {fmt(a)} : {k} = {fmt(t)}; {fmt(t)} − {c} = {fmt(v)}.')
        if r == 2:
            a = rnd(1000, 9000); b = rnd(100, 999); k = rnd(2, 8)
            v = (a + b) * k
            if v > 99999:
                return None
            return inp('congtru', 'Tính giá trị của biểu thức:', v, **BIG(f'({fmt(a)} + {b}) × {k} = ?'),
                       explain=f'Tính trong ngoặc trước: {fmt(a)} + {b} = {fmt(a+b)}; {fmt(a+b)} × {k} = {fmt(v)}.')
        k = rnd(2, 9); t = rnd(1000, 9000); s = t * k; b = rnd(100, s - 100)
        a = s + b
        if a > 99999:
            return None
        return inp('congtru', 'Tính giá trị của biểu thức:', t, **BIG(f'({fmt(a)} − {fmt(b)}) : {k} = ?'),
                   explain=f'Tính trong ngoặc trước: {fmt(a)} − {fmt(b)} = {fmt(s)}; {fmt(s)} : {k} = {fmt(t)}.')
    return g


def q_timx5():
    def g():
        r = rnd(0, 3)
        if r == 0:
            a = rnd(10000, 60000); c = rnd(a + 1000, 99999); x = c - a
            return inp('congtru', 'Tìm số thích hợp thay cho dấu ?:', x, **BIG(f'? + {fmt(a)} = {fmt(c)}'),
                       explain=f'Số hạng chưa biết = tổng − số hạng đã biết: {fmt(c)} − {fmt(a)} = {fmt(x)}.')
        if r == 1:
            b = rnd(1000, 40000); d = rnd(1000, 50000); x = b + d
            return inp('congtru', 'Tìm số thích hợp thay cho dấu ?:', x, **BIG(f'? − {fmt(b)} = {fmt(d)}'),
                       explain=f'Số bị trừ = hiệu + số trừ: {fmt(d)} + {fmt(b)} = {fmt(x)}.')
        if r == 2:
            k = rnd(2, 9); x = rnd(1000, 99999 // k)
            return inp('nhanchia', 'Tìm số thích hợp thay cho dấu ?:', x, **BIG(f'? × {k} = {fmt(x*k)}'),
                       explain=f'Thừa số chưa biết = tích : thừa số đã biết: {fmt(x*k)} : {k} = {fmt(x)}.')
        k = rnd(2, 9); t = rnd(1000, 99999 // k)
        return inp('nhanchia', 'Tìm số thích hợp thay cho dấu ?:', t * k, **BIG(f'? : {k} = {fmt(t)}'),
                   explain=f'Số bị chia = thương × số chia: {fmt(t)} × {k} = {fmt(t*k)}.')
    return g


def q_chanle():
    def g():
        r = R.random()
        if r < .3:
            n = rnd(10, 99999)
            a = 'Số chẵn' if n % 2 == 0 else 'Số lẻ'
            return mc('so', f'Số {fmt(n)} là số chẵn hay số lẻ?', a, [], fixed=['Số chẵn', 'Số lẻ'],
                      explain=f'Chữ số tận cùng là {n%10}. Số có chữ số tận cùng 0, 2, 4, 6, 8 là số chẵn; 1, 3, 5, 7, 9 là số lẻ.')
        if r < .55:
            even = R.random() < .5
            base = [rnd(100, 9999) for _ in range(6)]
            good = [x for x in base if x % 2 == (0 if even else 1)]
            bad = [x for x in base if x % 2 != (0 if even else 1)]
            if not good or len(bad) < 2:
                return None
            return mc('so', f'Số nào là số {"chẵn" if even else "lẻ"}?', fmt(good[0]), [fmt(x) for x in bad[:2]])
        if r < .75:
            a = rnd(1, 60) * 2; b = a + pick([10, 20, 30, 40, 50]); even = R.random() < .5
            lo, hi = (a, b) if even else (a + 1, b - 1)
            cnt = (hi - lo) // 2 + 1
            return inp('so', f'Từ {a} đến {b} có bao nhiêu số {"chẵn" if even else "lẻ"}?', cnt,
                       explain=f'Các số {"chẵn" if even else "lẻ"} từ {lo} đến {hi}, hai số liền nhau hơn kém 2 đơn vị: ({hi} − {lo}) : 2 + 1 = {cnt}.')
        FACTS = [('Số chẵn lớn nhất có ba chữ số là số nào?', 998), ('Số lẻ bé nhất có ba chữ số là số nào?', 101),
                 ('Số chẵn bé nhất có bốn chữ số là số nào?', 1000), ('Số lẻ lớn nhất có bốn chữ số là số nào?', 9999),
                 ('Số chẵn lớn nhất có năm chữ số là số nào?', 99998), ('Số lẻ bé nhất có năm chữ số là số nào?', 10001),
                 ('Số chẵn lớn nhất có hai chữ số khác nhau là số nào?', 98), ('Số lẻ lớn nhất có hai chữ số khác nhau là số nào?', 97),
                 ('Số lẻ bé nhất có ba chữ số khác nhau là số nào?', 103), ('Số chẵn bé nhất có ba chữ số khác nhau là số nào?', 102)]
        t, a = pick(FACTS)
        return inp('so', t, a)
    return g


def q_chanle_the():
    def g():
        ds = R.sample(range(0, 10), 3)
        if 0 in ds and ds.count(0) and all(d == 0 for d in ds[1:]):
            return None
        even = R.random() < .5
        from itertools import permutations
        nums = sorted({int(''.join(map(str, p))) for p in permutations(ds) if p[0] != 0 and p[-1] % 2 == (0 if even else 1)})
        if not nums:
            return None
        big = R.random() < .5
        v = nums[-1] if big else nums[0]
        return inp('so', f'Với ba thẻ số {", ".join(map(str, ds))} (mỗi thẻ dùng một lần), số {"chẵn" if even else "lẻ"} {"lớn" if big else "bé"} nhất có ba chữ số lập được là số nào?',
                   v, visual=cards(ds), explain=f'Chữ số hàng đơn vị phải là chữ số {"chẵn" if even else "lẻ"}. Số cần tìm là {v}.')
    return g


def q_bieuthucchu():
    def g():
        r = rnd(0, 4)
        if r == 0:
            a = rnd(5, 60)
            return inp('hinhhoc', f'Chu vi P của hình vuông cạnh a được tính theo công thức P = a × 4. Tính P với a = {a} cm.', a * 4, unit='cm',
                       explain=f'P = {a} × 4 = {a*4} (cm).')
        if r == 1:
            a, b = rnd(10, 60), rnd(5, 40)
            if a <= b:
                return None
            return inp('hinhhoc', f'Chu vi P của hình chữ nhật được tính theo công thức P = (a + b) × 2. Tính P với a = {a} cm, b = {b} cm.', (a + b) * 2, unit='cm',
                       explain=f'P = ({a} + {b}) × 2 = {a+b} × 2 = {(a+b)*2} (cm).')
        if r == 2:
            a = rnd(100, 900); m = rnd(2, 9); k = rnd(2, 9)
            return inp('congtru', f'Tính giá trị của biểu thức {a} + m × {k} với m = {m}.', a + m * k, **BIG(f'{a} + m × {k}'),
                       explain=f'Thay m = {m}: {a} + {m} × {k} = {a} + {m*k} = {a+m*k}.')
        if r == 3:
            a = rnd(20, 90); b = rnd(2, 19); c = rnd(2, 9)
            return inp('congtru', f'Tính giá trị của biểu thức (a − b) × c với a = {a}, b = {b}, c = {c}.', (a - b) * c, **BIG('(a − b) × c'),
                       explain=f'({a} − {b}) × {c} = {a-b} × {c} = {(a-b)*c}.')
        a = rnd(2, 9); b = rnd(2, 9); c = rnd(10, 99)
        ans = a * b + c
        wrong = [a * (b + c), (a + b) * c, a + b + c]
        return mc('congtru', f'Với a = {a}, b = {b}, c = {c}, giá trị của biểu thức a × b + c là:', ans, [w for w in wrong if w != ans][:2],
                  explain=f'{a} × {b} + {c} = {a*b} + {c} = {ans}.')
    return g


def q_3buoc():
    def g():
        r = rnd(0, 5); nm = pick(NAMES)
        if r == 0:
            a = rnd(1200, 3000); d = rnd(100, 500); b = a + d; c = rnd(500, a - 100)
            v = a + b - c
            return inp('giaitoan', f'Kho thứ nhất có {fmt(a)} kg gạo, kho thứ hai có nhiều hơn kho thứ nhất {d} kg gạo. Người ta đã chuyển đi {fmt(c)} kg gạo từ hai kho. Hỏi hai kho còn lại bao nhiêu ki-lô-gam gạo?',
                       v, unit='kg', icon='🌾', explain=sol([f'Kho thứ hai có: {fmt(a)} + {d} = {fmt(b)} (kg)', f'Hai kho có: {fmt(a)} + {fmt(b)} = {fmt(a+b)} (kg)', f'Còn lại: {fmt(a+b)} − {fmt(c)} = {fmt(v)} (kg)'], v, 'kg'))
        if r == 1:
            p = rnd(3, 9) * 1000; k = rnd(2, 5); q = rnd(4, 9) * 1000; money = pick([50000, 100000])
            v = money - p * k - q
            if v <= 0:
                return None
            return inp('giaitoan', f'{nm} có {fmt(money)} đồng. {nm} mua {k} quyển vở, mỗi quyển giá {fmt(p)} đồng và một hộp bút giá {fmt(q)} đồng. Hỏi {nm} còn lại bao nhiêu tiền?',
                       v, unit='đồng', icon='💰', explain=sol([f'Mua vở hết: {fmt(p)} × {k} = {fmt(p*k)} (đồng)', f'Mua vở và bút hết: {fmt(p*k)} + {fmt(q)} = {fmt(p*k+q)} (đồng)', f'Còn lại: {fmt(money)} − {fmt(p*k+q)} = {fmt(v)} (đồng)'], v, 'đồng'))
        if r == 2:
            rows = rnd(5, 12); per = rnd(8, 20); ban = rnd(20, rows * per - 20); k = rnd(2, 5)
            left = rows * per - ban
            if left % k:
                return None
            v = left // k
            return inp('giaitoan', f'Vườn có {rows} hàng cây, mỗi hàng {per} cây. Người ta đã bán {ban} cây, số cây còn lại chia đều cho {k} tổ chăm sóc. Hỏi mỗi tổ chăm sóc bao nhiêu cây?',
                       v, unit='cây', icon='🌳', explain=sol([f'Vườn có: {per} × {rows} = {rows*per} (cây)', f'Còn lại: {rows*per} − {ban} = {left} (cây)', f'Mỗi tổ: {left} : {k} = {v} (cây)'], v, 'cây'))
        if r == 3:
            a = rnd(120, 400); k = rnd(2, 4); b = a * k; c = rnd(50, 200); d = b - c
            v = a + b + d
            return inp('giaitoan', f'Ngày thứ nhất cửa hàng bán được {a} m vải, ngày thứ hai bán được gấp {k} lần ngày thứ nhất, ngày thứ ba bán ít hơn ngày thứ hai {c} m. Hỏi cả ba ngày bán được bao nhiêu mét vải?',
                       v, unit='m', icon='🧵', explain=sol([f'Ngày thứ hai: {a} × {k} = {b} (m)', f'Ngày thứ ba: {b} − {c} = {d} (m)', f'Cả ba ngày: {a} + {b} + {d} = {v} (m)'], v, 'm'))
        if r == 4:
            box = rnd(4, 9); per = rnd(12, 30); loose = rnd(10, 40); k = pick([2, 3, 4, 5])
            tot = box * per + loose
            if tot % k:
                return None
            v = tot // k
            return inp('giaitoan', f'Có {box} hộp bút, mỗi hộp {per} cái và {loose} cái bút rời. Số bút đó chia đều cho {k} lớp. Hỏi mỗi lớp được bao nhiêu cái bút?',
                       v, unit='cái', icon='🖊️', explain=sol([f'Số bút trong hộp: {per} × {box} = {box*per} (cái)', f'Tất cả có: {box*per} + {loose} = {tot} (cái)', f'Mỗi lớp: {tot} : {k} = {v} (cái)'], v, 'cái'))
        a = rnd(25, 45); b = rnd(20, 40); lop = rnd(3, 6); tru = rnd(5, 20)
        v = (a + b) * lop - tru
        return inp('giaitoan', f'Mỗi lớp khối Bốn có {a} bạn nam và {b} bạn nữ. Khối Bốn có {lop} lớp như vậy, hôm nay có {tru} bạn nghỉ học. Hỏi hôm nay khối Bốn có bao nhiêu bạn đi học?',
                   v, unit='bạn', icon='🏫', explain=sol([f'Mỗi lớp có: {a} + {b} = {a+b} (bạn)', f'Khối Bốn có: {a+b} × {lop} = {(a+b)*lop} (bạn)', f'Đi học: {(a+b)*lop} − {tru} = {v} (bạn)'], v, 'bạn'))
    return g


# ================= CHẶNG 2: GÓC; SỐ CÓ NHIỀU CHỮ SỐ =================
def goc_name(d):
    return 'Góc vuông' if d == 90 else 'Góc bẹt' if d == 180 else 'Góc nhọn' if d < 90 else 'Góc tù'


GOC_FIX = ['Góc nhọn', 'Góc vuông', 'Góc tù', 'Góc bẹt']


def q_goc():
    def g():
        r = R.random()
        if r < .45:
            d = pick([30, 40, 45, 50, 60, 70, 90, 90, 110, 120, 130, 135, 150, 180, 180])
            show = R.random() < .5
            return mc('hinhhoc', 'Góc đỉnh O dưới đây là góc gì?', goc_name(d), [], fixed=GOC_FIX,
                      visual=angle_svg(d, f'{d}°' if show else None),
                      explain='Góc nhọn bé hơn góc vuông; góc tù lớn hơn góc vuông nhưng bé hơn góc bẹt; góc vuông bằng 90°, góc bẹt bằng 180°.')
        if r < .7:
            d = rnd(1, 179)
            if d == 90:
                return None
            return mc('hinhhoc', f'Góc có số đo {d}° là góc gì?', goc_name(d), [], fixed=GOC_FIX,
                      explain='Góc nhọn bé hơn 90°; góc tù lớn hơn 90° và bé hơn 180°.')
        if r < .85:
            h = pick([3, 9, 6, 1, 2, 4, 5, 7, 8, 10, 11])
            d = min(h, 12 - h) * 30
            return mc('hinhhoc', f'Lúc {h} giờ, kim giờ và kim phút tạo thành góc gì?', goc_name(d), [], fixed=GOC_FIX, clock=[h, 0],
                      explain=f'Mỗi khoảng giữa hai số liền nhau trên mặt đồng hồ ứng với 30°. Lúc {h} giờ, hai kim tạo góc {d}°.')
        FACTS = [('Góc vuông có số đo bằng bao nhiêu độ?', 90), ('Góc bẹt có số đo bằng bao nhiêu độ?', 180),
                 ('Góc bẹt bằng mấy góc vuông?', 2), ('Lúc 6 giờ, kim giờ và kim phút tạo thành góc bao nhiêu độ?', 180),
                 ('Lúc 3 giờ, kim giờ và kim phút tạo thành góc bao nhiêu độ?', 90), ('Lúc 2 giờ, kim giờ và kim phút tạo thành góc bao nhiêu độ?', 60),
                 ('Lúc 4 giờ, kim giờ và kim phút tạo thành góc bao nhiêu độ?', 120), ('Lúc 1 giờ, kim giờ và kim phút tạo thành góc bao nhiêu độ?', 30)]
        t, a = pick(FACTS)
        return inp('hinhhoc', t, a, unit='độ' if a != 2 else 'góc vuông')
    return g


def q_demgoc():
    def g():
        k = pick(['vuông', 'chữ nhật', 'tam giác', 'thang', 'bình hành'])
        ans = {'vuông': (4, 0, 0), 'chữ nhật': (4, 0, 0), 'tam giác': (0, 3, 0), 'thang': (0, 2, 2), 'bình hành': (0, 2, 2)}[k]
        ask = pick([0, 1, 2]) if k in ('thang', 'bình hành') else (0 if k in ('vuông', 'chữ nhật') else 1)
        nm = ['góc vuông', 'góc nhọn', 'góc tù'][ask]
        return inp('hinhhoc', f'Hình {k} dưới đây có mấy {nm}?', ans[ask], unit='góc', visual=shape_svg(k))
    return g


def q_so6():
    def g():
        n = rnd(100001, 999999)
        if n % 1000 == 0:
            return None
        s = str(n); c = [int(s[0] + s[2] + s[1] + s[3:]) if s[1] != s[2] else None, n + 100000 if n < 900000 else n - 100000]
        c = [x for x in c if x and 100000 <= x <= 999999]
        r = R.random()
        if r < .4:
            return mc('so', f'Số “{readNum(n)}” viết là:', fmt(n), [fmt(x) for x in near(n, 100000, 999999, 2, c)])
        if r < .75:
            return mc('so', f'Số {fmt(n)} đọc là:', readNum(n), [readNum(x) for x in near(n, 100000, 999999, 2, c)])
        d = [int(x) for x in s]
        names = ['trăm nghìn', 'chục nghìn', 'nghìn', 'trăm', 'chục', 'đơn vị']
        desc = ', '.join(f'{d[i]} {names[i]}' for i in range(6) if d[i])
        return inp('so', f'Số gồm {desc} là số nào?', n, explain=f'Viết lần lượt các chữ số từ hàng trăm nghìn: {fmt(n)}.')
    return g


def q_trieu_facts():
    FACTS = [('10 trăm nghìn bằng bao nhiêu?', 1000000), ('Số một triệu có bao nhiêu chữ số 0?', 6),
             ('Số bé nhất có sáu chữ số là số nào?', 100000), ('Số lớn nhất có sáu chữ số là số nào?', 999999),
             ('Số liền sau của 999 999 là số nào?', 1000000), ('1 000 000 gồm mấy trăm nghìn?', 10),
             ('Số tròn trăm nghìn lớn nhất có sáu chữ số là số nào?', 900000), ('Số chẵn lớn nhất có sáu chữ số là số nào?', 999998),
             ('10 triệu viết là số có bao nhiêu chữ số?', 8), ('Số bé nhất có bảy chữ số là số nào?', 1000000),
             ('Số lớn nhất có sáu chữ số khác nhau là số nào?', 987654), ('Số bé nhất có sáu chữ số khác nhau là số nào?', 102345)]
    def g():
        t, a = pick(FACTS)
        return inp('so', t, a)
    return g


def q_dayso(lo, hi):
    def g():
        st = pick([1000, 10000, 100000, 5000, 2000, 100, 50000]); up = R.random() < .6
        s = rnd(lo // st, (hi - 4 * st) // st) * st + (rnd(0, 9) * (st // 10 if st >= 100 else 0) if R.random() < .3 else 0)
        seq = [s + st * i for i in range(5)]
        if not up:
            seq = seq[::-1]
        if min(seq) < 0 or max(seq) > hi:
            return None
        h = rnd(1, 4)
        show = [fmt(x) if i != h else '?' for i, x in enumerate(seq)]
        return inp('so', 'Tìm số thích hợp thay cho dấu ? trong dãy số:', seq[h], big=', '.join(show), bigSmall=True,
                   explain=f'Mỗi số {"hơn" if up else "kém"} số liền trước {fmt(st)} đơn vị.')
    return g


LOP = [('đơn vị', ['đơn vị', 'chục', 'trăm']), ('nghìn', ['nghìn', 'chục nghìn', 'trăm nghìn']), ('triệu', ['triệu', 'chục triệu', 'trăm triệu'])]
HANGS = ['đơn vị', 'chục', 'trăm', 'nghìn', 'chục nghìn', 'trăm nghìn', 'triệu', 'chục triệu', 'trăm triệu']


def q_hanglop(maxd=6):
    def g():
        L = rnd(max(5, maxd - 2), maxd)
        n = rnd(10 ** (L - 1), 10 ** L - 1); s = str(n)
        r = R.random()
        i = rnd(0, L - 1); pos = L - 1 - i  # vị trí từ phải
        dgt = s[i]
        if r < .35:
            if s.count(dgt) > 1:
                return None
            lop = LOP[pos // 3][0]
            return mc('so', f'Trong số {fmt(n)}, chữ số {dgt} thuộc lớp nào?', 'Lớp ' + lop,
                      ['Lớp ' + x[0] for x in LOP if x[0] != lop],
                      explain='Lớp đơn vị gồm hàng đơn vị, chục, trăm; lớp nghìn gồm hàng nghìn, chục nghìn, trăm nghìn; lớp triệu gồm hàng triệu, chục triệu, trăm triệu.')
        if r < .65:
            if s.count(dgt) > 1:
                return None
            wr = [HANGS[p] for p in (pos + 1, pos - 1, pos + 3, pos - 3) if 0 <= p < 9]
            return mc('so', f'Chữ số {dgt} trong số {fmt(n)} thuộc hàng nào?', 'Hàng ' + HANGS[pos], ['Hàng ' + x for x in wr[:2]])
        if dgt == '0':
            return None
        val = int(dgt) * 10 ** pos
        return inp('so', f'Giá trị của chữ số {dgt} ở hàng {HANGS[pos]} trong số {fmt(n)} là bao nhiêu?', val,
                   explain=f'Chữ số {dgt} ở hàng {HANGS[pos]} nên có giá trị {fmt(val)}.')
    return g


def q_lopfacts():
    def g():
        L = rnd(7, 9); n = rnd(10 ** (L - 1), 10 ** L - 1)
        k = pick(['nghìn', 'triệu', 'đơn vị'])
        v = {'đơn vị': n % 1000, 'nghìn': n // 1000 % 1000, 'triệu': n // 1000000}[k]
        if v < 10:
            return None
        return inp('so', f'Các chữ số thuộc lớp {k} của số {fmt(n)} tạo thành số nào?', v,
                   explain=f'Tách số thành các lớp, mỗi lớp 3 chữ số từ phải sang trái: {fmt(n)}. Lớp {k} là {v:03d}.' if k != 'triệu' else f'Tách số thành các lớp từ phải sang trái: {fmt(n)}. Lớp triệu là {v}.')
    return g


def q_trieu():
    def g():
        L = rnd(7, 9)
        n = rnd(10 ** (L - 1), 10 ** L - 1)
        if R.random() < .3:
            n = n // 1000 * 1000
        s = str(n)
        c = [n + 10 ** (L - 1) if n + 10 ** (L - 1) < 10 ** L else n - 10 ** (L - 1), n + 1000000, n - 1000]
        c = [x for x in c if 10 ** (L - 1) <= x < 10 ** L]
        r = R.random()
        if r < .45:
            return mc('so', f'Số {fmt(n)} đọc là:', readNum(n), [readNum(x) for x in near(n, 10 ** (L - 1), 10 ** L - 1, 2, c)])
        if r < .8:
            return mc('so', f'Số “{readNum(n)}” viết là:', fmt(n), [fmt(x) for x in near(n, 10 ** (L - 1), 10 ** L - 1, 2, c)])
        a = rnd(1, 9); b = rnd(1, 9); cc = rnd(1, 9)
        v = a * 10 ** 8 + b * 10 ** 6 + cc * 10 ** 3
        return inp('so', f'Số gồm {a} trăm triệu, {b} triệu và {cc} nghìn là số nào?', v, explain=f'Số đó là {fmt(v)}.')
    return g


def q_dstn():
    FACTS = [('Số tự nhiên bé nhất là số nào?', 0), ('Hai số tự nhiên liên tiếp hơn kém nhau mấy đơn vị?', 1),
             ('Hai số chẵn liên tiếp hơn kém nhau mấy đơn vị?', 2), ('Hai số lẻ liên tiếp hơn kém nhau mấy đơn vị?', 2),
             ('Số tự nhiên liền sau số 999 999 là số nào?', 1000000), ('Có bao nhiêu số tự nhiên có một chữ số?', 10),
             ('Có bao nhiêu số tự nhiên có hai chữ số?', 90), ('Có bao nhiêu số tự nhiên có ba chữ số?', 900),
             ('Có bao nhiêu số chẵn có hai chữ số?', 45), ('Có bao nhiêu số lẻ có hai chữ số?', 45)]
    def g():
        r = R.random()
        if r < .45:
            t, a = pick(FACTS)
            return inp('so', t, a)
        if r < .75:
            a = rnd(10, 5000); b = a + rnd(5, 60)
            return inp('so', f'Từ {fmt(a)} đến {fmt(b)} có tất cả bao nhiêu số tự nhiên?', b - a + 1, explain=f'{fmt(b)} − {fmt(a)} + 1 = {b-a+1}.')
        opt_ok = 'Không có số tự nhiên lớn nhất'
        return mc('so', 'Câu nào đúng về dãy số tự nhiên 0, 1, 2, 3, …?', opt_ok, ['Số tự nhiên lớn nhất là 1 000 000', 'Số tự nhiên bé nhất là 1'],
                  explain='Thêm 1 vào bất kì số tự nhiên nào cũng được số tự nhiên liền sau, nên không có số tự nhiên lớn nhất. Số tự nhiên bé nhất là 0.')
    return g


# ================= CHẶNG 3: ĐƠN VỊ ĐO; CỘNG TRỪ =================
def q_yenta():
    def g():
        r = R.random()
        if r < .45:
            c = pick([('yến', 'kg', 10), ('tạ', 'kg', 100), ('tấn', 'kg', 1000), ('tạ', 'yến', 10), ('tấn', 'tạ', 10), ('tấn', 'yến', 100)])
            k = rnd(1, 9) if R.random() < .6 else rnd(10, 50)
            if R.random() < .5:
                return inp('doluong', 'Điền số thích hợp:', k * c[2], **BIG(f'{k} {c[0]} = ? {c[1]}'), explain=f'1 {c[0]} = {c[2]} {c[1]} nên {k} {c[0]} = {k*c[2]} {c[1]}.')
            return inp('doluong', 'Điền số thích hợp:', k, **BIG(f'{fmt(k*c[2])} {c[1]} = ? {c[0]}'), explain=f'1 {c[0]} = {c[2]} {c[1]} nên {fmt(k*c[2])} {c[1]} = {k} {c[0]}.')
        if r < .65:
            a = rnd(1, 9); b = rnd(1, 99); u = pick([('tạ', 100), ('tấn', 1000)])
            if b >= u[1]:
                return None
            return inp('doluong', 'Điền số thích hợp:', a * u[1] + b, **BIG(f'{a} {u[0]} {b} kg = ? kg'), explain=f'{a} {u[0]} = {a*u[1]} kg; {a*u[1]} + {b} = {a*u[1]+b} (kg).')
        if r < .8:
            a = rnd(1, 9); u1 = pick([('tạ', 100), ('tấn', 1000), ('yến', 10)]); kg = a * u1[1] + pick([-u1[1] // 2, u1[1] // 2, 0])
            return mc('doluong', 'Chọn dấu thích hợp điền vào ô trống:', sign(a * u1[1], kg), [], fixed=SIGN_FIX, big=f'{a} {u1[0]} ☐ {fmt(kg)} kg',
                      explain=f'{a} {u1[0]} = {fmt(a*u1[1])} kg.')
        k = rnd(2, 9); t = rnd(12, 60)
        v = k * t
        if R.random() < .5:
            return inp('giaitoan', f'Mỗi bao gạo nặng {t} kg. Hỏi {k} bao gạo như thế nặng bao nhiêu yến?', v // 10 if v % 10 == 0 else None, unit='yến',
                       explain=sol([f'{k} bao nặng: {t} × {k} = {v} (kg)', f'{v} kg = {v//10} yến'], v // 10, 'yến')) if v % 10 == 0 else None
        a = rnd(2, 9); b = rnd(1, a * 10 - 1)
        return inp('giaitoan', f'Một xe tải chở {a} tấn hàng, đã dỡ xuống {b} tạ. Hỏi trên xe còn lại bao nhiêu tạ hàng?', a * 10 - b, unit='tạ',
                   explain=sol([f'{a} tấn = {a*10} tạ', f'Còn lại: {a*10} − {b} = {a*10-b} (tạ)'], a * 10 - b, 'tạ'))
    return g


def q_dientich():
    def g():
        r = R.random()
        CV = [('dm²', 'cm²', 100), ('m²', 'dm²', 100), ('cm²', 'mm²', 100), ('m²', 'cm²', 10000)]
        if r < .5:
            c = pick(CV); k = rnd(1, 9) if R.random() < .6 else rnd(10, 40)
            if R.random() < .5:
                return inp('doluong', 'Điền số thích hợp:', k * c[2], **BIG(f'{k} {c[0]} = ? {c[1]}'), explain=f'1 {c[0]} = {fmt(c[2])} {c[1]} nên {k} {c[0]} = {fmt(k*c[2])} {c[1]}.')
            return inp('doluong', 'Điền số thích hợp:', k, **BIG(f'{fmt(k*c[2])} {c[1]} = ? {c[0]}'), explain=f'1 {c[0]} = {fmt(c[2])} {c[1]}.')
        if r < .65:
            a = rnd(1, 9); b = rnd(1, 99); c = pick(CV[:3])
            return inp('doluong', 'Điền số thích hợp:', a * 100 + b, **BIG(f'{a} {c[0]} {b} {c[1]} = ? {c[1]}'), explain=f'{a} {c[0]} = {a*100} {c[1]}; {a*100} + {b} = {a*100+b}.')
        if r < .85:
            a, b = rnd(3, 12), rnd(2, 9)
            if R.random() < .5:
                return inp('hinhhoc', f'Một tấm bảng hình chữ nhật có chiều dài {a} dm, chiều rộng {b} dm. Diện tích tấm bảng là bao nhiêu đề-xi-mét vuông?', a * b, unit='dm²',
                           explain=f'Diện tích = chiều dài × chiều rộng = {a} × {b} = {a*b} (dm²).')
            s = rnd(2, 12)
            return inp('hinhhoc', f'Một viên gạch hình vuông cạnh {s} dm. Diện tích viên gạch là bao nhiêu đề-xi-mét vuông?', s * s, unit='dm²', explain=f'{s} × {s} = {s*s} (dm²).')
        items = [('Diện tích một con tem', 'cm²'), ('Diện tích lớp học', 'm²'), ('Diện tích mặt bàn học', 'dm²'), ('Diện tích một hạt vừng', 'mm²'), ('Diện tích sân trường', 'm²'), ('Diện tích móng tay', 'mm²')]
        t, u = pick(items)
        return mc('doluong', f'{t} khoảng 50 … Đơn vị thích hợp là:', u, R.sample([x for x in ['mm²', 'cm²', 'dm²', 'm²'] if x != u], 2))
    return g


ROMAN = {15: 'XV', 16: 'XVI', 17: 'XVII', 18: 'XVIII', 19: 'XIX', 20: 'XX', 21: 'XXI', 10: 'X', 11: 'XI', 12: 'XII', 13: 'XIII', 14: 'XIV'}


def q_giaytheki():
    def g():
        r = R.random()
        if r < .35:
            c = pick([('phút', 'giây', 60), ('thế kỉ', 'năm', 100), ('giờ', 'phút', 60)])
            k = rnd(2, 9)
            if R.random() < .5:
                return inp('doluong', 'Điền số thích hợp:', k * c[2], big=f'{k} {c[0]} = ? {c[1]}', explain=f'1 {c[0]} = {c[2]} {c[1]}.')
            return inp('doluong', 'Điền số thích hợp:', k, big=f'{k*c[2]} {c[1]} = ? {c[0]}', explain=f'1 {c[0]} = {c[2]} {c[1]}.')
        if r < .5:
            a = rnd(1, 4); b = rnd(1, 59)
            return inp('doluong', 'Điền số thích hợp:', a * 60 + b, big=f'{a} phút {b} giây = ? giây', explain=f'{a} phút = {a*60} giây; {a*60} + {b} = {a*60+b} (giây).')
        if r < .75:
            y = rnd(1001, 2099)
            if y % 100 == 0:
                return None
            c = (y - 1) // 100 + 1
            ws = [ROMAN.get(c - 1), ROMAN.get(c + 1)]
            return mc('doluong', f'Năm {y} thuộc thế kỉ nào?', 'Thế kỉ ' + ROMAN[c], ['Thế kỉ ' + w for w in ws if w],
                      explain=f'Từ năm {(c-1)*100+1} đến năm {c*100} là thế kỉ {ROMAN[c]}.')
        if r < .88:
            t1 = rnd(40, 90); t2 = rnd(40, 90)
            if t1 == t2:
                return None
            a, b = pick(NAMES), pick(NAMES)
            if a == b:
                return None
            fast = a if t1 < t2 else b
            return mc('doluong', f'Trong cuộc thi chạy, {a} chạy hết {t1} giây, {b} chạy hết {t2} giây. Ai chạy nhanh hơn?', fast, [a if fast == b else b],
                      explain='Chạy hết ít thời gian hơn thì chạy nhanh hơn.')
        y = rnd(2027, 2040); born = rnd(1990, 2016)
        return inp('giaitoan', f'Bạn {pick(NAMES)} sinh năm {born}. Đến năm {y}, bạn ấy bao nhiêu tuổi?', y - born, unit='tuổi', explain=f'{y} − {born} = {y-born} (tuổi).')
    return g


def q_giaohoan_cong():
    def g():
        r = rnd(0, 3)
        if r == 0:
            a, b = rnd(1000, 99999), rnd(1000, 99999)
            return inp('congtru', 'Tìm số thích hợp thay cho dấu ?:', a, **BIG(f'{fmt(a)} + {fmt(b)} = {fmt(b)} + ?'),
                       explain='Khi đổi chỗ các số hạng trong một tổng thì tổng không thay đổi.')
        if r == 1:
            x = rnd(11, 99) * 10 + pick([0, 5]); y = 1000 - x if x < 1000 else None
            if not y or y <= 0:
                return None
            b = rnd(100, 999)
            v = x + b + y
            return inp('congtru', 'Tính bằng cách thuận tiện:', v, **BIG(f'{x} + {b} + {y} = ?'),
                       explain=f'({x} + {y}) + {b} = 1000 + {b} = {v}.')
        if r == 2:
            a, b, c = rnd(100, 900), rnd(100, 900), rnd(100, 900)
            return inp('congtru', 'Tìm số thích hợp thay cho dấu ?:', c, **BIG(f'({a} + {b}) + {c} = {a} + ({b} + ?)'),
                       explain='Tính chất kết hợp: (a + b) + c = a + (b + c).')
        a = rnd(10, 99) * 100 + pick([25, 75, 50]); b = (100 - a % 100) + rnd(1, 9) * 100
        c = rnd(1000, 5000)
        v = a + c + b
        return inp('congtru', 'Tính bằng cách thuận tiện:', v, **BIG(f'{fmt(a)} + {fmt(c)} + {b} = ?'),
                   explain=f'({fmt(a)} + {b}) + {fmt(c)} = {fmt(a+b)} + {fmt(c)} = {fmt(v)}.')
    return g


def q_tonghieu():
    def g():
        r = rnd(0, 4)
        big = rnd(20, 900); small = rnd(5, big - 1)
        S, D = big + small, big - small
        if r == 0:
            if R.random() < .5:
                return inp('giaitoan', f'Tổng của hai số là {S}, hiệu của hai số là {D}. Tìm số lớn.', big,
                           explain=sol([f'Số lớn là: ({S} + {D}) : 2 = {big}'], big))
            return inp('giaitoan', f'Tổng của hai số là {S}, hiệu của hai số là {D}. Tìm số bé.', small,
                       explain=sol([f'Số bé là: ({S} − {D}) : 2 = {small}'], small))
        if r == 1:
            a = rnd(15, 40); b = rnd(1, a - 1); S, D = a + b, a - b
            return inp('giaitoan', f'Tổng số tuổi của bố và con là {S} tuổi. Bố hơn con {D} tuổi. Hỏi con bao nhiêu tuổi?', b, unit='tuổi', icon='👨‍👦',
                       explain=sol([f'Tuổi con là: ({S} − {D}) : 2 = {b} (tuổi)'], b, 'tuổi')) if a + b <= 90 and a - b >= 20 else None
        if r == 2:
            nam = rnd(12, 22); nu = nam + pick([-4, -2, 2, 4])
            S = nam + nu; D = abs(nam - nu)
            more = 'nam' if nam > nu else 'nữ'
            ask = pick(['nam', 'nữ'])
            v = nam if ask == 'nam' else nu
            return inp('giaitoan', f'Lớp 4A có {S} học sinh, số học sinh {more} nhiều hơn số học sinh {"nữ" if more == "nam" else "nam"} {D} bạn. Hỏi lớp 4A có bao nhiêu học sinh {ask}?', v, unit='bạn', icon='🏫',
                       explain=sol([f'Số học sinh {more}: ({S} + {D}) : 2 = {max(nam,nu)} (bạn)', f'Số học sinh {"nữ" if more=="nam" else "nam"}: {S} − {max(nam,nu)} = {min(nam,nu)} (bạn)'], v, 'bạn'))
        if r == 3:
            dai = rnd(12, 60); rong = rnd(5, dai - 2); P = (dai + rong) * 2; D = dai - rong
            if R.random() < .5:
                return inp('giaitoan', f'Hình chữ nhật có chu vi {P} cm, chiều dài hơn chiều rộng {D} cm. Tính chiều dài.', dai, unit='cm', icon='▭',
                           explain=sol([f'Nửa chu vi: {P} : 2 = {dai+rong} (cm)', f'Chiều dài: ({dai+rong} + {D}) : 2 = {dai} (cm)'], dai, 'cm'))
            return inp('giaitoan', f'Hình chữ nhật có chu vi {P} cm, chiều dài hơn chiều rộng {D} cm. Tính diện tích hình chữ nhật.', dai * rong, unit='cm²', icon='▭',
                       explain=sol([f'Nửa chu vi: {P} : 2 = {dai+rong} (cm)', f'Chiều dài: ({dai+rong} + {D}) : 2 = {dai} (cm)', f'Chiều rộng: {dai} − {D} = {rong} (cm)', f'Diện tích: {dai} × {rong} = {dai*rong} (cm²)'], dai * rong, 'cm²'))
        a = rnd(200, 800); b = rnd(100, a - 10); S, D = a + b, a - b
        return inp('giaitoan', f'Hai thùng có tất cả {S} l dầu. Thùng thứ nhất nhiều hơn thùng thứ hai {D} l. Hỏi thùng thứ hai có bao nhiêu lít dầu?', b, unit='l', icon='🛢️',
                   explain=sol([f'Thùng thứ hai: ({S} − {D}) : 2 = {b} (l)'], b, 'l'))
    return g


# ================= CHẶNG 4: VUÔNG GÓC, SONG SONG; HÌNH =================
def q_vuonggoc():
    def g():
        r = R.random()
        if r < .45:
            k = pick(['vg', 'vg', 'cat', 'ss'])
            a = 'Vuông góc' if k == 'vg' else 'Không vuông góc'
            return mc('hinhhoc', 'Hai đường thẳng dưới đây có vuông góc với nhau không?', a, [], fixed=['Vuông góc', 'Không vuông góc'], visual=lines_svg(k),
                      explain='Hai đường thẳng vuông góc tạo thành 4 góc vuông có chung đỉnh.')
        side = pick(['AB', 'BC', 'CD', 'DA'])
        perp = {'AB': ['AD', 'BC'], 'BC': ['AB', 'CD'], 'CD': ['BC', 'AD'], 'DA': ['AB', 'CD']}[side]
        par = {'AB': 'CD', 'BC': 'AD', 'CD': 'AB', 'DA': 'BC'}[side]
        ans = pick(perp)
        return mc('hinhhoc', f'Trong hình chữ nhật ABCD, cạnh {side} vuông góc với cạnh nào?', 'Cạnh ' + ans, ['Cạnh ' + par],
                  visual=rect_svg(), explain=f'Hình chữ nhật có 4 góc vuông nên {side} vuông góc với {perp[0]} và {perp[1]}.')
    return g


def q_songsong():
    def g():
        r = R.random()
        if r < .45:
            k = pick(['ss', 'ss', 'lech', 'vg'])
            a = 'Song song' if k == 'ss' else 'Không song song'
            return mc('hinhhoc', 'Hai đường thẳng dưới đây có song song với nhau không?', a, [], fixed=['Song song', 'Không song song'], visual=lines_svg(k),
                      explain='Hai đường thẳng song song không bao giờ cắt nhau.')
        if r < .75:
            side = pick(['AB', 'BC', 'CD', 'AD'])
            par = {'AB': 'CD', 'BC': 'AD', 'CD': 'AB', 'AD': 'BC'}[side]
            perp = {'AB': 'BC', 'BC': 'CD', 'CD': 'AD', 'AD': 'AB'}[side]
            return mc('hinhhoc', f'Trong hình chữ nhật ABCD, cạnh {side} song song với cạnh nào?', 'Cạnh ' + par, ['Cạnh ' + perp], visual=rect_svg(),
                      explain='Trong hình chữ nhật, hai cạnh đối diện song song với nhau.')
        k = pick(['vuông', 'chữ nhật', 'bình hành', 'thoi', 'thang'])
        n = {'vuông': 2, 'chữ nhật': 2, 'bình hành': 2, 'thoi': 2, 'thang': 1}[k]
        return inp('hinhhoc', f'Hình {k} dưới đây có mấy cặp cạnh song song?', n, unit='cặp', visual=shape_svg(k),
                   explain='Hình thang chỉ có một cặp cạnh đối diện song song.' if k == 'thang' else f'Hình {k} có hai cặp cạnh đối diện song song.')
    return g


def q_binhhanh():
    def g():
        r = R.random()
        if r < .35:
            k = pick(['bình hành', 'thoi', 'bình hành', 'thoi', 'thang', 'chữ nhật'])
            return mc('hinhhoc', 'Hình dưới đây là hình gì?', 'Hình ' + k, ['Hình ' + x for x in R.sample([y for y in ['bình hành', 'thoi', 'thang', 'chữ nhật', 'tam giác'] if y != k], 2)], visual=shape_svg(k))
        if r < .6:
            FACTS = [('Hình bình hành có hai cặp cạnh đối diện như thế nào?', 'Song song và bằng nhau', ['Vuông góc với nhau', 'Không bằng nhau']),
                     ('Hình thoi có bốn cạnh như thế nào?', 'Bằng nhau', ['Đều vuông góc', 'Dài ngắn khác nhau']),
                     ('Hai đường chéo của hình thoi như thế nào với nhau?', 'Vuông góc với nhau', ['Song song với nhau', 'Không cắt nhau']),
                     ('Hình nào có bốn cạnh bằng nhau nhưng không có góc vuông?', 'Hình thoi', ['Hình vuông', 'Hình chữ nhật']),
                     ('Hình bình hành có mấy cặp cạnh song song?', '2 cặp', ['1 cặp', '4 cặp']),
                     ('Hình nào dưới đây có hai cặp cạnh đối diện song song?', 'Hình bình hành', ['Hình thang', 'Hình tam giác'])]
            t, a, w = pick(FACTS)
            return mc('hinhhoc', t, a, w)
        if R.random() < .5:
            a, b = rnd(5, 30), rnd(3, 20)
            if a == b:
                return None
            return inp('hinhhoc', f'Hình bình hành có độ dài hai cạnh liền nhau là {a} cm và {b} cm. Tính chu vi hình bình hành.', (a + b) * 2, unit='cm',
                       explain=f'Chu vi = ({a} + {b}) × 2 = {(a+b)*2} (cm).')
        a = rnd(4, 30)
        if R.random() < .5:
            return inp('hinhhoc', f'Hình thoi có cạnh dài {a} cm. Tính chu vi hình thoi.', a * 4, unit='cm', explain=f'Chu vi = {a} × 4 = {a*4} (cm).')
        return inp('hinhhoc', f'Hình thoi có chu vi {a*4} cm. Tính độ dài một cạnh.', a, unit='cm', explain=f'{a*4} : 4 = {a} (cm).')
    return g


def q_demhinh():
    def g():
        # một hình chữ nhật được chia bởi k đoạn thẳng dọc -> số hình chữ nhật = (k+2)(k+1)/2
        k = rnd(1, 3)
        n = (k + 2) * (k + 1) // 2
        W = 260; xs = [20 + W * i // (k + 1) for i in range(1, k + 1)]
        s = '<svg class="geo" viewBox="0 0 300 110" style="max-width:300px" aria-hidden="true"><rect x="20" y="15" width="260" height="80" fill="#DBEAFE" stroke="currentColor" stroke-width="3"/>'
        s += ''.join(f'<line x1="{x}" y1="15" x2="{x}" y2="95" stroke="currentColor" stroke-width="3"/>' for x in xs) + '</svg>'
        return inp('hinhhoc', 'Hình dưới đây có tất cả bao nhiêu hình chữ nhật?', n, unit='hình', visual=s,
                   explain=f'Đếm các hình đơn, hình ghép 2 ô, 3 ô…: {" + ".join(str(k+1-i+0) for i in range(k+1))} = {n}.')
    return g


LBLS = [('A', 'B', 'C', 'D'), ('M', 'N', 'P', 'Q'), ('E', 'G', 'H', 'K'), ('P', 'Q', 'R', 'S')]


def q_vg_hinh():
    """Cạnh vuông góc / song song trong hình thang vuông, tam giác vuông, hình vuông (đỉnh đặt tên khác nhau)."""
    def g():
        L = pick(LBLS); a, b, c, d = L
        r = R.random()
        if r < .35:
            # hình thang vuông: góc a và d vuông; ab // dc
            pts = [(50, 25), (190, 25), (260, 140), (50, 140)]
            vis = poly_svg(pts, L)
            if R.random() < .5:
                return mc('hinhhoc', f'Hình thang {a}{b}{c}{d} có góc {a} và góc {d} là góc vuông. Cạnh {a}{d} vuông góc với những cạnh nào?',
                          f'{a}{b} và {d}{c}', [f'{b}{c} và {d}{c}', f'{a}{b} và {b}{c}'], visual=vis, explain=f'Góc {a} vuông nên {a}{d} ⊥ {a}{b}; góc {d} vuông nên {a}{d} ⊥ {d}{c}.')
            return mc('hinhhoc', f'Trong hình thang vuông {a}{b}{c}{d}, cạnh {a}{b} song song với cạnh nào?', f'{d}{c}', [f'{a}{d}', f'{b}{c}'], visual=vis,
                      explain=f'Hình thang {a}{b}{c}{d} có một cặp cạnh đối diện song song: {a}{b} và {d}{c}.')
        if r < .6:
            pts = [(60, 20), (60, 140), (260, 140)]
            vis = poly_svg(pts, (a, b, c)) .replace('</svg>', '<path d="M60 122 L78 122 L78 140" fill="none" stroke="#E11D48" stroke-width="2.5"/></svg>')
            return mc('hinhhoc', f'Tam giác {a}{b}{c} có góc vuông ở đỉnh {b}. Cạnh {b}{a} vuông góc với cạnh nào?', f'{b}{c}', [f'{a}{c}', f'{a}{b}'][:1],
                      visual=vis, explain=f'Góc {b} vuông nên {b}{a} vuông góc với {b}{c}.')
        if r < .8:
            k = pick(['vuông', 'chữ nhật'])
            n = 4
            return inp('hinhhoc', f'Hình {k} {a}{b}{c}{d} có bao nhiêu cặp cạnh vuông góc với nhau?', n, unit='cặp', visual=poly_svg(SHAPES[k], L, w=300, h=160),
                       explain=f'Mỗi góc vuông cho một cặp cạnh vuông góc: {a}{b} và {b}{c}, {b}{c} và {c}{d}, {c}{d} và {d}{a}, {d}{a} và {a}{b}.')
        F_ = [('Dụng cụ nào dùng để kiểm tra góc vuông?', 'Ê ke', ['Com-pa', 'Bút chì']),
              ('Hai đường thẳng vuông góc tạo thành mấy góc vuông?', '4 góc vuông', ['2 góc vuông', '1 góc vuông']),
              ('Hai đường thẳng song song thì như thế nào?', 'Không bao giờ cắt nhau', ['Cắt nhau tạo 4 góc vuông', 'Cắt nhau tại một điểm']),
              ('Hình nào có bốn góc vuông và bốn cạnh bằng nhau?', 'Hình vuông', ['Hình thoi', 'Hình bình hành']),
              ('Dụng cụ nào dùng để đo góc?', 'Thước đo góc', ['Ê ke', 'Thước dây'])]
        t, ans, w = pick(F_)
        return mc('hinhhoc', t, ans, w)
    return g
