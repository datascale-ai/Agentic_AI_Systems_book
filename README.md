# Agentic AI Systems

<p align="center">
  <strong>从大语言模型到现实世界智能体</strong><br>
  <em>From Large Language Models to Real-World Agents</em>
</p>

<p align="center">
  <a href="https://github.com/your-org/Agentic_AI_Systems_book/actions/workflows/validate.yml"><img src="https://github.com/your-org/Agentic_AI_Systems_book/actions/workflows/validate.yml/badge.svg" alt="Build status"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License"></a>
  <img src="https://img.shields.io/badge/parts-9-orange.svg" alt="Parts">
  <img src="https://img.shields.io/badge/chapters-39-orange.svg" alt="Chapters">
  <img src="https://img.shields.io/badge/submission-Nov%2030%2C%202026-7c3aed.svg" alt="Submission date">
</p>

这是一本面向研究生、软件工程师和技术管理者的智能体人工智能系统书稿。全书从模型交互和推理基础出发，逐步进入规划、工具调用、记忆、多智能体、运行时、评估、安全治理和可运行工程实践。

> 当前仓库是持续写作与构建工程：章节路径、公共接口、双语导航和 CI 已固定，正文、图表、实验与代码由六位作者按连续章节块协作补充。

## 在线阅读与本地预览

本仓库使用 MkDocs Material 生成中英文书籍网站。部署到 GitHub Pages 后，站点会从 `main` 分支自动发布。

```bash
uv sync --extra test
uv run pytest
uv run mkdocs serve
```

浏览器打开终端显示的地址。构建静态站点并执行严格链接检查：

```bash
uv run mkdocs build --clean --strict
```

`site/` 是生成目录，已加入 `.gitignore`，不会作为源文件提交。

## 全书结构

| 篇 | 内容 | 章节 |
| --- | --- | --- |
| I | 智能体人工智能系统基础 | Ch01–Ch04 |
| II | 模型交互与推理基础 | Ch05–Ch08 |
| III | 智能体核心能力 | Ch09–Ch13 |
| IV | 记忆、知识与智能体学习 | Ch14–Ch17 |
| V | 多智能体与环境交互系统 | Ch18–Ch21 |
| VI | 运行时工程与交互基础设施 | Ch22–Ch25 |
| VII | 评估、可信性与生产治理 | Ch26–Ch30 |
| VIII | 应用、综合项目与未来方向 | Ch31–Ch35 |
| IX | 工程实践、可运行代码与测试 | Ch36–Ch39 |

第九篇提供贯穿全书的参考实现、单元测试、集成测试、端到端测试、评估回归、故障注入、可观测性和部署演练。它与第八篇 Ch34 的综合项目共享代码、数据和运行清单。

## 仓库布局

```text
docs/                 双语书稿与 MkDocs 页面
├── zh/               中文主稿：九篇、39章
└── en/               英文翻译稿：与中文路径一一对应
examples/             综合项目、参考实现、测试和部署资产入口
tests/                目录、分工、配置和构建校验
mkdocs.yml            Material 双语站点导航
requirements-docs.txt 文档构建与测试依赖
.github/workflows/    提交校验与 GitHub Pages 发布
```

## 写作与协作规则

- 中文稿是首个冻结基线；计划于 **2026年10月25日** 冻结中文版本。
- 中文冻结后批量翻译英文；计划于 **2026年11月30日** 提交 Springer。
- 章节保留 `owner`、目标页数、图表 ID、实验 ID 和版本字段，作为协作接口。
- 图表、术语、接口 schema、实验卡和代码版本使用稳定 ID；正文引用 ID，不复制易失同步的公共定义。
- 案例、模拟实验和真实测量必须明确区分，所有关键结论保留来源、适用条件和限制。

## 贡献流程

1. 从对应 `docs/zh/partN/` 章节文件开始写作，先更新章节结构和公共资产登记；工程代码、测试夹具和运行清单放入 `examples/`。
2. 在本地运行 `uv run pytest` 与 `uv run mkdocs build --clean --strict`。
3. 提交正文、图表源文件、实验卡、引用登记和可复现命令。
4. 中文冻结后再生成对应 `docs/en/` 翻译稿，并由原主责作者完成技术确认。

内部写作指导、学生任务单、proposal、PDF 和其他规划产物位于本地 `private_materials/` 或历史文件中，并由 `.gitignore` 排除，不会上传到 GitHub。

## 项目许可

代码、配置和本仓库原创文档按 [MIT License](LICENSE) 发布。书稿最终出版版权以及第三方图表、数据和代码许可，以 Springer 合同和逐项许可登记为准。
