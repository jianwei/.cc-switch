---
name: kill-port
description: 根据端口号终止对应进程的 Skill。当用户提供一个或多个端口号，想要终止这些端口上运行的进程时，必须使用此 Skill。触发关键词：杀进程、kill 端口、关闭端口、终止端口、释放端口、端口占用、kill port、free port、停止端口进程。即使用户只说"帮我杀掉 3000 端口"或"8080 端口被占用了"也要触发此 Skill。
---

# Kill Port Skill

根据用户提供的端口号，查找并终止对应的进程。

## 工作流程

### 第一步：解析端口

从用户输入中提取所有端口号（一个或多个），例如：
- "杀掉 3000 端口" → [3000]
- "杀掉 8080 和 3000" → [8080, 3000]
- "端口 3000 8080 9000" → [3000, 8080, 9000]

### 第二步：查找进程

对每个端口，使用以下命令查找占用该端口的进程：

```bash
# Linux / macOS 通用
lsof -ti :<PORT>

# 备选方案（如果 lsof 不可用）
fuser <PORT>/tcp

# 或者
ss -tlnp | grep :<PORT>
```

### 第三步：展示找到的进程信息（终止前先展示）

在执行 kill 之前，先查询进程详情并告知用户：

```bash
# 获取进程详细信息
lsof -i :<PORT>
```

输出格式示例：
```
端口 3000 → PID 12345 (node server.js)
端口 8080 → PID 67890 (python app.py)
```

### 第四步：执行 Kill

```bash
# 优先使用 SIGTERM（优雅退出）
kill -15 <PID>

# 如果 SIGTERM 无效，再使用 SIGKILL（强制终止）
kill -9 <PID>

# 或者直接用 lsof 配合 kill 一步完成：
kill -9 $(lsof -ti:<PORT>)
```

**多个端口批量处理脚本：**
```bash
for port in 3000 8080 9000; do
  pid=$(lsof -ti:$port 2>/dev/null)
  if [ -n "$pid" ]; then
    kill -9 $pid && echo "✅ 端口 $port (PID $pid) 已终止"
  else
    echo "⚠️  端口 $port 没有找到对应进程"
  fi
done
```

### 第五步：验证结果

终止之后，再次检查端口是否已释放：

```bash
lsof -i :<PORT>
# 如果没有输出，说明端口已释放
```

## 输出格式

向用户汇报结果，格式要清晰：

```
🔍 查找结果：
  端口 3000 → PID 12345 (node)
  端口 8080 → 未找到进程

💀 执行结果：
  ✅ 端口 3000：已成功终止 PID 12345
  ⚠️  端口 8080：无需处理（端口未被占用）

✔️  验证：端口 3000 已释放
```

## 注意事项

- **权限问题**：如果进程是 root 启动的，普通用户可能需要 `sudo`，此时提示用户
- **系统进程**：如果端口被系统关键进程占用（如 22/SSH、80/nginx），提醒用户谨慎操作
- **端口范围**：有效端口为 1–65535，超出范围提示错误
- **Windows 兼容**：如果检测到 Windows 环境，改用：
  ```cmd
  netstat -ano | findstr :<PORT>
  taskkill /PID <PID> /F
  ```
