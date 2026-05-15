#!/usr/bin/env python
"""api2case 渲染脚本：JSON/CSV → 卡片式 Markdown 接口测试用例文档

用法:
    python render_md.py --input cases.json --title "开场问题" --output out.md
    python render_md.py --csv cases.csv --title "开场问题" --output out.md
    python render_md.py --help    # 查看 JSON 格式说明
"""

import argparse, csv, json, io, os, sys

# ======================================================================
# 渲染核心
# ======================================================================

def fmt_json(s):
    try:
        return json.dumps(json.loads(s), indent=2, ensure_ascii=False)
    except Exception:
        return s

def render_md(cases, title="接口测试用例"):
    """将用例 dict 列表渲染为卡片式 Markdown 字符串"""
    # 按接口名称分组
    groups = {}
    for c in cases:
        gname = c.get("api_name", c.get("接口名称", ""))
        groups.setdefault(gname, []).append(c)

    lines = []
    cnt = len(cases)
    ngrp = len(groups)
    lines.append(f'# 接口测试用例 — {title}')
    lines.append('')
    lines.append(f'共 {cnt} 条用例，覆盖 {ngrp} 个接口')
    lines.append('')

    # 目录
    lines.append('## 目录')
    lines.append('')
    for gname, items in groups.items():
        lines.append(f'- [{gname}](#{gname})（{len(items)}条）')
    lines.append('')
    lines.append('---')
    lines.append('')

    seq = [0]

    for gname, items in groups.items():
        lines.append(f'## {gname}')
        lines.append('')

        for c in items:
            seq[0] += 1
            n = seq[0]

            name = c.get("name", c.get("用例名称", ""))
            priority = c.get("priority", c.get("优先级", ""))
            url = c.get("url", c.get("URL路径", ""))
            scene = c.get("scene", c.get("场景", ""))
            desc = c.get("desc", c.get("用例描述", ""))
            pre = c.get("pre", c.get("前置条件", ""))
            post = c.get("post", c.get("后置条件", ""))
            body = c.get("body", c.get("请求体", ""))
            assertions = c.get("assertions", [])

            lines.append(f'### {n}. [{priority}] {name}')
            lines.append('')

            # 元信息表
            lines.append('| 字段 | 内容 |')
            lines.append('|------|------|')
            lines.append(f'| **接口** | `{url}` |')
            lines.append(f'| **场景** | {scene} |')
            lines.append(f'| **描述** | {desc} |')

            pre_clean = pre.replace('\\n', '\n')
            if pre_clean and pre_clean not in ('无', '无需特殊前置', '无（只读查询，不修改数据）'):
                display = pre_clean.replace('\n', '<br>')
                lines.append(f'| **前置条件** | {display} |')

            if post and post not in ('无（只读查询，不修改数据）',):
                lines.append(f'| **后置条件** | {post} |')

            lines.append('')

            # 请求体
            if body and body not in ('（GET请求无Body）',):
                formatted = fmt_json(body)
                lines.append('**请求体：**')
                lines.append('')
                lines.append('```json')
                lines.append(formatted)
                lines.append('```')
                lines.append('')
            else:
                lines.append('**请求体：** 无（GET请求）')
                lines.append('')

            # 断言
            lines.append('**断言：**')
            lines.append('')
            lines.append('| 列名 | 对比类型 | 断言值 |')
            lines.append('|------|---------|--------|')

            # assertions 可能是 [(path,op,val),...] 或 "多行字符串"
            if isinstance(assertions, str):
                assertion_str = assertions
                for a in assertion_str.split('\n'):
                    a_clean = a.strip()
                    if a_clean:
                        path, op, val = _parse_assertion(a_clean)
                        lines.append(f'| {path} | {op} | {val} |')
            else:
                for item in assertions:
                    if isinstance(item, (list, tuple)):
                        path, op, val = item[0], item[1], item[2]
                    else:
                        path, op, val = "", "", str(item)
                    if not path and not op:
                        lines.append(f'| | | {val} |')
                    else:
                        lines.append(f'| {path} | {op} | {val} |')
            lines.append('')
            lines.append('---')
            lines.append('')

    return '\n'.join(lines)


def _parse_assertion(a):
    """解析字符串断言为 (path, op, value)"""
    a = a.strip()
    # 移除 $.response. 前缀统一处理
    for op in ('!=', '<=', '>=', '=', '<', '>'):
        if op in a:
            idx = a.index(op)
            path = a[:idx].strip()
            val = a[idx + len(op):].strip()
            # 去掉断言值两端的双引号
            if val.startswith('"') and val.endswith('"'):
                val = val[1:-1]
            return path, op, val
    return "", "", a


# ======================================================================
# CSV 输入
# ======================================================================

