# Initializer Agent — Vue 版完整提示模板

## 前置说明

用户已在启动时完成了一次性确认，提供了：
- 项目根目录路径
- 特别注意事项（如有）

**本 Agent 全程自动执行，不向用户提任何问题。**

---

## Step 0：自动识别模型名，确定目录名

```bash
# Agent 自我声明（最高优先级）：直接使用已知的模型标准名称
# 转小写，空格和斜杠替换为 -
# 例：Claude Sonnet 4.6 → claude-sonnet-4-6

MODEL_NAME="${ANTHROPIC_MODEL:-${OPENAI_MODEL:-${MODEL_NAME_ENV:-}}}"

if [ -z "$MODEL_NAME" ]; then
  for f in .env .env.local .cursorrules .claude.json; do
    [ -f "$f" ] && MODEL_NAME=$(grep -i "^model" "$f" 2>/dev/null | head -1 | sed 's/.*[:=]\s*//' | tr -d '"' | xargs) && [ -n "$MODEL_NAME" ] && break
  done
fi

MODEL_NAME="${MODEL_NAME:-unknown-model}"
MODEL_NAME=$(echo "$MODEL_NAME" | tr '[:upper:]' '[:lower:]' | sed 's/[ /]/-/g')

DOCS_DIR="project-docs-${MODEL_NAME}"
mkdir -p "$DOCS_DIR"

echo "模型：$MODEL_NAME  →  目录：$DOCS_DIR"
```

---

## Step 1：识别 Vue 项目类型

```bash
cd [启动时用户提供的项目路径]

# 读取 package.json 识别 Vue 版本
python3 -c "
import json
pkg = json.load(open('package.json'))
deps = {**pkg.get('dependencies',{}), **pkg.get('devDependencies',{})}
vue_ver = deps.get('vue','unknown')
vuex_ver = deps.get('vuex','none')
print(f'Vue版本: {vue_ver}')
print(f'Vuex版本: {vuex_ver}')
print(f'构建工具: {\"webpack\" if \"webpack\" in str(deps) or \"@vue/cli-service\" in deps else \"vite\" if \"vite\" in deps else \"unknown\"}')
"

# 扫描项目文件结构
find src -type f \( -name "*.vue" -o -name "*.js" -o -name "*.ts" \) | grep -v node_modules | sort

# 读取路由配置
cat src/router/index.js 2>/dev/null || cat src/router/index.ts 2>/dev/null || cat src/router.js 2>/dev/null

# 读取 Store 目录
ls src/store/ 2>/dev/null && cat src/store/index.js 2>/dev/null || cat src/store/index.ts 2>/dev/null

# 扫描 composables（Composition API 自管理状态）
ls src/composables/ 2>/dev/null || ls src/hooks/ 2>/dev/null

# 扫描 API 层
ls src/api/ 2>/dev/null || ls src/services/ 2>/dev/null || ls src/request/ 2>/dev/null
```

---

## Step 2：识别状态管理方案

```bash
python3 -c "
import json, os
pkg = json.load(open('package.json'))
deps = {**pkg.get('dependencies',{}), **pkg.get('devDependencies',{})}

vuex = deps.get('vuex','')
has_composables = os.path.isdir('src/composables') or os.path.isdir('src/hooks')

if vuex.startswith('^3') or vuex.startswith('3'):
    print('STATE_VUEX3')
elif vuex.startswith('^4') or vuex.startswith('4'):
    print('STATE_VUEX4')

if has_composables:
    print('STATE_COMPOSABLE')

if not vuex and not has_composables:
    print('STATE_UNKNOWN')
"
```

根据识别结果，doc-tasks.json 中 state 任务使用对应模板：
- `STATE_VUEX3` / `STATE_VUEX4` → `references/tpl-state-vuex.md`
- `STATE_COMPOSABLE` → `references/tpl-state-composable.md`
- 混合模式 → 两套模板分别生成，各独立一个任务

---

## Step 3：生成任务清单 vue-docs-config.json

基于扫描结果生成任务清单，写入项目根目录 `vue-docs-config.json`。

**此文件只包含任务定义（category、template、source_files 等），不用于状态跟踪。运行时状态由 OMC Task 系统管理。**

**Vue 版任务分类与优先级：**

