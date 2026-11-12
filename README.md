# Agent Workflows with LangGraph

A Python-based AI agent workflow project demonstrating how to build stateful, tool-enabled AI applications using LangGraph, OpenAI, Redis, and FastAPI. The project focuses on developing reliable AI agents capable of executing multi-step workflows, retrieving relevant information, handling tool failures, and incorporating human oversight.

## Overview

Unlike traditional AI assistants that rely on a single model call, this project explores building an AI agent capable of managing complex workflows through a state-based architecture.

Using **LangGraph**, the agent operates as a state machine, allowing it to make decisions, execute tools, retrieve supporting documents, and maintain conversation context across interactions.

The system integrates Retrieval-Augmented Generation (RAG), human-in-the-loop approval, and Redis-backed persistence to support more reliable AI-powered applications.

## Key Features

- **Stateful Agent Workflows:** Model agent behavior using LangGraph nodes, edges, and conditional transitions.
- **Dynamic Tool Calling:** Allow the AI agent to select and execute tools based on user requests.
- **Safe Tool Execution:** Handle tool failures and exceptions without crashing the entire workflow.
- **Retrieval-Augmented Generation (RAG):** Retrieve relevant documents to ground model responses in supporting information.
- **Human-in-the-Loop Approval:** Introduce approval checkpoints before executing sensitive or consequential actions.
- **Conversation Persistence:** Use Redis to maintain conversation state across requests.
- **REST API Integration:** Expose agent workflows through FastAPI endpoints.
- **Deterministic Testing:** Test workflow transitions, tool execution, and error handling using a fake language model.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core application development |
| LangGraph | Agent orchestration and state management |
| OpenAI API | Language model reasoning and tool selection |
| Redis | Conversation state persistence |
| RAG | Document retrieval and response grounding |
| FastAPI | REST API for interacting with the agent |

## System Architecture

The application consists of several interconnected components:

1. **FastAPI Service:** Receives user requests and communicates with the agent workflow.
2. **LangGraph Agent:** Manages workflow state, decision-making, and execution paths.
3. **Tool Execution Layer:** Executes approved tools and handles errors safely.
4. **Retrieval Layer:** Retrieves relevant documents to provide context for generated responses.
5. **Human Approval Gate:** Pauses workflows when an action requires user authorization.
6. **Redis Persistence:** Stores conversation state to support continuity across interactions.

### Agent Workflow

```text
             User Request
                  |
                  v
              FastAPI
                  |
                  v
           LangGraph Agent
                  |
                  v
           Evaluate Request
                  |
          +-------+-------+
          |               |
          v               v
    Retrieve Docs     Select Tool
       (RAG)              |
          |               v
          |        Approval Required?
          |          /          \
          |        Yes           No
          |         |             |
          |    Human Approval     |
          |         |             |
          |         +------+------+
          |                |
          |                v
          |          Execute Tool
          |                |
          |                v
          |         Handle Result
          |                |
          +--------+-------+
                   |
                   v
           Generate Response
                   |
                   v
          Persist State (Redis)
                   |
                   v
             API Response
```

*Conceptual workflow illustrating the primary components. Actual execution paths depend on the agent's decisions and graph configuration.*

## Learning Objectives

This project focuses on developing practical skills in:

- Designing stateful AI agents with LangGraph.
- Implementing conditional workflow execution and tool calling.
- Integrating OpenAI models into multi-step applications.
- Building Retrieval-Augmented Generation pipelines.
- Managing persistent conversation state with Redis.
- Implementing human approval checkpoints for safer execution.
- Building and exposing AI services through REST APIs.
- Writing deterministic tests for AI workflows.
- Improving reliability through structured error handling.

## Potential Applications

The architecture can be extended to support:

- AI-powered customer support assistants
- Internal knowledge retrieval systems
- Automated business workflows
- Research and document analysis agents
- Enterprise assistants with approval requirements
- Developer productivity tools

## Future Improvements

Potential enhancements include:

- Adding authentication and role-based access control.
- Implementing workflow tracing and observability.
- Tracking token usage, latency, and API costs.
- Supporting multiple specialized agents.
- Introducing evaluation pipelines for response quality and retrieval accuracy.
- Containerizing services with Docker for deployment.



