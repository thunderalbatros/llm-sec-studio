# Official Delta Reference: semgrep_cli
Source: https://github.com/semgrep/semgrep
Domain: cybersec_audit

Title: GitHub - semgrep/semgrep: Lightweight static analysis for many languages. Find bug variants with patterns that look like source code.

URL Source: https://github.com/semgrep/semgrep

Markdown Content:
[![Image 1: Semgrep logo](https://raw.githubusercontent.com/semgrep/semgrep/develop/images/semgrep-logo-light.svg)](https://semgrep.dev/)

## Code scanning at ludicrous speed.

[](https://github.com/semgrep/semgrep#--code-scanning-at-ludicrous-speed)
[![Image 2: Homebrew](https://camo.githubusercontent.com/c7927f86a0c1a9d00884d6276d883eeaf954175fe2c10703e33621206682c897/68747470733a2f2f696d672e736869656c64732e696f2f686f6d65627265772f762f73656d677265703f7374796c653d666c61742d737175617265)](https://formulae.brew.sh/formula/semgrep)[![Image 3: PyPI](https://camo.githubusercontent.com/83b6881389d6dbf02a5bf6dc7c28d27f805768a075aa58514497a914c3273a54/68747470733a2f2f696d672e736869656c64732e696f2f707970692f762f73656d677265703f7374796c653d666c61742d73717561726526636f6c6f723d626c7565)](https://pypi.org/project/semgrep/)[![Image 4: Documentation](https://camo.githubusercontent.com/26d3a16d5335e6fe67f652b635c028bc5e53d3ca01a61ef542549217fc064feb/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f646f63732d73656d677265702e6465762d707572706c653f7374796c653d666c61742d737175617265)](https://semgrep.dev/docs/)[![Image 5: Join Semgrep community Slack](https://camo.githubusercontent.com/b48f57b4efdf4e0c089942ba56a7d23b6455a70b614c781e11c4990e002d153a/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f736c61636b2d332e356b2532306d656d626572732d677265656e3f7374796c653d666c61742d737175617265)](https://go.semgrep.dev/slack)[![Image 6: Issues welcome!](https://camo.githubusercontent.com/381c6f7fa28d78a6a8235dca80250d78854982fe21792c767204bff1f1ee19d6/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f6973737565732d77656c636f6d652d677265656e3f7374796c653d666c61742d737175617265)](https://github.com/semgrep/semgrep/issues/new/choose)[![Image 7: Star Semgrep on GitHub](https://camo.githubusercontent.com/25901ec29f443bad65efb3763249d3135b777950ef329d78d2f5fae974606e1f/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f73746172732f73656d677265702f73656d677265703f6c6162656c3d4769744875622532305374617273267374796c653d666c61742d737175617265)](https://github.com/semgrep/semgrep#readme)[![Image 8: Docker Pulls (Old)](https://camo.githubusercontent.com/60cb29675746309f91b9ac5cd88528414e67c029841110eb53740d018cdbd9b9/68747470733a2f2f696d672e736869656c64732e696f2f646f636b65722f70756c6c732f73656d677265702f73656d677265702e7376673f7374796c653d666c61742d737175617265)](https://hub.docker.com/r/semgrep/semgrep)[![Image 9: Docker Pulls (Old)](https://camo.githubusercontent.com/60cb29675746309f91b9ac5cd88528414e67c029841110eb53740d018cdbd9b9/68747470733a2f2f696d672e736869656c64732e696f2f646f636b65722f70756c6c732f73656d677265702f73656d677265702e7376673f7374796c653d666c61742d737175617265)](https://hub.docker.com/r/semgrep/semgrep)[![Image 10: Follow @semgrep on Twitter](https://camo.githubusercontent.com/df4fed1fd2e8132381a92ff850af52bd7ec853e5613dd62fb5b76b3635259322/68747470733a2f2f696d672e736869656c64732e696f2f747769747465722f666f6c6c6f772f73656d677265703f6c6162656c3d466f6c6c6f7725323073656d67726570267374796c653d736f6369616c26636f6c6f723d626c7565)](https://twitter.com/intent/follow?screen_name=semgrep)

Semgrep is a fast, open-source, static analysis tool that searches code, finds bugs, and enforces secure guardrails and coding standards. Semgrep [supports 30+ languages](https://github.com/semgrep/semgrep#language-support) and can run in an IDE, as a pre-commit check, and as part of CI/CD workflows.

Semgrep is semantic grep for code. While running `grep "2"` would only match the exact string _2_, Semgrep would [match `x = 1; y = x + 1` when searching for _2_](https://semgrep.dev/playground/s/5rKgj). Semgrep rules look like the code you already write; no abstract syntax trees, regex wrestling, or painful DSLs.

Note that in security contexts, Semgrep Community Edition will miss many true positives as it can only analyze code within the boundaries of a single function or file. If you want to use Semgrep for security purposes (**SAST**, **SCA**, or **secrets scanning**), the Semgrep AppSec Platform is strongly recommended since it adds the following critical capabilities:

1.   Improved core analysis capabilities (cross-file, cross-function, data-flow reachability) that greatly reduce false positives by 25% and increase detected true positives by 250%
2.   Contextual post-processing of findings with Semgrep Assistant (AI) to further reduce noise by [~20%](https://a.storyblok.com/f/151984/x/2d12dc0223/whitepaper_-ai-powered-appsec-engineer-automate.pdf?cv=1728584410408). In addition, Assistant enriches findings with tailored, step-by-step remediation guidance that humans find actionable >80% of the time.
3.   Customizable policies and seamless integration into developer workflows, giving security teams granular control over where, when, and how different findings are presented to developers (IDE, PR comment, etc.)

The Semgrep AppSec Platform works out-of-the-box with 20000+ proprietary rules across SAST, SCA, and secrets. Pro rules are written and maintained by the Semgrep security research team and are highly accurate, meaning AppSec teams can feel confident bringing findings directly to developers without slowing them down.

Semgrep analyzes code locally on your computer or in your build environment: **by default, code is never uploaded**. [Get started→.](https://github.com/semgrep/semgrep#getting-started-)

[![Image 11: Semgrep CLI image](https://raw.githubusercontent.com/semgrep/semgrep/develop/images/semgrep-scan-cli.jpg)](https://github.com/semgrep/semgrep#option-1-getting-started-from-the-cli)
### Language support

[](https://github.com/semgrep/semgrep#language-support)
**Semgrep Code** supports 30+ languages, including:

Apex · Bash · C · C++ · C# · Clojure · Dart · Dockerfile · Elixir · HTML · Go · Java · JavaScript · JSX · JSON · Julia · Jsonnet · Kotlin · Lisp · Lua · OCaml · PHP · Python · R · Ruby · Rust · Scala · Scheme · Solidity · Swift · Terraform · TypeScript · TSX · YAML · XML · Generic (ERB, Jinja, etc.)

**Semgrep Supply Chain** supports 12 languages across 15 package managers, including:

C# (NuGet) · Dart (Pub) · Go (Go modules, `go mod`) · Java (Gradle, Maven) · Javascript/Typescript (npm, Yarn, Yarn 2, Yarn 3, pnpm) · Kotlin (Gradle, Maven) · PHP (Composer) · Python (pip, pip-tool, Pipenv, Poetry) · Ruby (RubyGems) · Rust (Cargo) · Scala (Maven) · Swift (SwiftPM)

For more information, see [Supported languages](https://semgrep.dev/docs/supported-languages/).

### Getting started 🚀

[](https://github.com/semgrep/semgrep#getting-started-)
1.   [From the Semgrep AppSec Platform](https://github.com/semgrep/semgrep#option-1-getting-started-from-the-semgrep-appsec-platform-recommended)
2.   [From the CLI](https://github.com/semgrep/semgrep#option-2-getting-started-from-the-cli)

For new users, we recommend starting with the [Semgrep AppSec Platform](https://github.com/semgrep/semgrep#option-1-getting-started-from-the-semgrep-appsec-platform-recommended) because it provides a visual interface, a demo project, result triaging and exploration workflows, and makes setup in CI/CD fast. Scans are still local and code isn't uploaded. Alternatively, you can also start with the CLI and navigate the terminal output to run one-off searches.

### Option 1: Getting started from the Semgrep Appsec Platform (Recommended)

[](https://github.com/semgrep/semgrep#option-1-getting-started-from-the-semgrep-appsec-platform-recommended)
[![Image 12: Semgrep platform image](https://raw.githubusercontent.com/semgrep/semgrep/develop/images/semgrep-main-image.jpg)](https://go.semgrep.dev/login-ghrmgo)

1.   Register on [semgrep.dev](https://go.semgrep.dev/login-ghrmgo)

2.   Explore the demo findings to learn how Semgrep works

3.   Scan your project by navigating to `Projects > Scan New Project > Run scan in CI`

4.   Select your version control system and follow the onboarding steps to add your project. After this setup, Semgrep will scan your project after every pull request.

5.   [Optional] If you want to run Semgrep locally, follow the steps in the CLI section.

### Notes:

[](https://github.com/semgrep/semgrep#notes)
If there are any issues, [please ask for help in the Semgrep Slack](https://go.semgrep.dev/slack).

### Option 2: Getting started from the CLI

[](https://github.com/semgrep/semgrep#option-2-getting-started-from-the-cli)
1.   Install Semgrep CLI

```
# For macOS
# preferred: install through pipx (https://pipx.pypa.io/stable/how-to/install-pipx.html)
pipx install semgrep

# preferred: install through uv (https://docs.astral.sh/uv/getting-started/installation/)
uv tool install semgrep

# best-effort: install through homebrew (maintained on a best-effort basis; often lags behind the latest release)
brew install semgrep

# For Ubuntu/WSL/Linux/macOS
$ python3 -m pip install semgrep

# To try Semgrep without installation run via Docker
$ docker run -it -v "${PWD}:/src" semgrep/semgrep semgrep login
$ docker run -e SEMGREP_APP_TOKEN=<TOKEN> --rm -v "${PWD}:/src" semgrep/semgrep semgrep ci
``` 
2.   Run `semgrep login` to create your account and login to Semgrep. This step is optional, but logging into Semgrep gets you access to:

    *   [Semgrep Supply Chain](https://semgrep.dev/products/semgrep-supply-chain?utm_medium=readme&utm_source=github&utm_content=ssc-product): A dependency scanner that detects reachable vulnerabilities in third party libraries
    *   [Semgrep Code's Pro rules](https://semgrep.dev/products/semgrep-code?utm_medium=readme&utm_source=github&utm_content=code-pro-rules): 600+ high confidence rules written by Semgrep's security research team
    *   [Semgrep Code's Pro engine](https://semgrep.dev/products/pro-engine?utm_medium=readme&utm_source=github&utm_content=pro-engine): An advanced code analysis engine, designed to detect complex vulnerabilities, and reduce false positives

3.   Go to your app's root directory and run `semgrep ci`. This will scan your project to check for vulnerabilities in your source code and its dependencies.

4.   Try writing your own query interactively with `-e`. For example, a check for Python == where the left and right hand sides are the same (potentially a bug): `$ semgrep -e '$X == $X' --lang=py path/to/src`

### Semgrep Ecosystem

[](https://github.com/semgrep/semgrep#semgrep-ecosystem)
The Semgrep ecosystem includes the following:

*   [Semgrep Community Edition](https://semgrep.dev/docs/cli-reference/) - The open-source program analysis engine at the heart of everything. Suitable for ad-hoc use cases with a high tolerance for false positives - think consultants, security auditors, or pentesters.

*   [Semgrep AppSec Platform](https://semgrep.dev/login?utm_medium=readme&utm_source=github&utm_content=appsec-platform) - Easily orchestrate and scale SAST, SCA, and Secrets scanning across an organization, with no risk of overwhelming developers. Customize which findings developers see, where they see them, and integrate with CI providers like GitHub, GitLab, CircleCI, and more. Includes both free and paid tiers.

    *   [Semgrep Code (SAST)](https://semgrep.dev/products/semgrep-code?utm_medium=readme&utm_source=github&utm_content=semgrep-code) - Make real progress on your vulnerability backlog with SAST that minimizes noise and empowers developers to quickly fix issues on their own, even if they have no security knowledge. Easy to deploy secure guardrails and tailored, step-by-step remediation guidance mean developers actually fix issues since they don't feel slowed down.

    *   [Semgrep Supply Chain (SSC)](https://semgrep.dev/products/semgrep-supply-chain?utm_medium=readme&utm_source=github&utm_content=ssc) - A high-signal dependency scanner that detects reachable vulnerabilities in open source third-party libraries and functions.

    *   [Semgrep Secrets (Secrets scanning)](https://semgrep.dev/blog/2023/introducing-semgrep-secrets/) - Secrets detection that uses semantic analysis, improved entropy analysis, and validation to accurately surface sensitive credentials in the developer workflow.

    *   [Semgrep Assistant (AI)](https://semgrep.dev/products/semgrep-code/assistant?utm_medium=readme&utm_source=github&utm_content=assistant) - Assistant is an AI-powered AppSec engineer that helps both developers and AppSec teams prioritize, triage, and remediate Semgrep findings at scale. Humans agree with Assistant auto-triage decisions 97% of the time, and rate generated remediation guidance as helpful 80% of the time. For an overview of how Assistant works, [read this overview](https://a.storyblok.com/f/151984/x/2d12dc0223/whitepaper_-ai-powered-appsec-engineer-automate.pdf?cv=1728584410408).

*   [Semgrep MCP Server](https://github.com/semgrep/semgrep/tree/develop/cli/src/semgrep/mcp) - A [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server that lets AI coding assistants run Semgrep scans directly. Integrates with Cursor, VS Code, Windsurf, Claude Desktop, and more. Run `semgrep mcp` to start it locally.

    *   **Hooks** - Automatically trigger Semgrep scans as you code.
    *   **Skills / Prompts** - Built-in MCP prompts like `write_custom_semgrep_rule` help AI assistants write accurate Semgrep rules.
    *   **Claude Code plugin** - Available on the official marketplace and via the [semgrep/mcp-marketplace](https://github.com/semgrep/mcp-marketplace) repo: `/plugin marketplace add semgrep/mcp-marketplace`
    *   **Cursor plugin** - Available on the official marketplace and via the [semgrep/cursor-plugin](https://github.com/semgrep/cursor-plugin) repo.

Additional resources:

*   [Semgrep Playground](https://semgrep.dev/editor) - An online interactive tool for writing and sharing rules.
*   [Semgrep Registry](https://semgrep.dev/explore) - 2,000+ community-driven rules covering security, correctness, and dependency vulnerabilities.

Join hundreds of thousands of other developers and security engineers already using Semgrep at companies like GitLab, Dropbox, Slack, Figma, Shopify, HashiCorp, Snowflake, and Trail of Bits.

Semgrep is developed and commercially supported by [Semgrep, Inc., a software security company](https://semgrep.dev/).

### Semgrep Rules

[](https://github.com/semgrep/semgrep#semgrep-rules)
Semgrep rules look like the code you already write; no abstract syntax trees, regex wrestling, or painful DSLs. Here's a quick rule for finding Python `print()` statements.

Run it online in Semgrep’s Playground by [clicking here](https://semgrep.dev/playground/r/3qUzQD/ievans.print-to-logger).

[![Image 13: Semgrep rule example for finding Python print() statements](https://raw.githubusercontent.com/semgrep/semgrep/develop/images/semgrep-example-rules-editor.jpg)](https://semgrep.dev/playground/r/3qUzQD/ievans.print-to-logger)

#### Examples

[](https://github.com/semgrep/semgrep#examples)
Visit [Docs > Rule examples](https://semgrep.dev/docs/writing-rules/rule-ideas/) for use cases and ideas.

| Use case | Semgrep rule |
| --- | --- |
| Ban dangerous APIs | [Prevent use of exec](https://semgrep.dev/playground/s/lglB) |
| Search routes and authentication | [Extract Spring routes](https://semgrep.dev/playground/s/Y6wD) |
| Enforce the use secure defaults | [Securely set Flask cookies](https://semgrep.dev/playground/s/6KwW) |
| Tainted data flowing into sinks | [ExpressJS dataflow into sandbox.run](https://semgrep.dev/playground/s/qEpR) |
| Enforce project best-practices | [Use assertEqual for == checks](https://semgrep.dev/playground/s/oEox), [Always check subprocess calls](https://semgrep.dev/playground/s/zENk) |
| Codify project-specific knowledge | [Verify transactions before making them](https://semgrep.dev/playground/s/p8zk) |
| Audit security hotspots | [Finding XSS in Apache Airflow](https://semgrep.dev/playground/s/KPwj), [Hardcoded credentials](https://semgrep.dev/playground/s/2Br8) |
| Audit configuration files | [Find S3 ARN uses](https://semgrep.dev/playground/s/jEKD) |
| Migrate from deprecated APIs | [DES is deprecated](https://semgrep.dev/playground/r/java.lang.security.audit.crypto.des-is-deprecated.des-is-deprecated), [Deprecated Flask APIs](https://semgrep.dev/playground/r/python.flask.maintainability.deprecated.deprecated-apis.flask-deprecated-apis), [Deprecated Bokeh APIs](https://semgrep.dev/playground/r/python.bokeh.maintainability.deprecated.deprecated_apis.bokeh-deprecated-apis) |
| Apply automatic fixes | [Use listenAndServeTLS](https://semgrep.dev/playground/s/1Ayk) |

### Extensions

[](https://github.com/semgrep/semgrep#extensions)
Visit [Docs > Extensions](https://semgrep.dev/docs/extensions/) to learn about using Semgrep in your editor or pre-commit. When integrated into CI and configured to scan pull requests, Semgrep will only report issues introduced by that pull request; this lets you start using Semgrep without fixing or ignoring pre-existing issues!

### Documentation

[](https://github.com/semgrep/semgrep#documentation)
Browse the full Semgrep [documentation on the website](https://semgrep.dev/docs). If you’re new to Semgrep, check out [Docs > Getting started](https://semgrep.dev/docs/getting-started/) or the [interactive tutorial](https://semgrep.dev/learn).

### Metrics

[](https://github.com/semgrep/semgrep#metrics)
Using remote configuration from the [Registry](https://semgrep.dev/r) (like `--config=p/ci`) reports pseudonymous rule metrics to semgrep.dev.

When using configs from local files (like `--config=xyz.yml`), metrics are sent only when the user is logged in.

To disable Registry rule metrics, use `--metrics=off`.

The Semgrep [privacy policy](https://semgrep.dev/docs/metrics) describes the principles that guide data-collection decisions and the breakdown of the data that are and are not collected when the metrics are enabled.

### More

[](https://github.com/semgrep/semgrep#more)
*   [Frequently asked questions (FAQs)](https://semgrep.dev/docs/faq/)
*   [Contributing](https://semgrep.dev/docs/contributing/contributing/)
*   [Build instructions for developers](https://github.com/semgrep/semgrep/blob/develop/INSTALL.md)
*   [Ask questions in the Semgrep community Slack](https://go.semgrep.dev/slack)
*   [CLI reference and exit codes](https://semgrep.dev/docs/cli-usage)
*   [Semgrep YouTube channel](https://www.youtube.com/c/semgrep)
*   [License (LGPL-2.1)](https://github.com/semgrep/semgrep/blob/develop/LICENSE)
*   [Licensing Semgrep](https://semgrep.dev/docs/licensing/)

### Upgrading

[](https://github.com/semgrep/semgrep#upgrading)
To upgrade, run the command below associated with how you installed Semgrep:

# Using pipx
$ pipx upgrade semgrep

# Using uv tool command
$ uv tool upgrade semgrep

# Using Homebrew
$ brew upgrade semgrep

# Using Docker
$ docker pull semgrep/semgrep:latest
