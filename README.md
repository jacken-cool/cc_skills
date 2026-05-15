# cc_skills

Claude Code 技能包集合。用于扩展 AI 代理的专用能力，涵盖浏览器自动化、接口测试、需求转测试、思维导图、Obsidian 集成等场景。

## 技能清单

| 技能 | 说明 |
|------|------|
| [agent-browser](./agent-browser) | 浏览器自动化 CLI，基于 Chrome/Chromium CDP，支持页面导航、表单填写、截图、数据抓取 |
| [api2case](./api2case) | 接口描述（PDF/OpenAPI/文本）→ 卡片式 Markdown 接口测试用例文档 |
| [req2test](./req2test) | 需求一条龙：Axure 原型 / PDF 产品方案 → 需求分析 → 测试点 → 测试用例 |
| [mm-creat-skill](./mm-creat-skill) | Markdown → 飞书思维笔记可导入的 .mm 格式思维导图文件 |
| [darwin-skill](./darwin-skill) | 自主 skill 优化器，基于评估-改进-实测循环自动提升 SKILL.md 质量 |
| [find-skills](./find-skills) | 从开放技能生态中搜索和安装 agent skills |
| [json-canvas](./json-canvas) | 创建和编辑 JSON Canvas (.canvas) 文件（节点、边、分组） |
| [obsidian-markdown](./obsidian-markdown) | Obsidian 风格 Markdown 语法（wikilinks、callouts、properties） |
| [obsidian-bases](./obsidian-bases) | 创建和编辑 Obsidian Bases (.base) 数据库视图 |
| [obsidian-cli](./obsidian-cli) | 通过 CLI 与 Obsidian 仓库交互（笔记管理、搜索、插件开发） |

## 快速开始

技能通过 Claude Code 的 `Skill` 工具调用，系统会自动匹配：

```
用户："把这个 Axure 原型转成测试用例"
→ 自动匹配 req2test 技能执行
```

## 使用方法

每个技能目录包含一个 `SKILL.md`，定义了触发条件、执行流程和输出规则。Claude Code 会在对话中根据用户意图自动匹配并加载对应技能。

## 一键推送

```bash
git-push.bat   # 双击运行，自动推送到 GitHub + Gitee
```

远程仓库：
- GitHub: `https://github.com/jacken-cool/cc_skills`
- Gitee: `https://gitee.com/sjk314/cc_skills`