| 类别 | priority | source_files 来源 | 负责角色 |
|------|---------|-------------------|---------|
| architecture | 1 | `package.json`, `src/App.vue`, `src/router/index.js` | architecture-agent |
| state | 2 | `src/store/index.js` 或 `src/store/modules/*.js` 或 `src/composables/*.js` | state-agent |
| api | 3 | `src/api/*.js` 或 `src/services/*.js`，每个文件一个任务 | api-agent |
| view | 4 | `src/views/**/*.vue`，每个路由页面一个任务 | view-agent |
| component | 5 | `src/components/**/*.vue`，重要复用组件 | component-agent |
| tech-debt | 6 | 整个 src 目录，最后做 | tech-debt-agent |

**⚠️ Vue 特有规则：**
- `target_file` 中页面文档路径用 `views/` 而非 `pages/`
- 组件 `source_files` 使用 `.vue` 文件路径
- Vuex store 有 modules 时，每个 module 单独一个 state 任务

```bash
cat > vue-docs-config.json << 'JSONEOF'
{
  "project": "[package.json 中的 name]",
  "framework": "vue2",
  "model": "[MODEL_NAME]",
  "docs_dir": "[DOCS_DIR]",
  "created_at": "[当前时间]",
  "total": N,
  "tasks": [
    {
      "id": "arch-001",
      "category": "architecture",
      "description": "生成整体架构文档",
      "target_file": "[DOCS_DIR]/architecture.md",
      "source_files": ["package.json", "src/App.vue", "src/router/index.js"],
      "template": "references/tpl-architecture.md",
      "priority": 1,
      "phase": 1
    }
  ]
}
JSONEOF

# 验证写入成功
ls -lh vue-docs-config.json
python3 -c "import json; d=json.load(open('vue-docs-config.json')); print(f'✅ 任务数：{d[\"total\"]}，framework：{d[\"framework\"]}')"
```

---

## Step 4：生成 $DOCS_DIR/doc-progress.md

```bash
cat > "$DOCS_DIR/doc-progress.md" << 'PROGRESSEOF'
# 文档生成进度

## 项目信息
- 项目名：[package.json name]
- 框架：Vue 2 + Webpack
- 状态管理：[Vuex 3 / Vuex 4 / Composition API / 混合]
- 使用模型：[MODEL_NAME]
- 文档目录：[DOCS_DIR]
- 初始化时间：[当前时间]
- 总任务数：N
- 已完成：0

## 技术栈概览
（从 package.json 提取：Vue 版本、路由版本、状态管理版本、UI 库、构建工具等）

## 会话记录
### Session 1（Initializer）- [当前时间]
- ✅ 自动识别模型：[MODEL_NAME]
- ✅ 识别框架：Vue 2 + Webpack
- ✅ 确定文档目录：[DOCS_DIR]
- ✅ 完成项目扫描
- ✅ 生成 vue-docs-config.json（N 个任务）
- ✅ 建立目录结构
PROGRESSEOF

ls -lh "$DOCS_DIR/doc-progress.md" || echo "❌ 写入失败"
```

---

## Step 5：建立 $DOCS_DIR/ 目录结构

```bash
mkdir -p $DOCS_DIR/api $DOCS_DIR/views $DOCS_DIR/components $DOCS_DIR/state
touch $DOCS_DIR/architecture.md $DOCS_DIR/tech-debt.md
```

---

## Step 6：生成 run-docs.sh 和 .coding-agent-prompt.txt

### 6a：生成 .coding-agent-prompt.txt

```bash
cat > .coding-agent-prompt.txt << 'PROMPTEOF'
你是 Vue 项目文档生成专家。当前工作目录已包含 doc-tasks.json。

请严格按照以下步骤执行，完成 1 个文档任务后立即退出，不要继续下一个任务。

## Step 0：读状态 + 时间差检查

```bash
python3 << 'PYEOF'
import json, datetime, sys
d = json.load(open('doc-tasks.json'))
started = d.get('session_started_at','')
remaining = [t for t in d['tasks'] if not t['passes']]
done = d['total'] - len(remaining)
print(f'进度：{done}/{d["total"]}  框架：{d.get("framework","vue")}  目录：{d["docs_dir"]}')
if not remaining:
    print('ALL_DONE')
    sys.exit(0)
