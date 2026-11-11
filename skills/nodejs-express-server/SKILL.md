---
name: nodejs-express-server
description: 使用中间件（Middleware）、认证（Authentication）、路由（Routing）和数据库集成构建生产级 Express.js 服务器。用于创建 REST API、管理请求/响应、实现中间件链和处理服务器逻辑。
---

# Node.js Express 服务器

## 概述

使用路由（Routing）、中间件链（Middleware Chain）、认证机制（Authentication）和数据库集成（遵循行业最佳实践）创建健壮的 Express.js 应用程序。

## 使用场景

- 使用 Node.js 构建 REST API
- 实现服务端请求处理
- 为横切关注点（Cross-cutting Concerns）创建中间件链
- 管理身份验证（Authentication）和授权（Authorization）
- 从 Node.js 连接数据库
- 实现错误处理和日志记录

## 指南

### 1. **基础 Express 配置**

```javascript
const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;

// 中间件（Middleware）
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// 路由（Routes）
app.get('/health', (req, res) => {
  res.json({ status: 'OK', timestamp: new Date().toISOString() });
});

// 错误处理
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(err.status || 500).json({
    error: err.message,
    requestId: req.id
  });
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
```

### 2. **中间件链实现**

```javascript
// 日志中间件
const logger = (req, res, next) => {
  const start = Date.now();
  res.on('finish', () => {
    const duration = Date.now() - start;
    console.log(`${req.method} ${req.path} ${res.statusCode} ${duration}ms`);
  });
  next();
};

// 认证中间件
const authenticateToken = (req, res, next) => {
  const token = req.headers['authorization']?.split(' ')[1];
  if (!token) return res.status(401).json({ error: 'No token' });

  jwt.verify(token, process.env.JWT_SECRET, (err, user) => {
    if (err) return res.status(403).json({ error: 'Invalid token' });
    req.user = user;
    next();
  });
};

// 异步错误捕获中间件包装器
const asyncHandler = (fn) => (req, res, next) => {
  Promise.resolve(fn(req, res, next)).catch(next);
};

app.use(logger);
app.use(express.json());
app.get('/protected', authenticateToken, (req, res) => {
  res.json({ user: req.user });
});
```

### 3. **数据库集成（PostgreSQL + Sequelize）**

```javascript
const { Sequelize, DataTypes } = require('sequelize');

const sequelize = new Sequelize(
  process.env.DB_NAME,
  process.env.DB_USER,
  process.env.DB_PASS,
  {
    host: process.env.DB_HOST,
    dialect: 'postgres',
    logging: false
  }
);

const User = sequelize.define('User', {
  id: {
    type: DataTypes.UUID,
    defaultValue: DataTypes.UUIDV4,
    primaryKey: true
  },
  email: {
    type: DataTypes.STRING,
    unique: true,
    allowNull: false
  },
  password: DataTypes.STRING,
  role: {
    type: DataTypes.ENUM('user', 'admin'),
    defaultValue: 'user'
  }
}, {
  timestamps: true
});

// 同步数据库
sequelize.sync({ alter: true });
```

### 4. **JWT 身份验证**

```javascript
const jwt = require('jsonwebtoken');
const bcrypt = require('bcrypt');

const generateToken = (userId) => {
  return jwt.sign(
    { userId, iat: Math.floor(Date.now() / 1000) },
    process.env.JWT_SECRET,
    { expiresIn: '24h' }
  );
};

app.post('/login', asyncHandler(async (req, res) => {
  const { email, password } = req.body;
  const user = await User.findOne({ where: { email } });

  if (!user) return res.status(404).json({ error: 'User not found' });

  const validPassword = await bcrypt.compare(password, user.password);
  if (!validPassword) return res.status(401).json({ error: 'Invalid password' });

  const token = generateToken(user.id);
  res.json({ token, user: { id: user.id, email: user.email } });
}));
```

### 5. **RESTful 路由与 CRUD 操作**

