const router = require('express').Router();
const pool = require('../db');
const { authMiddleware, requireRole } = require('../auth');
const { rankingForUser } = require('../rank');

async function getOwnStudent(userId) {
  const { rows } = await pool.query('SELECT id, user_id, name, avatar, gender, join_code, created_at, total_points FROM students WHERE user_id=$1', [userId]);
  return rows[0];
}

router.use(authMiddleware, requireRole('student'));

// Dữ liệu tối thiểu cho trang chủ.
// Quan trọng: toàn bộ dữ liệu được lấy bằng MỘT round-trip tới Neon.
// Không tải skill_stats, lịch sử session, sticker/shop hoặc BXH ở đây.
router.get('/me/home', async (req, res) => {
  try {
    const { rows } = await pool.query(
      `
      SELECT
        s.id,
        s.name,
        s.avatar,
        s.gender,
        s.join_code,
        s.total_points,
        COALESCE(p.total_stars, 0)::int AS total_stars,
        COALESCE(p.progress, '[]'::json) AS progress,
        COALESCE(r.coins, 0)::int AS coins,
        COALESCE(d.seconds, 0)::int AS today_seconds
      FROM students s
      LEFT JOIN LATERAL (
        SELECT
          COALESCE(SUM(pr.stars), 0)::int AS total_stars,
          COALESCE(
            json_agg(
              json_build_object('level_key', pr.level_key, 'stars', pr.stars)
              ORDER BY pr.level_key
            ),
            '[]'::json
          ) AS progress
        FROM progress pr
        WHERE pr.student_id = s.id
      ) p ON TRUE
      LEFT JOIN student_rewards r ON r.student_id = s.id
      LEFT JOIN daily_sessions d
        ON d.student_id = s.id AND d.day = CURRENT_DATE
      WHERE s.user_id = $1
      LIMIT 1
      `,
      [req.user.id]
    );

    const row = rows[0];
    if (!row) return res.status(404).json({ error: 'Không tìm thấy hồ sơ học sinh' });

    res.json({
      student: {
        id: row.id,
        name: row.name,
        avatar: row.avatar,
        gender: row.gender,
        join_code: row.join_code,
        total_points: Number(row.total_points || 0),
      },
      total_stars: Number(row.total_stars || 0),
      progress: row.progress || [],
      coins: Number(row.coins || 0),
      today_seconds: Number(row.today_seconds || 0),
    });
  } catch (e) {
    console.error('GET /student/me/home:', e);
    res.status(500).json({ error: 'Không thể tải dữ liệu trang chủ' });
  }
});

// Sticker/cửa hàng chỉ tải khi học sinh mở Thành tích.
// Chỉ MỘT round-trip tới Neon (trước đây 3 truy vấn nối tiếp nhau).
router.get('/me/rewards', async (req, res) => {
  try {
    const { rows } = await pool.query(
      `SELECT s.id,
              r.stickers, r.shop, r.coins, r.en_stickers,
              COALESCE((
                SELECT json_agg(substr(p.level_key, 4)::int)
                FROM progress p
                WHERE p.student_id = s.id AND p.level_key ~ '^en_[0-9]+$' AND p.stars >= 1
              ), '[]'::json) AS en_done
       FROM students s
       LEFT JOIN student_rewards r ON r.student_id = s.id
       WHERE s.user_id = $1
       LIMIT 1`,
      [req.user.id]
    );
    const row = rows[0];
    if (!row) return res.status(404).json({ error: 'Không tìm thấy hồ sơ học sinh' });
    const r = {
      stickers: row.stickers || [],
      shop: row.shop || [],
      coins: Number(row.coins) || 0,
      en_stickers: Array.isArray(row.en_stickers) ? row.en_stickers : [],
    };
    // Sticker Xe cộ = thưởng bài English. Gộp thêm từ tiến độ đã lưu để bù các sticker bị mất trước đây.
    const fromProgress = (row.en_done || []).map(Number).filter((i) => i < 48);
    r.en_stickers = [...new Set([...r.en_stickers, ...fromProgress])].sort((a, b) => a - b);
    res.set('Cache-Control', 'private, no-cache');
    res.json(r);
  } catch (e) {
    console.error(e);
    res.status(500).json({ error: 'Không thể tải bộ sưu tập' });
  }
});


// Lấy toàn bộ dữ liệu của chính học sinh đang đăng nhập
router.get('/me', async (req, res) => {
  const student = await getOwnStudent(req.user.id);
  if (!student) return res.status(404).json({ error: 'Không tìm thấy hồ sơ học sinh' });
  const [progress, skills, sessions, rewards] = await Promise.all([
    pool.query('SELECT level_key, stars FROM progress WHERE student_id=$1', [student.id]),
    pool.query('SELECT skill_key, correct, total FROM skill_stats WHERE student_id=$1', [student.id]),
    pool.query('SELECT day, seconds FROM daily_sessions WHERE student_id=$1 ORDER BY day DESC LIMIT 30', [student.id]),
    pool.query('SELECT stickers, shop, coins, en_stickers FROM student_rewards WHERE student_id=$1', [student.id]),
  ]);
  res.json({ student, progress: progress.rows, skills: skills.rows, sessions: sessions.rows, rewards: rewards.rows[0] || {stickers: [], shop: [], coins: 0} });
});