if started:
    delta = datetime.datetime.now() - datetime.datetime.strptime(started,'%Y-%m-%d %H:%M:%S')
    if delta.total_seconds() > 3600:
        print(f'TIMEOUT: {int(delta.total_seconds()/60)} 分钟，请重新运行 /vue-reverse-docs')
        sys.exit(0)
t = sorted(remaining, key=lambda x:(x['priority'],x['seq']))[0]
print(f'下一个：[{t["seq"]}/{d["total"]}] #{t["id"]} {t["description"]}')
PYEOF
```

若输出 ALL_DONE 或 TIMEOUT，直接停止。

## Step 1：检查上次遗留

验证最近一个 passes=true 的任务其 target_file 是否存在且非空。
文件缺失则重新生成，然后继续。

## Step 2：选取本次任务（只选 1 个）

从 doc-tasks.json 选 passes=false、priority 最小、seq 最小的任务。

## Step 3：读模板 + 读源文件 + 生成文档

**Vue 版模板选择规则：**
- category=architecture → references/tpl-architecture.md
- category=api          → references/tpl-api.md
- category=view         → references/tpl-prd.md（注意：Vue 用 view 不用 page）
- category=component    → references/tpl-component.md
- category=state，source 含 store → references/tpl-state-vuex.md
- category=state，source 含 composables/hooks → references/tpl-state-composable.md
- category=tech-debt    → references/tpl-tech-debt.md

**分析 .vue 文件时的重点：**
- `<template>` → 提取页面/组件布局结构、条件渲染（v-if/v-show）、列表渲染（v-for）
- `<script>` Options API → `data()`=状态、`methods()`=方法、`computed`=计算属性、`watch`=监听、生命周期钩子
- `<script setup>` Composition API → `ref`/`reactive`=状态、`computed`=计算、`watch`/`watchEffect`=监听
- `this.$store` / `mapState` / `mapActions` → Vuex 数据流
- `this.$router.push` / `useRouter()` → 路由跳转
- `this.$emit` / `defineEmits` → 组件通信
- `inject` / `provide` → 跨层级传值

写文件：
```bash
mkdir -p "$(dirname TARGET_FILE)"
cat > TARGET_FILE << 'DOCEOF'
[完整文档内容]
DOCEOF
ls -lh TARGET_FILE
```

禁止使用 Write 工具，只用 bash cat >。

## Step 4：验证

```bash
ls -lh TARGET_FILE
wc -l TARGET_FILE
```

必须看到 ls 实际输出才能继续。

## Step 5：更新 doc-tasks.json

```bash
python3 << 'PYEOF'
import json, subprocess
d = json.load(open('doc-tasks.json'))
now = subprocess.check_output('date +"%Y-%m-%d %H:%M:%S"', shell=True).decode().strip()
for t in d['tasks']:
    if t['id'] == 'TASK_ID_PLACEHOLDER':
        t['passes'] = True
        t['completed_at'] = now
        print(f"✅ #{t['id']} 完成")
d['completed'] = sum(1 for t in d['tasks'] if t['passes'])
json.dump(d, open('doc-tasks.json','w'), ensure_ascii=False, indent=2)
print(f"📊 {d['completed']}/{d['total']}")
PYEOF
```

## Step 6：更新 doc-progress.md

```bash
DOCS_DIR=$(python3 -c "import json; print(json.load(open('doc-tasks.json'))['docs_dir'])")
NOW=$(date +"%Y-%m-%d %H:%M:%S")
echo "" >> "$DOCS_DIR/doc-progress.md"
echo "### $NOW" >> "$DOCS_DIR/doc-progress.md"
echo "- ✅ 完成 #TASK_ID：TASK_DESC" >> "$DOCS_DIR/doc-progress.md"
echo "- 📄 TARGET_FILE" >> "$DOCS_DIR/doc-progress.md"
```

## Step 7：git commit

```bash
git add -A
git commit -m "docs(CATEGORY): TASK_DESC

- #TASK_ID  进度：M/N
- $(date +'%Y-%m-%d %H:%M:%S')"
git log --oneline -1
echo "✅ commit 完成"
```

## Step 8：输出结束标记，停止

```bash
python3 -c "
import json
d = json.load(open('doc-tasks.json'))
r = [t for t in d['tasks'] if not t['passes']]
if r:
    nxt = sorted(r, key=lambda t:(t['priority'],t['seq']))[0]
    print(f'TASK_DONE 还剩 {len(r)} 个，下一个 #{nxt[\"id\"]}')
