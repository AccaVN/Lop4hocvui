"""Dựng Học Vui Lớp 4 từ khung app Học Vui Lớp 2 (một lần).
Cách chạy:  SRC=<thư mục Lop2hocvui-main> DST=<thư mục ra> python3 build4.py
Sau này chỉ cần sửa câu hỏi rồi chạy update_banks.py."""
import json, os, re, shutil, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from m4b import build as build_math
from tvbank4 import build_tv
from en4 import build_en
from common import R

SRC = os.environ.get('SRC', '../Lop2hocvui-main')
DST = os.environ.get('DST', './out')
J = lambda o: json.dumps(o, ensure_ascii=False, separators=(',', ':'))

mb, meta = build_math()
R.seed(4202609); tvu, tvb = build_tv()
R.seed(4202610); enu, enb = build_en()

if os.path.exists(DST):
    shutil.rmtree(DST)
shutil.copytree(SRC, DST, ignore=shutil.ignore_patterns('.git', 'node_modules', 'gen-lop2', '.cache', '__pycache__', '.env'))
P = DST + '/public/index.html'
s = open(P, encoding='utf-8').read()
L = s.split('\n')


def setline(prefix, new):
    idx = [i for i, l in enumerate(L) if l.startswith(prefix)]
    assert len(idx) == 1, (prefix, idx)
    L[idx[0]] = new


setline('const MATH_BANK=', 'const MATH_BANK=' + J(mb) + ';')
setline('const EN_UNITS=', 'const EN_UNITS=' + J(enu) + ';')
setline('const EN_BANK=', 'const EN_BANK=' + J(enb) + ';')
setline('const TV_UNITS=', 'const TV_UNITS=' + J(tvu) + ';')
setline('const TV_BANK=', 'const TV_BANK=' + J(tvb) + ';')
setline('const WEEKS=', 'const WEEKS=' + J(meta) + ';')
setline('const TV_LV=', "const TV_LV=[{n:'Đọc hiểu',i:'📖'},{n:'Luyện từ, chính tả',i:'✍️'},{n:'Luyện câu, dấu câu',i:'📝'}];")
setline('const EN_LV=', "const EN_LV=[{n:'Vocabulary',i:'📚'},{n:'Listening',i:'🎧'},{n:'Sentences',i:'💬'}];")
# Tính nhẩm siêu tốc theo chương trình lớp 4
setline('function speedQ(', "function speedQ(){const r=Math.random();"
        "if(isUnlocked(24)&&r<.3){if(Math.random()<.5){const a=rnd(11,99),p=Math.random()<.5?10:100;return{t:`${a} × ${p}`,a:a*p};}const a=rnd(11,49),k=rnd(2,5);return{t:`${a} × ${k}`,a:a*k};}"
        "if(isUnlocked(12)&&r<.6){const a=rnd(1,9)*100,b=rnd(1,9)*100;if(Math.random()<.5)return{t:`${a} + ${b}`,a:a+b};return{t:`${Math.max(a,b)} − ${Math.min(a,b)}`,a:Math.abs(a-b)};}"
        "const k=rnd(2,9),n=rnd(2,10);return Math.random()<.5?{t:`${k} × ${n}`,a:k*n}:{t:`${k*n} : ${k}`,a:n};}")
s = '\n'.join(L)


def rep(old, new, count=1):
    global s
    c = s.count(old)
    assert c == count, (old[:90], c)
    s = s.replace(old, new)


# ----- CSS: phân số, bảng số liệu -----
CSS = """
/* lớp 4 */
.fr{display:inline-flex;flex-direction:column;align-items:center;vertical-align:middle;line-height:1.05;margin:0 .08em;font-size:.86em}
.fr b{display:block;padding:0 .12em;font-weight:inherit}.fr b:first-child{border-bottom:.09em solid currentColor}
.opt .fr{font-size:.95em}.big .fr{font-size:.8em}
.fb-ans .fr,.fb-exp .fr{font-size:.9em}
"""
rep("/* lớp 2 */", "/* lớp 2 */" + CSS)

# ----- Hiển thị phân số, số nhiều chữ số -----
rep("function setSlot(v){const s=$('#slot');if(s){s.textContent=v||'?';s.classList.toggle('filled',!!v);}}",
    "const fmtNum=v=>{v=String(v);return /^\\d{4,}$/.test(v)?v.replace(/\\B(?=(\\d{3})+(?!\\d))/g,'\\u00a0'):v;};\n"
    "const frH=h=>String(h).replace(/(\\d+|\\?)\\/(\\d+|\\?)/g,'<span class=\"fr\"><b>$1</b><b>$2</b></span>');\n"
    "const qH=(q,t)=>q&&q.skill==='phanso'?frH(esc(t)):esc(t);\n"
    "function setSlot(v){const s=$('#slot');if(s){s.innerHTML=v?frH(esc(fmtNum(v))):'?';s.classList.toggle('filled',!!v);}}")