// Cập nhật tên / nhân vật / giới tính (gọi khi học sinh đổi tên hoặc chọn lại nhân vật)
router.put('/me/profile', async (req, res) => {
  const { name, avatar, gender } = req.body;
  const student = await getOwnStudent(req.user.id);
  if (!student) return res.status(404).json({ error: 'Không tìm thấy hồ sơ học sinh' });
  await pool.query(
    `UPDATE students SET name = COALESCE($1, name), avatar = COALESCE($2, avatar), gender = COALESCE($3, gender) WHERE id=$4`,
    [name || null, avatar || null, gender || null, student.id]
  );
  res.json({ ok: true });
});

// Đồng bộ bộ sưu tập sticker/cửa hàng theo tài khoản học sinh
// Bảng xếp hạng toàn bộ học viên — điểm tích lũy là tiêu chí chính, sao và số bài là tiêu chí phụ.
router.get('/me/rank', async (req, res) => {
  const { meId, list } = await rankingForUser(req.user.id);
  if (meId == null) return res.status(404).json({ error: 'Không tìm thấy hồ sơ học sinh' });
  res.set('Cache-Control', 'private, no-cache');
  res.json({ students: list, me: list.find((x) => x.me) || null });
});

// Điểm tích lũy chỉ tăng, không thể bị giảm bởi client.
router.put('/me/points', async (req, res) => {
  const student = await getOwnStudent(req.user.id);
  if (!student) return res.status(404).json({ error: 'Không tìm thấy hồ sơ học sinh' });
  const points = Math.max(0, Math.floor(Number(req.body.total_points) || 0));
  const { rows } = await pool.query(`UPDATE students SET total_points=GREATEST(total_points,$1) WHERE id=$2 RETURNING total_points`, [points, student.id]);
  res.json({ ok:true, total_points: rows[0].total_points });
});

router.put('/me/rewards', async (req, res) => {
  const student = await getOwnStudent(req.user.id);
  if (!student) return res.status(404).json({ error: 'Không tìm thấy hồ sơ học sinh' });
  const stickers = Array.isArray(req.body.stickers) ? req.body.stickers.map(Number).filter(Number.isInteger) : [];
  const shop = Array.isArray(req.body.shop) ? req.body.shop.map(Number).filter(Number.isInteger) : [];
  const coins = Math.max(0, Number(req.body.coins) || 0);
  // en_stickers (Xe cộ) chỉ cộng thêm, không bị xóa bởi máy chưa có dữ liệu.
  const enSt = Array.isArray(req.body.en_stickers) ? [...new Set(req.body.en_stickers.map(Number).filter((i) => Number.isInteger(i) && i >= 0 && i < 48))] : [];
  await pool.query(`INSERT INTO student_rewards(student_id,stickers,shop,coins,en_stickers,updated_at) VALUES($1,$2::jsonb,$3::jsonb,$4,$5::jsonb,now())
    ON CONFLICT(student_id) DO UPDATE SET stickers=$2::jsonb,shop=$3::jsonb,coins=$4,
      en_stickers=(SELECT COALESCE(jsonb_agg(DISTINCT x ORDER BY x),'[]'::jsonb) FROM jsonb_array_elements(student_rewards.en_stickers || $5::jsonb) AS t(x)),
      updated_at=now()`, [student.id, JSON.stringify(stickers), JSON.stringify(shop), coins, JSON.stringify(enSt)]);
  res.json({ ok: true });
});

// Lưu/tăng số sao cho 1 bài (gọi mỗi khi học sinh hoàn thành 1 level)
router.put('/me/progress', async (req, res) => {
  const { level_key, stars } = req.body;
  if (!level_key || stars == null) return res.status(400).json({ error: 'Thiếu level_key hoặc stars' });
  const student = await getOwnStudent(req.user.id);
  await pool.query(
    `INSERT INTO progress (student_id, level_key, stars, updated_at) VALUES ($1,$2,$3, now())
     ON CONFLICT (student_id, level_key)
     DO UPDATE SET stars = GREATEST(progress.stars, $3), updated_at = now()`,
    [student.id, level_key, stars]
  );
  res.json({ ok: true });
});

// Cộng dồn số câu đúng/tổng số câu theo kỹ năng
router.post('/me/skill', async (req, res) => {
  const { skill_key, correct, total } = req.body;
  if (!skill_key) return res.status(400).json({ error: 'Thiếu skill_key' });
  const student = await getOwnStudent(req.user.id);
  await pool.query(
    `INSERT INTO skill_stats (student_id, skill_key, correct, total) VALUES ($1,$2,$3,$4)
     ON CONFLICT (student_id, skill_key)
     DO UPDATE SET correct = skill_stats.correct + $3, total = skill_stats.total + $4`,
    [student.id, skill_key, correct || 0, total || 0]
  );
  res.json({ ok: true });
});

// Cộng dồn thời gian học trong ngày hôm nay (giây)
router.post('/me/session', async (req, res) => {
  const { seconds } = req.body;
  const student = await getOwnStudent(req.user.id);
  await pool.query(
    `INSERT INTO daily_sessions (student_id, day, seconds) VALUES ($1, CURRENT_DATE, $2)
     ON CONFLICT (student_id, day) DO UPDATE SET seconds = daily_sessions.seconds + $2`,
    [student.id, seconds || 0]
  );
  res.json({ ok: true });
});

module.exports = router;
