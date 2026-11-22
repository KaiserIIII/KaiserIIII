<p align="center">
  <img src="./assets/profile-hero.svg" alt="Yue Yu — Engineering Management × Computer Science; build systems, validate claims, ship useful work" width="100%" />
</p>

<p align="center">
  <a href="https://kaiseriii.tech/">Portfolio / 个人网站</a> ·
  <a href="https://kaiseriii.tech/projects/">Project index / 项目目录</a> ·
  <a href="https://store.steampowered.com/app/4338300/">CardCraft on Steam</a> ·
  <a href="https://kaiseriii.tech/#contact">Contact / 联系</a>
</p>

## Hi, I'm Yue Yu / 你好，我是于越

**Engineering Management × Computer Science** · Northeast Forestry University  
工程管理本科、计算机科学与技术辅修。关注如何把真实领域问题转化为**可运行的软件、可检验的结果和可持续维护的系统**。

I build products and research tools across **game systems, knowledge infrastructure, networks, data reliability and construction engineering**. My work emphasizes explicit assumptions, repeatable tests, careful failure handling and usable delivery—not just feature lists.

> **How I work / 我的工程理念:** Understand the problem → define boundaries → build → test against evidence → document limitations → ship.

## The project landscape / 项目地图

<p align="center">
  <img src="./assets/project-atlas.svg" alt="Four focus areas: products and play, built and industrial engineering, reliability and data, AI and research" width="100%" />
</p>

<sub>This is an editorial map of representative **public** work, not an automated skill score. / 图示为公开项目分类，不是能力百分比。</sub>

## Featured work / 代表项目

