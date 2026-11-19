# Official Delta Reference: ast_grep_cli
Source: https://github.com/ast-grep/ast-grep
Domain: agent_harness

Title: GitHub - ast-grep/ast-grep: ⚡A CLI tool for code structural search, lint and rewriting. Written in Rust

URL Source: https://github.com/ast-grep/ast-grep

Markdown Content:
[![Image 1: ast-grep](https://camo.githubusercontent.com/af23fce35de4fc9626d6ba777d5014a2f456228ca51dfc2fa2d3ee4810ccc6d5/68747470733a2f2f6173742d677265702e6769746875622e696f2f6c6f676f2e737667)](https://camo.githubusercontent.com/af23fce35de4fc9626d6ba777d5014a2f456228ca51dfc2fa2d3ee4810ccc6d5/68747470733a2f2f6173742d677265702e6769746875622e696f2f6c6f676f2e737667)

[![Image 2: coverage badge](https://github.com/ast-grep/ast-grep/actions/workflows/coverage.yaml/badge.svg)](https://github.com/ast-grep/ast-grep/actions/workflows/coverage.yaml/badge.svg)[![Image 3](https://camo.githubusercontent.com/3e01f3ba4a3495c9cf7451a4ecc5b4f668301c7d9b8288a09160599efed99155/68747470733a2f2f636f6465636f762e696f2f67682f6173742d677265702f6173742d677265702f6272616e63682f6d61696e2f67726170682f62616467652e7376673f746f6b656e3d33375658384832455756)](https://app.codecov.io/gh/ast-grep/ast-grep)[![Image 4: Discord](https://camo.githubusercontent.com/0e7a48ff70fb6166ce23984c5f03780ab95bd2f81c7607304281e519bcd90257/68747470733a2f2f696d672e736869656c64732e696f2f646973636f72642f313130373734393834373732323838393231373f6c6162656c3d446973636f7264)](https://discord.gg/4YZjf6htSQ)[![Image 5: Repology](https://camo.githubusercontent.com/f3ce1c295dfa772a8995c7b77c4df15d8d0968aaaf1efa97887aa6acebd2d4f8/68747470733a2f2f7265706f6c6f67792e6f72672f62616467652f74696e792d7265706f732f6173742d677265702e737667)](https://repology.org/project/ast-grep/versions)[![Image 6: Badge](https://camo.githubusercontent.com/0bcdd0cc2be2f42e55ff51d93e15d592f04df7de3b64109ac49991742481ade3/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f73746172732f6173742d677265702f6173742d677265703f7374796c653d736f6369616c)](https://github.com/ast-grep/ast-grep/stargazers)[![Image 7: Badge](https://camo.githubusercontent.com/f90a791dd4e01241bbf0227bfdd2fb38aea598258f32b748fc694277e6f29a5f/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f666f726b732f6173742d677265702f6173742d677265703f7374796c653d736f6369616c)](https://github.com/ast-grep/ast-grep/network/members)[![Image 8: GitHub Sponsors](https://camo.githubusercontent.com/6a6bcee589066f075313836500c33734030bb63929c58a478984316197bc8ffe/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f73706f6e736f72732f48657272696e67746f6e4461726b686f6c6d653f7374796c653d736f6369616c)](https://github.com/sponsors/HerringtonDarkholme)[![Image 9: Gurubase](https://camo.githubusercontent.com/39302c885bfe01247762554ba3ddd9ba7d8b34873e5cd492b961865e390dab72/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f47757275626173652d41736b2532306173742d2d67726570253230477572752d303036424646)](https://gurubase.io/g/ast-grep)

ast-grep(sg) is a CLI tool for code structural search, lint, and rewriting.

## Introduction

[](https://github.com/ast-grep/ast-grep#introduction)
ast-grep is an [abstract syntax tree](https://dev.to/balapriya/abstract-syntax-tree-ast-explained-in-plain-english-1h38) based tool to search code by pattern code. Think of it as your old-friend [`grep`](https://en.wikipedia.org/wiki/Grep#:~:text=grep%20is%20a%20command%2Dline,which%20has%20the%20same%20effect.), but matching AST nodes instead of text. You can write patterns as if you are writing ordinary code. It will match all code that has the same syntactical structure. You can use `$` sign + upper case letters as a [wildcard](https://en.wikipedia.org/wiki/Wildcard_character), e.g. `$MATCH`, to match any single AST node. Think of it as [regular expression dot](https://regexone.com/lesson/wildcards_dot)`.`, except it is not textual.

Try the [online playground](https://ast-grep.github.io/playground.html) for a taste!

## Screenshot

[](https://github.com/ast-grep/ast-grep#screenshot)
[![Image 10: demo](https://camo.githubusercontent.com/be0a171d8473777cf4111dc2115e7a061a1e270b5a0606bbd0f6ca2a182b1285/68747470733a2f2f6173742d677265702e6769746875622e696f2f696d6167652f7365617263682d7265706c6163652e706e67)](https://camo.githubusercontent.com/be0a171d8473777cf4111dc2115e7a061a1e270b5a0606bbd0f6ca2a182b1285/68747470733a2f2f6173742d677265702e6769746875622e696f2f696d6167652f7365617263682d7265706c6163652e706e67)

See more screenshots on the [website](https://ast-grep.github.io/).

## Installation

[](https://github.com/ast-grep/ast-grep#installation)
You can install it from [npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm), [pip](https://pypi.org/), [cargo](https://doc.rust-lang.org/cargo/getting-started/installation.html), [cargo-binstall](https://github.com/cargo-bins/cargo-binstall), [homebrew](https://brew.sh/), [scoop](https://scoop.sh/), [mise](https://github.com/jdx/mise) or [MacPorts](https://www.macports.org/)!

Installing from npm requires Node.js 20 or later.

npm install --global @ast-grep/cli
# `pnpm approve-builds` may be needed
pip install ast-grep-cli
brew install ast-grep

Click for more installation methods

cargo install ast-grep --locked
cargo binstall ast-grep

# install via scoop, thank @brian6932
scoop install main/ast-grep

# install via MacPorts
sudo port install ast-grep

# try ast-grep in nix-shell
nix-shell -p ast-grep

# try ast-grep with mise
mise use -g ast-grep

Or you can build ast-grep from source. You need to install rustup, clone the repository and then

cargo install --path ./crates/cli --locked

[Packages](https://repology.org/project/ast-grep/versions) are available on other platforms too.

## Command line usage example

[](https://github.com/ast-grep/ast-grep#command-line-usage-example)
ast-grep has following form.

```
ast-grep --pattern 'var code = $PATTERN' --rewrite 'let code = new $PATTERN' --lang ts
```

### Example

[](https://github.com/ast-grep/ast-grep#example)
*   [Rewrite code in null coalescing operator](https://twitter.com/Hchan_mgn/status/1547061516993699841?s=20&t=ldDoj4U2nq-FRKQkU5GWXA)

ast-grep -p '$A && $A()' -l ts -r '$A?.()'

*   [Rewrite](https://twitter.com/Hchan_mgn/status/1561802312846278657)[Zodios](https://github.com/ecyrbe/zodios#migrate-to-v8)

ast-grep -p 'new Zodios($URL, $CONF as const,)' -l ts -r 'new Zodios($URL, $CONF)' -i

*   [Implement eslint rule using YAML.](https://twitter.com/Hchan_mgn/status/1560108625460355073)

## Sponsor

[](https://github.com/ast-grep/ast-grep#sponsor)
[![Image 11: Sponsors](https://raw.githubusercontent.com/HerringtonDarkholme/sponsors/main/sponsorkit/sponsors.svg)](https://raw.githubusercontent.com/HerringtonDarkholme/sponsors/main/sponsorkit/sponsors.svg)

If you find ast-grep interesting and useful for your work, please [buy me a coffee](https://github.com/sponsors/HerringtonDarkholme) so I can spend more time on the project!

## Feature Highlight

[](https://github.com/ast-grep/ast-grep#feature-highlight)
ast-grep's core is an algorithm to search and replace code based on abstract syntax tree produced by tree-sitter. It can help you to do lightweight static analysis and massive scale code manipulation in an intuitive way.

Key highlights:

*   An intuitive pattern to find and replace AST. ast-grep's pattern looks like ordinary code you would write every day (you could say the pattern is isomorphic to code).

*   jQuery like API for AST traversal and manipulation.

*   YAML configuration to write new linting rules or code modification.

*   Written in compiled language, with tree-sitter based parsing and utilizing multiple cores.

*   Beautiful command line interface :)

ast-grep's vision is to democratize abstract syntax tree magic and to liberate one from cumbersome AST programming!

*   If you are an open-source library author, ast-grep can help your library users adopt breaking changes more easily.
*   if you are a tech lead in your team, ast-grep can help you enforce code best practice tailored to your business need.
*   If you are a security researcher, ast-grep can help you write rules much faster.
