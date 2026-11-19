# Official Delta Reference: hkuds_cli_anything
Source: https://github.com/HKUDS/CLI-Anything
Domain: agent_harness

<h1 align="center"><img src="assets/icon.png" alt="" width="64" style="vertical-align: middle;">&nbsp; CLI-Anything: Making ALL Software Agent-Native</h1>

<div align="center">
<a href="https://www.star-history.com/hkuds/cli-anything"><picture><source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/badge?repo=HKUDS/CLI-Anything&amp;type=trending&amp;theme=dark"><source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/badge?repo=HKUDS/CLI-Anything&amp;type=trending"><img alt="GitHub Trending Repository of the Day" src="https://api.star-history.com/badge?repo=HKUDS/CLI-Anything&amp;type=trending" height="55"></picture></a>&#32;<a href="https://trendshift.io/repositories/22991" target="_blank"><img src="https://trendshift.io/api/badge/repositories/22991" alt="HKUDS/CLI-Anything | Trendshift" height="55"></a>&#32;<a href="https://www.star-history.com/hkuds/cli-anything"><picture><source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/badge?repo=HKUDS/CLI-Anything&amp;type=rank&amp;theme=dark"><source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/badge?repo=HKUDS/CLI-Anything&amp;type=rank"><img alt="Star History Rank" src="https://api.star-history.com/badge?repo=HKUDS/CLI-Anything&amp;type=rank" height="55"></picture></a>
</div>

<p align="center">
  <strong>Today's Software Serves Humans👨‍💻. Tomorrow's Users will be Agents🤖.<br>
CLI-Anything: Bridging the Gap Between AI Agents and the World's Software</strong><br>
</p>