| Product & user experience / 产品与体验 | Systems & application engineering / 系统与应用 |
|:--|:--|
| **[CardCraft Engineering / 卡制工程](https://github.com/KaiserIIII/cardcraft-engineering-portfolio)** <br/> Godot · GDScript · Steamworks · P2P · Workshop <br/> A card-game engineering case study covering multiplayer state, mod content, persistence and release validation. **[Steam Demo ↗](https://store.steampowered.com/app/4338300/)** · [Engineering notes ↗](https://github.com/KaiserIIII/cardcraft-engineering-portfolio) <br/> 卡牌游戏、联机状态管理、创意工坊和发布工程。游戏源码私有，公开工程案例可查。 | **[Zhixu / 知序](https://github.com/KaiserIIII/zhixu)** <br/> FastAPI · SQLAlchemy · RAG · Chroma · workflows <br/> Self-hosted knowledge system with tenant isolation, evidence-linked retrieval and versioned visual workflows. **[Verification ↗](https://github.com/KaiserIIII/zhixu/blob/main/docs/verification.md)** <br/> 自托管知识系统，覆盖权限、检索、文档处理与可视化流程。 |
| **[WiFiScope](https://github.com/KaiserIIII/WiFiScope)** <br/> Python · Tkinter · TCP/TLS · PCAP · SQLite <br/> Local-first network investigation with bounded probes, evidence provenance and privacy-aware reports. **[Windows release ↗](https://github.com/KaiserIIII/WiFiScope/releases/latest)** · [Validation ↗](https://github.com/KaiserIIII/WiFiScope/blob/main/docs/validation.md) <br/> 网络证据工作台，强调授权范围、部分结果和数据脱敏。 | **[Construction Cost Analyzer / 工程造价分析](https://github.com/KaiserIIII/construction-cost-analyzer)** <br/> Python · Decimal · BOQ · estimating · appraisal <br/> Takeoff, unit rates, bills of quantities and development appraisal in one auditable calculation engine. **[Methods ↗](https://github.com/KaiserIIII/construction-cost-analyzer/blob/main/docs/course-methods.md)** · [Web lab ↗](https://kaiseriii.tech/projects/construction-cost-analyzer/lab/) <br/> 将工程计量、组价、清单和开发评价整合为可复核的工具。 |
| **[MigrationWitness](https://github.com/KaiserIIII/migrationwitness)** <br/> PostgreSQL · isolation · contract testing <br/> Reproduces permission-contract failures across PostgreSQL 16/17; distinguishes process success from application correctness. **[Reproduction record ↗](https://github.com/KaiserIIII/migrationwitness/blob/main/PG_OSC_197_RESULTS.md)** <br/> 用真实 PostgreSQL 实验验证迁移后权限与应用契约。 | **[QLDeviceCheck](https://github.com/KaiserIIII/QLDeviceCheck_Generic_WebUI_Linux)** <br/> Python · Modbus · SQLite · field acceptance <br/> Config-to-inspection evidence, read-only device checks and failure-focused retests. **[Demo ↗](https://github.com/KaiserIIII/QLDeviceCheck_Generic_WebUI_Linux/blob/main/docs/DEMO.md)** <br/> 面向设备交付与复测的工业协议验收工作台。 |

## Evidence map / 项目验证视图

<p align="center">
  <img src="./assets/evidence-board.svg" alt="Evidence matrix for six selected projects, showing inspectable outputs, hosted CI, scoped native or real checks, and research artifacts" width="100%" />
</p>

The matrix tells you **what sort of evidence is available**, not how good a developer is. A green check means that project's public repository documents that evidence. It does **not** certify security, universal correctness or production readiness. / 勾选代表仓库里有对应的公开验证证据，不代表功能完全可靠或达到商用级别。

- **[WiFiScope CI](https://github.com/KaiserIIII/WiFiScope/actions)** — Python 3.12/3.13 on Windows and Ubuntu; 708 tests per matrix job in the v0.2.0 run, with platform-specific skips.
- **[MigrationWitness](https://github.com/KaiserIIII/migrationwitness/blob/main/CROSS_VERSION_RESULTS.md)** — recorded PostgreSQL 16/17 tests and a concrete pg-osc permission-loss reproduction.
- **[Zhixu validation](https://github.com/KaiserIIII/zhixu/blob/main/docs/verification.md)** — backend/frontend tests and scoped browser checks; production integrations have stated gaps.
- **[ImportProof acceptance](https://github.com/KaiserIIII/importproof/blob/main/PUBLICATION_READINESS.md)** — real LibreOffice conversions, with unsupported/ambiguous XLSX comparisons reported as unknown.

## Research & reproducibility / 科研与可复现性

| Research track | Public work |
|:--|:--|
| **AI research & scientific workflows** | [CS Nature Paper Skill](https://github.com/KaiserIIII/cs-nature-paper-skill) · [Research Discovery](https://github.com/KaiserIIII/research-discovery) |
| **ML empirical studies** | [Return-to-Source Hysteresis / TTA](https://github.com/KaiserIIII/return-to-source-hysteresis) · [ReproShift / dependency compatibility](https://github.com/KaiserIIII/reproshift-artifact) |
| **Data & runtime correctness** | [ImportProof](https://github.com/KaiserIIII/importproof) · [CancelProof](https://github.com/KaiserIIII/cancelproof) · [Calendar Migration Auditor](https://github.com/KaiserIIII/calendar-migration-auditor) |
| **Agent tooling** | [LangBot Attachment Pipeline](https://github.com/KaiserIIII/langbot-unified-attachment-pipeline) · [Claude ↔ Codex Bridge](https://github.com/KaiserIIII/claude-codex-bridge) |

I keep negative findings and limitations visible. **A reproducible experiment is not automatically a published paper; a passing CI run is not automatically a production guarantee.**

## Stack / 技术栈

`Python` · `FastAPI` · `SQLAlchemy` · `SQLite / PostgreSQL` · `JavaScript / TypeScript` · `Astro` · `Godot / GDScript` · `GitHub Actions` · `Linux / Windows` · `RAG` · `Network protocols` · `Research automation`

<details>
<summary><b>More projects / 展开更多项目</b></summary>

**Tools & infrastructure / 工具与基础设施**

- [DeskTrace](https://github.com/KaiserIIII/desktrace) — Desktop regression/replay / 桌面回归与回放
- [RelayDesk](https://github.com/KaiserIIII/relaydesk) — Conversation-to-deliverable continuity / 任务成果交接
- [CourseRelay](https://github.com/KaiserIIII/courserelay) — Course source and note-version tracking / 课程资料追踪
- [PatchVerdict Lab](https://github.com/KaiserIIII/patchverdict-lab) — Benchmark evidence diagnostics / 基准证据诊断
- [KAISER portfolio source](https://github.com/KaiserIIII/kaiser-site) — Astro personal website / 个人网站源码

**Games & applied work / 游戏与应用**

- [General Simulator / 将军模拟器](https://github.com/KaiserIIII/jiangjun) — Event-driven Godot strategy prototype / 策略游戏原型
- [Campus UAV Inspection Manager](https://github.com/KaiserIIII/-UAV-inspection-task-management-system-in-college-parks) — Flask and GaussDB/openGauss scheduling prototype / 无人机巡检管理

**The full public repository list / 全部公开仓库** → [github.com/KaiserIIII?tab=repositories](https://github.com/KaiserIIII?tab=repositories)

</details>

---

<p align="center">
  <b>Build · Verify · Deliver · Learn</b><br/>
  <sub>See the <a href="https://kaiseriii.tech/projects/">project portfolio</a> for deeper explanations. Profile diagrams are versioned SVG assets; claims link back to public records. / 图表为随仓库版本管理的静态 SVG，项目详情与验证范围以对应仓库为准。</sub>
</p>