rep("let big='';if(q.big){big=esc(q.big);", "let big='';if(q.big){big=qH(q,q.big);")
rep("<div class=\"prompt\">${q.icon?`<span class=\"picon\" aria-hidden=\"true\">${q.icon}</span>`:''}${esc(q.prompt)}</div>",
    "<div class=\"prompt\">${q.icon?`<span class=\"picon\" aria-hidden=\"true\">${q.icon}</span>`:''}${qH(q,q.prompt)}</div>")
rep("${q.options.map((o,k)=>`<button class=\"opt\" data-k=\"${k}\">${esc(o)}</button>`).join('')}",
    "${q.options.map((o,k)=>`<button class=\"opt\" data-k=\"${k}\">${qH(q,o)}</button>`).join('')}")
rep("<div class=\"fb-ans\">Đáp án đúng: <b>${esc(ansText(q))}</b></div>", "<div class=\"fb-ans\">Đáp án đúng: <b>${qH(q,ansText(q))}</b></div>")
rep("<div class=\"fb-exp\">${esc(q.explain)}</div>", "<div class=\"fb-exp\">${qH(q,q.explain)}</div>")
rep("q.type==='input'?q.answer+(q.unit?' '+q.unit:''):q.answer;", "q.type==='input'?fmtNum(q.answer)+(q.unit?' '+q.unit:''):q.answer;")
# ô nhập: cho phép tới 9 chữ số (lớp triệu)
rep("else if(Q.typed.length<4)Q.typed=(Q.typed==='0'?'':Q.typed)+k;", "else if(Q.typed.length<9)Q.typed=(Q.typed==='0'?'':Q.typed)+k;")
rep("if(q.type==='input'&&(dig||k==='Backspace')){typeKey(dig?k:'B',()=>{setSlot(Q.typed);", "if(q.type==='input'&&(dig||k==='Backspace')){typeKey(dig?k:'B',()=>{setSlot(Q.typed);")
# giọng đọc: số có nhóm chữ số, phân số, đơn vị đo
rep("const cleanSpeech=t=>String(t==null?'':t).replace(EMO_RE,' ')",
    "const cleanSpeech=t=>String(t==null?'':t).replace(/(\\d)[ \\u00a0](?=\\d{3}(?!\\d))/g,'$1').replace(/(\\d+)\\/(\\d+)/g,'$1 phần $2')"
    ".replace(/mm²/g,' mi-li-mét vuông').replace(/cm²/g,' xăng-ti-mét vuông').replace(/dm²/g,' đề-xi-mét vuông').replace(/m²/g,' mét vuông').replace(/°/g,' độ')"
    ".replace(/(\\d|\\)) : (?=\\d)/g,'$1 chia ').replace(/ × /g,' nhân ').replace(/ − /g,' trừ ').replace(EMO_RE,' ')")

# ----- Kỹ năng -----
rep("const SKILLS={", "const SKILLS={phanso:'Phân số',")
rep("const TOAN=['so','congtru','hinhhoc','doluong','giaitoan','nhanchia','thongke'];", "const TOAN=['so','congtru','nhanchia','phanso','hinhhoc','doluong','giaitoan','thongke'];")
rep("doluong:'Đo lường, giờ, lịch, tiền'", "doluong:'Đo lường: khối lượng, diện tích, thời gian'")
rep("thongke:'Thống kê, xác suất'", "thongke:'Thống kê, trung bình cộng'")
rep("const TV_LEVEL_INFO=[{d:'Bài 1',n:'Đọc hiểu',i:'📖'},{d:'Bài 2',n:'Chính tả & Từ ngữ',i:'✍️'},{d:'Bài 3',n:'Câu & Viết',i:'📝'}];",
    "const TV_LEVEL_INFO=[{d:'Bài 1',n:'Đọc hiểu',i:'📖'},{d:'Bài 2',n:'Luyện từ & Chính tả',i:'✍️'},{d:'Bài 3',n:'Luyện câu & Dấu câu',i:'📝'}];")

