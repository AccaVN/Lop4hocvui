"""Kiểm tra toàn bộ ngân hàng Toán 4: cấu trúc, đáp án, tự tính lại các phép tính."""
import re
from fractions import Fraction as F
from collections import Counter
from m4b import build
bank, meta = build()
assert len(bank) == 8 and all(len(w) == 6 for w in bank)
err = 0
def val(tok):
    tok = tok.replace(' ', '').replace('\u00a0', '')
    if '/' in tok:
        a, b = tok.split('/'); return F(int(a), int(b))
    return F(int(tok))
def ev(expr):
    e = expr.replace('×', '*').replace(' : ', ' / ').replace('−', '-')
    e = re.sub(r'(\d)[ \u00a0](?=\d{3}\b)', r'\1', e)
    e = re.sub(r'(\d+)/(\d+)', r'F(\1,\2)', e)
    return eval(e, {'F': F})
n_checked = 0
for w, W in enumerate(bank):
    for d, L in enumerate(W):
        prompts = Counter(q['prompt'][:25] for q in L)
        for q in L:
            s = str(q)
            if 'None' in s.replace("'None'", '') and "None" in (q.get('prompt', '') + str(q.get('explain', '')) + str(q.get('big', ''))):
                print('NONE', w, d, q['prompt']); err += 1
            if q['type'] == 'mc':
                if q['answer'] not in q['options'] or len(set(q['options'])) != len(q['options']) or len(q['options']) < 2:
                    print('MC', w, d, q); err += 1
            elif q['type'] == 'input':
                if not (0 <= q['answer'] <= 999999999):
                    print('RANGE', w, d, q); err += 1
            big = q.get('big', '')
            # tự tính lại "a op b = ?" và "... = ☐" (phân số)
            m = re.fullmatch(r'([\d /()+×:−\u00a0]+) = (\?|☐)', big or '')
            if m and not re.search(r'[a-z]', big):
                try:
                    v = ev(m.group(1))
                except Exception as e:
                    v = None
                if v is not None:
                    n_checked += 1
                    exp = q['answer'] if q['type'] == 'input' else val(q['answer'].replace(' m²', ''))
                    if F(v) != F(exp):
                        print('CALC', w, d, big, q['answer'], v); err += 1
                    if q['type'] == 'mc':
                        for o in q['options']:
                            if o != q['answer'] and val(o) == F(v):
                                print('DUPVAL', w, d, big, q['options']); err += 1
            # "? op b = c" dạng tìm thành phần
            m = re.fullmatch(r'(.*) = (.*)', big or '')
            if m and '?' in big and q['type'] == 'input' and not re.search(r'[a-zđ²]', big) and big.count('=') == 1 and not big.endswith('= ?'):
                try:
                    l = ev(m.group(1).replace('?', str(q['answer']))); r = ev(m.group(2).replace('?', str(q['answer'])))
                    n_checked += 1
                    if F(l) != F(r):
                        print('EQ', w, d, big, q['answer']); err += 1
                except Exception as e:
                    pass
            # so sánh ☐ với >,<,=
            if q['type'] == 'mc' and q.get('fixed') == ['>', '<', '='] and re.fullmatch(r'[\d /\u00a0]+ ☐ [\d /\u00a0]+', big):
                a, b = big.split(' ☐ ')
                A, B = val(a), val(b)
                exp = '>' if A > B else '<' if A < B else '='
                n_checked += 1
                if exp != q['answer']:
                    print('CMP', w, d, big, q['answer']); err += 1
        print(f'C{w+1}B{d+1} {meta[w]["ls"][d][:38]:40s} {len(L)} câu | dạng: {len(prompts)}')
print('checked calc', n_checked, 'errors', err)