def read_csv(path):
    """读取 CSV，根据列名自动映射为 api 或 app 格式的 dict 列表"""
    encodings = ['utf-8-sig', 'utf-8', 'gbk']
    rows = None
    for enc in encodings:
        try:
            with open(path, 'r', encoding=enc) as f:
                reader = list(csv.reader(f))
                rows = reader
                break
        except (UnicodeDecodeError, Exception):
            continue
    if rows is None:
        raise ValueError(f'无法读取 CSV 文件: {path}')

    header = rows[0]
    data_rows = rows[1:]

    # 检测格式：接口用例（含接口名称/URL/断言列）vs APP用例（含操作步骤/预期结果）
    has_url = any('url' in h.lower() or '路径' in h for h in header)

    cases = []
    for r in data_rows:
        if not any(r):  # 跳过空行
            continue
        d = {header[i]: r[i] for i in range(min(len(header), len(r)))}
        if has_url:
            # 接口用例：保留原始字段名，render_md 会兼容
            cases.append(d)
        else:
            # APP用例：字段名不同，暂不处理（api2case 仅处理接口用例）
            pass

    # 断言字符串 → 解析为三元组
    for c in cases:
        assertion_str = c.get("断言(JSONPath)", "")
        if assertion_str:
            parsed = []
            for line in assertion_str.split('\n'):
                line = line.strip()
                if not line:
                    continue
                path, op, val = _parse_assertion(line)
                if not path and not op:
                    parsed.append(("", "", val))
                else:
                    parsed.append((path, op, val))
            c["assertions"] = parsed

    return cases


# ======================================================================
# 命令行入口
# ======================================================================

HELP_TEXT = """
用例 JSON 数据格式 (--input):

[
  {
    "api_name": "查询用户智能体",
    "url": "POST /api/v1/agents/list",
    "scene": "入口场景-首页",
    "name": "首页入口-不传suggestCateCode",
    "desc": "不传参数时默认返回首页开场问题",
    "pre": "1. 首页分类已配置开场问题",
    "post": "",
    "body": "{\\"appType\\":\\"infinitus\\",\\"scene\\":\\"healthbuddy\\",\\"limit\\":1}",
    "assertions": [
      ["$.response.code", "=", "00000"],
      ["$.response.data[0].suggestes", "!=", "null"]
    ],
    "priority": "P0"
  }
]

字段说明:
  api_name   - 接口中文名（用于分组）
  url        - Method + Path
  scene      - 场景分类
  name       - 用例标题
  desc       - 用例描述（一句话）
  pre        - 前置条件（\\\\n 分点，无则空字符串）
  post       - 后置条件（无则空字符串）
  body       - 请求体 JSON 字符串（GET 请求时为空字符串）
  assertions - [[path, op, value], ...] 断言三元组列表
  priority   - P0 / P1 / P2
"""


def main():
    parser = argparse.ArgumentParser(
        description='api2case 渲染：JSON/CSV → 卡片式 Markdown 接口测试用例文档',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='示例:\n  python render_md.py --input cases.json -t "开场问题" -o out.md\n  python render_md.py --csv cases.csv -t "开场问题" -o out.md\n  python render_md.py --help'
    )
    parser.add_argument('--input', '-i', help='JSON 用例数据文件')
    parser.add_argument('--csv', '-c', help='CSV 用例文件')
    parser.add_argument('--title', '-t', default='接口测试用例', help='文档标题（# 接口测试用例 — {title}）')
    parser.add_argument('--output', '-o', help='输出 .md 文件路径')
    parser.add_argument('--json-help', action='store_true', help='打印 JSON 输入格式说明')
    args = parser.parse_args()

    if args.json_help:
        print(HELP_TEXT)
        return

    if not args.input and not args.csv:
        parser.error('请指定 --input 或 --csv')

    # 读取数据
    cases = []
    if args.input:
        with open(args.input, 'r', encoding='utf-8') as f:
            cases = json.load(f)
    elif args.csv:
        cases = read_csv(args.csv)

    if not cases:
        print('错误：未读取到任何用例数据', file=sys.stderr)
        sys.exit(1)

    # 渲染
    md = render_md(cases, title=args.title)

    # 输出
    if args.output:
        outpath = args.output
    else:
        base = os.path.splitext(args.input or args.csv)[0]
        outpath = f'{base}.md'

    with open(outpath, 'w', encoding='utf-8') as f:
        f.write(md)

    api_count = len(set(
        c.get("api_name", c.get("接口名称", "")) for c in cases
    ))
    print(f'已生成: {outpath}')
    print(f'共 {len(cases)} 条接口测试用例，覆盖 {api_count} 个接口')


if __name__ == '__main__':
    main()
