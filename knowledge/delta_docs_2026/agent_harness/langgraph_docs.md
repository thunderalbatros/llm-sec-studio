# Official Delta Reference: langgraph_docs
Source: https://github.com/langchain-ai/langgraph
Domain: agent_harness

Title: GitHub - langchain-ai/langgraph: Build resilient agents.

URL Source: https://github.com/langchain-ai/langgraph

Markdown Content:
[![Image 1: LangGraph Logo](https://github.com/langchain-ai/langgraph/raw/main/.github/images/logo-dark.svg)](https://www.langchain.com/langgraph)

### Low-level orchestration framework for building stateful agents.

[](https://github.com/langchain-ai/langgraph#low-level-orchestration-framework-for-building-stateful-agents)

[![Image 2: PyPI - License](https://camo.githubusercontent.com/390f6bace8ad36a6a0f4493fd8bc38a9b7d7f6fda2067b2307d2373cab4020eb/68747470733a2f2f696d672e736869656c64732e696f2f707970692f6c2f6c616e676772617068)](https://opensource.org/licenses/MIT)[![Image 3: PyPI - Downloads](https://camo.githubusercontent.com/f3a99cf4268c770b835b8b4447da3385ecd5ae8af2701173c8d0266b08090c89/68747470733a2f2f696d672e736869656c64732e696f2f706570792f64742f6c616e676772617068)](https://pypistats.org/packages/langgraph)[![Image 4: Version](https://camo.githubusercontent.com/a4816472f36b508a31850866522aa65a39664783f8b5d305162257334ee83a9d/68747470733a2f2f696d672e736869656c64732e696f2f707970692f762f6c616e6767726170682e7376673f6c6162656c3d253230)](https://pypi.org/project/langgraph/)[![Image 5: Twitter / X](https://camo.githubusercontent.com/e391462876aaba05f7974010f04c930692c681908d591a5aff008d0fc2b941d4/68747470733a2f2f696d672e736869656c64732e696f2f747769747465722f75726c2f68747470732f747769747465722e636f6d2f6c616e67636861696e5f6f73732e7376673f7374796c653d736f6369616c266c6162656c3d466f6c6c6f772532302534304c616e67436861696e)](https://x.com/langchain_oss)

Trusted by companies shaping the future of agents – including Klarna, Replit, Elastic, and more – LangGraph is a low-level orchestration framework for building, managing, and deploying long-running, stateful agents.

pip install -U langgraph

Tip

If you're looking to quickly build agents, check out **[Deep Agents](https://docs.langchain.com/oss/python/deepagents/overview)** — a higher-level package built on LangGraph for agents that can plan, use subagents, and leverage file systems for complex tasks.

For an equivalent JS/TS library, check out [LangGraph.js](https://github.com/langchain-ai/langgraphjs) and the [JS docs](https://docs.langchain.com/oss/javascript/langgraph/overview).

## Why use LangGraph?

[](https://github.com/langchain-ai/langgraph#why-use-langgraph)
LangGraph provides low-level supporting infrastructure for _any_ long-running, stateful workflow or agent:

*   **[Durable execution](https://docs.langchain.com/oss/python/langgraph/durable-execution)** — Build agents that persist through failures and can run for extended periods, automatically resuming from exactly where they left off.
*   **[Human-in-the-loop](https://docs.langchain.com/oss/python/langgraph/interrupts)** — Seamlessly incorporate human oversight by inspecting and modifying agent state at any point during execution.
*   **[Comprehensive memory](https://docs.langchain.com/oss/python/langgraph/memory)** — Create truly stateful agents with both short-term working memory for ongoing reasoning and long-term persistent memory across sessions.
*   **[Debugging with LangSmith](https://www.langchain.com/langsmith)** — Gain deep visibility into complex agent behavior with visualization tools that trace execution paths, capture state transitions, and provide detailed runtime metrics.
*   **[Production-ready deployment](https://docs.langchain.com/langsmith/deployments)** — Deploy sophisticated agent systems confidently with scalable infrastructure designed to handle the unique challenges of stateful, long-running workflows.

Tip

For developing, debugging, and deploying AI agents and LLM applications, see [LangSmith](https://docs.langchain.com/langsmith/home).

## LangGraph ecosystem

[](https://github.com/langchain-ai/langgraph#langgraph-ecosystem)
While LangGraph can be used standalone, it also integrates seamlessly with any LangChain product, giving developers a full suite of tools for building agents.

To improve your LLM application development, pair LangGraph with:

*   [Deep Agents](https://docs.langchain.com/oss/python/deepagents/overview) – Build agents that can plan, use subagents, and leverage file systems for complex tasks.
*   [LangChain](https://docs.langchain.com/oss/python/langchain/overview) – Provides integrations and composable components to streamline LLM application development.
*   [LangSmith](https://www.langchain.com/langsmith) – Helpful for agent evals and observability. Debug poor-performing LLM app runs, evaluate agent trajectories, gain visibility in production, and improve performance over time.
*   [LangSmith Deployment](https://docs.langchain.com/langsmith/deployments) – Deploy and scale agents effortlessly with a purpose-built deployment platform for long-running, stateful workflows. Discover, reuse, configure, and share agents across teams – and iterate quickly with visual prototyping in [LangSmith Studio](https://docs.langchain.com/langsmith/studio).

* * *

## Documentation

[](https://github.com/langchain-ai/langgraph#documentation)
*   [docs.langchain.com](https://docs.langchain.com/oss/python/langgraph/overview) – Comprehensive documentation, including conceptual overviews and guides
*   [reference.langchain.com/python/langgraph](https://reference.langchain.com/python/langgraph) – API reference docs for LangGraph packages
*   [LangGraph Quickstart](https://docs.langchain.com/oss/python/langgraph/quickstart) – Get started building with LangGraph
*   [Chat LangChain](https://chat.langchain.com/) – Chat with the LangChain documentation and get answers to your questions

**Discussions**: Visit the [LangChain Forum](https://forum.langchain.com/) to connect with the community and share all of your technical questions, ideas, and feedback.

## Additional resources

[](https://github.com/langchain-ai/langgraph#additional-resources)
*   **[Guides](https://docs.langchain.com/oss/python/learn)** – Quick, actionable code snippets for topics such as streaming, adding memory & persistence, and design patterns (e.g. branching, subgraphs, etc.).
*   **[LangChain Academy](https://academy.langchain.com/courses/intro-to-langgraph)** – Learn the basics of LangGraph in our free, structured course.
*   **[Case studies](https://www.langchain.com/built-with-langgraph)** – Hear how industry leaders use LangGraph to ship AI applications at scale.
*   [Contributing Guide](https://docs.langchain.com/oss/python/contributing/overview) – Learn how to contribute to LangChain projects and find good first issues.
*   [Code of Conduct](https://github.com/langchain-ai/langchain/?tab=coc-ov-file) – Our community guidelines and standards for participation.

* * *

## Acknowledgements

[](https://github.com/langchain-ai/langgraph#acknowledgements)
LangGraph is inspired by [Pregel](https://research.google/pubs/pub37252/) and [Apache Beam](https://beam.apache.org/). The public interface draws inspiration from [NetworkX](https://networkx.org/documentation/latest/). LangGraph is built by LangChain Inc, the creators of LangChain, but can be used without LangChain.