```javascript
const userRouter = express.Router();

// GET 所有用户（支持分页）
userRouter.get('/', authenticateToken, asyncHandler(async (req, res) => {
  const { page = 1, limit = 20 } = req.query;
  const users = await User.findAndCountAll({
    offset: (page - 1) * limit,
    limit: parseInt(limit)
  });

  res.json({
    data: users.rows,
    pagination: { page, limit, total: users.count }
  });
}));

// GET 单个用户
userRouter.get('/:id', authenticateToken, asyncHandler(async (req, res) => {
  const user = await User.findByPk(req.params.id);
  if (!user) return res.status(404).json({ error: 'Not found' });
  res.json({ data: user });
}));

// POST 创建用户
userRouter.post('/', asyncHandler(async (req, res) => {
  const { email, password } = req.body;
  const hashedPassword = await bcrypt.hash(password, 10);

  const user = await User.create({
    email,
    password: hashedPassword
  });

  res.status(201).json({ data: user });
}));

// PATCH 更新用户
userRouter.patch('/:id', authenticateToken, asyncHandler(async (req, res) => {
  const user = await User.findByPk(req.params.id);
  if (!user) return res.status(404).json({ error: 'Not found' });

  await user.update(req.body, {
    fields: ['email', 'role']
  });

  res.json({ data: user });
}));

// DELETE 用户
userRouter.delete('/:id', authenticateToken, asyncHandler(async (req, res) => {
  const user = await User.findByPk(req.params.id);
  if (!user) return res.status(404).json({ error: 'Not found' });

  await user.destroy();
  res.status(204).send();
}));

app.use('/api/users', userRouter);
```

### 6. **错误处理中间件**

```javascript
class AppError extends Error {
  constructor(message, statusCode) {
    super(message);
    this.statusCode = statusCode;
    Error.captureStackTrace(this, this.constructor);
  }
}

app.use((err, req, res, next) => {
  err.statusCode = err.statusCode || 500;

  if (err.name === 'SequelizeValidationError') {
    return res.status(400).json({
      error: 'Validation failed',
      details: err.errors.map(e => ({ field: e.path, message: e.message }))
    });
  }

  if (process.env.NODE_ENV === 'production') {
    return res.status(err.statusCode).json({
      error: err.message,
      requestId: req.id
    });
  }

  res.status(err.statusCode).json({
    error: err.message,
    stack: err.stack
  });
});

app.use((req, res) => {
  res.status(404).json({ error: 'Route not found' });
});
```

### 7. **环境配置**

```javascript
require('dotenv').config();

const config = {
  port: process.env.PORT || 3000,
  env: process.env.NODE_ENV || 'development',
  database: {
    url: process.env.DATABASE_URL,
    dialect: 'postgres'
  },
  jwt: {
    secret: process.env.JWT_SECRET,
    expiresIn: '24h'
  },
  cors: {
    origin: process.env.CORS_ORIGIN || 'http://localhost:3000'
  }
};

module.exports = config;
```

## 最佳实践

### ✅ 推荐做法
- 使用中间件处理横切关注点（Cross-cutting Concerns）
- 实现适当的错误处理
- 在处理前验证输入数据
- 使用 async/await 处理异步操作
- 在受保护的路由上实现身份验证
- 使用环境变量进行配置
- 添加日志记录和监控
- 在生产环境使用 HTTPS
- 实现限流（Rate Limiting）
- 保持路由处理器专注且小巧

### ❌ 避免做法
- 静默处理错误
- 在代码中存储敏感数据
- 在路由中使用同步操作
- 忘记验证用户输入
- 在路由处理器中实现身份验证逻辑
- 使用回调地狱（Callback Hell）（改用 Promise/async-await）
- 在生产环境暴露堆栈跟踪（Stack Traces）
- 仅信任客户端验证

## 完整示例

```javascript
const express = require('express');
const jwt = require('jsonwebtoken');
const { Sequelize, DataTypes } = require('sequelize');

const app = express();
app.use(express.json());

const sequelize = new Sequelize('postgres://user:pass@localhost/db');

const User = sequelize.define('User', {
  email: DataTypes.STRING,
  password: DataTypes.STRING
});

const authenticateToken = (req, res, next) => {
  const token = req.headers['authorization']?.split(' ')[1];
  jwt.verify(token, 'secret', (err, user) => {
    if (err) return res.status(403).json({ error: 'Forbidden' });
    req.user = user;
    next();
  });
};

app.get('/users', authenticateToken, async (req, res, next) => {
  try {
    const users = await User.findAll();
    res.json({ data: users });
  } catch (err) {
    next(err);
  }
});

app.post('/users', async (req, res, next) => {
  try {
    const user = await User.create(req.body);
    res.status(201).json({ data: user });
  } catch (err) {
    next(err);
  }
});

app.listen(3000, () => console.log('Server running on port 3000'));
```
