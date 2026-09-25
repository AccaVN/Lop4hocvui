from common import *
from tv4d import U
CATS = {'dt': 'Danh từ', 'dgt': 'Động từ', 'tt': 'Tính từ'}
TN_T = {'tg': 'Thời gian', 'nc': 'Nơi chốn', 'ng': 'Nguyên nhân', 'md': 'Mục đích', 'pt': 'Phương tiện'}
TN_FIX = ['Thời gian', 'Nơi chốn', 'Nguyên nhân', 'Mục đích', 'Phương tiện']
LV = ['Đọc hiểu', 'Luyện từ, chính tả', 'Luyện câu, dấu câu']


def passage_qs(p):
    PP = {'title': p['title'], 'text': p['text']}
    return [mc('dochieu', q, a, w, passage=PP) for q, a, w in p['qs']]


def word_qs(W):
    out = []; used = set()
    order = shuffle(['dt', 'dgt', 'tt', 'dt', 'dgt', 'tt'])
    for i, k in enumerate(order[:5]):
        others = [c for c in CATS if c != k]
        if i % 2 == 0:
            ans = pick([x for x in W[k] if x not in used]); used.add(ans)
            q = mc('tucau', f'Từ nào là {CATS[k].lower()}?', ans, [pick(W[c]) for c in others], explain=f'“{ans}” là {CATS[k].lower()}.')
        else:
            wd = pick([x for x in W[k] if x not in used]); used.add(wd)
            q = mc('tucau', f'Từ “{wd}” thuộc từ loại nào?', CATS[k], [], fixed=list(CATS.values()),
                   explain=f'“{wd}” là {CATS[k].lower()}: ' + {'dt': 'từ chỉ sự vật.', 'dgt': 'từ chỉ hoạt động, trạng thái.', 'tt': 'từ chỉ đặc điểm, tính chất.'}[k])
        out.append(q)
    return out


def sentence(c):
    tn, _, cn, vn = c
    return f'{tn}, {cn} {vn}' if tn else f'{cn} {vn}'


def cau_qs(C):
    out = []; keys = set()
    cands = []
    for c in C:
        tn, tt, cn, vn = c
        s = sentence(c); v = vn.rstrip('.!?')
        cands.append(('cn', mc('tucau', f'Chủ ngữ của câu “{s}” là:', cn, [v] + ([tn] if tn else []), explain=f'“{cn}” trả lời câu hỏi Ai (cái gì, con gì)?')))
        cands.append(('vn', mc('tucau', f'Vị ngữ của câu “{s}” là:', v, [cn] + ([tn] if tn else []), explain=f'“{v}” cho biết người, vật được nói đến làm gì, thế nào, là gì.')))
        if tn:
            cands.append(('tn', mc('tucau', f'Trạng ngữ của câu “{s}” là:', tn, [cn, v], explain=f'“{tn}” là thành phần phụ đứng đầu câu, ngăn cách với chủ ngữ bằng dấu phẩy.')))
            cands.append(('tt', mc('tucau', f'Trạng ngữ “{tn}” trong câu “{s}” bổ sung thông tin gì?', TN_T[tt], [], fixed=TN_FIX, explain=f'“{tn}” chỉ {TN_T[tt].lower()}.')))
    cands = shuffle(cands)
    # ưu tiên đa dạng: lần lượt lấy mỗi loại
    by = {}
    for k, q in cands:
        by.setdefault(k, []).append(q)
    kinds = [k for k in ['tn', 'cn', 'vn', 'tt'] if k in by]
    i = 0
    while len(out) < 5:
        k = kinds[i % len(kinds)]; i += 1
        if by[k]:
            q = by[k].pop()
            if key(q) not in keys:
                keys.add(key(q)); out.append(q)
        if i > 100:
            break
    return out


PEX = {'?': 'Câu hỏi dùng dấu chấm hỏi (?).', '!': 'Câu bộc lộ cảm xúc, câu cầu khiến dùng dấu chấm than (!).', '.': 'Câu kể dùng dấu chấm (.).',
       ',': 'Dấu phẩy ngăn cách trạng ngữ với chủ ngữ và vị ngữ.', ':': 'Dấu hai chấm báo hiệu lời nói của nhân vật hoặc phần liệt kê, giải thích.',
       '–': 'Dấu gạch ngang đánh dấu lời nói của nhân vật hoặc nối các từ ngữ trong một liên danh.'}


def build_tv():
    units = []; bank = []
    for unit in U:
        units.append({'lab': unit['lab'], 't': unit['t'], 'vn': unit['vn'], 'lv': LV})
        av = [mc('tucau', q, a, w) for q, a, w in shuffle(unit['AV'])[:5]]
        d0 = passage_qs(unit['A'][0]) + passage_qs(unit['A'][1]) + av
        wq = word_qs(unit['W'])
        tc = [mc('tucau', q, a, w) for q, a, w in shuffle(unit['TC'])[:5]]
        ct = []
        for a, b in shuffle(unit['CT'])[:5]:
            norm = lambda x: x.replace('-', ' ').lower()
            if norm(a) == norm(b):
                ct.append(mc('chinhta', 'Chọn cách viết đúng:', a, [b], explain=f'Viết đúng là “{a}”.'))
            else:
                ct.append(mc('chinhta', 'Nghe đọc rồi chọn từ viết đúng chính tả:', a, [b], say=a, explain=f'Viết đúng là “{a}”.'))
        d1 = []
        for i in range(5):
            d1 += [wq[i], tc[i], ct[i]]
        cq = cau_qs(unit['CAU'])
        od = [ordq('tucau', 'Sắp xếp các từ ngữ thành câu đúng:', s) for s in shuffle(unit['ORD'])[:5]]
        pc = [mc('daucau', 'Chọn dấu câu thích hợp điền vào ô trống:', p, [], fixed=o or ['.', '?', '!'], big=s, bigSmall=True, explain=PEX[p]) for s, p, o in shuffle(unit['PUNCT'])[:5]]
        d2 = []
        for i in range(5):
            d2 += [cq[i], od[i], pc[i]]
        for L in (d0, d1, d2):
            assert len(L) == 15 and len({key(q) for q in L}) == 15, (unit['lab'], len(L))
            for q in L:
                if q['type'] == 'mc':
                    assert q['answer'] in q['options'] and len(set(q['options'])) == len(q['options']) >= 2, q
        bank.append([d0, d1, d2])
    return units, bank


if __name__ == '__main__':
    us, b = build_tv()
    print(len(us), sum(len(d) for x in b for d in x))
    for u in U:
        allw = u['W']['dt'] + u['W']['dgt'] + u['W']['tt']
        assert len(allw) == len(set(allw)) == 18, u['lab']
        for a, bb in u['CT']: assert a != bb
        assert len(u['A']) == 2 and all(len(p['qs']) == 5 for p in u['A'])
        for p in u['A']:
            for q, a, w in p['qs']:
                assert a not in w and len(set(w)) == len(w), (u['lab'], q)
        assert len(u['AV']) >= 5 and len(u['TC']) >= 5 and len(u['CT']) >= 5 and len(u['ORD']) >= 5 and len(u['PUNCT']) >= 5 and len(u['CAU']) >= 5, u['lab']
        for s, p, o in u['PUNCT']:
            assert s.count('☐') == 1 and p in (o or ['.', '?', '!']), s
        for c in u['CAU']:
            assert (c[0] == '') == (c[1] == '') and (c[1] in TN_T or c[1] == ''), c
        # thứ tự câu xếp phải khác nhau
        for o in u['ORD']:
            assert len(set(o)) == len(o), o
    print('data ok')
