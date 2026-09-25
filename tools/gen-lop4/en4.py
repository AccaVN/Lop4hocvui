"""English 4 — bám mục lục Tiếng Anh 4 Global Success (20 unit, gộp vào 16 bài của app).
Mỗi bài: từ vựng (en, emoji, nghĩa), câu mẫu (en, nghĩa, emoji), hỏi – đáp (câu hỏi, câu trả lời đúng)."""
from common import *

UN = [
 ('Unit 1', 'My friends', 'Bạn bè của em',
  [('America', '🇺🇸', 'nước Mỹ'), ('Australia', '🇦🇺', 'nước Úc'), ('Britain', '🇬🇧', 'nước Anh'), ('Japan', '🇯🇵', 'Nhật Bản'), ('Malaysia', '🇲🇾', 'Ma-lai-xi-a'), ('Singapore', '🇸🇬', 'Xin-ga-po'), ('Thailand', '🇹🇭', 'Thái Lan'), ('Viet Nam', '🇻🇳', 'Việt Nam')],
  [("I'm from Viet Nam.", 'Tớ đến từ Việt Nam.', '🇻🇳'), ("She's from Japan.", 'Bạn ấy đến từ Nhật Bản.', '🇯🇵'), ("He's from Australia.", 'Bạn ấy đến từ Úc.', '🇦🇺'),
   ('Where are you from?', 'Bạn đến từ đâu?', '🌏'), ("Nice to meet you.", 'Rất vui được gặp bạn.', '🤝'), ('This is my friend Mary.', 'Đây là bạn tớ, Mary.', '👧')],
  [('Where are you from?', "I'm from Thailand."), ("What's your name?", 'My name is Nam.'), ('Where is she from?', "She's from Singapore."), ('Who is this?', "It's my friend Ben.")]),
 ('Unit 2', 'Time and daily routines', 'Thời gian và thói quen hằng ngày',
  [('get up', '⏰', 'thức dậy'), ('have breakfast', '🍳', 'ăn sáng'), ('go to school', '🏫', 'đi học'), ('have lunch', '🍱', 'ăn trưa'), ('have dinner', '🍲', 'ăn tối'), ('go to bed', '🛏️', 'đi ngủ'), ('seven o\'clock', '🕖', 'bảy giờ đúng'), ('nine fifteen', '🕘', 'chín giờ mười lăm')],
  [("It's seven o'clock.", 'Bây giờ là bảy giờ đúng.', '🕖'), ('I get up at six.', 'Tớ thức dậy lúc sáu giờ.', '⏰'), ('I go to school at seven.', 'Tớ đi học lúc bảy giờ.', '🏫'),
   ('What time is it?', 'Bây giờ là mấy giờ?', '🕰️'), ('I go to bed at nine thirty.', 'Tớ đi ngủ lúc chín giờ ba mươi.', '🛏️'), ('I have lunch at eleven thirty.', 'Tớ ăn trưa lúc mười một giờ ba mươi.', '🍱')],
  [('What time is it?', "It's ten o'clock."), ('What time do you get up?', 'I get up at six.'), ('What time do you go to bed?', 'I go to bed at nine.'), ('What time do you have breakfast?', 'I have breakfast at six thirty.')]),
 ('Unit 3', 'My week', 'Tuần của em',
  [('Monday', '1️⃣', 'thứ Hai'), ('Tuesday', '2️⃣', 'thứ Ba'), ('Wednesday', '3️⃣', 'thứ Tư'), ('Thursday', '4️⃣', 'thứ Năm'), ('Friday', '5️⃣', 'thứ Sáu'), ('Saturday', '6️⃣', 'thứ Bảy'), ('Sunday', '☀️', 'Chủ nhật'), ('help my parents', '🧹', 'giúp bố mẹ')],
  [("It's Monday today.", 'Hôm nay là thứ Hai.', '1️⃣'), ('I study at school on Mondays.', 'Tớ học ở trường vào các ngày thứ Hai.', '🏫'), ('I help my parents on Saturdays.', 'Tớ giúp bố mẹ vào thứ Bảy.', '🧹'),
   ('I listen to music on Sundays.', 'Tớ nghe nhạc vào Chủ nhật.', '🎧'), ('What day is it today?', 'Hôm nay là thứ mấy?', '📅'), ('I play the piano on Fridays.', 'Tớ chơi đàn piano vào thứ Sáu.', '🎹')],
  [('What day is it today?', "It's Wednesday."), ('What do you do on Saturdays?', 'I help my parents.'), ('When do you play the piano?', 'On Fridays.'), ('Do you go to school on Sundays?', "No, I don't.")]),
 ('Unit 4', 'My birthday party', 'Tiệc sinh nhật của em',
  [('January', '❄️', 'tháng Một'), ('March', '🌸', 'tháng Ba'), ('June', '🌞', 'tháng Sáu'), ('October', '🎃', 'tháng Mười'), ('December', '🎄', 'tháng Mười Hai'), ('chips', '🍟', 'khoai tây chiên'), ('grapes', '🍇', 'quả nho'), ('lemonade', '🍋', 'nước chanh')],
  [("When's your birthday?", 'Sinh nhật bạn vào khi nào?', '🎂'), ("It's in June.", 'Vào tháng Sáu.', '🌞'), ('I want some grapes.', 'Tớ muốn ăn một ít nho.', '🍇'),
   ('I want some chips.', 'Tớ muốn ăn một ít khoai tây chiên.', '🍟'), ('Would you like some lemonade?', 'Bạn có muốn uống nước chanh không?', '🍋'), ('Happy birthday to you!', 'Chúc mừng sinh nhật bạn!', '🎉')],
  [("When's your birthday?", "It's in October."), ('What do you want to eat?', 'I want some chips.'), ('What do you want to drink?', 'I want some lemonade.'), ('Would you like some grapes?', 'Yes, please.')]),
 ('Unit 5', 'Things we can do', 'Những việc chúng ta có thể làm',
  [('ride a bike', '🚲', 'đi xe đạp'), ('ride a horse', '🐎', 'cưỡi ngựa'), ('roller skate', '🛼', 'trượt pa-tanh'), ('swim', '🏊', 'bơi'), ('cook', '👩‍🍳', 'nấu ăn'), ('draw', '🎨', 'vẽ'), ('dance', '💃', 'nhảy múa'), ('play the guitar', '🎸', 'chơi đàn ghi-ta')],
  [('I can swim.', 'Tớ biết bơi.', '🏊'), ("I can't ride a horse.", 'Tớ không biết cưỡi ngựa.', '🐎'), ('She can dance.', 'Bạn ấy biết nhảy múa.', '💃'),
   ('Can you ride a bike?', 'Bạn có biết đi xe đạp không?', '🚲'), ('He can play the guitar.', 'Bạn ấy biết chơi đàn ghi-ta.', '🎸'), ('What can you do?', 'Bạn có thể làm gì?', '🤔')],
  [('Can you swim?', 'Yes, I can.'), ('What can you do?', 'I can draw.'), ('Can she cook?', "No, she can't."), ('What can he do?', 'He can roller skate.')]),
 ('Unit 6', 'Our school facilities', 'Cơ sở vật chất trường em',
  [('school', '🏫', 'trường học'), ('library', '📚', 'thư viện'), ('computer room', '💻', 'phòng máy tính'), ('art room', '🖌️', 'phòng mĩ thuật'), ('music room', '🎼', 'phòng âm nhạc'), ('playground', '🛝', 'sân chơi'), ('garden', '🌷', 'khu vườn'), ('gym', '🏀', 'phòng thể dục')],
  [('This is my school.', 'Đây là trường của tớ.', '🏫'), ('The library is on the second floor.', 'Thư viện ở tầng hai.', '📚'), ('Is there a garden?', 'Có khu vườn không?', '🌷'),
   ('Yes, there is.', 'Có.', '👍'), ('My school has a big playground.', 'Trường tớ có sân chơi lớn.', '🛝'), ("Let's go to the computer room.", 'Chúng mình cùng đến phòng máy tính nhé.', '💻')],
  [('Where is the library?', "It's on the second floor."), ('Is there a gym at your school?', 'Yes, there is.'), ('How many classrooms are there?', 'There are twenty classrooms.'), ("What's your school like?", "It's big and beautiful.")]),
 ('Unit 7 – 8', 'Our timetables · My favourite subjects', 'Thời khoá biểu · Môn học em yêu thích',
  [('Maths', '➗', 'môn Toán'), ('English', '🔤', 'môn Tiếng Anh'), ('Vietnamese', '📖', 'môn Tiếng Việt'), ('Science', '🔬', 'môn Khoa học'), ('Music', '🎵', 'môn Âm nhạc'), ('Art', '🎨', 'môn Mĩ thuật'), ('PE', '⚽', 'môn Thể dục'), ('IT', '🖥️', 'môn Tin học')],
  [('I have Maths today.', 'Hôm nay tớ có môn Toán.', '➗'), ('We have English on Mondays.', 'Chúng tớ học Tiếng Anh vào thứ Hai.', '🔤'), ('My favourite subject is Art.', 'Môn học yêu thích của tớ là Mĩ thuật.', '🎨'),
   ('I like Science.', 'Tớ thích môn Khoa học.', '🔬'), ('I want to be a music teacher.', 'Tớ muốn trở thành giáo viên âm nhạc.', '🎵'), ('What subjects do you have today?', 'Hôm nay bạn có những môn gì?', '📅')],
  [('What subjects do you have today?', 'I have Maths and English.'), ('When do you have PE?', 'I have it on Tuesdays.'), ("What's your favourite subject?", "It's Music."), ('Why do you like Science?', "Because it's interesting.")]),
 ('Unit 9', 'Our sports day', 'Ngày hội thể thao',
  [('sports day', '🏅', 'ngày hội thể thao'), ('running', '🏃', 'chạy'), ('jumping', '🤾', 'nhảy'), ('swimming', '🏊', 'bơi'), ('playing football', '⚽', 'chơi bóng đá'), ('playing basketball', '🏀', 'chơi bóng rổ'), ('playing badminton', '🏸', 'chơi cầu lông'), ('playing table tennis', '🏓', 'chơi bóng bàn')],
  [("When's sports day?", 'Ngày hội thể thao là khi nào?', '🏅'), ("It's in November.", 'Vào tháng Mười Một.', '🍂'), ("I'm running.", 'Tớ đang chạy.', '🏃'),
   ("He's playing basketball.", 'Bạn ấy đang chơi bóng rổ.', '🏀'), ("They're playing football.", 'Họ đang chơi bóng đá.', '⚽'), ('What are you doing?', 'Bạn đang làm gì thế?', '❓')],
  [("When's sports day?", "It's in November."), ('What are you doing?', "I'm swimming."), ("What's she doing?", "She's playing badminton."), ('What are they doing?', "They're playing table tennis.")]),
 ('Unit 10', 'Our summer holidays', 'Kì nghỉ hè của chúng em',
  [('beach', '🏖️', 'bãi biển'), ('countryside', '🌾', 'vùng quê'), ('campsite', '🏕️', 'khu cắm trại'), ('mountains', '⛰️', 'núi'), ('swam in the sea', '🌊', 'đã bơi ở biển'), ('built sandcastles', '🏰', 'đã xây lâu đài cát'), ('took photos', '📷', 'đã chụp ảnh'), ('visited', '🧳', 'đã đến thăm')],
  [('Where were you last summer?', 'Hè năm ngoái bạn ở đâu?', '☀️'), ('I was at the beach.', 'Tớ đã ở bãi biển.', '🏖️'), ('I was in the countryside.', 'Tớ đã ở vùng quê.', '🌾'),
   ('I built sandcastles.', 'Tớ đã xây lâu đài cát.', '🏰'), ('We took photos.', 'Chúng tớ đã chụp ảnh.', '📷'), ('What did you do there?', 'Bạn đã làm gì ở đó?', '❓')],
  [('Where were you last summer?', 'I was at the campsite.'), ('What did you do there?', 'I swam in the sea.'), ('Where was he last summer?', 'He was in the mountains.'), ('Did you take photos?', 'Yes, I did.')]),
 ('Unit 11', 'My home', 'Nhà của em',
  [('street', '🛣️', 'đường phố'), ('road', '🛤️', 'con đường'), ('city', '🏙️', 'thành phố'), ('village', '🏘️', 'ngôi làng'), ('busy', '🚦', 'đông đúc'), ('quiet', '🤫', 'yên tĩnh'), ('noisy', '📢', 'ồn ào'), ('beautiful', '🌺', 'đẹp')],
  [('Where do you live?', 'Bạn sống ở đâu?', '🏠'), ('I live in the city.', 'Tớ sống ở thành phố.', '🏙️'), ('I live on Tran Hung Dao Street.', 'Tớ sống ở phố Trần Hưng Đạo.', '🛣️'),
   ("It's a quiet village.", 'Đó là một ngôi làng yên tĩnh.', '🤫'), ('My street is busy.', 'Phố nhà tớ đông đúc.', '🚦'), ("What's it like?", 'Nơi đó như thế nào?', '🤔')],
  [('Where do you live?', 'I live in a village.'), ("What's your street like?", "It's busy and noisy."), ('Where does she live?', 'She lives in the city.'), ('Do you live in the city?', 'No, I live in the countryside.')]),
 ('Unit 12', 'Jobs', 'Nghề nghiệp',
  [('farmer', '👨‍🌾', 'nông dân'), ('nurse', '👩‍⚕️', 'y tá'), ('doctor', '🧑‍⚕️', 'bác sĩ'), ('teacher', '🧑‍🏫', 'giáo viên'), ('driver', '🚕', 'tài xế'), ('worker', '👷', 'công nhân'), ('cook', '🧑‍🍳', 'đầu bếp'), ('police officer', '👮', 'cảnh sát')],
  [('What does your father do?', 'Bố bạn làm nghề gì?', '👨'), ("He's a farmer.", 'Bố tớ là nông dân.', '👨‍🌾'), ("She's a nurse.", 'Mẹ tớ là y tá.', '👩‍⚕️'),
   ('He works on a farm.', 'Bố tớ làm việc ở nông trại.', '🚜'), ('She works in a hospital.', 'Mẹ tớ làm việc ở bệnh viện.', '🏥'), ('I want to be a teacher.', 'Tớ muốn trở thành giáo viên.', '🧑‍🏫')],
  [('What does your mother do?', "She's a teacher."), ('Where does he work?', 'He works in a factory.'), ('What does your father do?', "He's a driver."), ('Is your father a doctor?', "No, he isn't.")]),
 ('Unit 13', 'Appearance', 'Ngoại hình',
  [('tall', '🦒', 'cao'), ('short', '🐭', 'thấp'), ('slim', '🧍', 'mảnh khảnh'), ('big', '🐘', 'to lớn'), ('young', '👶', 'trẻ'), ('old', '👴', 'già'), ('long hair', '👱‍♀️', 'tóc dài'), ('big eyes', '👀', 'mắt to')],
  [('What does he look like?', 'Bạn ấy trông như thế nào?', '🤔'), ("He's tall and slim.", 'Bạn ấy cao và mảnh khảnh.', '🧍'), ('She has long hair.', 'Bạn ấy có mái tóc dài.', '👱‍♀️'),
   ('My grandfather is old.', 'Ông tớ đã già.', '👴'), ('My brother is taller than me.', 'Anh tớ cao hơn tớ.', '📏'), ('She has big eyes.', 'Bạn ấy có đôi mắt to.', '👀')],
  [('What does your sister look like?', "She's short and slim."), ('What does he look like?', "He's tall and big."), ('Who is taller?', 'My brother is.'), ('Does she have long hair?', 'Yes, she does.')]),
 ('Unit 14 – 15', "Daily activities · My family's weekends", 'Hoạt động hằng ngày · Cuối tuần của gia đình',
  [('do morning exercise', '🤸', 'tập thể dục buổi sáng'), ('wash the clothes', '🧺', 'giặt quần áo'), ('cook dinner', '🍳', 'nấu bữa tối'), ('water the flowers', '🪴', 'tưới hoa'), ('clean the floor', '🧹', 'lau nhà'), ('cinema', '🎬', 'rạp chiếu phim'), ('swimming pool', '🏊', 'bể bơi'), ('shopping centre', '🛍️', 'trung tâm mua sắm')],
  [('I do morning exercise.', 'Tớ tập thể dục buổi sáng.', '🤸'), ('She cooks dinner in the evening.', 'Mẹ tớ nấu bữa tối vào buổi tối.', '🍳'), ('I water the flowers in the afternoon.', 'Tớ tưới hoa vào buổi chiều.', '🪴'),
   ('My father is at the cinema.', 'Bố tớ đang ở rạp chiếu phim.', '🎬'), ('We go to the swimming pool on Sundays.', 'Chúng tớ đi bể bơi vào Chủ nhật.', '🏊'), ('What do you do in the morning?', 'Bạn làm gì vào buổi sáng?', '🌅')],
  [('What do you do in the morning?', 'I do morning exercise.'), ('What does she do in the evening?', 'She cooks dinner.'), ('Where is your father on Saturdays?', "He's at the shopping centre."), ('What does he do there?', 'He watches films.')]),
 ('Unit 16 – 17', 'Weather · In the city', 'Thời tiết · Trong thành phố',
  [('sunny', '☀️', 'nắng'), ('rainy', '🌧️', 'mưa'), ('cloudy', '☁️', 'nhiều mây'), ('windy', '🌬️', 'có gió'), ('post office', '🏤', 'bưu điện'), ('bookshop', '📚', 'hiệu sách'), ('supermarket', '🛒', 'siêu thị'), ('turn left', '⬅️', 'rẽ trái')],
  [("What's the weather like today?", 'Thời tiết hôm nay thế nào?', '🌤️'), ("It's sunny.", 'Trời nắng.', '☀️'), ("It's rainy and cold.", 'Trời mưa và lạnh.', '🌧️'),
   ('Where is the post office?', 'Bưu điện ở đâu?', '🏤'), ('Go straight and turn left.', 'Đi thẳng rồi rẽ trái.', '⬅️'), ("It's next to the bookshop.", 'Nó ở cạnh hiệu sách.', '📚')],
  [("What's the weather like today?", "It's windy."), ('Where is the supermarket?', "It's opposite the park."), ('How can I get to the zoo?', 'Go straight and turn right.'), ('Is it cloudy today?', 'Yes, it is.')]),
 ('Unit 18', 'At the shopping centre', 'Ở trung tâm mua sắm',
  [('T-shirt', '👕', 'áo phông'), ('jeans', '👖', 'quần bò'), ('dress', '👗', 'váy liền'), ('jacket', '🧥', 'áo khoác'), ('shoes', '👟', 'đôi giày'), ('socks', '🧦', 'đôi tất'), ('hat', '👒', 'cái mũ'), ('scarf', '🧣', 'khăn quàng')],
  [('How much is the T-shirt?', 'Cái áo phông giá bao nhiêu?', '👕'), ("It's seventy thousand dong.", 'Nó giá bảy mươi nghìn đồng.', '💵'), ('I want to buy a jacket.', 'Tớ muốn mua một chiếc áo khoác.', '🧥'),
   ('How much are the shoes?', 'Đôi giày giá bao nhiêu?', '👟'), ('Can I help you?', 'Tôi có thể giúp gì cho bạn?', '🙋'), ('I like this dress.', 'Tớ thích chiếc váy này.', '👗')],
  [('How much is the hat?', "It's fifty thousand dong."), ('How much are the jeans?', "They're two hundred thousand dong."), ('Can I help you?', 'Yes, I want to buy a scarf.'), ('What colour is the dress?', "It's red.")]),
 ('Unit 19 – 20', 'The animal world · At the summer camp', 'Thế giới động vật · Ở trại hè',
  [('tiger', '🐯', 'con hổ'), ('giraffe', '🦒', 'hươu cao cổ'), ('crocodile', '🐊', 'cá sấu'), ('kangaroo', '🦘', 'chuột túi'), ('elephant', '🐘', 'con voi'), ('monkey', '🐒', 'con khỉ'), ('put up a tent', '⛺', 'dựng lều'), ('sing songs', '🎤', 'hát')],
  [('What animal is it?', 'Đó là con vật gì?', '❓'), ("It's a kangaroo.", 'Đó là con chuột túi.', '🦘'), ('The monkey can climb.', 'Con khỉ có thể leo trèo.', '🐒'),
   ('The elephant is big.', 'Con voi to lớn.', '🐘'), ("They're putting up a tent.", 'Họ đang dựng lều.', '⛺'), ("We're singing songs.", 'Chúng tớ đang hát.', '🎤')],
  [('What animal is it?', "It's a tiger."), ('What can the monkey do?', 'It can climb.'), ('Why do you like elephants?', "Because they're big and friendly."), ('What are they doing?', "They're putting up a tent.")]),
]


