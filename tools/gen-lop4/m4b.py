"""Toán 4 — Chặng 5–8 (nhân, chia; thống kê; phân số) và dựng ngân hàng."""
import re
from m4a import *

# ================= CHẶNG 5: NHÂN, CHIA (1) =================
def q_nhan1():
    def g():
        k = rnd(2, 9); a = rnd(10000, 999999 // k if R.random() < .5 else 99999)
        v = a * k
        r = R.random()
        if r < .4:
            return inp('nhanchia', 'Đặt tính rồi tính:', v, visual=vcalc(a, k, '×'), explain=f'{fmt(a)} × {k} = {fmt(v)}')
        if r < .75:
            return inp('nhanchia', 'Tính:', v, **BIG(f'{fmt(a)} × {k} = ?'), explain=f'{fmt(a)} × {k} = {fmt(v)}')
        p = rnd(12, 99) * 1000 + pick([0, 500]); n = rnd(2, 9)
        return inp('giaitoan', f'Mỗi quyển truyện giá {fmt(p)} đồng. Mua {n} quyển truyện như thế hết bao nhiêu tiền?', p * n, unit='đồng', icon='📚',
                   explain=sol([f'{fmt(p)} × {n} = {fmt(p*n)} (đồng)'], p * n, 'đồng'))
    return g


def q_chia1():
    def g():
        k = rnd(2, 9); r = R.random()
        if r < .45:
            t = rnd(1000, 99999); a = t * k
            return inp('nhanchia', 'Tính:', t, **BIG(f'{fmt(a)} : {k} = ?'), explain=f'{fmt(a)} : {k} = {fmt(t)}')
        if r < .75:
            t = rnd(100, 9999); d = rnd(1, k - 1); a = t * k + d
            if R.random() < .5:
                return inp('nhanchia', f'Trong phép chia {fmt(a)} : {k}, thương là bao nhiêu?', t, explain=f'{fmt(a)} : {k} = {fmt(t)} (dư {d})')
            return inp('nhanchia', f'Trong phép chia {fmt(a)} : {k}, số dư là bao nhiêu?', d, explain=f'{fmt(a)} : {k} = {fmt(t)} (dư {d}). Số dư luôn bé hơn số chia.')
        if r < .88:
            n = rnd(2, 9); per = rnd(12, 60); tot = n * per
            return inp('giaitoan', f'Có {fmt(tot)} quyển vở chia đều cho {n} lớp. Hỏi mỗi lớp được bao nhiêu quyển vở?', per, unit='quyển', icon='📒',
                       explain=sol([f'{tot} : {n} = {per} (quyển)'], per, 'quyển'))
        k = rnd(4, 8); t = rnd(20, 120); d = rnd(1, k - 1); a = t * k + d
        return inp('giaitoan', f'Có {a} người đi tham quan, mỗi xe chở được {k} người. Cần ít nhất bao nhiêu xe để chở hết số người đó?', t + 1, unit='xe', icon='🚐',
                   explain=sol([f'{a} : {k} = {t} (dư {d})', f'Còn {d} người nên cần thêm 1 xe: {t} + 1 = {t+1} (xe)'], t + 1, 'xe'))
    return g


def q_nhan10():
    def g():
        r = R.random(); p = pick([10, 100, 1000])
        if r < .3:
            a = rnd(12, 9999)
            return inp('nhanchia', 'Tính nhẩm:', a * p, **BIG(f'{fmt(a)} × {fmt(p)} = ?'), explain=f'Nhân với {p} chỉ việc viết thêm {len(str(p))-1} chữ số 0 vào bên phải: {fmt(a*p)}.')
        if r < .6:
            a = rnd(12, 9999) * p
            return inp('nhanchia', 'Tính nhẩm:', a // p, **BIG(f'{fmt(a)} : {fmt(p)} = ?'), explain=f'Chia số tròn cho {p} chỉ việc bỏ bớt {len(str(p))-1} chữ số 0 ở bên phải: {fmt(a//p)}.')
        if r < .8:
            a = rnd(12, 999); t = pick([20, 30, 40, 50, 200, 300, 400, 500])
            return inp('nhanchia', 'Tính:', a * t, **BIG(f'{a} × {t} = ?'), explain=f'{a} × {t} = {a} × {t//(10 if t<100 else 100)} × {10 if t<100 else 100} = {fmt(a*t)}.')
        c = pick([('tạ', 'kg', 100), ('tấn', 'kg', 1000), ('m', 'cm', 100), ('km', 'm', 1000), ('m²', 'dm²', 100)]); k = rnd(12, 99)
        return inp('doluong', 'Điền số thích hợp:', k * c[2], **BIG(f'{k} {c[0]} = ? {c[1]}'), explain=f'1 {c[0]} = {c[2]} {c[1]} nên {k} {c[0]} = {k} × {c[2]} = {fmt(k*c[2])} {c[1]}.')
    return g


def q_tinhchatnhan():
    def g():
        r = rnd(0, 3)
        if r == 0:
            a, b = rnd(12, 999), rnd(2, 99)
            return inp('nhanchia', 'Tìm số thích hợp thay cho dấu ?:', a, **BIG(f'{a} × {b} = {b} × ?'), explain='Khi đổi chỗ các thừa số trong một tích thì tích không thay đổi.')
        if r == 1:
            pair = pick([(2, 5), (4, 25), (5, 20), (2, 50), (25, 8), (125, 8), (5, 4), (50, 4)]); x = rnd(12, 99)
            a, b = pair
            v = a * b * x
            return inp('nhanchia', 'Tính bằng cách thuận tiện:', v, **BIG(f'{a} × {x} × {b} = ?'), explain=f'({a} × {b}) × {x} = {a*b} × {x} = {fmt(v)}.')
        if r == 2:
            a, b, c = rnd(2, 20), rnd(2, 20), rnd(2, 20)
            return inp('nhanchia', 'Tìm số thích hợp thay cho dấu ?:', c, **BIG(f'({a} × {b}) × {c} = {a} × ({b} × ?)'), explain='Tính chất kết hợp: (a × b) × c = a × (b × c).')
        x = rnd(11, 99)
        return inp('nhanchia', 'Tính bằng cách thuận tiện:', x * 1000, **BIG(f'125 × {x} × 8 = ?'), explain=f'(125 × 8) × {x} = 1000 × {x} = {fmt(x*1000)}.')
    return g


def q_nhantong():
    def g():
        r = rnd(0, 4)
        if r == 0:
            a = rnd(12, 99); b = rnd(10, 90); c = 100 - b
            return inp('nhanchia', 'Tính bằng cách thuận tiện:', a * 100, **BIG(f'{a} × {b} + {a} × {c} = ?'), explain=f'{a} × ({b} + {c}) = {a} × 100 = {a*100}.')
        if r == 1:
            a = rnd(12, 99); b = rnd(101, 150); c = b - 100
            return inp('nhanchia', 'Tính bằng cách thuận tiện:', a * 100, **BIG(f'{a} × {b} − {a} × {c} = ?'), explain=f'{a} × ({b} − {c}) = {a} × 100 = {fmt(a*100)}.')
        if r == 2:
            a = rnd(12, 99); b = pick([9, 99, 11, 101])
            if b in (9, 99):
                v = a * b
                return inp('nhanchia', 'Tính bằng cách thuận tiện:', v, **BIG(f'{a} × {b} = ?'), explain=f'{a} × ({b+1} − 1) = {a*(b+1)} − {a} = {fmt(v)}.')
            v = a * b
            return inp('nhanchia', 'Tính bằng cách thuận tiện:', v, **BIG(f'{a} × {b} = ?'), explain=f'{a} × ({b-1} + 1) = {a*(b-1)} + {a} = {fmt(v)}.')
        if r == 3:
            a, b, c = rnd(2, 30), rnd(2, 30), rnd(2, 30)
            return inp('nhanchia', 'Tìm số thích hợp thay cho dấu ?:', c, **BIG(f'{a} × ({b} + {c}) = {a} × {b} + {a} × ?'), explain='Nhân một số với một tổng: a × (b + c) = a × b + a × c.')
        a = rnd(3, 9); b = rnd(20, 40); c = rnd(10, 19)
        return inp('giaitoan', f'Một cửa hàng có {a} thùng táo, mỗi thùng {b} kg và {a} thùng cam, mỗi thùng {c} kg. Hỏi cửa hàng có tất cả bao nhiêu ki-lô-gam táo và cam?', a * (b + c), unit='kg', icon='🍎',
                   explain=sol([f'{a} × ({b} + {c}) = {a} × {b+c} = {a*(b+c)} (kg)'], a * (b + c), 'kg'))
    return g


# ================= CHẶNG 6: NHÂN, CHIA (2); TRUNG BÌNH CỘNG; THỐNG KÊ =================
def q_nhan2():
    def g():
        a = rnd(100, 9999) if R.random() < .6 else rnd(12, 99); b = rnd(11, 99)
        if b % 10 == 0:
            return None
        v = a * b
        r = R.random()
        if r < .35:
            return inp('nhanchia', 'Đặt tính rồi tính:', v, visual=vcalc(a, b, '×'), explain=f'{fmt(a)} × {b} = {fmt(a)} × {b//10*10} + {fmt(a)} × {b%10} = {fmt(a*(b//10*10))} + {fmt(a*(b%10))} = {fmt(v)}')
        if r < .75:
            return inp('nhanchia', 'Tính:', v, **BIG(f'{fmt(a)} × {b} = ?'), explain=f'{fmt(a)} × {b} = {fmt(v)}')
        rows = rnd(12, 40); per = rnd(12, 35)
        return inp('giaitoan', f'Một hội trường có {rows} hàng ghế, mỗi hàng có {per} ghế. Hỏi hội trường có bao nhiêu ghế?', rows * per, unit='ghế', icon='🪑',
                   explain=sol([f'{per} × {rows} = {rows*per} (ghế)'], rows * per, 'ghế'))
    return g


def q_chia2():
    def g():
        b = rnd(12, 99); r = R.random()
        if r < .45:
            t = rnd(12, 999); a = t * b
            return inp('nhanchia', 'Tính:', t, **BIG(f'{fmt(a)} : {b} = ?'), explain=f'{fmt(a)} : {b} = {t} (thử lại: {t} × {b} = {fmt(a)})')
        if r < .75:
            t = rnd(12, 400); d = rnd(1, b - 1); a = t * b + d
            if R.random() < .5:
                return inp('nhanchia', f'Trong phép chia {fmt(a)} : {b}, thương là bao nhiêu?', t, explain=f'{fmt(a)} : {b} = {t} (dư {d})')
            return inp('nhanchia', f'Trong phép chia {fmt(a)} : {b}, số dư là bao nhiêu?', d, explain=f'{fmt(a)} : {b} = {t} (dư {d})')
        per = rnd(12, 48); n = rnd(12, 60)
        return inp('giaitoan', f'Người ta xếp {fmt(per*n)} gói kẹo vào các hộp, mỗi hộp {per} gói. Hỏi xếp được bao nhiêu hộp?', n, unit='hộp', icon='🍬',
                   explain=sol([f'{fmt(per*n)} : {per} = {n} (hộp)'], n, 'hộp'))
    return g


def q_tbc():
    def g():
        r = rnd(0, 4)
        if r == 0:
            k = rnd(2, 5); avg = rnd(10, 200); xs = [avg + rnd(-9, 9) for _ in range(k - 1)]; last = avg * k - sum(xs)
            if last <= 0:
                return None
            xs.append(last); R.shuffle(xs)
            return inp('thongke', f'Tìm số trung bình cộng của các số: {", ".join(map(str, xs))}.', avg,
                       explain=f'({" + ".join(map(str, xs))}) : {k} = {sum(xs)} : {k} = {avg}.')
        if r == 1:
            d = [rnd(20, 45) for _ in range(3)]; s = sum(d)
            if s % 3:
                d[2] += 3 - s % 3; s = sum(d)
            return inp('thongke', f'Ba bạn cân nặng lần lượt {d[0]} kg, {d[1]} kg, {d[2]} kg. Hỏi trung bình mỗi bạn cân nặng bao nhiêu ki-lô-gam?', s // 3, unit='kg', icon='⚖️',
                       explain=sol([f'({d[0]} + {d[1]} + {d[2]}) : 3 = {s} : 3 = {s//3} (kg)'], s // 3, 'kg'))
        if r == 2:
            k = rnd(3, 5); avg = rnd(20, 60)
            return inp('thongke', f'Trung bình cộng của {k} số là {avg}. Tổng của {k} số đó là bao nhiêu?', avg * k, explain=f'Tổng = trung bình cộng × số các số hạng = {avg} × {k} = {avg*k}.')
        if r == 3:
            avg = rnd(20, 80); a = rnd(avg - 15, avg + 15); b = 2 * avg - a
            if b <= 0 or a == b:
                return None
            return inp('thongke', f'Trung bình cộng của hai số là {avg}. Một số là {a}. Tìm số kia.', b, explain=f'Tổng hai số: {avg} × 2 = {2*avg}; số kia: {2*avg} − {a} = {b}.')
        n1, n2 = rnd(2, 4), rnd(2, 4); a, b = rnd(30, 60), rnd(30, 60)
        tot = n1 * a + n2 * b
        if tot % (n1 + n2):
            return None
        v = tot // (n1 + n2)
        return inp('thongke', f'Một cửa hàng {n1} ngày đầu mỗi ngày bán {a} kg đường, {n2} ngày sau mỗi ngày bán {b} kg đường. Hỏi trung bình mỗi ngày bán được bao nhiêu ki-lô-gam đường?', v, unit='kg', icon='🍚',
                   explain=sol([f'{n1} ngày đầu: {a} × {n1} = {a*n1} (kg)', f'{n2} ngày sau: {b} × {n2} = {b*n2} (kg)', f'Trung bình: ({a*n1} + {b*n2}) : {n1+n2} = {v} (kg)'], v, 'kg'))
    return g


def q_rutdonvi():
    def g():
        r = rnd(0, 4)
        it = pick([('hộp bánh', 'cái bánh', 'cái'), ('thùng sữa', 'hộp sữa', 'hộp'), ('bao gạo', 'ki-lô-gam gạo', 'kg'), ('túi kẹo', 'viên kẹo', 'viên')])
        a = rnd(2, 9); per = rnd(6, 50); b = rnd(2, 12)
        if b == a:
            return None
        if r <= 1:
            return inp('giaitoan', f'{a} {it[0]} như nhau có {a*per} {it[1]}. Hỏi {b} {it[0]} như thế có bao nhiêu {it[1]}?', b * per, unit=it[2], icon='📦',
                       explain=sol([f'Mỗi {it[0]}: {a*per} : {a} = {per} ({it[2]})', f'{b} {it[0]}: {per} × {b} = {b*per} ({it[2]})'], b * per, it[2]))
        if r == 2:
            price = rnd(3, 25) * 1000
            return inp('giaitoan', f'Mua {a} quyển vở hết {fmt(price*a)} đồng. Hỏi mua {b} quyển vở như thế hết bao nhiêu tiền?', price * b, unit='đồng', icon='📒',
                       explain=sol([f'Giá 1 quyển: {fmt(price*a)} : {a} = {fmt(price)} (đồng)', f'{b} quyển: {fmt(price)} × {b} = {fmt(price*b)} (đồng)'], price * b, 'đồng'))
        if r == 3:
            q = rnd(2, 12); n = rnd(2, 6); tot = a * per
            return inp('giaitoan', f'Có {tot} {it[1]} xếp đều vào {a} {it[0]}. Hỏi {q*per} {it[1]} thì xếp được bao nhiêu {it[0]} như thế?', q, unit=it[0].split()[0], icon='📦',
                       explain=sol([f'Mỗi {it[0]}: {tot} : {a} = {per} ({it[2]})', f'Số {it[0]}: {q*per} : {per} = {q} ({it[0].split()[0]})'], q, it[0].split()[0]))
        km = rnd(20, 60); h = rnd(2, 5); h2 = rnd(2, 7)
        if h2 == h:
            return None
        return inp('giaitoan', f'Một ô tô đi {h} giờ được {km*h} km. Hỏi trong {h2} giờ ô tô đó đi được bao nhiêu ki-lô-mét (quãng đường mỗi giờ như nhau)?', km * h2, unit='km', icon='🚗',
                   explain=sol([f'Mỗi giờ: {km*h} : {h} = {km} (km)', f'{h2} giờ: {km} × {h2} = {km*h2} (km)'], km * h2, 'km'))
    return g


BC_DATA = [('Số cây trồng được', 'cây', ['4A', '4B', '4C', '4D'], 10), ('Số sách quyên góp', 'quyển', ['Tổ 1', 'Tổ 2', 'Tổ 3', 'Tổ 4'], 5),
           ('Số học sinh thích môn thể thao', 'bạn', ['Bóng đá', 'Bơi', 'Cờ vua', 'Cầu lông'], 2), ('Số vở bán được', 'quyển', ['Thứ Hai', 'Thứ Ba', 'Thứ Tư', 'Thứ Năm'], 20)]


def q_bieudo():
    def g():
        t, u, cats, step = pick(BC_DATA)
        vals = [rnd(1, 9) * step for _ in cats]
        if len(set(vals)) < len(vals):
            return None
        vis = f'<div class="ctx" style="font-size:18px">{t}</div>' + bar_svg(cats, vals, u, step)
        r = R.random()
        if r < .3:
            i = rnd(0, 3)
            return inp('thongke', f'Xem biểu đồ cột. {cats[i]} có bao nhiêu {u}?', vals[i], unit=u, visual=vis)
        if r < .5:
            most = R.random() < .5; i = vals.index(max(vals) if most else min(vals))
            return mc('thongke', f'Xem biểu đồ cột. Cột nào có {"nhiều" if most else "ít"} {u} nhất?', cats[i], [c for c in cats if c != cats[i]][:2] if False else R.sample([c for c in cats if c != cats[i]], 2), visual=vis)
        if r < .7:
            i, j = R.sample(range(4), 2)
            if vals[i] < vals[j]:
                i, j = j, i
            return inp('thongke', f'Xem biểu đồ cột. {cats[i]} nhiều hơn {cats[j]} bao nhiêu {u}?', vals[i] - vals[j], unit=u, visual=vis, explain=f'{vals[i]} − {vals[j]} = {vals[i]-vals[j]}')
        if r < .85:
            return inp('thongke', f'Xem biểu đồ cột. Tất cả có bao nhiêu {u}?', sum(vals), unit=u, visual=vis, explain=' + '.join(map(str, vals)) + f' = {sum(vals)}')
        s = sum(vals)
        if s % 4:
            return None
        return inp('thongke', f'Xem biểu đồ cột. Trung bình mỗi cột có bao nhiêu {u}?', s // 4, unit=u, visual=vis, explain=f'({" + ".join(map(str, vals))}) : 4 = {s//4}')
    return g


def q_dayso_lieu():
    def g():
        n = rnd(5, 7); xs = [rnd(120, 150) for _ in range(n)]
        if len(set(xs)) < n:
            return None
        r = R.random()
        vis = f'<div class="ctx">{" ; ".join(map(str, xs))}</div>'
        head = 'Chiều cao (cm) của một nhóm bạn: '
        if r < .25:
            return inp('thongke', head + 'Dãy số liệu có bao nhiêu số?', n, visual=vis)
        if r < .5:
            k = rnd(2, n)
            return inp('thongke', head + f'Số thứ {k} trong dãy là số nào?', xs[k - 1], visual=vis)
        if r < .75:
            big = R.random() < .5
            return inp('thongke', head + f'Bạn {"cao" if big else "thấp"} nhất cao bao nhiêu xăng-ti-mét?', max(xs) if big else min(xs), unit='cm', visual=vis)
        return inp('thongke', head + 'Bạn cao nhất cao hơn bạn thấp nhất bao nhiêu xăng-ti-mét?', max(xs) - min(xs), unit='cm', visual=vis, explain=f'{max(xs)} − {min(xs)} = {max(xs)-min(xs)} (cm)')
    return g


def q_solan():
    def g():
        r = R.random()
        if r < .45:
            n = rnd(10, 30); s = rnd(2, n - 2)
            vis = table_html(['Mặt', 'Số lần'], [['Sấp', s], ['Ngửa', n - s]], caption=f'Tung đồng xu {n} lần')
            ask = pick(['Sấp', 'Ngửa'])
            return inp('thongke', f'Tung một đồng xu {n} lần. Mặt {ask.lower()} xuất hiện bao nhiêu lần?', s if ask == 'Sấp' else n - s, unit='lần', visual=vis,
                       explain=f'Số lần mặt ngửa = {n} − {s} = {n-s}.' if ask == 'Ngửa' else None) if R.random() < .5 else \
                inp('thongke', f'Tung một đồng xu {n} lần, mặt sấp xuất hiện {s} lần. Hỏi mặt ngửa xuất hiện bao nhiêu lần?', n - s, unit='lần', explain=f'{n} − {s} = {n-s} (lần)')
        if r < .75:
            cols = ['đỏ', 'xanh', 'vàng']; cnt = [rnd(2, 12) for _ in cols]
            if len(set(cnt)) < 3:
                return None
            vis = table_html(['Màu bóng', 'Số lần lấy được'], [[c, k] for c, k in zip(cols, cnt)], caption=f'Lấy bóng {sum(cnt)} lần')
            if R.random() < .5:
                most = cols[cnt.index(max(cnt))]
                return mc('thongke', 'Bóng màu nào được lấy ra nhiều lần nhất?', 'Màu ' + most, ['Màu ' + c for c in cols if c != most], visual=vis)
            return inp('thongke', 'Bạn An lấy bóng trong hộp rồi trả lại, ghi kết quả vào bảng. An đã lấy bóng tất cả bao nhiêu lần?', sum(cnt), unit='lần', visual=vis)
        FIX = ['chắc chắn', 'có thể', 'không thể']
        L = [('Tung xúc xắc 6 mặt (1 đến 6 chấm), …… xuất hiện mặt 7 chấm.', 'không thể'), ('Tung xúc xắc 6 mặt, …… xuất hiện mặt 3 chấm.', 'có thể'),
             ('Tung xúc xắc 6 mặt, số chấm xuất hiện …… bé hơn 7.', 'chắc chắn'), ('Tung đồng xu, …… xuất hiện mặt sấp.', 'có thể'),
             ('Hộp chỉ có bóng xanh. Lấy ra một quả, …… lấy được bóng xanh.', 'chắc chắn'), ('Hộp chỉ có bóng xanh. Lấy ra một quả, …… lấy được bóng đỏ.', 'không thể'),
             ('Hộp có bóng đỏ và bóng xanh. Lấy ra một quả, …… lấy được bóng đỏ.', 'có thể')]
        t, a = pick(L)
        return mc('thongke', 'Chọn từ thích hợp điền vào chỗ chấm:', a, [], fixed=FIX, big=t, bigSmall=True)
    return g


# ================= CHẶNG 7: PHÂN SỐ =================
def q_khainiem():
    def g():
        r = R.random()
        d = rnd(2, 12); n = rnd(1, d - 1)
        if r < .4:
            return mc('phanso', 'Phân số chỉ phần đã tô màu của hình là:', f'{n}/{d}', fr_wrong(F(n, d), [(d - n, d), (n, d - n) if d - n != n else None, (d, n), (n + 1, d)]),
                      visual=frac_svg(n, d), explain=f'Hình được chia thành {d} phần bằng nhau, tô màu {n} phần: {n}/{d}.')
        if r < .6:
            ask = pick(['tử số', 'mẫu số'])
            return inp('phanso', f'Phân số {n}/{d} có {ask} là bao nhiêu?', n if ask == 'tử số' else d, explain='Tử số viết trên gạch ngang, mẫu số viết dưới gạch ngang.')
        if r < .8:
            DN = {2: 'hai', 3: 'ba', 4: 'tư', 5: 'năm', 6: 'sáu', 7: 'bảy', 8: 'tám', 9: 'chín', 10: 'mười', 11: 'mười một', 12: 'mười hai'}
            NN = {1: 'một', 2: 'hai', 3: 'ba', 4: 'bốn', 5: 'năm', 6: 'sáu', 7: 'bảy', 8: 'tám', 9: 'chín', 10: 'mười', 11: 'mười một'}
            txt = f'{NN[n]} phần {DN[d]}'
            if R.random() < .5:
                return mc('phanso', f'Phân số “{txt}” viết là:', f'{n}/{d}', fr_wrong(F(n, d), [(d, n), (n + 1, d), (n, d + 1)]))
            ws = []
            for x, y in [(d, n), (n + 1, d), (n, d + 1)]:
                if y in DN and x in NN and (x, y) != (n, d):
                    ws.append(f'{NN[x]} phần {DN[y]}')
            if len(ws) < 2:
                return None
            return mc('phanso', f'Phân số {n}/{d} đọc là:', txt, ws[:2])
        return inp('phanso', f'Hình được chia thành {d} phần bằng nhau, đã tô màu {n} phần. Phần chưa tô màu là mấy phần {d}?', d - n,
                   visual=frac_svg(n, d, 'bang'), explain=f'Phần chưa tô: {d} − {n} = {d-n}, tức là {d-n}/{d}.')
    return g


def q_ps_chia():
    def g():
        r = R.random()
        a, b = rnd(1, 15), rnd(2, 12)
        if r < .35:
            if a % b == 0:
                return None
            return mc('phanso', f'Viết thương của phép chia {a} : {b} dưới dạng phân số:', f'{a}/{b}', fr_wrong(F(a, b), [(b, a), (a + b, b), (a, a + b)]),
                      explain='Thương của phép chia số tự nhiên cho số tự nhiên (khác 0) có thể viết thành phân số: tử số là số bị chia, mẫu số là số chia.')
        if r < .65:
            n, d = rnd(1, 15), rnd(2, 12)
            ans = 'Lớn hơn 1' if n > d else 'Bằng 1' if n == d else 'Bé hơn 1'
            return mc('phanso', f'Phân số {n}/{d} so với 1 thì thế nào?', ans, [], fixed=['Bé hơn 1', 'Bằng 1', 'Lớn hơn 1'],
                      explain='Tử số bé hơn mẫu số thì phân số bé hơn 1; tử số bằng mẫu số thì bằng 1; tử số lớn hơn mẫu số thì lớn hơn 1.')
        if r < .85:
            k = rnd(2, 9); d = rnd(2, 9)
            return inp('phanso', 'Tìm số thích hợp thay cho dấu ?:', k * d, big=f'{k} = ?/{d}', explain=f'{k} = {k*d} : {d} = {k*d}/{d}.')
        c = rnd(2, 6); n = rnd(3, 11)
        return mc('phanso', f'Chia đều {n} cái bánh cho {c} bạn. Mỗi bạn được bao nhiêu phần cái bánh?', f'{n}/{c}', fr_wrong(F(n, c), [(c, n), (1, c), (n, c + n)]), icon='🥮',
                  explain=f'{n} : {c} = {n}/{c} (cái bánh).') if n % c else None
    return g


def rutgon(n, d):
    g_ = gcd(n, d); return n // g_, d // g_


def q_rutgon():
    def g():
        r = R.random()
        n0, d0 = rnd(1, 8), rnd(2, 9)
        if n0 >= d0 and R.random() < .8:
            return None
        if gcd(n0, d0) != 1:
            return None
        k = rnd(2, 6); n, d = n0 * k, d0 * k
        if r < .35:
            return mc('phanso', f'Rút gọn phân số {n}/{d} ta được phân số tối giản:', f'{n0}/{d0}', fr_wrong(F(n0, d0), [(n // 2, d) if n % 2 == 0 else None, (n0, d0 + 1), (n0 + 1, d0), (n, d0), (d0, n0)]),
                      explain=f'Chia cả tử số và mẫu số cho {k}: {n}/{d} = {n0}/{d0}.')
        if r < .6:
            if R.random() < .5:
                return inp('phanso', 'Tìm số thích hợp thay cho dấu ?:', n0, big=f'{n}/{d} = ?/{d0}', explain=f'{d} : {k} = {d0} nên {n} : {k} = {n0}.')
            return inp('phanso', 'Tìm số thích hợp thay cho dấu ?:', d, big=f'{n0}/{d0} = {n}/?', explain=f'{n0} × {k} = {n} nên {d0} × {k} = {d}.')
        if r < .8:
            opts = [(n0, d0), (n, d), (n0 * 2, d0 * 2 + 1 if gcd(n0 * 2, d0 * 2 + 1) != 1 else d0 * 2)]
            good = f'{n0}/{d0}'
            bads = []
            for x, y in [(n, d), (2 * rnd(1, 5), 2 * rnd(3, 7)), (3 * rnd(1, 3), 3 * rnd(2, 5))]:
                if gcd(x, y) != 1 and x < y and f'{x}/{y}' not in bads:
                    bads.append(f'{x}/{y}')
            if len(bads) < 2:
                return None
            return mc('phanso', 'Phân số nào dưới đây là phân số tối giản?', good, bads[:2], explain=f'{good} có tử số và mẫu số không cùng chia hết cho số nào lớn hơn 1.')
        return mc('phanso', f'Phân số nào bằng phân số {n0}/{d0}?', f'{n}/{d}', fr_wrong(F(n0, d0), [(n0 + k, d0 + k), (n, d + 1), (n + k, d), (n0 * k, d0)]),
                  explain=f'Nhân cả tử số và mẫu số với {k}: {n0}/{d0} = {n}/{d}.')
    return g


def q_quydong():
    def g():
        r = R.random()
        d1 = rnd(2, 6); k = rnd(2, 4); d2 = d1 * k
        n1 = rnd(1, d1 - 1) if d1 > 1 else 1; n2 = rnd(1, d2 - 1)
        if gcd(n1, d1) != 1:
            return None
        if r < .45:
            return inp('phanso', f'Quy đồng mẫu số hai phân số {n1}/{d1} và {n2}/{d2} (mẫu số chung {d2}). Tìm số thích hợp thay cho dấu ?:', n1 * k, big=f'{n1}/{d1} = ?/{d2}',
                       explain=f'{d2} : {d1} = {k}; nhân cả tử và mẫu của {n1}/{d1} với {k}: {n1*k}/{d2}.')
        if r < .75:
            a, b = rnd(2, 5), rnd(2, 5)
            if a == b or gcd(a, b) != 1:
                return None
            x, y = rnd(1, a - 1), rnd(1, b - 1)
            return mc('phanso', f'Quy đồng mẫu số hai phân số {x}/{a} và {y}/{b} ta được:', f'{x*b}/{a*b} và {y*a}/{a*b}',
                      [f'{x*a}/{a*b} và {y*b}/{a*b}' if (x * a, y * b) != (x * b, y * a) else f'{x}/{a*b} và {y}/{a*b}', f'{x+b}/{a*b} và {y+a}/{a*b}'],
                      explain=f'Mẫu số chung {a} × {b} = {a*b}; {x}/{a} = {x*b}/{a*b}; {y}/{b} = {y*a}/{a*b}.')
        return inp('phanso', f'Mẫu số chung bé nhất để quy đồng hai phân số {n1}/{d1} và {n2}/{d2} là bao nhiêu?', d2, explain=f'{d2} chia hết cho {d1} nên chọn {d2} làm mẫu số chung.')
    return g


def q_sosanh_ps():
    def g():
        r = R.random()
        if r < .3:
            d = rnd(3, 12); a, b = rnd(1, d + 3), rnd(1, d + 3)
            return mc('phanso', 'Chọn dấu thích hợp điền vào ô trống:', sign(F(a, d), F(b, d)), [], fixed=SIGN_FIX, big=f'{a}/{d} ☐ {b}/{d}',
                      explain='Hai phân số cùng mẫu số: phân số nào có tử số lớn hơn thì lớn hơn.')
        if r < .5:
            n = rnd(1, 9); a, b = rnd(2, 12), rnd(2, 12)
            return mc('phanso', 'Chọn dấu thích hợp điền vào ô trống:', sign(F(n, a), F(n, b)), [], fixed=SIGN_FIX, big=f'{n}/{a} ☐ {n}/{b}',
                      explain='Hai phân số cùng tử số: phân số nào có mẫu số bé hơn thì lớn hơn.')
        if r < .75:
            d1 = rnd(2, 6); k = rnd(2, 3); d2 = d1 * k; a = rnd(1, d1 - 1) if d1 > 2 else 1; b = rnd(1, d2 - 1)
            x, y = (f'{a}/{d1}', f'{b}/{d2}') if R.random() < .5 else (f'{b}/{d2}', f'{a}/{d1}')
            fx, fy = F(*map(int, x.split('/'))), F(*map(int, y.split('/')))
            return mc('phanso', 'Chọn dấu thích hợp điền vào ô trống:', sign(fx, fy), [], fixed=SIGN_FIX, big=f'{x} ☐ {y}',
                      explain=f'Quy đồng mẫu số rồi so sánh: {a}/{d1} = {a*k}/{d2}.')
        d = rnd(5, 12); ns = R.sample(range(1, d + 2), 4)
        up = R.random() < .5
        srt = sorted(ns, reverse=not up)
        if R.random() < .5:
            return ordq('phanso', f'Sắp xếp các phân số theo thứ tự {"từ bé đến lớn" if up else "từ lớn đến bé"}:', [f'{x}/{d}' for x in srt])
        big = R.random() < .5
        fs = [(rnd(1, 9), rnd(2, 10)) for _ in range(3)]
        vals = [F(*f) for f in fs]
        if len(set(vals)) < 3:
            return None
        i = vals.index(max(vals) if big else min(vals))
        return mc('phanso', f'Phân số nào {"lớn" if big else "bé"} nhất?', f'{fs[i][0]}/{fs[i][1]}', [f'{x}/{y}' for j, (x, y) in enumerate(fs) if j != i])
    return g


# ================= CHẶNG 8: PHÉP TÍNH VỚI PHÂN SỐ =================
def red(fr):
    return frac(F(fr))


def q_congps(op='+'):
    def g():
        same = R.random() < .5
        if same:
            d = rnd(3, 12); a, b = rnd(1, d), rnd(1, d)
            A, B = F(a, d), F(b, d); sa, sb = f'{a}/{d}', f'{b}/{d}'
        else:
            d1 = rnd(2, 6); k = rnd(2, 3); d2 = d1 * k
            if R.random() < .4:
                d2 = rnd(2, 7)
                if d2 == d1:
                    return None
            a, b = rnd(1, d1), rnd(1, d2)
            A, B = F(a, d1), F(b, d2); sa, sb = f'{a}/{d1}', f'{b}/{d2}'
            if R.random() < .5:
                A, B, sa, sb = B, A, sb, sa
        if op == '−' and A <= B:
            A, B, sa, sb = B, A, sb, sa
            if A == B:
                return None
        v = A + B if op == '+' else A - B
        na, da = map(int, sa.split('/')); nb, db = map(int, sb.split('/'))
        cands = [(na + nb if op == '+' else na - nb, da + db), (na + nb if op == '+' else abs(na - nb), max(da, db)), (v.numerator + 1, v.denominator), (v.numerator, v.denominator + 1)]
        return mc('phanso', 'Tính (kết quả viết dưới dạng phân số tối giản):', red(v), fr_wrong(v, cands), big=f'{sa} {op} {sb} = ☐',
                  explain=('Cùng mẫu số: ' if da == db else 'Quy đồng mẫu số rồi ') + f'{"cộng" if op == "+" else "trừ"} hai tử số, giữ nguyên mẫu số. Kết quả: {red(v)}.')
    return g


def q_ps_word(kind):
    def g():
        if kind == '+':
            d = rnd(4, 10); a = rnd(1, d - 2); b = rnd(1, d - a)
            v = F(a, d) + F(b, d)
            return mc('phanso', f'Ngày thứ nhất bạn Nam đọc được {a}/{d} cuốn sách, ngày thứ hai đọc được {b}/{d} cuốn sách. Hỏi cả hai ngày Nam đọc được bao nhiêu phần cuốn sách?', red(v),
                      fr_wrong(v, [(a + b, 2 * d), (v.numerator + 1, v.denominator), (a * b, d)]), icon='📖', explain=f'{a}/{d} + {b}/{d} = {red(v)} (cuốn sách).')
        d = rnd(3, 9); a = rnd(1, d - 1)
        v = 1 - F(a, d)
        return mc('phanso', f'Một tấm vải, người ta đã may áo hết {a}/{d} tấm vải. Hỏi còn lại bao nhiêu phần tấm vải?', red(v),
                  fr_wrong(v, [(a, d), (d - a + 1, d), (1, d)]), icon='🧵', explain=f'Cả tấm vải là 1 = {d}/{d}; {d}/{d} − {a}/{d} = {red(v)}.')
    return g


def q_nhanps():
    def g():
        r = R.random()
        if r < .6:
            a, b, c, d = rnd(1, 7), rnd(2, 9), rnd(1, 7), rnd(2, 9)
            v = F(a, b) * F(c, d)
            return mc('phanso', 'Tính (kết quả viết dưới dạng phân số tối giản):', red(v), fr_wrong(v, [(a * c, b + d), (a + c, b * d), (a * d, b * c), (v.numerator + 1, v.denominator)]), big=f'{a}/{b} × {c}/{d} = ☐',
                      explain=f'Nhân tử số với tử số, mẫu số với mẫu số: {a*c}/{b*d} = {red(v)}.')
        if r < .8:
            a, b, k = rnd(1, 7), rnd(2, 9), rnd(2, 6)
            v = F(a, b) * k
            return mc('phanso', 'Tính (kết quả viết dưới dạng phân số tối giản):', red(v), fr_wrong(v, [(a * k, b * k), (a, b * k), (a + k, b)]), big=f'{a}/{b} × {k} = ☐',
                      explain=f'Nhân tử số với {k}, giữ nguyên mẫu số: {a*k}/{b} = {red(v)}.')
        a = rnd(2, 12); b = rnd(2, 9); c = rnd(1, b - 1)
        v = F(a) * F(c, b)
        return mc('phanso', f'Hình chữ nhật có chiều dài {a} m, chiều rộng {c}/{b} m. Diện tích hình chữ nhật là:', red(v) + ' m²', [x + ' m²' for x in fr_wrong(v, [(a + c, b), (a * c, b * b), (2 * (a * b + c), b)])],
                  explain=f'{a} × {c}/{b} = {a*c}/{b} = {red(v)} (m²).') if (a * c) % b else None
    return g


def q_chiaps():
    def g():
        r = R.random()
        if r < .6:
            a, b, c, d = rnd(1, 7), rnd(2, 9), rnd(1, 7), rnd(2, 9)
            v = F(a, b) / F(c, d)
            return mc('phanso', 'Tính (kết quả viết dưới dạng phân số tối giản):', red(v), fr_wrong(v, [(a * c, b * d), (a * c, b * d) if False else (b * c, a * d), (a, b * c), (v.numerator + 1, v.denominator)]), big=f'{a}/{b} : {c}/{d} = ☐',
                      explain=f'Nhân phân số thứ nhất với phân số thứ hai đảo ngược: {a}/{b} × {d}/{c} = {a*d}/{b*c} = {red(v)}.')
        if r < .8:
            a, b, k = rnd(1, 9), rnd(2, 9), rnd(2, 6)
            v = F(a, b) / k
            return mc('phanso', 'Tính (kết quả viết dưới dạng phân số tối giản):', red(v), fr_wrong(v, [(a * k, b), (a, b + k), (k, a * b)]), big=f'{a}/{b} : {k} = ☐',
                      explain=f'{a}/{b} : {k} = {a}/{b} × 1/{k} = {a}/{b*k} = {red(v)}.')
        c, d = rnd(1, 5), rnd(2, 7)
        if c >= d:
            return None
        return mc('phanso', f'Phân số đảo ngược của {c}/{d} là:', f'{d}/{c}' if c != 1 else str(d), fr_wrong(F(d, c), [(c, d), (1, d), (d + c, c)]),
                  explain='Đổi chỗ tử số và mẫu số ta được phân số đảo ngược.')
    return g


def q_psmotso():
    def g():
        r = R.random()
        n, d = rnd(1, 5), rnd(2, 9)
        if n >= d or gcd(n, d) != 1:
            return None
        k = rnd(2, 15); tot = d * k; v = n * k
        if r < .4:
            return inp('phanso', f'Tìm {n}/{d} của {tot}.', v, explain=f'{tot} × {n}/{d} = {v}.')
        if r < .7:
            it = pick([('Lớp 4A có', 'học sinh', 'học sinh thích vẽ', 'bạn'), ('Cửa hàng có', 'kg gạo', 'số gạo đã bán', 'kg'), ('Đàn gà có', 'con', 'số gà mái', 'con')])
            return inp('phanso', f'{it[0]} {tot} {it[1]}, {it[2]} bằng {n}/{d} số đó. Hỏi {it[2]} là bao nhiêu?', v, unit=it[3], icon='🧮',
                       explain=sol([f'{tot} × {n}/{d} = {v} ({it[3]})'], v, it[3]))
        return inp('phanso', f'Một đoạn đường dài {tot} m, đội công nhân đã sửa được {n}/{d} đoạn đường. Hỏi còn phải sửa bao nhiêu mét đường nữa?', tot - v, unit='m', icon='🚧',
                   explain=sol([f'Đã sửa: {tot} × {n}/{d} = {v} (m)', f'Còn lại: {tot} − {v} = {tot-v} (m)'], tot - v, 'm'))
    return g


# ================= CẤU TRÚC 8 CHẶNG × 6 BÀI =================
WEEKS = [
    dict(t='Ôn tập và bổ sung', s='Các số đến 100 000; phép tính trong phạm vi 100 000; số chẵn, số lẻ; biểu thức chứa chữ; bài toán có ba bước tính.',
         ls=['Ôn tập các số đến 100 000', 'Ôn tập các phép tính trong phạm vi 100 000', 'Số chẵn, số lẻ', 'Biểu thức chứa chữ', 'Giải bài toán có ba bước tính', 'Luyện tập chung'],
         L=[[q_doc5(), q_cautao5(), q_cmp(10000, 99999), q_sort(10000, 99999), q_lienke(10000, 99999), q_lamtron([1000, 10000], 10000, 99999), q_maxmin(10000, 99999)],
            [q_congtru(10000, 99999), q_nhanchia1(1000, 99999), q_bieuthuc(), q_timx5()],
            [q_chanle(), q_chanle_the()],
            [q_bieuthucchu()],
            [q_3buoc()],
            [q_doc5(), q_congtru(10000, 99999), q_chanle(), q_bieuthucchu(), q_3buoc(), q_timx5(), q_bieuthuc()]]),
    dict(t='Góc và số có nhiều chữ số', s='Đo góc, góc nhọn, góc tù, góc bẹt; số có sáu chữ số, số 1 000 000; hàng và lớp; lớp triệu; làm tròn, so sánh; dãy số tự nhiên.',
         ls=['Đo góc. Góc nhọn, góc tù, góc bẹt', 'Số có sáu chữ số. Số 1 000 000', 'Hàng và lớp', 'Các số trong phạm vi lớp triệu', 'Làm tròn, so sánh số có nhiều chữ số', 'Dãy số tự nhiên. Luyện tập chung'],
         L=[[q_goc(), q_demgoc()],
            [q_so6(), q_trieu_facts(), q_dayso(100000, 1000000)],
            [q_hanglop(6), q_hanglop(9), q_lopfacts()],
            [q_trieu(), q_hanglop(9), q_dayso(1000000, 999999999)],
            [q_lamtron([100000, 10000, 1000000], 100000, 99999999), q_cmp(100000, 999999999), q_sort(1000000, 999999999), q_maxmin(100000, 99999999)],
            [q_dstn(), q_dayso(0, 10000000), q_trieu(), q_goc(), q_cmp(100000, 99999999)]]),
    dict(t='Đơn vị đo đại lượng. Phép cộng, phép trừ', s='Yến, tạ, tấn; đề-xi-mét vuông, mét vuông, mi-li-mét vuông; giây, thế kỉ; cộng, trừ số có nhiều chữ số; tính chất phép cộng; tìm hai số biết tổng và hiệu.',
         ls=['Yến, tạ, tấn', 'dm², m², mm²', 'Giây, thế kỉ', 'Cộng, trừ các số có nhiều chữ số', 'Tính chất giao hoán, kết hợp của phép cộng', 'Tìm hai số biết tổng và hiệu'],
         L=[[q_yenta()], [q_dientich()], [q_giaytheki()],
            [q_congtru(100000, 999999), q_congtru(10000, 9999999)],
            [q_giaohoan_cong()], [q_tonghieu()]]),
    dict(t='Vuông góc, song song. Ôn tập học kì 1', s='Hai đường thẳng vuông góc, song song; hình bình hành, hình thoi; ôn tập số, phép tính, hình học và đo lường.',
         ls=['Hai đường thẳng vuông góc', 'Hai đường thẳng song song', 'Hình bình hành, hình thoi', 'Ôn tập số và phép tính', 'Ôn tập hình học và đo lường', 'Ôn tập học kì 1'],
         L=[[q_vuonggoc(), q_vg_hinh(), q_demhinh()], [q_songsong(), q_vg_hinh()], [q_binhhanh(), q_demgoc()],
            [q_trieu(), q_cmp(100000, 999999999), q_congtru(100000, 999999), q_tonghieu(), q_giaohoan_cong(), q_lamtron([100000], 100000, 9999999)],
            [q_goc(), q_yenta(), q_dientich(), q_giaytheki(), q_binhhanh(), q_songsong()],
            [q_hanglop(9), q_tonghieu(), q_3buoc(), q_goc(), q_yenta(), q_congtru(100000, 999999), q_chanle()]]),
    dict(t='Phép nhân, phép chia', s='Nhân với số có một chữ số; chia cho số có một chữ số; nhân, chia với 10, 100, 1 000; tính chất của phép nhân; nhân một số với một tổng, một hiệu.',
         ls=['Nhân với số có một chữ số', 'Chia cho số có một chữ số', 'Nhân, chia với 10, 100, 1 000…', 'Tính chất giao hoán, kết hợp của phép nhân', 'Nhân một số với một tổng, một hiệu', 'Luyện tập chung'],
         L=[[q_nhan1()], [q_chia1()], [q_nhan10()], [q_tinhchatnhan()], [q_nhantong()],
            [q_nhan1(), q_chia1(), q_nhan10(), q_tinhchatnhan(), q_nhantong()]]),
    dict(t='Nhân, chia với số có hai chữ số. Thống kê', s='Nhân, chia với số có hai chữ số; số trung bình cộng; bài toán rút về đơn vị; dãy số liệu, biểu đồ cột; số lần xuất hiện của một sự kiện.',
         ls=['Nhân với số có hai chữ số', 'Chia cho số có hai chữ số', 'Tìm số trung bình cộng', 'Bài toán rút về đơn vị', 'Dãy số liệu. Biểu đồ cột', 'Số lần xuất hiện của một sự kiện'],
         L=[[q_nhan2()], [q_chia2()], [q_tbc()], [q_rutdonvi()], [q_bieudo(), q_dayso_lieu()], [q_solan()]]),
    dict(t='Phân số', s='Khái niệm phân số; phân số và phép chia số tự nhiên; tính chất cơ bản, rút gọn phân số; quy đồng mẫu số; so sánh phân số.',
         ls=['Khái niệm phân số', 'Phân số và phép chia số tự nhiên', 'Tính chất cơ bản. Rút gọn phân số', 'Quy đồng mẫu số các phân số', 'So sánh phân số', 'Luyện tập chung'],
         L=[[q_khainiem()], [q_ps_chia()], [q_rutgon()], [q_quydong()], [q_sosanh_ps()],
            [q_khainiem(), q_ps_chia(), q_rutgon(), q_quydong(), q_sosanh_ps()]]),
    dict(t='Phép tính với phân số. Ôn tập cuối năm', s='Cộng, trừ, nhân, chia phân số; tìm phân số của một số; ôn tập cả năm.',
         ls=['Phép cộng phân số', 'Phép trừ phân số', 'Phép nhân phân số', 'Phép chia phân số', 'Tìm phân số của một số', 'Tổng ôn lên lớp 5'],
         L=[[q_congps('+'), q_ps_word('+')], [q_congps('−'), q_ps_word('−')], [q_nhanps()], [q_chiaps()], [q_psmotso()],
            [q_trieu(), q_nhan2(), q_chia2(), q_tbc(), q_tonghieu(), q_congps('+'), q_congps('−'), q_nhanps(), q_psmotso(), q_goc(), q_bieudo()]]),
]

BANK_N = 20
SEED = 2026092504


NUM_RE = re.compile(r'(?<![\d/.,])(?<!năm )(?<!Năm )(\d{4,})(?![\d/])')


def grp(t):
    return NUM_RE.sub(lambda m: fmt(int(m.group(1))), t) if isinstance(t, str) else t


def tidy(q):
    """Viết mọi số từ 4 chữ số trở lên theo nhóm 3 chữ số (trừ số chỉ năm)."""
    for k in ('prompt', 'big', 'explain'):
        if k in q:
            q[k] = grp(q[k])
    if q['type'] == 'mc':
        q['answer'] = grp(q['answer']); q['options'] = [grp(o) for o in q['options']]
        if 'fixed' in q:
            q['fixed'] = [grp(o) for o in q['fixed']]
    if q['type'] == 'order':
        q['answer'] = [grp(o) for o in q['answer']]; q['items'] = [grp(o) for o in q['items']]
    return q


def build():
    R.seed(SEED)
    bank = []
    for W in WEEKS:
        bank.append([[tidy(q) for q in fill15(list(L), n=BANK_N, tries=4000)] for L in W['L']])
    meta = [{'t': W['t'], 's': W['s'], 'ls': W['ls']} for W in WEEKS]
    return bank, meta


def q_ct_word():
    def g():
        r = rnd(0, 3)
        if r == 0:
            a = rnd(100000, 500000); b = rnd(10000, 90000)
            return inp('giaitoan', f'Năm trước một huyện có {fmt(a)} người. Năm nay số dân tăng thêm {fmt(b)} người. Hỏi năm nay huyện đó có bao nhiêu người?', a + b, unit='người', icon='🏘️',
                       explain=sol([f'{fmt(a)} + {fmt(b)} = {fmt(a+b)} (người)'], a + b, 'người'))
        if r == 1:
            a = rnd(200000, 900000); b = rnd(50000, a - 10000)
            return inp('giaitoan', f'Một nhà máy sản xuất được {fmt(a)} chai nước, đã bán {fmt(b)} chai. Hỏi nhà máy còn lại bao nhiêu chai nước?', a - b, unit='chai', icon='🍶',
                       explain=sol([f'{fmt(a)} − {fmt(b)} = {fmt(a-b)} (chai)'], a - b, 'chai'))
        if r == 2:
            a = rnd(10000, 60000); d = rnd(1000, 9000); b = a + d
            return inp('giaitoan', f'Tháng Một cửa hàng bán được {fmt(a)} quyển sách, tháng Hai bán nhiều hơn tháng Một {fmt(d)} quyển. Hỏi cả hai tháng bán được bao nhiêu quyển sách?', a + b, unit='quyển', icon='📚',
                       explain=sol([f'Tháng Hai: {fmt(a)} + {fmt(d)} = {fmt(b)} (quyển)', f'Cả hai tháng: {fmt(a)} + {fmt(b)} = {fmt(a+b)} (quyển)'], a + b, 'quyển'))
        a = rnd(100000, 999999); b = rnd(100000, 999999); c = rnd(1000, 99999)
        if R.random() < .5:
            v = a + b - c
            return mc('congtru', f'Giá trị của biểu thức {fmt(a)} + {fmt(b)} − {fmt(c)} là:', fmt(v), [fmt(v + 1000), fmt(v - 100)], explain=f'{fmt(a)} + {fmt(b)} = {fmt(a+b)}; {fmt(a+b)} − {fmt(c)} = {fmt(v)}.')
        x = rnd(100000, 999999); y = rnd(10000, x - 1)
        return inp('congtru', 'Tìm số thích hợp thay cho dấu ?:', x - y, **BIG(f'{fmt(y)} + ? = {fmt(x)}'), explain=f'{fmt(x)} − {fmt(y)} = {fmt(x-y)}.')
    return g


def q_gh_mc():
    def g():
        a, b, c = rnd(100, 999), rnd(100, 999), rnd(100, 999)
        good = f'{a} + ({b} + {c})'
        return mc('congtru', f'Biểu thức nào có giá trị bằng ({a} + {b}) + {c}?', good, [f'{a} + {b} − {c}', f'({a} + {b}) × {c}'], explain='Tính chất kết hợp: (a + b) + c = a + (b + c).')
    return g


def q_ps_word2():
    def g():
        r = rnd(0, 2)
        if r == 0:
            n, d = rnd(1, 4), rnd(2, 6); k = rnd(2, 6)
            if n >= d or gcd(n, d) != 1:
                return None
            v = F(n, d) * k
            return mc('phanso', f'Mỗi chai chứa {n}/{d} l nước cam. Hỏi {k} chai như thế chứa bao nhiêu lít nước cam?', red(v) + ' l', [x + ' l' for x in fr_wrong(v, [(n * k, d * k), (n + k, d), (n, d * k)])], icon='🍊',
                      explain=f'{n}/{d} × {k} = {n*k}/{d} = {red(v)} (l).')
        if r == 1:
            n, d = rnd(1, 5), rnd(2, 8); k = rnd(2, 5)
            if n >= d:
                return None
            v = F(n, d) / k
            return mc('phanso', f'Có {n}/{d} kg kẹo chia đều cho {k} bạn. Hỏi mỗi bạn được bao nhiêu ki-lô-gam kẹo?', red(v) + ' kg', [x + ' kg' for x in fr_wrong(v, [(n * k, d), (n, d + k), (k, d)])], icon='🍬',
                      explain=f'{n}/{d} : {k} = {n}/{d*k} = {red(v)} (kg).')
        a, b = rnd(2, 9), rnd(2, 9)
        if gcd(a, b) != 1:
            return None
        v = F(a, b) * F(b, a)
        return mc('phanso', f'Tích của {a}/{b} và {b}/{a} bằng bao nhiêu?', '1', fr_wrong(v, [(a * a, b * b), (a + b, a * b), (2, 1)]), explain='Tích của một phân số với phân số đảo ngược của nó bằng 1.') if a != b else None
    return g


WEEKS[0]['L'][1].append(q_ct_word())
WEEKS[2]['L'][3].append(q_ct_word())
WEEKS[2]['L'][4].append(q_gh_mc())
WEEKS[7]['L'][2].append(q_ps_word2())
WEEKS[7]['L'][3].append(q_ps_word2())


if __name__ == '__main__':
    b, m = build()
    print(sum(len(d) for w in b for d in w))

