const router = require('express').Router();
const crypto = require('crypto');
const pool = require('../db');
const { hashPassword, comparePassword, signToken, authMiddleware } = require('../auth');

function genJoinCode() {
  return crypto.randomBytes(4).toString('hex').toUpperCase(); // 8 ký tự, VD: "A1B2C3D4"
}

// Đăng ký tài khoản phụ huynh
router.post('/register/parent', async (req, res) => {
  const { email, password } = req.body;
  if (!email || !password) return res.status(400).json({ error: 'Thiếu email hoặc mật khẩu' });
  try {
    const hash = await hashPassword(password);
    const { rows } = await pool.query(
      `INSERT INTO users (email, password_hash, role) VALUES ($1,$2,'parent') RETURNING id, email, role`,
      [email.toLowerCase().trim(), hash]
    );
    res.json({ user: rows[0], token: signToken(rows[0]) });
  } catch (e) {
    if (e.code === '23505') return res.status(409).json({ error: 'Email này đã được đăng ký' });
    console.error(e);
    res.status(500).json({ error: 'Lỗi máy chủ' });
  }
});

// Đăng ký tài khoản học sinh — tự tạo luôn hồ sơ student + join_code
router.post('/register/student', async (req, res) => {
  const { email, password, name, avatar, gender } = req.body;
  if (!email || !password || !name) return res.status(400).json({ error: 'Thiếu email, mật khẩu hoặc tên' });

  const client = await pool.connect();
  try {
    await client.query('BEGIN');
    const hash = await hashPassword(password);
    const { rows: uRows } = await client.query(
      `INSERT INTO users (email, password_hash, role) VALUES ($1,$2,'student') RETURNING id, email, role`,
      [email.toLowerCase().trim(), hash]
    );
    const user = uRows[0];

    let joinCode = genJoinCode();
    for (let i = 0; i < 5; i++) {
      const dup = await client.query('SELECT 1 FROM students WHERE join_code=$1', [joinCode]);
      if (dup.rowCount === 0) break;
      joinCode = genJoinCode();
    }

    const { rows: sRows } = await client.query(
      `INSERT INTO students (user_id, name, avatar, gender, join_code) VALUES ($1,$2,$3,$4,$5) RETURNING *`,
      [user.id, name.trim(), avatar || '🦊', gender || 'both', joinCode]
    );

    await client.query('COMMIT');
    res.json({ user, student: sRows[0], token: signToken(user) });
  } catch (e) {
    await client.query('ROLLBACK');
    if (e.code === '23505') return res.status(409).json({ error: 'Email này đã được đăng ký' });
    console.error(e);
    res.status(500).json({ error: 'Lỗi máy chủ' });
  } finally {
    client.release();
  }
});

// Đăng nhập chung cho cả admin / phụ huynh / học sinh
router.post('/login', async (req, res) => {
  const { email, password } = req.body;
  if (!email || !password) return res.status(400).json({ error: 'Thiếu email hoặc mật khẩu' });
  const { rows } = await pool.query('SELECT * FROM users WHERE email=$1', [email.toLowerCase().trim()]);
  const user = rows[0];
  if (!user || !(await comparePassword(password, user.password_hash))) {
    return res.status(401).json({ error: 'Sai email hoặc mật khẩu' });
  }
  res.json({ user: { id: user.id, email: user.email, role: user.role, display_name: user.display_name || null }, token: signToken(user) });
});

router.get('/me', authMiddleware, async (req, res) => {
  const { rows } = await pool.query('SELECT id, email, role, display_name FROM users WHERE id=$1', [req.user.id]);
  if (!rows[0]) return res.status(404).json({ error: 'Tài khoản không còn tồn tại' });
  res.json({ user: rows[0] });
});

// Mọi tài khoản tự đổi tên hiển thị / mật khẩu của chính mình.
// Đổi mật khẩu phải nhập đúng mật khẩu hiện tại.
router.put('/me', authMiddleware, async (req, res) => {
  const { name, current_password, new_password } = req.body;
  const { rows } = await pool.query('SELECT * FROM users WHERE id=$1', [req.user.id]);
  const user = rows[0];
  if (!user) return res.status(404).json({ error: 'Tài khoản không còn tồn tại' });
  if (new_password) {
    if (String(new_password).length < 4) return res.status(400).json({ error: 'Mật khẩu mới cần ít nhất 4 ký tự' });
    if (!current_password || !(await comparePassword(String(current_password), user.password_hash))) {
      return res.status(400).json({ error: 'Mật khẩu hiện tại chưa đúng' });
    }
    await pool.query('UPDATE users SET password_hash=$1 WHERE id=$2', [await hashPassword(String(new_password)), user.id]);
  }
  if (typeof name === 'string') {
    const n = name.trim().slice(0, 40);
    if (user.role === 'student') {
      if (!n) return res.status(400).json({ error: 'Tên không được để trống' });
      await pool.query('UPDATE students SET name=$1 WHERE user_id=$2', [n, user.id]);
    } else {
      await pool.query('UPDATE users SET display_name=$1 WHERE id=$2', [n || null, user.id]);
    }
  }
  res.json({ ok: true });
});

module.exports = router;