def units():
    return [{'lab': lab, 't': t, 'vn': vn, 'w': [list(w) for w in W], 'c': [list(c) for c in C]} for lab, t, vn, W, C, QA in UN]


def others(pool, w, n):
    c = [x for x in pool if x[0] != w[0] and x[1] != w[1] and x[2] != w[2]]
    return R.sample(c, n)


ALLW = [w for u in UN for w in u[3]]


def build_unit(u):
    lab, t, vn, W, C, QA = UN[u]
    D = [w for k in range(max(0, u - 3), u + 1) for w in UN[k][3]]  # từ của bài này và vài bài trước (làm phương án nhiễu)

    # ---------------- Bài 1: Vocabulary ----------------
    def picWord():
        w = pick(W); o = others(W, w, 2)
        return mc('en_vocab', 'What is this? (Đây là gì?)', w[0], [x[0] for x in o], visual=f'<div class="emo">{w[1]}</div>', voice=[['vi', 'Đây là gì?']], explain=f'{w[1]} = {w[0]} ({w[2]})')
    def wordPic():
        w = pick(W); o = others(W, w, 2)
        return mc('en_vocab', 'Choose the picture. (Chọn hình đúng)', w[1], [x[1] for x in o], big=w[0], bigSmall=len(w[0]) > 10 or None, emo=True, voice=[['vi', 'Chọn hình đúng'], ['en', w[0]]], explain=f'{w[0]} = {w[2]}')
    def meaning():
        w = pick(W); o = others(D, w, 2)
        return mc('en_vocab', 'What does it mean? (Từ này nghĩa là gì?)', w[2], [x[2] for x in o], big=w[0], bigSmall=len(w[0]) > 10 or None, voice=[['vi', 'Từ này nghĩa là gì?'], ['en', w[0]]])
    def viToEn():
        w = pick(W); o = others(D, w, 2)
        return mc('en_vocab', f'Choose the English word. (Chọn từ tiếng Anh): “{w[2]}”', w[0], [x[0] for x in o], voice=[['vi', f'Chọn từ tiếng Anh có nghĩa là {w[2]}']])
    ALL = {x[0] for x in ALLW}
    def missing():
        w = pick(W); word = w[0]
        idx = [i for i, ch in enumerate(word) if ch.isalpha() and i > 0]
        i = pick(idx); ch = word[i]
        pool = [c for c in 'aeioubcdghklmnprstwy' if c != ch.lower() and (word[:i] + c + word[i + 1:]) not in ALL]
        ws = R.sample(pool, 2)
        return mc('en_vocab', 'Find the missing letter. (Tìm chữ cái còn thiếu)', ch, ws, visual=f'<div class="emo sm">{w[1]}</div>', big=word[:i] + '_' + word[i + 1:], voice=[['vi', 'Tìm chữ cái còn thiếu'], ['en', word]], explain=f'{word} = {w[2]}')
    def spell():
        cand = [w for w in W if ' ' not in w[0] and '-' not in w[0] and 4 <= len(w[0]) <= 8 and len(set(w[0].lower())) == len(w[0])]
        if not cand:
            return None
        w = pick(cand)
        return ordq('en_vocab', 'Put the letters in order. (Sắp xếp các chữ cái thành từ đúng)', list(w[0]), visual=f'<div class="emo sm">{w[1]}</div>', voice=[['vi', 'Sắp xếp các chữ cái thành từ đúng']], explain=f'{w[0]} = {w[2]}')
    d0 = fill15([picWord, wordPic, meaning, viToEn, missing, spell], tries=2000)

    # ---------------- Bài 2: Listening ----------------
    def listenWord():
        w = pick(W); o = others(W, w, 2)
        return mc('en_listen', 'Listen and choose. (Nghe và chọn từ đúng)', w[0], [x[0] for x in o], voice=[['en', w[0]]], auto=True, explain=f'{w[0]} {w[1]} = {w[2]}')
    def listenPic():
        w = pick(W); o = others(W, w, 2)
        return mc('en_listen', 'Listen and choose the picture. (Nghe và chọn hình)', w[1], [x[1] for x in o], emo=True, voice=[['en', w[0]]], auto=True, explain=f'{w[0]} = {w[2]}')
    def listenMatch():
        w = pick(W); x = pick([y for y in W if y[1] != w[1]]) if R.random() < .55 else w
        a = 'Yes' if x[0] == w[0] else 'No'
        return mc('en_listen', 'Listen. Is it the same picture? (Nghe. Có đúng hình không?)', a, [], fixed=['Yes', 'No'], visual=f'<div class="emo">{w[1]}</div>', voice=[['en', x[0]]], auto=True, explain=f'Bạn nghe: {x[0]} ({x[2]}). Hình là {w[0]} ({w[2]}).')
    def listenSent():
        c = pick(C); o = R.sample([x for x in C if x[2] != c[2]], 2)
        return mc('en_listen', 'Listen and choose the picture. (Nghe câu và chọn hình)', c[2], [x[2] for x in o], emo=True, voice=[['en', c[0]]], auto=True, explain=f'{c[0]} = {c[1]}')
    def listenMean():
        c = pick(C); o = R.sample([x for x in C if x[1] != c[1]], 2)
        return mc('en_listen', 'Listen and choose the meaning. (Nghe và chọn nghĩa đúng)', c[1], [x[1] for x in o], voice=[['en', c[0]]], auto=True, explain=f'{c[0]} = {c[1]}')
    def listenQA():
        q, a = pick(QA); o = R.sample([y for x, y in QA if y != a], 2)
        return mc('en_listen', 'Listen to the question and choose the answer. (Nghe câu hỏi, chọn câu trả lời)', a, o, voice=[['en', q]], auto=True, explain=f'{q} → {a}')
    d1 = fill15([listenWord, listenPic, listenMatch, listenSent, listenMean, listenQA], tries=2000)

    # ---------------- Bài 3: Sentences ----------------
    def readQA():
        q, a = pick(QA); o = R.sample([y for x, y in QA if y != a], 2)
        return mc('en_sent', 'Read and choose the answer. (Đọc câu hỏi, chọn câu trả lời đúng)', a, o, big=q, bigSmall=True, voice=[['en', q]])
    def sentMeaning():
        c = pick(C); o = R.sample([x for x in C if x[1] != c[1]], 2)
        return mc('en_sent', 'What does it mean? (Câu này nghĩa là gì?)', c[1], [x[1] for x in o], big=c[0], bigSmall=True, voice=[['vi', 'Câu này nghĩa là gì?'], ['en', c[0]]])
    def viToEnS():
        c = pick(C); o = R.sample([x for x in C if x[0] != c[0]], 2)
        return mc('en_sent', f'Choose the English sentence. (Chọn câu tiếng Anh đúng): “{c[1]}”', c[0], [x[0] for x in o], voice=[['vi', 'Chọn câu tiếng Anh đúng']])
    def arrange():
        pool = [x for x in C if len(x[0].split()) >= 3] + [(q, '', '') for q, a in QA if len(q.split()) >= 3] + [(a, '', '') for q, a in QA if len(a.split()) >= 3]
        c = pick(pool)
        toks = c[0].split()
        if len(set(toks)) != len(toks):
            return None
        return ordq('en_sent', 'Put the words in order. (Sắp xếp các từ thành câu đúng)', toks, voice=[['en', c[0]]], auto=True, explain=c[0] + (f' = {c[1]}' if c[1] else ''))
    def gap():
        c = pick(C); low = c[0].lower()
        cand = [w for w in W if w[0].lower() in low]
        if not cand:
            return None
        w = max(cand, key=lambda x: len(x[0]))
        i = low.index(w[0].lower())
        shown = c[0][:i] + '____' + c[0][i + len(w[0]):]
        o = others(D, w, 2)
        return mc('en_sent', 'Look and complete. (Chọn từ đúng điền vào chỗ trống)', c[0][i:i + len(w[0])], [x[0] for x in o], visual=f'<div class="emo sm">{c[2]}</div><div class="ctx">{shown}</div>', voice=[['vi', 'Chọn từ đúng điền vào chỗ trống']], explain=f'{c[0]} = {c[1]}')
    d2 = fill15([readQA, sentMeaning, viToEnS, arrange, gap], tries=2000)
    return [d0, d1, d2]


def build_en():
    return units(), [build_unit(u) for u in range(len(UN))]


if __name__ == '__main__':
    us, b = build_en()
    assert len(us) == 16
    for u in UN:
        es = [w[1] for w in u[3]]; assert len(es) == len(set(es)), u[0]
        vs = [w[2] for w in u[3]]; assert len(vs) == len(set(vs)), u[0]
        cs = [c[2] for c in u[4]]; assert len(cs) == len(set(cs)), u[0]
        ans = [a for q, a in u[5]]; assert len(set(ans)) == len(ans) >= 3, u[0]
    for x in b:
        for d in x:
            assert len(d) == 15
            for q in d:
                if q['type'] == 'mc':
                    assert q['answer'] in q['options'] and len(set(q['options'])) == len(q['options']) >= 2, q
    print(len(us), sum(len(d) for x in b for d in x), 'ok')
