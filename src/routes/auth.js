const router = require('express').Router();
const pool = require('../db');
const { hashPassword, comparePassword, newSessionId, signToken, authMiddleware } = require('../auth');

// Đã TẮT tự đăng ký: tài khoản học sinh / phụ huynh chỉ do admin tạo trong trang quản trị.
router.post(['/register', '/register/parent', '/register/student'], (req, res) => {
  res.status(403).json({ error: 'Chức năng tạo tài khoản đã tắt. Vui lòng liên hệ quản trị viên để được cấp tài khoản.' });
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
  // Tạo phiên mới → thiết bị đang đăng nhập trước đó (nếu có) bị đá ra ở request kế tiếp
  const sid = newSessionId();
  const ip = String(req.headers['x-real-ip'] || req.headers['x-forwarded-for'] || req.socket.remoteAddress || '').split(',')[0].trim().slice(0, 60);
  const device = String(req.headers['user-agent'] || '').slice(0, 300);
  await pool.query(
    'UPDATE users SET session_id=$1, last_login_at=now(), last_login_ip=$2, last_login_device=$3 WHERE id=$4',
    [sid, ip || null, device || null, user.id]);
  res.json({ user: { id: user.id, email: user.email, role: user.role, display_name: user.display_name || null }, token: signToken(user, sid) });
});

// Đăng xuất: hủy phiên hiện tại trên máy chủ
router.post('/logout', authMiddleware, async (req, res) => {
  await pool.query('UPDATE users SET session_id=NULL WHERE id=$1 AND session_id=$2', [req.user.id, req.user.sid]);
  res.json({ ok: true });
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
