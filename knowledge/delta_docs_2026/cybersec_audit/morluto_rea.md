# Official Delta Reference: morluto_rea
Source: https://github.com/morluto/rea
Domain: cybersec_audit

Title: GitHub - morluto/rea: Reverse engineer anything with agents, from app behavior down to native binaries.

URL Source: https://github.com/morluto/rea

Markdown Content:
Important

Get REA from [morluto/rea](https://github.com/morluto/rea), [rea.tools](https://rea.tools/), or the [rea-agents npm package](https://www.npmjs.com/package/rea-agents). Follow the installation and release links from these official sources. A similar repository name or copied README does not establish that a download is official.

[![Image 1: REA launching its analysis bridge inside Hopper while inspecting a native binary](https://github.com/morluto/rea/raw/main/docs/assets/rea-hopper-analysis.png)](https://github.com/morluto/rea/blob/main/docs/assets/rea-hopper-analysis.png)

  

* * *

See a feature in an app that you want in your own product? Ask your agent to investigate it with REA. It can inspect the app without its source code, explain how the feature works, show the evidence, and build a version for your project.

REA connects your agent to tools for inspecting native binaries, JavaScript and Electron apps, .NET assemblies, and websites. You can also use the same tools from your terminal. Analysis runs locally, and results include the evidence and limitations behind each conclusion.

Setup registers REA with your agent and installs matching workflow instructions. Native analysis can use an existing Hopper, Ghidra, IDA or Kuna installation; setup can optionally install Hopper with approval. Static JavaScript analysis needs no native analysis engine.

> **[Visit the REA website](https://rea.tools/)** for setup instructions, illustrated guides, and real case studies.

## Quick start

[](https://github.com/morluto/rea#quick-start)
On Linux, Ghidra, JADX, firmware tool launches and static JavaScript/Electron analysis require a procps-compatible system `ps` for process ownership checks. Recovery steps are in `docs/getting-started/installation.md` under "Linux owned-process prerequisite".

### Set up your agent

[](https://github.com/morluto/rea#set-up-your-agent)
With Node.js and npm installed, run:

npx rea-agents setup

Choose your agents, review the proposed changes, and approve them. Setup adds REA's MCP server and matching workflow instructions, with backups of existing configuration. Restart your agent afterward. Setup records the selected runtime and REA entry script directly. If acquired through a package runner, keep its cache entry available. Run package acquisition from a trusted directory outside the target project. Installation and recovery details are in the setup guide below.

Setup supports Claude Code, Codex, Cursor, Gemini CLI, Grok Build and [other agents](https://github.com/morluto/rea/blob/main/docs/getting-started/installation.md#supported-agents). See [installation and setup](https://github.com/morluto/rea/blob/main/docs/getting-started/installation.md) for provider configuration, manual MCP registration, Claude Code/Codex plugins, and the Cursor Marketplace plugin.

MCP advertises compact input schemas to reduce context overhead; guidance a compact schema omits follows the tool description. The full tool set and canonical server validation are unchanged. See "Compact input schema profile" in the MCP contracts guide.

Output schemas are omitted from `tools/list` by default: no model API reads them, and REA validates every result itself. Set `REA_MCP_OUTPUT_SCHEMA_PROFILE=compact` to advertise each output schema within a 4,096-byte budget. Both settings keep canonical server-side validation and complete structured results. See "Output schemas" in the MCP contracts guide.

### Ask your agent

[](https://github.com/morluto/rea#ask-your-agent)

```
Understand how search works in the Notes app, show me the evidence, and build a
similar feature for my project.
```

Replace Notes with your target app and the feature you want to understand.

### Use the terminal

[](https://github.com/morluto/rea#use-the-terminal)
Inspect an extracted JavaScript/Electron app directory or ASAR:

npx -y rea-agents@latest analyze-javascript-application /absolute/path/to/app --json

The result includes modules, imports, Electron boundaries and their evidence. Replace the path with your target, such as `"D:/apps/example"` on Windows.

To install the `rea` command for regular use:

npm install --global rea-agents
rea --help

For native analysis, configure a provider first. See the [CLI and Evidence guide](https://github.com/morluto/rea/blob/main/docs/getting-started/cli.md) for native commands, provider selection, snapshots and scripting.

### Update REA

[](https://github.com/morluto/rea#update-rea)
REA changes quickly, and new releases include frequent bug fixes. Keep your installation up to date.

For a CLI installed with `npm install --global` or `bun add --global`:

rea update

`rea --update` is an alias for this verified workflow and accepts the same global output flags. Use `rea update` when combining it with other command controls.

Updater commands retain at most 4 MiB of stdout and stderr combined. Oversized metadata replies are rejected after the command exits; verbose installs continue with bounded diagnostics. Human progress output respects terminal backpressure and waits for submitted writes to finish.

Bun global updates require Bun 1.2.17 or later. With an older Bun release, upgrade Bun manually before running `rea update`.

To refresh your agent registrations and skill, run the setup command printed by the update.

If you use `npx`, update your agent setup with:

npx rea-agents@latest setup

Review the setup changes and restart your agent. For one-off CLI commands, use `npx rea-agents@latest` followed by the command. With Bun, use `bunx rea-agents@latest` in place of `npx rea-agents@latest`.

## How REA works

[](https://github.com/morluto/rea#how-rea-works)
Your agent calls REA through MCP to inspect the target and trace relevant code. REA returns findings with their evidence. The agent uses them to ask follow-up questions, explain the behavior, or write and test an implementation. CLI commands use the same workflows.

[![Image 2: REA investigation flow: your agent asks about a local target, REA inspects and traces it using analysis tools, and the agent uses the returned code, references and unknowns to explain, implement and test.](https://github.com/morluto/rea/raw/main/website/public/assets/figures/rea-investigation-flow.svg)](https://github.com/morluto/rea/blob/main/website/public/assets/figures/rea-investigation-flow.svg)

[Open the full-size figure](https://github.com/morluto/rea/blob/main/website/public/assets/figures/rea-investigation-flow.svg).

## What you can analyze

[](https://github.com/morluto/rea#what-you-can-analyze)
REA requires Node.js 22.x (>=22.23.4), 24.x (>=24.22.1), or 26.12.1+, plus npm. Additional tools and host support depend on the target:

| Target | What REA returns | Requirements and guide |
| --- | --- | --- |
| Desktop installations | Runtime candidates, supporting files, component markers and next probes | Built-in bounded directory/header inspection; [desktop applications](https://github.com/morluto/rea/blob/main/docs/desktop-applications.md) |
| Native binaries | Pseudocode, assembly, strings, symbols, calls and references | Hopper, Ghidra, IDA or Kuna; [native analysis](https://github.com/morluto/rea/blob/main/docs/guides/native/native-investigation.md) |
| Offline ELF layout | Sections, segments, original symbols/relocations and static mitigation candidates | Caller-supplied pwntools on Linux x64; [binary diagnostics](https://github.com/morluto/rea/blob/main/docs/guides/native/binary-diagnostics.md) |
| Go binaries | Embedded compiler version, modules, replacements and build settings | Built-in static ELF/PE/thin Mach-O inspection; no Go installation required |
| GPU code objects | CUDA/HIP targets, selected kernel parameters and resources, retained PTX text | Built-in static ELF/PE/fatbin/CUBIN/PTX inspection; [GPU code objects](https://github.com/morluto/rea/blob/main/docs/gpu-code-objects.md) |
| Model artifacts | GGUF / safetensors metadata, tensor declarations and derived totals | Built-in header inspection; optional full-file hash; [model files](https://github.com/morluto/rea/blob/main/docs/model-artifacts.md) |
| IL2CPP metadata | Unity global-metadata.dat assembly images, type and method names and index ranges | Built-in static decoding of versions 24, 27, 29, 31 and 39; no Unity required |
| Godot PCK | Archive inventory and extraction, original header/directory facts and selected content identities | Built-in static formats 2, 3 and 4; no Godot required |
| Rust binaries | Embedded cargo-auditable crate names, versions, sources and dependency edges | Built-in static ELF/PE/thin Mach-O/WebAssembly module inspection; [Rust binaries](https://github.com/morluto/rea/blob/main/docs/rust-binaries.md) |
| PE certificates | Authenticode WIN_CERTIFICATE entries and PKCS#7 signer/X.509 identity fields | Built-in static PE inspection; [PE certificates](https://github.com/morluto/rea/blob/main/docs/pe-certificates.md) |
| PE imports | Import and delay-load DLL names, ordinals, IAT RVAs and pefile import hash | Built-in static PE inspection; [PE imports](https://github.com/morluto/rea/blob/main/docs/pe-imports.md) |
| Windows shortcuts | Shell Link target, arguments, working dir, ExtraData and Tracker droid facts | Built-in static LNK inspection; [Windows shortcuts](https://github.com/morluto/rea/blob/main/docs/guides/native/windows-shortcut.md) |
| ELF notes | PT_NOTE/SHT_NOTE owners, types, GNU build-id and ABI-tag fields | Built-in static ELF inspection; [ELF notes](https://github.com/morluto/rea/blob/main/docs/elf-notes.md) |
| DWARF compile units | Compile-unit name, directory, producer, language, and dwo_name | Built-in static ELF, Mach-O, and PE inspection; [DWARF compile units](https://github.com/morluto/rea/blob/main/docs/guides/native/dwarf-units.md) |
| ELF dependencies | DT_NEEDED, SONAME, RPATH/RUNPATH, GNU versions, and undefined imports | Built-in static ELF inspection; [ELF dependencies](https://github.com/morluto/rea/blob/main/docs/elf-dependencies.md) |
| Binary hardening | PIE, NX, RELRO, CFG and related header flags for ELF, PE and Mach-O | Built-in static header inspection; [binary hardening](https://github.com/morluto/rea/blob/main/docs/binary-hardening.md) |
| Apple IPS crashes | .ips metadata, threads, images, registers and documented crash classes | Built-in static JSON inspection; [Apple IPS](https://github.com/morluto/rea/blob/main/docs/apple-ips.md) |
| Linux kernel modules | .modinfo keys, __versions CRCs, this_module presence, and signature trailer | Built-in static ELF inspection; [kernel modules](https://github.com/morluto/rea/blob/main/docs/kernel-modules.md) |
| Erlang BEAM | IFF chunks, atoms, exports, imports, lambdas and the Code header | Built-in static BEAM inspection; [Erlang BEAM](https://github.com/morluto/rea/blob/main/docs/erlang-beam.md) |
| NuGet packages | Package identity, dependency groups, license, repository and ZIP contents | Built-in static .nupkg inspection; [NuGet packages](https://github.com/morluto/rea/blob/main/docs/guides/managed/nuget-nupkg.md) |
| WASM artifact | Validation, sections, exact import/export WAT forms and decoded WAT | Caller-supplied WABT 1.0.42; `inspect_wasm_artifact` |
| EVM bytecode | Dispatch selectors, byte offsets, inferred arguments and mutability | Local raw/hex carrier on Linux x64; [offline EVM guide](https://github.com/morluto/rea/blob/main/docs/guides/evm/evm-bytecode.md) |
| SQLite databases | Tables, columns, indexes, views, triggers and selected ordinary-table rows | Local database/WAL snapshot; Node.js 24.x >=24.15 or 26+ with native SQLite limits |
| Recorded Linux crashes | Raw notes, every recorded thread's registers/signals and optional mapping candidates | Caller-supplied pwntools on Linux x64; optional GDB/pwndbg; [recorded crashes](https://github.com/morluto/rea/blob/main/docs/guides/native/recorded-crashes.md) |
| JavaScript / Electron | Modules, imports, source maps, routes, IPC, native add-ons, `rea audit-release-exposure` | Node.js and npm; Linux: procps-compatible `ps`; [application analysis](https://github.com/morluto/rea/blob/main/docs/guides/javascript/javascript-application-workflows.md) |
| Websites | Page structure, scripts, network observations and requested screenshots | A Chrome-family browser; [browser analysis](https://github.com/morluto/rea/blob/main/docs/guides/web/browser-observation.md) |
| Saved network captures | Requests, responses, exposed payloads and source locations | HAR or Fiddler Everywhere SAZ; mitmdump on Linux for native mitmproxy; [capture guide](https://github.com/morluto/rea/blob/main/docs/guides/web/web-network-captures.md) |
| .NET assemblies | Metadata, CIL instructions, declared native dependencies and build comparisons | None (static only); [managed-code guide](https://github.com/morluto/rea/blob/main/docs/guides/managed/managed-code-analysis.md) |
| Android APKs | Manifest declarations, classes, decompiled methods and references | Headless JADX and a full JDK on Linux/macOS/Windows x64; [Android guide](https://github.com/morluto/rea/blob/main/docs/guides/android/android-analysis.md) |
| APK signatures | v1/v2/v3/v3.1 signers, certificate fingerprints, key rotation and digest self-consistency | None (static only); `inspect_apk_signature` |
| Android devices | Devices, packages, processes, logs, dumps, screen captures, and APK/file transfers | Caller-supplied adb (emulator or hardware); [ADB guide](https://github.com/morluto/rea/blob/main/docs/guides/android/adb-device-analysis.md) |
| JEB projects | Engine-backed project units, artifact digests and type/method pseudo-code | A caller-started JEB client serving MCP, selected with REA_JEB_MCP_URL; [JEB guide](https://github.com/morluto/rea/blob/main/docs/providers/jeb-analysis.md) |
| Android resources | Decoded manifest, string tables, locales and version facts | Caller-supplied Apktool launcher; [resource guide](https://github.com/morluto/rea/blob/main/docs/guides/android/apktool-resource-analysis.md) |
| Flutter apps | Dart snapshot hash, per-ABI library digests and engine build provenance | None (static APK parsing); [Flutter guide](https://github.com/morluto/rea/blob/main/docs/guides/android/flutter-analysis.md) |
| Firmware | Regions, extraction results and native-analysis handoffs | Binwalk / Unblob on Linux; [firmware guide](https://github.com/morluto/rea/blob/main/docs/guides/firmware/firmware-analysis.md) |
| Recorded packets | Selected fields, repeated values, filters and decode-as rules | Linux: TShark 4.x + prlimit; [capture guide](https://github.com/morluto/rea/blob/main/docs/guides/data/packet-captures.md) |
| Packet summaries | Endpoints, DNS, TLS SNI, protocol distribution and HTTP requests | Caller-supplied tshark and capinfos (Linux-verified); [pcap guide](https://github.com/morluto/rea/blob/main/docs/guides/data/pcap-analysis.md) |
| Recorded logic signals | Decoder annotations, sample ranges and diagnostics | Linux: sigrok-cli 0.7.2 + prlimit; [signal recordings](https://github.com/morluto/rea/blob/main/docs/guides/signals/signal-recordings.md) |
| Packages and resources | File inventories, digests, plists, Apple bundle anatomy and extracted resources | [Artifact and JavaScript guide](https://github.com/morluto/rea/blob/main/docs/guides/javascript/javascript-artifact-reconstruction.md), [Apple applications](https://github.com/morluto/rea/blob/main/docs/guides/apple/apple-application-analysis.md) |
| Process behavior | Terminal output, interactions, exit and filesystem observations, and run comparisons | Linux/macOS with a native PTY; [process capture](https://github.com/morluto/rea/blob/main/docs/guides/runtime/process-capture.md) |
| PyInstaller executables | CArchive members, Python version, entry scripts and extracted bytecode | None (static only); [Python packaged applications](https://github.com/morluto/rea/blob/main/docs/python-packaged-applications.md) |
| Deno compile binaries | Virtual files, entry point, recorded options, npm snapshot length | None (static only); [Deno compile executables](https://github.com/morluto/rea/blob/main/docs/deno-standalone.md) |

Static JavaScript and .NET inspection read the supplied files without running the application. Runtime capture runs or interacts with the selected target using your user permissions; each runtime guide describes its effects.

For offline native-binary inspection, REA also supports caller-supplied GNU objdump and Rizin. See the [reverse-engineering tools guide](https://github.com/morluto/rea/blob/main/docs/reverse-engineering-tools.md) for provider setup, CLI commands, and Evidence limitations. REA does not install or update either provider.

Native formats and host support vary by provider. See [Hopper and Ghidra setup](https://github.com/morluto/rea/blob/main/docs/getting-started/installation.md#hopper), the [IDA guide](https://github.com/morluto/rea/blob/main/docs/providers/ida-provider.md) (including an optional native MCP bridge), the [Kuna decompiler guide](https://github.com/morluto/rea/blob/main/docs/kuna-provider.md), and [experimental Windows Ghidra support](https://github.com/morluto/rea/blob/main/docs/providers/windows-ghidra-p0.md). Ghidra also supports [16-bit DOS analysis](https://github.com/morluto/rea/blob/main/docs/providers/ghidra-dos.md). For large binaries, raise the provider's startup deadline with `REA_GHIDRA_STARTUP_TIMEOUT_MS` or `REA_HOPPER_STARTUP_TIMEOUT_MS`. For provider selection, see the [CLI guide](https://github.com/morluto/rea/blob/main/docs/getting-started/cli.md#choose-a-provider). Check [release availability](https://github.com/morluto/rea/blob/main/docs/getting-started/installation.md#released-package-and-main) for features added since the latest npm release.

## Showcases

[](https://github.com/morluto/rea#showcases)[![Image 3: Illustrations of the DX-Ball sound-pan, Notion clipboard-bridge, and TH04 bullet-ring showcases](https://github.com/morluto/rea/raw/main/docs/assets/rea-showcases.svg)](https://rea.tools/showcase/)
### DX-Ball: reconstruct a sound-pan calculation

[](https://github.com/morluto/rea#dx-ball-reconstruct-a-sound-pan-calculation)
Follow a sound call into its position-to-pan helper, inspect the instructions, and turn incomplete pseudocode into C. The reconstruction passes 3,205 original-x86 cases and reproduces all 63 compiled function bytes.

[Read the case study](https://rea.tools/showcase/dx-ball/) · [Reconstruction repository](https://github.com/N0zoM1z0/dx-ball)

### Notion: trace the Electron clipboard bridge

[](https://github.com/morluto/rea#notion-trace-the-electron-clipboard-bridge)
Find the renderer's clipboard API, follow it through preload and IPC into the main process, and inspect the rich clipboard format.

[Read the case study](https://rea.tools/showcase/notion/)

### TH04: recover a DOS bullet-ring calculation

[](https://github.com/morluto/rea#th04-recover-a-dos-bullet-ring-calculation)
Inspect the original PC-98 game's 16-bit instructions, recover the fixed and aimed angle calculations, and compare the reconstructed C++ with the historical compiler output.

[Read the case study](https://rea.tools/showcase/th04/) · [Reconstruction repository](https://github.com/N0zoM1z0/th04)

### Build RL environments with REA

[](https://github.com/morluto/rea#build-rl-environments-with-rea)
Record a web app session, turn its API into tools, and export an environment an AI agent can use. Run it with AgentEnv, then add tasks and reward checks for RL training or evaluation.

[Read the guide](https://rea.tools/guides/rl-environments/) · [Watch the video](https://x.com/reatools/status/2112574822584918075?s=20)

If you've used REA on something interesting, we'd love to see it. Share your case in an [issue](https://github.com/morluto/rea/issues) or a [pull request](https://github.com/morluto/rea/pulls), including the target, your question, how REA helped, and what you found.

## Build RL environments

[](https://github.com/morluto/rea#build-rl-environments)
Give an AI agent a local environment to practice tasks such as finding an issue or creating a folder, without running the original app. Use it for reinforcement learning (RL) or to test how well an agent completes tasks.

REA turns recorded API requests and responses into tools the agent can call. The environment uses the recorded data and supports changes only when the recording confirms their effects.

With REA set up in your agent, replace the example URL and folder tasks below with your own:

```
Use REA to build an RL environment from my test web app at
http://127.0.0.1:3000.
Cover listing, creating, renaming, and deleting folders. You may create and
remove test folders. Leave existing data unchanged.
Save it in a folder named my-env. Check which operations work and tell me
how to run it.
```

Use the command line instead
Use these commands if you already have a file containing the app’s recorded browser requests and responses. Running the result also requires AgentEnv and Docker.

rea environment-build ./session.har ./my-env --name my-env --json
agent-env run ./my-env

REA exports a runnable environment with a basic test to check that it starts and responds. Use it with your RL framework to define task goals, add reward checks, and run training.

[Build an environment](https://rea.tools/guides/rl-environments/) · [Environment reference](https://github.com/morluto/rea/blob/main/docs/agent-environments.md) · [Watch the demo on X](https://x.com/reatools/status/2112574822584918075?s=20)

### Desktop app environments

[](https://github.com/morluto/rea#desktop-app-environments)
REA can also build an environment of a Linux desktop app, which an agent uses through screenshots, the mouse and the keyboard. From a one-line request, such as "Build me a Gnote environment where the agent adds olive oil to the shopping list note", your agent installs the app on a local build computer, writes the task, exports the environment and checks the task in a fresh computer. The machine that builds it needs Linux on amd64 or arm64, Docker and the agentenv framework version the guide pins.

[Set up desktop app environments](https://github.com/morluto/rea/blob/main/docs/desktop-build-computer.md)

## FAQ

[](https://github.com/morluto/rea#faq)

**Which agents can use REA?**
Any agent that supports local MCP servers. Setup configures the [supported agents](https://github.com/morluto/rea/blob/main/docs/getting-started/installation.md#supported-agents); other clients can use [manual MCP registration](https://github.com/morluto/rea/blob/main/docs/getting-started/installation.md#mcp-registry).

**Do I need a native analysis engine?**
Deep native analysis uses Hopper, Ghidra, IDA or Kuna, depending on the target and operation. Static JavaScript and .NET inspection work without a native analysis engine. Setup can install Hopper after approval; Ghidra, IDA and Kuna use your existing installations. See [provider setup](https://github.com/morluto/rea/blob/main/docs/getting-started/installation.md#hopper) for the options and their supported targets.

**Do I need to start Hopper first?**
REA starts Hopper when an operation needs it. On macOS, a first-run dialog may ask you to choose demo mode or activate your license. Complete that prompt in the same user session before your first CLI/MCP operation or unattended job. Open Hopper manually if needed. See [Hopper startup and troubleshooting](https://github.com/morluto/rea/blob/main/docs/getting-started/installation.md#launcher-paths-and-troubleshooting).

**What does installing the skill from skills.sh do?**
The skill supplies investigation instructions for your agent. Use `npx rea-agents setup` to register REA's MCP server and install the matching instructions, then restart your agent. See [skill-only installation](https: