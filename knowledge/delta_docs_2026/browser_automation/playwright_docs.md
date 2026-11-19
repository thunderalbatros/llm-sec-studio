# Official Delta Reference: playwright_docs
Source: https://github.com/microsoft/playwright
Domain: browser_automation

Title: GitHub - microsoft/playwright: Playwright is a framework for Web Testing and Automation. It allows testing Chromium, Firefox and WebKit with a single API.

URL Source: https://github.com/microsoft/playwright

Markdown Content:
[![Image 1: npm version](https://camo.githubusercontent.com/dca89916f770efa770fe1920ee41fa281fe6e872be6605560086978f494a0cff/68747470733a2f2f696d672e736869656c64732e696f2f6e706d2f762f706c61797772696768742e737667)](https://www.npmjs.com/package/playwright)[![Image 2: Chromium version](https://camo.githubusercontent.com/55e71f9110ef361275b5e6651eb950edcdad2002ef0c7603c71f6cf34321a4a9/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f6368726f6d69756d2d3135392e302e383135342e362d626c75652e7376673f6c6f676f3d676f6f676c652d6368726f6d65)](https://www.chromium.org/Home)[![Image 3: Firefox version](https://camo.githubusercontent.com/1710b23b456297a8adeff777e2495a640a1598c24b962ac1a024bd669ba8bd62/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f66697265666f782d3135392e302d626c75652e7376673f6c6f676f3d66697265666f7862726f77736572)](https://www.mozilla.org/en-US/firefox/new/)[![Image 4: WebKit version](https://camo.githubusercontent.com/01060808e60a7b4e31bebd0646743aea46f74d3c61929dd9e14af610013fed7a/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f7765626b69742d32372e322d626c75652e7376673f6c6f676f3d736166617269)](https://webkit.org/)[![Image 5: Join Discord](https://camo.githubusercontent.com/f05a9aec0dbb1dea66d8d80d8f8be7c23c27d11988fbb668cabf2ec09021b42c/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f6a6f696e2d646973636f72642d696e666f726d6174696f6e616c)](https://aka.ms/playwright/discord)

## [Documentation](https://playwright.dev/) | [API reference](https://playwright.dev/docs/api/class-playwright)

[](https://github.com/microsoft/playwright#documentation--api-reference)
Playwright is a framework for web automation and testing. It drives Chromium, Firefox, and WebKit with a single API — in your tests, in your scripts, and as a tool for AI agents.

## Get Started

[](https://github.com/microsoft/playwright#get-started)
Choose the path that fits your workflow:

|  | Best for | Install |
| --- | --- | --- |
| **[Playwright Test](https://github.com/microsoft/playwright#playwright-test)** | End-to-end testing | `npm init playwright@latest` |
| **[Playwright CLI](https://github.com/microsoft/playwright#playwright-cli)** | Coding agents (Claude Code, Copilot) | `npm i -g @playwright/cli@latest` |
| **[Playwright MCP](https://github.com/microsoft/playwright#playwright-mcp)** | AI agents and LLM-driven automation | `npx @playwright/mcp@latest` |
| **[Playwright Library](https://github.com/microsoft/playwright#playwright-library)** | Browser automation scripts | `npm i playwright` |
| **[VS Code Extension](https://github.com/microsoft/playwright#vs-code-extension)** | Test authoring and debugging in VS Code | [Install from Marketplace](https://marketplace.visualstudio.com/items?itemName=ms-playwright.playwright) |

* * *

## Playwright Test

[](https://github.com/microsoft/playwright#playwright-test)
Playwright Test is a full-featured test runner built for end-to-end testing. It runs tests across Chromium, Firefox, and WebKit with full browser isolation, auto-waiting, and web-first assertions.

### Install

[](https://github.com/microsoft/playwright#install)

npm init playwright@latest

Or add manually:

npm i -D @playwright/test
npx playwright install

### Write a test

[](https://github.com/microsoft/playwright#write-a-test)

import { test, expect } from '@playwright/test';

test('has title', async ({ page }) => {
  await page.goto('https://playwright.dev/');
  await expect(page).toHaveTitle(/P l a y w r i g h t/);
});

test('get started link', async ({ page }) => {
  await page.goto('https://playwright.dev/');
  await page.getByRole('link', { name: 'Get started' }).click();
  await expect(page.getByRole('heading', { name: 'Installation' })).toBeVisible();
});

### Run tests

[](https://github.com/microsoft/playwright#run-tests)

npx playwright test

Tests run in parallel across all configured browsers, in headless mode by default. Each test gets a fresh browser context — full isolation with near-zero overhead.

### Key capabilities

[](https://github.com/microsoft/playwright#key-capabilities)
**Auto-wait and web-first assertions.** No artificial timeouts. Playwright waits for elements to be actionable, and assertions automatically retry until conditions are met.

**Locators.** Find elements with resilient locators that mirror how users see the page:

page.getByRole('button', { name: 'Submit' })
page.getByLabel('Email')
page.getByPlaceholder('Search...')
page.getByTestId('login-form')

**Test isolation.** Each test runs in its own browser context — equivalent to a fresh browser profile. Save authentication state once and reuse it across tests:

// Save state after login
await page.context().storageState({ path: 'auth.json' });

// Reuse in other tests
test.use({ storageState: 'auth.json' });

**Tracing.** Capture execution traces, screenshots, and videos on failure. Inspect every action, DOM snapshot, network request, and console message in the [Trace Viewer](https://playwright.dev/docs/trace-viewer):

// playwright.config.ts
export default defineConfig({
  use: {
    trace: 'on-first-retry',
  },
});

npx playwright show-trace trace.zip

**Parallelism.** Tests run in parallel by default across all configured browsers.

[Full testing documentation](https://playwright.dev/docs/intro)

* * *

## Playwright CLI

[](https://github.com/microsoft/playwright#playwright-cli)
[Playwright CLI](https://github.com/microsoft/playwright-cli) is a command-line interface for browser automation designed for coding agents. It's more token-efficient than MCP — commands avoid loading large tool schemas and accessibility trees into the model context.

### Install

[](https://github.com/microsoft/playwright#install-1)

npm install -g @playwright/cli@latest

Optionally install skills for richer agent integration:

playwright-cli install --skills

### Usage

[](https://github.com/microsoft/playwright#usage)
Point your coding agent at a task:

```
Test the "add todo" flow on https://demo.playwright.dev/todomvc using playwright-cli.
Take screenshots for all successful and failing scenarios.
```

Or run commands directly:

playwright-cli open https://demo.playwright.dev/todomvc/ --headed
playwright-cli type "Buy groceries"
playwright-cli press Enter
playwright-cli screenshot

### Session monitoring

[](https://github.com/microsoft/playwright#session-monitoring)
Use `playwright-cli show` to open a visual dashboard with live screencast previews of all running browser sessions. Click any session to zoom in and take remote control.

playwright-cli show

[Full CLI documentation](https://playwright.dev/agent-cli/introduction) | [GitHub](https://github.com/microsoft/playwright-cli)

* * *

## Playwright MCP

[](https://github.com/microsoft/playwright#playwright-mcp)
The [Playwright MCP server](https://github.com/microsoft/playwright-mcp) gives AI agents full browser control through the [Model Context Protocol](https://modelcontextprotocol.io/). Agents interact with pages using structured accessibility snapshots — no vision models or screenshots required.

### Setup

[](https://github.com/microsoft/playwright#setup)
Add to your MCP client (VS Code, Cursor, Claude Desktop, Windsurf, etc.):

{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest"]
    }
  }
}

**One-click install for VS Code:**

[![Image 6: Install in VS Code](https://camo.githubusercontent.com/66c393ed101de4870c2ba90e5e57fa702cf9783715856fb15530e0d186805566/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f56535f436f64652d56535f436f64653f7374796c653d666c61742d737175617265266c6162656c3d496e7374616c6c2532304d435025323053657276657226636f6c6f723d303039384646)](https://insiders.vscode.dev/redirect?url=vscode%3Amcp%2Finstall%3F%257B%2522name%2522%253A%2522playwright%2522%252C%2522command%2522%253A%2522npx%2522%252C%2522args%2522%253A%255B%2522%2540playwright%252Fmcp%2540latest%2522%255D%257D)

**For Claude Code:**

claude mcp add playwright npx @playwright/mcp@latest

### How it works

[](https://github.com/microsoft/playwright#how-it-works)
Ask your AI assistant to interact with any web page:

```
Navigate to https://demo.playwright.dev/todomvc and add a few todo items.
```

The agent sees the page as a structured accessibility tree:

```
- heading "todos" [level=1]
- textbox "What needs to be done?" [ref=e5]
- listitem:
  - checkbox "Toggle Todo" [ref=e10]
  - text: "Buy groceries"
```

It uses element refs like `e5` and `e10` to click, type, and interact — deterministically and without visual ambiguity. Tools cover navigation, form filling, screenshots, network mocking, storage management, and more.

[Full MCP documentation](https://playwright.dev/mcp/introduction) | [GitHub](https://github.com/microsoft/playwright-mcp)

* * *

## Playwright Library

[](https://github.com/microsoft/playwright#playwright-library)
Use `playwright` as a library for browser automation scripts — web scraping, PDF generation, screenshot capture, and any workflow that needs programmatic browser control without a test runner.

### Install

[](https://github.com/microsoft/playwright#install-2)

npm i playwright

### Examples

[](https://github.com/microsoft/playwright#examples)
**Take a screenshot:**

import { chromium } from 'playwright';

const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto('https://playwright.dev/');
await page.screenshot({ path: 'screenshot.png' });
await browser.close();

**Generate a PDF:**

import { chromium } from 'playwright';

const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto('https://playwright.dev/');
await page.pdf({ path: 'page.pdf', format: 'A4' });
await browser.close();

**Emulate a mobile device:**

import { chromium, devices } from 'playwright';

const browser = await chromium.launch();
const context = await browser.newContext(devices['iPhone 15']);
const page = await context.newPage();
await page.goto('https://playwright.dev/');
await page.screenshot({ path: 'mobile.png' });
await browser.close();

**Intercept network requests:**

import { chromium } from 'playwright';

const browser = await chromium.launch();
const page = await browser.newPage();
await page.route('**/*.{png,jpg,jpeg}', route => route.abort());
await page.goto('https://playwright.dev/');
await browser.close();

[Library documentation](https://playwright.dev/docs/library) | [API reference](https://playwright.dev/docs/api/class-playwright)

* * *

## VS Code Extension

[](https://github.com/microsoft/playwright#vs-code-extension)
The [Playwright VS Code extension](https://marketplace.visualstudio.com/items?itemName=ms-playwright.playwright) brings test running, debugging, and code generation directly into your editor.

**Run and debug tests** from the editor with a single click. Set breakpoints, inspect variables, and step through test execution with a live browser view.

**Generate tests with CodeGen.** Click "Record new" to open a browser — navigate and interact with your app while Playwright writes the test code for you.

**Pick locators.** Hover over any element in the browser to see the best available locator, then click to copy it to your clipboard.

**Trace Viewer integration.** Enable "Show Trace Viewer" in the sidebar to get a full execution trace after each test run — DOM snapshots, network requests, console logs, and screenshots at every step.

[Install the extension](https://marketplace.visualstudio.com/items?itemName=ms-playwright.playwright) | [VS Code guide](https://playwright.dev/docs/getting-started-vscode)

* * *

## Cross-Browser Support

[](https://github.com/microsoft/playwright#cross-browser-support)
|  | Linux | macOS | Windows |
| --- | --- | --- | --- |
| Chromium 1 159.0.8154.6 | ✅ | ✅ | ✅ |
| WebKit 27.2 | ✅ | ✅ | ✅ |
| Firefox 159.0 | ✅ | ✅ | ✅ |

Headless and headed execution on all platforms. 1 Uses [Chrome for Testing](https://developer.chrome.com/blog/chrome-for-testing) by default.

## Other Languages

[](https://github.com/microsoft/playwright#other-languages)
Playwright is also available for [Python](https://playwright.dev/python/docs/intro), [.NET](https://playwright.dev/dotnet/docs/intro), and [Java](https://playwright.dev/java/docs/intro).

## Resources

[](https://github.com/microsoft/playwright#resources)
*   [Documentation](https://playwright.dev/)
*   [API reference](https://playwright.dev/docs/api/class-playwright)
*   [MCP server](https://github.com/microsoft/playwright-mcp)
*   [CLI for coding agents](https://github.com/microsoft/playwright-cli)
*   [VS Code extension](https://github.com/microsoft/playwright-vscode)
*   [Contribution guide](https://github.com/microsoft/playwright/blob/main/CONTRIBUTING.md)
*   [Changelog](https://github.com/microsoft/playwright/releases)
*   [Discord](https://aka.ms/playwright/discord)
