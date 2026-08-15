# Agent Workflows with LangGraph

An intermediate project that levels the assistant up from one chat call into a real agent workflow. You model the agent as a LangGraph state machine, give it tools it can choose to call, make tools fail safely, ground its answers in retrieved documents (RAG), add a human-in-the-loop approval gate, persist conversation state in Redis, expose it over FastAPI, and test the graph deterministically with a fake model. This is the workflow engine the platform exposes to startups.

Built step-by-step with [KhwajaLabs Build](https://khwajalabs.com).

## Stack
- Python
- LangGraph
- OpenAI
- Redis
- RAG