# ----- Khóa lưu trữ (tách riêng với lớp 1, 2, 3) -----
rep("const KEY='lop2_hoc_vui_v1';", "const KEY='lop4_hoc_vui_v1';")
s = s.replace("'hv2_token'", "'hv4_token'").replace("'hv2_role'", "'hv4_role'").replace("'hv2_tts_cfg'", "'hv4_tts_cfg'")

# ----- Chữ hiển thị -----
rep("<title>Học Vui Lớp 2</title>", "<title>Học Vui Lớp 4</title>")
rep("<h1>Học Vui Lớp 2</h1>", "<h1>Học Vui Lớp 4</h1>")
rep("'Huyền thoại lớp 2'", "'Huyền thoại lớp 4'")
rep('"Huyền thoại lớp 2"', '"Huyền thoại lớp 4"')
rep("8 chặng của chương trình lớp 2", "8 chặng của chương trình lớp 4")
rep("Lớp 2 nên để chậm 10–20%", "Lớp 4 nên để bình thường hoặc chậm 5–10%")
rep("Đi hết 8 chặng là con đã học xong Toán lớp 2 và sẵn sàng lên lớp 3! 🎓", "Đi hết 8 chặng là con đã học xong Toán lớp 4 và sẵn sàng lên lớp 5! 🎓")
rep("16 bài theo sách Tiếng Anh 2 Global Success (Kết nối tri thức). Mỗi bài có 3 phần: Vocabulary, Listen & Phonics, Sentences.",
    "16 bài theo sách Tiếng Anh 4 Global Success (20 unit, một số unit gộp đôi). Mỗi bài có 3 phần: Vocabulary, Listening, Sentences.")
rep("Hoàn thành 16 bài, con đã học xong Tiếng Anh lớp 2! 🌟", "Hoàn thành 16 bài, con đã học xong Tiếng Anh lớp 4! 🌟")
rep("16 chặng theo sách Tiếng Việt 2 Kết nối tri thức: 8 chặng Tập 1 và 8 chặng Tập 2. Mỗi chặng có 3 bài: Đọc hiểu, Từ ngữ – chính tả, Câu – dấu câu.",
    "16 chặng theo sách Tiếng Việt 4 Kết nối tri thức: 8 chặng Tập 1 và 8 chặng Tập 2. Mỗi chặng có 3 bài: Đọc hiểu, Luyện từ – chính tả, Luyện câu – dấu câu.")
rep("Hoàn thành 16 chặng, con đã học xong Tiếng Việt lớp 2! 📚", "Hoàn thành 16 chặng, con đã học xong Tiếng Việt lớp 4! 📚")

# Kiểm tra: không còn nhắc lớp 2 ở phần giao diện (bỏ qua các dòng dữ liệu cũ không dùng)
code = '\n'.join(l for l in s.split('\n') if len(l) < 3000)
left = sorted(set(m.group(0) for m in re.finditer(r'(Học Vui Lớp 2|lop2_|hv2_|Tiếng Anh 2 |Tiếng Việt 2 |học xong [^ ]+ lớp 2)', code)))
assert not left, left
open(P, 'w', encoding='utf-8').write(s)

# ----- Âm thanh thu sẵn: chỉ giữ các câu còn dùng -----
vd = json.load(open(SRC + '/public/voice-data.json', encoding='utf-8'))
keep = {k: v for k, v in vd.items() if k in s}
json.dump(keep, open(DST + '/public/voice-data.json', 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))


# ----- Backend / tài liệu -----
def sub_file(path, pairs):
    p = DST + '/' + path; t = open(p, encoding='utf-8').read()
    for a, b in pairs:
        assert a in t, (path, a); t = t.replace(a, b)
    open(p, 'w', encoding='utf-8').write(t)


sub_file('package.json', [('"hocvui2-backend"', '"hocvui4-backend"')])
sub_file('package-lock.json', [('"hocvui2-backend"', '"hocvui4-backend"')])
sub_file('schema.sql', [('Học Vui Lớp 2', 'Học Vui Lớp 4')])
# công cụ sinh câu hỏi
tools = DST + '/tools/gen-lop4'
os.makedirs(tools, exist_ok=True)
for f in ['common.py', 'm4a.py', 'm4b.py', 'check_m4.py', 'tv4a.py', 'tv4b.py', 'tv4c.py', 'tv4d.py', 'tvbank4.py', 'en4.py', 'build4.py', 'update_banks.py']:
    shutil.copy(os.path.join(HERE, f), tools)
print('clips kept', len(keep), '/', len(vd), '| html bytes', len(s.encode()))