else:
    print('ALL_DONE')
"
```

⚠️ 输出 TASK_DONE 或 ALL_DONE 后立即停止，不要继续下一个任务。
PROMPTEOF

ls -lh .coding-agent-prompt.txt
echo "✅ .coding-agent-prompt.txt 已生成"
```

### 6b：生成 run-docs.sh

```bash
cat > run-docs.sh << 'RUNDOCSEOF'
#!/bin/bash
# run-docs.sh — Vue 项目全自动文档生成驱动脚本
# 用法：bash run-docs.sh

cd "$(dirname "$0")"
MAX_TASKS=200
COUNT=0

echo "🚀 启动 Vue 项目全自动文档生成..."
python3 -c "
import json
d = json.load(open('doc-tasks.json'))
done = sum(1 for t in d['tasks'] if t['passes'])
print(f'📋 {d[\"project\"]}（{d.get(\"framework\",\"vue\")}）  📁 {d[\"docs_dir\"]}  进度：{done}/{d[\"total\"]}')
"
echo ""

while [ $COUNT -lt $MAX_TASKS ]; do
  COUNT=$((COUNT + 1))

  REMAINING=$(python3 -c "
import json
d = json.load(open('doc-tasks.json'))
print(len([t for t in d['tasks'] if not t['passes']]))
")

  if [ "$REMAINING" -eq 0 ]; then
    echo ""
    echo "╔══════════════════════════════════════════════════╗"
    echo "║           🎉 全部文档任务已完成！                 ║"
    echo "╚══════════════════════════════════════════════════╝"
    python3 -c "
import json
d = json.load(open('doc-tasks.json'))
print(f'📁 {d[\"docs_dir\"]}  🤖 {d[\"model\"]}  📊 {d[\"total\"]}/{d[\"total\"]} 个任务')
"
    break
  fi

  python3 -c "
import json
d = json.load(open('doc-tasks.json'))
done = d['total'] - $REMAINING
r = sorted([t for t in d['tasks'] if not t['passes']], key=lambda t:(t['priority'],t['seq']))[0]
print(f'--- [{done+1}/{d[\"total\"]}] #{r[\"id\"]}：{r[\"description\"]}')
"

  OUTPUT=$(claude -p "$(cat .coding-agent-prompt.txt)" \
    --allowedTools "Bash,Read" 2>&1)
  EXIT_CODE=$?

  echo "$OUTPUT" | grep -E "^(✅|❌|📊|TASK_DONE|ALL_DONE|⚠️|📄|\[docs)" | tail -8

  if echo "$OUTPUT" | grep -q "ALL_DONE"; then
    echo "🎉 全部完成"
    break
  fi

  if echo "$OUTPUT" | grep -q "TIMEOUT"; then
    echo "⚠️ 超过1小时，停止。请重新运行 /vue-reverse-docs。"
    break
  fi

  if [ $EXIT_CODE -ne 0 ]; then
    echo "⚠️ 子进程异常 (exit $EXIT_CODE)，继续下一个..."
  fi

  echo ""
done

echo "✅ run-docs.sh 结束（共 $COUNT 轮）"
RUNDOCSEOF

chmod +x run-docs.sh
ls -lh run-docs.sh
echo "✅ run-docs.sh 已生成"
```

---

## Step 7：初始 git commit

```bash
git add -A
git commit -m "docs: 初始化 $DOCS_DIR/ Vue 文档生成环境

- 框架：Vue 2 + Webpack
- 模型：$MODEL_NAME
- 新建目录：$DOCS_DIR/
- 生成 doc-tasks.json（N 个任务）
- 生成 doc-progress.md / init.sh / run-docs.sh
- 建立子目录：api/ views/ components/ state/

运行方式：bash run-docs.sh（全自动，无需介入）"
git log --oneline -1
```

---

## Step 8：提示用户启动

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ 初始化完成！

📁 文档目录：$DOCS_DIR
📋 任务总数：N 个
🤖 生成模型：$MODEL_NAME
🏗  框架类型：Vue 2 + Webpack

▶ 在终端运行以下命令开始全自动生成：

   bash run-docs.sh

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```