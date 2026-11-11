---
name: pnpm-ci-cd-setup
description: Optimizing pnpm for continuous integration and deployment workflows
---

# pnpm CI/CD 配置

在 CI/CD 环境中使用 pnpm 实现快速可靠构建的最佳实践。

## GitHub Actions

### 基础配置

```yaml
name: CI

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: pnpm/action-setup@v4
        with:
          version: 9

      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'pnpm'

      - run: pnpm install --frozen-lockfile
      - run: pnpm test
      - run: pnpm build
```

### 使用存储缓存

对于较大的项目，缓存 pnpm 存储：

```yaml
- uses: pnpm/action-setup@v4
  with:
    version: 9

- name: Get pnpm store directory
  shell: bash
  run: |
    echo "STORE_PATH=$(pnpm store path --silent)" >> $GITHUB_ENV

- uses: actions/cache@v4
  name: Setup pnpm cache
  with:
    path: ${{ env.STORE_PATH }}
    key: ${{ runner.os }}-pnpm-store-${{ hashFiles('**/pnpm-lock.yaml') }}
    restore-keys: |
      ${{ runner.os }}-pnpm-store-

- run: pnpm install --frozen-lockfile
```

### 矩阵测试

```yaml
jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        node: [18, 20, 22]
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node }}
          cache: 'pnpm'
      - run: pnpm install --frozen-lockfile
      - run: pnpm test
```

## GitLab CI

```yaml
image: node:20

stages:
  - install
  - test
  - build

variables:
  PNPM_HOME: /root/.local/share/pnpm
  PATH: $PNPM_HOME:$PATH

before_script:
  - corepack enable
  - corepack prepare pnpm@latest --activate

cache:
  key: ${CI_COMMIT_REF_SLUG}
  paths:
    - .pnpm-store

install:
  stage: install
  script:
    - pnpm config set store-dir .pnpm-store
    - pnpm install --frozen-lockfile

test:
  stage: test
  script:
    - pnpm test

build:
  stage: build
  script:
    - pnpm build
```

## Docker

### 多阶段构建

```dockerfile
# Build stage
FROM node:20-slim AS builder

# Enable corepack for pnpm
RUN corepack enable

WORKDIR /app

# Copy package files first for layer caching
COPY package.json pnpm-lock.yaml pnpm-workspace.yaml ./
COPY packages/*/package.json ./packages/

# Install dependencies
RUN pnpm install --frozen-lockfile

# Copy source and build
COPY . .
RUN pnpm build

# Production stage
FROM node:20-slim AS runner

RUN corepack enable
WORKDIR /app

COPY --from=builder /app/dist ./dist
COPY --from=builder /app/package.json ./
COPY --from=builder /app/pnpm-lock.yaml ./

# Production install
RUN pnpm install --frozen-lockfile --prod

CMD ["node", "dist/index.js"]
```

### 适用于 Monorepo 的优化

```dockerfile
FROM node:20-slim AS builder
RUN corepack enable
WORKDIR /app

# Copy workspace config
COPY pnpm-lock.yaml pnpm-workspace.yaml ./

# Copy all package.json files maintaining structure
COPY packages/core/package.json ./packages/core/
COPY packages/api/package.json ./packages/api/

# Install all dependencies
RUN pnpm install --frozen-lockfile

# Copy source
COPY . .

# Build specific package
RUN pnpm --filter @myorg/api build
```

## 关键 CI 参数

### --frozen-lockfile

**始终在 CI 中使用。** 如果 `pnpm-lock.yaml` 需要更新则失败：

```bash
pnpm install --frozen-lockfile
```

### --prefer-offline

尽可能使用缓存的包：

```bash
pnpm install --frozen-lockfile --prefer-offline
```

### --ignore-scripts

跳过生命周期脚本以加快安装速度（谨慎使用）：

```bash
pnpm install --frozen-lockfile --ignore-scripts
```

## Corepack 集成

使用 Corepack 管理 pnpm 版本：

```json
// package.json
{
  "packageManager": "pnpm@9.0.0"
}
```

```yaml
# GitHub Actions
- run: corepack enable
- run: pnpm install --frozen-lockfile
```

## Monorepo CI 策略

### 仅构建已更改的包

```yaml
- name: Build changed packages
  run: |
    pnpm --filter "...[origin/main]" build
```

### 每个包并行作业

```yaml
jobs:
  detect-changes:
    runs-on: ubuntu-latest
    outputs:
      packages: ${{ steps.changes.outputs.packages }}
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - id: changes
        run: |
          echo "packages=$(pnpm --filter '...[origin/main]' list --json | jq -c '[.[].name]')" >> $GITHUB_OUTPUT

  test:
    needs: detect-changes
    if: needs.detect-changes.outputs.packages != '[]'
    runs-on: ubuntu-latest
    strategy:
      matrix:
        package: ${{ fromJson(needs.detect-changes.outputs.packages) }}
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
      - run: pnpm install --frozen-lockfile
      - run: pnpm --filter ${{ matrix.package }} test
```

## 最佳实践总结

1. **始终在 CI 中使用 `--frozen-lockfile`**
2. **缓存 pnpm 存储**以加快安装速度
3. **使用 Corepack** 以保持一致的 pnpm 版本
4. **在 package.json 中指定 `packageManager`**
5. **在 monorepo 中使用 `--filter`** 仅构建更改的内容
6. **使用多阶段 Docker 构建**以获得更小的镜像

<!--
Source references:
- https://pnpm.io/continuous-integration
- https://github.com/pnpm/action-setup
-->