**🌐 [CLI-Hub](https://hkuds.github.io/CLI-Anything/)**: `pip install cli-anything-hub` then `cli-hub install <name>` — browse, install, and manage all community-built CLIs. Want to add your own? [Open a PR](https://github.com/HKUDS/CLI-Anything/blob/main/CONTRIBUTING.md) — the hub updates instantly.

**🎬 [See Demos](#-real-world-demos)**: Watch AI agents use generated CLIs plus preview, live preview, and trajectory loops to produce real artifacts — CAD builds, 3D scenes, diagrams, gameplay, subtitles, and more.

**🙋 [Become a Contributor, or Request a CLI]**: [Join us](https://github.com/HKUDS/CLI-Anything/issues/new?template=contributor-signup.yml)! Sign up to build a new CLI harness — once reviewed and merged, you'll gain access as one of our community contributors! Wish CLI-Anything supported a specific software or service? Submit a [wishlist request](https://github.com/HKUDS/CLI-Anything/issues/new?template=cli-wishlist.yml)!

<p align="center">
  <a href="#-quick-start"><img src="https://img.shields.io/badge/Quick_Start-5_min-blue?style=for-the-badge" alt="Quick Start"></a>
  <a href="https://hkuds.github.io/CLI-Anything/"><img src="https://img.shields.io/badge/CLI_Hub-Browse_%26_Install-ff69b4?style=for-the-badge" alt="CLI Hub"></a>
  <a href="#-demonstrations"><img src="https://img.shields.io/badge/Demos-18_Apps-green?style=for-the-badge" alt="Demos"></a>
  <a href="#-test-results"><img src="https://img.shields.io/badge/Tests-2%2C461_Passing-brightgreen?style=for-the-badge" alt="Tests"></a>
  <a href="https://arxiv.org/abs/2606.03854"><img src="https://img.shields.io/badge/Tech_Report-arXiv%3A2606.03854-b31b1b?style=for-the-badge" alt="Tech Report"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-Apache_2.0-yellow?style=for-the-badge" alt="License"></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-≥3.10-blue?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/click-≥8.0-green" alt="Click">
  <img src="https://img.shields.io/badge/pytest-100%25_pass-brightgreen" alt="Pytest">
  <img src="https://img.shields.io/badge/coverage-unit_%2B_e2e-orange" alt="Coverage">
  <img src="https://img.shields.io/badge/output-JSON_%2B_Human-blueviolet" alt="Output">
  <a href="https://github.com/HKUDS/.github/blob/main/profile/README.md"><img src="https://img.shields.io/badge/Feishu-Group-E9DBFC?style=flat&logo=feishu&logoColor=white" alt="Feishu"></a>
<a href="https://github.com/HKUDS/.github/blob/main/profile/README.md"><img src="https://img.shields.io/badge/WeChat-Group-C5EAB4?style=flat&logo=wechat&logoColor=white" alt="WeChat"></a>
</p>

**One Command Line**: Make any software agent-ready for Pi, OpenClaw, nanobot, Cursor, Claude Code, etc.&nbsp;&nbsp;[**中文文档**](README_CN.md) | [**日本語ドキュメント**](README_JA.md) | [**Deutsch**](README_DE.md)

<p align="center">
  <img src="assets/cli-typing.gif" alt="CLI-Anything typing demo" width="800">
</p>

<p align="center">
  <img src="assets/teaser.png" alt="CLI-Anything Teaser" width="800">
</p>

---

## 📰 News

> Thanks to all invaluable efforts from the community! More updates continuously on the way everyday..

- **2026-05-30** 🧭 **Hermes skill** proposed (#320), adding a CLI-Anything orchestration skill with installer scripts and HARNESS fallback guidance. 🗺️ **ArcGIS Pro** was proposed for the public registry (#318) as a Windows/ArcPy CLI for cartography, geoprocessing, feature editing, and live-Pro MCP workflows.

- **2026-05-27** 🔧 **CLI-Hub** registry date updates now handle `python -m pip` install commands (#312), improving package-date detection for registry automation.

- **2026-05-23** 📝 **Obsidian Agent CLI** was proposed for the public registry (#307), bringing a PyPI-installed Obsidian automation CLI with persistent agent memory workflows and a pinned skill link.

- **2026-05-21** 🔒 **Sketch CLI** token-file handling was hardened against path traversal and symlink escapes (#304).

- **2026-05-20** 📓 **Joplin CLI** was proposed (#300) with notebooks, notes, to-dos, tags, attachments, search/sync, import/export, server/E2EE helpers, full docs, packaged skill docs, and a 134-test validation baseline.

- **2026-05-20** 🎛️ **Rekordbox CLI** merged (#252) with guarded SQLCipher write paths, backup-required forced writes, smoke coverage, and root skill sync. 📚 **Calibre CLI** merged (#223) with library/search/metadata/conversion/export workflows, 41 unit tests, real-Calibre E2E evidence, and root skill validation. 🧊 **3MF CLI** merged (#209) with mesh inspection, hole resizing, repair, comparison, and preserved triangle attributes. 🎙️ **MiniMax CLI** merged (#189) with chat/TTS workflows, JSON-safe model/voice listing, REPL quote handling, and smoke/E2E coverage. 🎮 **UEAtelier** joined the registry (#297) as an Unreal Editor MCP self-extension workbench with a Python CLI proxy.

- **2026-05-19** 🛠️ Existing harnesses got a quality/security pass — **Zoom** downloads recordings from direct URLs (#294), **Obsidian** search now uses the Local REST API vendor content types (#289), **LibreOffice** headless conversion is more robust on macOS (#290), and XML/SVG/ODF/MLT/MusicXML/CSL parsing now routes untrusted input through `defusedxml` (#296).

- **2026-05-18** 📈 README presentation refreshed with the Trendshift badge and centered project header polish (#285, #286), keeping the landing section focused on discovery and project momentum.

- **2026-05-17** 🌐 **CLI-Hub** registry handling was hardened (#281) — registry entries are now copied before `_source` tagging, preventing cached or mocked registry data from being mutated in place.

- **2026-05-16** 🔧 **n8n** received the REPL banner crash fix that later merged into main (#280), restoring the no-subcommand interactive startup path with regression coverage.

<details>
<summary>Earlier news (Apr 10–18)</summary>

- **2026-04-18** 🧩 **All SKILL.md files are now being unified under the top-level `skills/` directory** — every CLI skill can be installed from one canonical source with `npx skills add HKUDS/CLI-Anything --skill <skill-name> -g -y`. We also added root-skill validation CI, synced contribution / PR docs and REPL skill-path hints to the new layout, and refreshed the **CLI-Hub** install-first frontend around the new `npx skills` flow.

- **2026-04-17** 🌐 **CLI-Hub** received another install UX pass — public registry metadata and skill coverage were tightened, visit counting was corrected, and the web hub was further refined. 🧪 **Shotcut** render output duration was fixed (#92). 📝 **SKILL** contribution paths were corrected for the new docs flow (#224), and the skill generator now safely handles empty intros (#203).

- **2026-04-16** 🗺️ **QGIS CLI** merged (#207) — a full GIS / map authoring harness landed. 🧬 **UniMol Tools CLI** merged (#219) for molecular modeling workflows. 🌐 **CLI-Hub** also added more public CLIs, including **py4csr**, refreshed its generated meta-skill, corrected SKILL contribution docs, and fixed `apt-get` package extraction in skill generation (#204).

- **2026-04-16** 📈 **Unreal Insights CLI** expanded — added background capture session control (`capture start/status/snapshot/stop`), engine-root-matched `UnrealInsights.exe` resolution/build flows, and refreshed docs/tests for the new orchestration workflow.

- **2026-04-15** 🌐 **CLI-Hub** updated to **v0.2.0** — the PyPI package now supports public CLIs from multiple install sources (`pip`, `npm`, `brew`, bundled/system tools), backed by a new `public_registry.json`. The Hub frontend was redesigned with separate **CLI-Anything CLIs** and **Public CLIs** decks, and live end-to-end checks now cover real install, update, and uninstall flows across both pip and npm packages.

- **2026-04-14** 🧭 **Safari CLI** merged (#212) and added to the Hub registry — browser automation via `safari-mcp`. 🎬 **Kdenlive** also received compatibility fixes for Gen 5 project output and invalid project generation.

- **2026-04-13** 📓 **Obsidian CLI** merged (#211) — knowledge management harness via the Local REST API, with 48 unit tests and 7 E2E tests. ⛓️ **Eth2-Quickstart CLI** merged (#195) — Ethereum staking node management harness. 📚 **Zotero CLI** updated to v0.4.1 (#201) — now shipped from its standalone repo, and CLI-Hub gained support for remote `skill_md` URLs.

- **2026-04-11** 🔗 **n8n CLI** merged (#188) — workflow automation harness for self-hosted automation flows. 🔧 **Exa CLI** fix (#205) added the `x-exa-integration` header for usage tracking. 📦 **CLI-Hub** also gained its PyPI auto-publish workflow and package refresh pipeline.

- **2026-04-10** 📦 **CLI-Hub package manager** launched — `pip install cli-anything-hub` to browse, search, install, update, and uninstall CLI-Anything harnesses from one command. The web Hub also shipped its first install-focused frontend refresh and "Empower yourself" toolkit card.

</details>

<details>
<summary>Earlier news (Apr 1–9)</summary>

- **2026-04-09** 🧹 Cleanup and docs pass (#200) — fixed Openscreen test subtotals, added Openscreen to the Chinese README and project structure, and clarified `/cli-anything` command syntax in the docs.

- **2026-04-08** 🎬 **Openscreen CLI** merged (#183) — screen recording editor harness with 101 tests. ☁️ **CloudAnalyzer CLI** merged (#181) — cloud cost analysis harness with 27 commands. 🌊 **SeaClip / PM2 / ChromaDB** harnesses merged (#129).

- **2026-04-07** 🔄 **Dify Workflow CLI** merged (#191) — workflow automation wrapper. 🔧 **Inkscape** auto-save fix (#193, fixes #182). 🛡️ **DomShell security hardening** (#156) — URL validation and DOM sanitization for the browser CLI. 🥧 **Pi Coding Agent extension** merged (#178).

- **2026-04-06** 🔍 **Exa CLI** merged (#172) — AI-powered web search and answers harness. 🎮 **Godot CLI** merged (#140) — game engine harness with a full demo-game E2E pipeline. ☁️ **CloudAnalyzer** review fixes and frontend improvements also landed.

- **2026-04-03** 🧪 **WireMock CLI** merged (#170) — HTTP mock server harness for API testing. 🥧 **Pi Coding Agent** extension support also landed, and CLI demo recordings were added to the docs.

- **2026-04-01** ⚔️ **Slay the Spire II CLI** merged (#148) — deck-building roguelike harness. 🎥 **VideoCaptioner CLI** merged (#166) — AI-powered video captioning harness. 🛰️ **IntelWatch** was added to the registry for B2B OSINT workflows.

</details>

<details>
<summary>Earlier news (Mar 23–30)</summary>

- **2026-03-30** 🏗️ **CLI-Anything v0.2.0** — HARNESS.md progressive disclosure redesign. Detailed guides extracted into `guides/` for on-demand loading. Phases 1–7 now contiguous. Key Principles and Rules merged into a single authoritative section.

- **2026-03-29** 📐 Blender skill docs updated — enforce absolute render paths and correct prerequisites.

- **2026-03-28** 🌐 **CLIBrowser** added to CLI-Hub registry for agent-accessible browser automation.

- **2026-03-27** 📚 Zotero SKILL.md enhanced with agent-facing constraints; REPL config and executable resolution fixes.

- **2026-03-26** 📖 **Zotero CLI** harness landed for Zotero desktop (library management, collections, citations). Draw.io custom ID bugfix (#132) and registry.json syntax fix.

- **2026-03-25** 🎮 **RenderDoc CLI** merged for GPU frame capture analysis. FreeCAD updated for v1.1. Blender EEVEE engine name corrected. Zoom token permissions hardened.

- **2026-03-24** 🏭 **FreeCAD CLI** added with 258 commands across 17 groups. **iTerm2** and **Teltonika RMS** harnesses added to registry.

- **2026-03-23** 🤖 Launched **CLI-Hub meta-skill** — agents can now discover and install CLIs autonomously. **Krita CLI** harness merged for digital painting.

</details>

<details>
<summary>Earlier news (Mar 11–22)</summary>

- **2026-03-22** 🎵 **MuseScore CLI** merged with transpose, export, and instrument management.

- **2026-03-21** 🔧 Infrastructure improvements — refined test harnesses and documentation across multiple CLIs. Enhanced Windows compatibility for several backends.

- **2026-03-20** 🌐 **Novita AI** CLI added for OpenAI-compatible API access. Registry metadata improvements for better hub discovery.

- **2026-03-19** 📦 Package structure refinements across harnesses. Improved SKILL.md generation with better command documentation.

- **2026-03-18** 🧪 Test coverage expansion — additional E2E scenarios and edge case validation across multiple CLIs.

- **2026-03-17** 🌐 Launched the **[CLI-Hub](https://hkuds.github.io/CLI-Anything/)** — a central registry where you can browse, search, and install any CLI with a single `pip` command.

- **2026-03-16** 🤖 Added **SKILL.md generation** (Phase 6.5) — every generated CLI now ships with an AI-discoverable skill definition.

- **2026-03-15** 🐾 Support for **OpenClaw** from the community! Merged Windows `cygpath` guard for cross-platform support.

- **2026-03-14** 🔒 Fixed a GIMP Script-Fu path injection vulnerability and added **Japanese README** translation.

- **2026-03-13** 🔌 **Qodercli** plugin officially merged as a community contribution with dedicated setup scripts.

- **2026-03-12** 📦 **Codex skill** integration landed, bringing CLI-Anything to yet another AI coding platform.

- **2026-03-11** 📞 **Zoom** video conferencing harness added as the 11th supported application.

</details>

---

## 🤔 Why CLI?

CLI is the universal interface for both humans and AI agents:

• **Structured & Composable** - Text commands match LLM format and chain for complex workflows

• **Lightweight & Universal** - Minimal overhead, works across all systems without dependencies

• **Self-Describing** - --help flags provide automatic documentation agents can discover

• **Proven Success** - Claude Code runs thousands of real workflows through CLI daily

• **Agent-First Design** - Structured JSON output eliminates parsing complexity

• **Deterministic & Reliable** - Consistent results enable predictable agent behavior

## 🚀 Quick Start

CLI-Anything has two equally useful starting points:

| Goal | Start Here |
|------|------------|
| **Use the existing CLI ecosystem now** | Install `cli-anything-hub`, browse the registry, and install ready-made CLIs. |
| **Build a new agent-native CLI** | Install the CLI-Anything plugin/skill for your agent, then run the 7-phase harness generator. |

<details open>
<summary><strong>Phase 1: Empower yourself — your CLI toolkit</strong></summary>

Install the CLI-Hub package manager first. It lets you browse, search, inspect, install, update, uninstall, and launch CLI-Anything harnesses plus public third-party CLIs from one command.

**PIP**

```bash
pip install cli-anything-hub
```

| Command | What it does |
|---------|--------------|
| `cli-hub list` | Browse the registry |
| `cli-hub search <query>` | Search by keyword |
| `cli-hub info <name>` | Inspect one CLI |
| `cli-hub install <name>` | Install from CLI-Hub |
| `cli-hub update <name>` | Update an install |
| `cli-hub uninstall <name>` | Remove an install |
| `cli-hub launch <name> [args...]` | Run an installed CLI |

```bash
# Browse what is available
cli-hub list
cli-hub search image

# Install and try a CLI immediately
cli-hub install gimp
cli-hub info gimp
cli-hub launch gimp
```

> Some CLIs wrap real desktop or backend software. If a selected CLI needs GIMP, Blender, LibreOffice, or another upstream tool, install that upstream application too.

</details>

<details open>
<summary><strong>Phase 1.5: Empower your agents — install in one command</strong></summary>

Give SKILL-compatible agents the CLI-Hub meta-skill so they can discover and install the right CLI for a task.

**Also available on:** [ClawHub](https://clawhub.ai/yuh-yang/cli-anything-hub), [SkillHub](https://www.skillhub.club/web/skills/itsyuhao-cli-anything-hub), [SkillHub.cn](https://skillhub.cn/skills/cli-hub-meta-skill)

**NPX SKILLS**

```bash
npx skills add HKUDS/CLI-Anything --skill cli-hub-meta-skill -g -y
```

**Works with:** OpenClaw, Nanobot, Claude Code, Codex, Reasonix, Antigravity, and other SKILL-compatible agents.

Then prompt:

```text
Find appropriate CLI software in CLI-Hub and complete the task: ...
```

</details>

<details open>
<summary><strong>Phase 3: Build a new CLI when the registry does not have one yet</strong></summary>

Use the CLI-Anything generator when you need a new harness for software, a codebase, or an internal tool that is not already available through CLI-Hub.

**Prerequisites**

- **Python 3.10+**
- Target software or source repo available locally or online
- A supported AI coding agent: [Claude Code](#-claude-code) | [Cursor](#-cursor) | [Pi](#-pi-coding-agent) | [OpenClaw](#-openclaw) | [OpenCode](#-opencode) | [Codex](#-codex) | [Hermes](#-hermes) | [Reasonix](#-reasonix) | [Qodercli](#-qodercli) | [GitHub Copilot CLI](#-github-copilot-cli) | [More Platforms](#-more-platforms-coming-soon)

### Pick Your Agent Platform

<details open>
<summary><h4 id="-claude-code">⚡ Claude Code</h4></summary>

**Step 1: Add the Marketplace**

CLI-Anything is distributed as a Claude Code plugin marketplace hosted on GitHub.

```bash
# Add the CLI-Anything marketplace
/plugin marketplace add HKUDS/CLI-Anything
```

**Step 2: Install the Plugin**

```bash
# Install the cli-anything plugin from the marketplace
/plugin install cli-anything
```

That's it. The plugin is now available in your Claude Code session.

> **Note for Win Users:** Claude Code runs shell commands via `bash`. On Windows, install Git for Windows (includes `bash` and
`cygpath`) or use WSL; otherwise commands may fail with `cygpath: command not found`.

**Step 3: Build a CLI in One Command**

```bash
# /cli-anything <software-path-or-repo>
# Generate a complete CLI for GIMP (all 7 phases)
/cli-anything ./gimp
```

Command compatibility across Claude Code versions:
- Use `/cli-anything` as the primary entrypoint.
- On older builds where `/cli-anything` isn't recognized **after confirming the plugin is installed and loaded**, try the legacy entry form `/cli-anything:cli-anything`.
- Auxiliary commands keep the `:subcommand` form (e.g. `/cli-anything:refine`).

If you see `Unknown skill: cli-anything`, focus on plugin install/load first (both entry forms reference the same skill, so swapping forms won't help):
1. Reload plugin commands: `/reload-plugins`
2. Verify the plugin is loaded: `/help cli-anything` (CLI-Anything help/commands should appear)
3. Reinstall from marketplace if needed:
   - `/plugin marketplace add HKUDS/CLI-Anything`
   - `/plugin install cli-anything`
4. After confirming the plugin is available, retry the entry command:
   - Preferred: `/cli-anything ./gimp`
   - Older builds only: `/cli-anything:cli-anything ./gimp`

This runs the full pipeline:
1. 🔍 **Analyze** — Scans source code, maps GUI actions to APIs
2. 📐 **Design** — Architects command groups, state model, output formats
3. 🔨 **Implement** — Builds Click CLI with REPL, JSON output, undo/redo
4. 📋 **Plan Tests** — Creates TEST.md with unit + E2E test plans
5. 🧪 **Write Tests** — Implements comprehensive test suite
6. 📝 **Document** — Updates TEST.md with results
7. 📦 **Publish** — Creates `setup.py`, installs to PATH

**Step 4 (Optional): Refine and Improve the CLI**

After the initial build, you can iteratively refine the CLI to expand coverage and add missing capabilities:

```bash
# Broad refinement — agent analyzes gaps across all capabilities
/cli-anything:refine ./gimp

# Focused refinement — target a specific functionality area
/cli-anything:refine ./gimp "I want more CLIs on image batch processing and filters"
```

The refine command performs gap analysis between the software's full capabilities and current CLI coverage, then implements new commands, tests, and documentation for the identified gaps. You can run it multiple times to steadily expand coverage — each run is incremental and non-destructive.

<details>
<summary><strong>Alternative: Manual Installation</strong></summary>

If you prefer not to use the marketplace:

```bash
# Clone the repo
git clone https://github.com/HKUDS/CLI-Anything.git

# Copy plugin to Claude Code plugins directory
cp -r CLI-Anything/cli-anything-plugin ~/.claude/plugins/cli-anything

# Reload plugins
/reload-plugins
```

</details>

</details>

<details>
<summary><h4 id="-pi-coding-agent">⚡ Pi Coding Agent</h4></summary>

**Step 1: Install the Extension**

The extension lives at `.pi-extension/cli-anything/` in this repository. Install it globally so `/cli-anything` commands are available in **all** Pi projects:

```bash
# Clone the repo
git clone https://github.com/HKUDS/CLI-Anything.git
cd CLI-Anything

# Install globally into Pi's extensions directory
bash .pi-extension/cli-anything/install.sh
```

To uninstall:

```bash
bash .pi-extension/cli-anything/install.sh --uninstall
```

> **How it works:** `install.sh` copies the extension files (including HARNESS.md, commands, guides, scripts, and templates from `cli-anything-plugin/`) into `~/.pi/agent/extensions/cli-anything/`, which Pi auto-discovers on startup. Run `/reload` in Pi or restart Pi to activate.

**Step 2: Build a CLI in One Command**

Once the extension is loaded, the following commands are available:

```bash
# Generate a complete CLI for GIMP (all 7 phases)
/cli-anything ./gimp

# Build from a GitHub repo
/cli-anything https://github.com/blender/blender
```

**Step 3 (Optional): Refine and Improve the CLI**

```bash
# Broad refinement — agent analyzes gaps across all capabilities
/cli-anything:refine ./gimp

# Focused refinement — target a specific functionality area
/cli-anything:refine ./gimp "batch processing and filters"
```

**Available Commands**

| Command | Description |
|---------|-------------|
| `/cli-anything <path-or-repo>` | Build a complete CLI harness |
| `/cli-anything:refine <path> [focus]` | Refine an existing CLI harness |
| `/cli-anything:test <path-or-repo>` | Run tests for a CLI harness |
| `/cli-anything:validate <path-or-repo>` | Validate a CLI harness |
| `/cli-anything:list [options]` | List all CLI-Anything tools |

</details>

<details>
<summary><h4 id="-opencode">⚡ OpenCode (Experimental)</h4></summary>

**Step 1: Install the Commands**

> **Note:** Please upgrade to the latest OpenCode. Older versions may use a different commands path.

Copy the CLI-Anything commands **and** `HARNESS.md` to your OpenCode commands directory:

```bash
# Clone the repo
git clone https://github.com/HKUDS/CLI-Anything.git

# Glob