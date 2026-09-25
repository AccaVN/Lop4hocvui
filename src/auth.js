const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');

const SECRET = process.env.JWT_SECRET;

function hashPassword(pw) {
  return bcrypt.hash(pw, 10);
}

function comparePassword(pw, hash) {
  return bcrypt.compare(pw, hash);
}

function signToken(user) {
  return jwt.sign({ id: user.id, role: user.role, email: user.email }, SECRET, { expiresIn: '30d' });
}

// Bắt buộc phải có Bearer token hợp lệ
function authMiddleware(req, res, next) {
  const header = req.headers.authorization;
  if (!header || !header.startsWith('Bearer ')) {
    return res.status(401).json({ error: 'Thiếu token đăng nhập' });
  }
  try {
    req.user = jwt.verify(header.slice(7), SECRET);
    next();
  } catch (e) {
    return res.status(401).json({ error: 'Token không hợp lệ hoặc đã hết hạn' });
  }
}

// Chỉ cho phép một số role nhất định (dùng sau authMiddleware)
function requireRole(...roles) {
  return (req, res, next) => {
    if (!req.user || !roles.includes(req.user.role)) {
      return res.status(403).json({ error: 'Tài khoản không có quyền truy cập mục này' });
    }
    next();
  };
}

module.exports = { hashPassword, comparePassword, signToken, authMiddleware, requireRole };
