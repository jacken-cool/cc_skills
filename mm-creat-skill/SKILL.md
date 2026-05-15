---
name: mm-creat-skill
description: 将需求文档、测试点Markdown等内容转换为飞书思维笔记可导入的.mm格式思维导图文件。当用户要求生成飞书思维导图、飞书思维笔记、.mm文件、导入飞书的思维导图、Markdown转飞书思维导图时使用。触发词：「飞书思维导图」「mm文件」「飞书思维笔记」「导入飞书」「思维导图mm」「生成mm」「转飞书格式」「.mm格式」。
---

# 飞书思维笔记 .mm 文件生成器

将任意层级化内容（需求文档、测试点、脑图大纲等）转换为飞书思维笔记可直接导入的 `.mm` XML 格式文件。

## When to Use

- 用户要求将文档/测试点/大纲转为飞书思维笔记可导入的 `.mm` 文件
- 用户提到"飞书思维导图""飞书思维笔记"".mm文件""导入飞书"等关键词
- 用户有一个已有的 Markdown 层级文档，希望转成飞书思维导图

## 核心规则 — 飞书 .mm 文件格式规范

以下规则是从实际导入失败的调试过程中提炼的，**必须严格遵守**，否则飞书导入会失败。

### 规则1：文件头部

```
（空行）
<map>
  <node ID="root" TEXT="根节点标题">
```

- **禁止** XML 声明头 `<?xml ...?>`
- **禁止** UTF-8 BOM（`EF BB BF`）
- 第一行**必须是空行**，第二行才是 `<map>`
- root 节点使用 `ID="root"`

### 规则2：属性顺序

所有 `<node>` 标签的属性**必须**按以下顺序排列：

```
<node TEXT="节点文本" ID="唯一ID" STYLE="样式" POSITION="位置">
```

- **TEXT 在 ID 前面**（这是飞书解析的关键要求）
- ID 使用 32 位十六进制字符串（可用随机生成）

### 规则3：节点样式

| 节点层级 | STYLE | POSITION | 说明 |
|---------|-------|----------|------|
| root 的直接子节点（一级分支） | `bubble` | `right` | 每个一级分支**独立并列**在 root 下 |
| 二级及以下子节点 | `fork` | 无 | 递归嵌套 |

### 规则4：一级分支平级结构

root 的一级子节点必须**平级并列**，不要嵌套在一个 bubble 子节点里：

```xml
<!-- 正确 ✅ -->
<node ID="root" TEXT="主题">
  <node TEXT="分支A" ID="..." STYLE="bubble" POSITION="right">
    ...
  </node>
  <node TEXT="分支B" ID="..." STYLE="bubble" POSITION="right">
    ...
  </node>
</node>

<!-- 错误 ❌：不要在root和分支之间加额外嵌套层 -->
<node ID="root" TEXT="主题">
  <node TEXT="主题" ID="..." STYLE="bubble" POSITION="right">
    <node TEXT="分支A" ID="..." STYLE="fork">...</node>
    <node TEXT="分支B" ID="..." STYLE="fork">...</node>
  </node>
</node>
```

### 规则5：TEXT属性中禁止ASCII双引号

TEXT 属性值用 `"` 包裹，因此属性值**内部不能出现 ASCII 双引号 `"`**（包括中文引号 `"` `"` 如果它们被转成了 ASCII 引号）。

| 原文 | 正确写法 | 错误写法 |
|------|---------|---------|
| 新增"功能"tab | `TEXT="新增「功能」tab"` | `TEXT="新增"功能"tab"` |
| 输入"超过20字" | `TEXT="输入「超过20字」"` | `TEXT="输入"超过20字""` |

**解决方案**：将中文引号替换为直角引号 `「」`，或用 `&amp;ldquo;` / `&amp;rdquo;` 转义。

### 规则6：换行符

- 使用 **LF**（`\n`）换行符，不要用 CRLF（`\r\n`）
- 写文件时指定 `newline='\n'`

### 规则7：XML自闭合标签

叶子节点（没有子节点的节点）使用自闭合标签：

```xml
<node TEXT="叶子节点" ID="..." STYLE="fork"/>
```

### 规则8：XML合法性校验

生成文件后**必须**用 XML 解析器验证合法性，确保不会因特殊字符导致解析失败：

```
python3 -c "import xml.etree.ElementTree as ET; ET.parse('output.mm')"
```

## Workflow

### Step 1：分析输入内容

- 读取用户提供的 Markdown/文本文件
- 识别层级结构（标题层级、列表嵌套）
- 确定一级分支主题（如：测试范围、前端测试点、后端测试点等）

### Step 2：规划思维导图结构

- 确定 root 节点标题
- 确定一级分支（每个一级分支对应 `STYLE="bubble" POSITION="right"`）
- 确定二级及以下子节点层级

### Step 3：生成 .mm 文件

按照上述格式规范生成 XML 内容，特别注意：

1. 第一行空行，第二行 `<map>`
2. 属性顺序：TEXT → ID → STYLE → POSITION
3. 一级分支用 bubble，子节点用 fork
4. TEXT 内的中文引号替换为 `「」`
5. 叶子节点自闭合 `<node .../>`
6. 换行符用 LF
7. 无 BOM、无 XML 声明

### Step 4：验证

- 用 Python XML 解析器验证文件合法性
- 如果验证失败，修复问题后重新验证
- 检查确认无以下常见错误：
  - TEXT 属性内有未转义的 `"` 字符
  - 属性顺序不对（ID 在 TEXT 前面）
  - 多余的 XML 声明头或 BOM
  - 换行符为 CRLF
  - root 下有多余嵌套层

### Step 5：输出

- 将 .mm 文件写入用户指定路径
- 告知用户可以在飞书思维笔记中导入

## Quick Template

```xml

<map>
  <node ID="root" TEXT="{{根节点标题}}">
    <node TEXT="{{一级分支A}}" ID="{{id1}}" STYLE="bubble" POSITION="right">
      <node TEXT="{{二级节点A1}}" ID="{{id2}}" STYLE="fork">
        <node TEXT="{{三级叶子节点}}" ID="{{id3}}" STYLE="fork"/>
        <node TEXT="{{另一个叶子}}" ID="{{id4}}" STYLE="fork"/>
      </node>
      <node TEXT="{{二级节点A2}}" ID="{{id5}}" STYLE="fork"/>
    </node>
    <node TEXT="{{一级分支B}}" ID="{{id6}}" STYLE="bubble" POSITION="right">
      <node TEXT="{{二级节点B1}}" ID="{{id7}}" STYLE="fork"/>
    </node>
  </node>
</map>
```

## 常见失败原因排查清单

| 现象 | 可能原因 | 修复方法 |
|------|---------|---------|
| 导入失败无提示 | XML 不合法 | 用 Python ET.parse 验证 |
| 导入失败 | TEXT 内有 `"` 字符 | 替换为 `「」` 或转义 |
| 导入失败 | 有 XML 声明头 | 删除 `<?xml ...?>` |
| 导入失败 | 有 BOM | 用无 BOM 的 UTF-8 保存 |
| 导入失败 | 属性顺序错 | TEXT 必须在 ID 前面 |
| 导入失败 | 换行符 CRLF | 转为 LF |
| 导入后结构扁平 | root 下多了嵌套层 | 一级分支直接挂在 root 下 |
| 导入后样式不对 | STYLE 值错误 | 一级用 bubble，子级用 fork |
| XML 解析 line XX 报错 | 属性值内特殊字符 | 检查该行是否有未转义的引号/尖括号/&符 |
