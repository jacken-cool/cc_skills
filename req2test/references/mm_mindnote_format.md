# 飞书思维笔记 .mm 格式规范

## 1. 概述

`.mm` 格式是 FreeMind/Freeplane 思维导图的标准 XML 格式，可直接导入飞书思维笔记进行可视化编辑。

## 2. 文件结构

```xml
<?xml version="1.0" encoding="utf-8"?>
<map>
  <node ID="root" TEXT="根节点标题">
    <node ID="xxx" TEXT="一级节点" STYLE="bubble" POSITION="right">
      <node ID="xxx" TEXT="二级节点" STYLE="fork"/>
    </node>
  </node>
</map>
```

## 3. 节点属性规范

### 3.1 ID 生成规则

```python
import hashlib
node_id = hashlib.md5(text.encode()).hexdigest()
```

- 输入：节点文本内容
- 输出：32 位 MD5 十六进制字符串
- 根节点固定为 `"root"`

### 3.2 STYLE 属性

| 层级 | STYLE 值 | 说明 |
|-----|---------|------|
| 一级节点 | `bubble` | 气泡样式，作为模块分组标题 |
| 二级及以下 | `fork` | 分叉样式，作为具体测试点 |
| 根节点 | 不设置 | 根节点不需要 STYLE |

### 3.3 POSITION 属性

- 一级节点需要设置 `POSITION="left"` 或 `POSITION="right"`
- 建议将一级节点平均分配到左右两侧，便于阅读
- 二级及以下子节点不设置 POSITION

## 4. 层级结构建议

```
根节点（需求名称）
├── 左侧一级节点（STYLE="bubble", POSITION="left"）
│   ├── 二级节点（STYLE="fork"）
│   │   └── 三级节点（STYLE="fork"）
│   └── 二级节点
├── 右侧一级节点（STYLE="bubble", POSITION="right"）
│   ├── 二级节点
│   └── 二级节点
```

## 5. 测试点专用结构

推荐按以下模块组织一级节点：

- 测试范围（范围内/范围外）
- 核心业务链路
- 测试策略
- APP 前端测试点
- 配置后台测试点
- 运营后台测试点
- 跨系统联动测试点
- 高优先级场景
- 待确认项

## 6. 与 Markdown 格式的转换

### 从 Markdown 转换到 .mm

Markdown 层级（缩进 2 空格 = 一级）：
```markdown
- 需求名称
  - 测试范围
    - 范围内
      - 功能A
```

转换为 .mm 层级：
```xml
<node ID="root" TEXT="需求名称">
  <node ID="xxx" TEXT="测试范围" STYLE="bubble" POSITION="right">
    <node ID="xxx" TEXT="范围内" STYLE="fork">
      <node ID="xxx" TEXT="功能A" STYLE="fork"/>
    </node>
  </node>
</node>
```

## 7. 输出要求

1. 生成符合 XML 规范的 .mm 文件
2. ID 使用 MD5 哈希确保唯一性
3. 一级节点使用 bubble 样式并分配 POSITION
4. 子节点使用 fork 样式
5. 文件编码为 UTF-8

## 8. 示例文件

参考 `assets/test_points_feishu_template.mm` 了解完整格式。
