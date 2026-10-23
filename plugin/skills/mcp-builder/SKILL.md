---
name: mcp-builder
description: Build high-quality MCP (Model Context Protocol) servers that give LLMs well-designed tools for external services. Use when you build an MCP server for an external API or service in Python (FastMCP) or Node/TypeScript (MCP SDK).
license: Complete terms in LICENSE.txt
---

# MCP Server Development Guide

## Overview

An MCP (Model Context Protocol) server gives LLMs well-designed tools to use external services. The quality of an MCP server is how well it helps LLMs do real tasks.

---

# Process

## 🚀 High-Level Workflow

The creation of a high-quality MCP server has four main phases.

### Phase 1: Research and Planning

#### 1.1 Understand Modern MCP Design

**API Coverage vs. Workflow Tools:**
- Balance full API endpoint coverage with specialized workflow tools.
- Workflow tools can be easier for specific tasks. Full coverage lets agents combine operations freely.
- Performance is different for each client. Some clients work better with code execution that combines basic tools. Other clients work better with higher-level workflows.
- If you are not sure, give priority to full API coverage.

**Tool Naming and Discoverability:**
Clear, descriptive tool names help agents find the correct tools quickly. Use consistent prefixes (for example, `github_create_issue`, `github_list_repos`) and names that start with the action.

**Context Management:**
- Write concise tool descriptions.
- Let agents filter and paginate results.
- Design tools that return focused, relevant data.
- Some clients support code execution. Code execution helps agents filter and process data efficiently.

**Actionable Error Messages:**
An error message must guide the agent to a solution. Give specific suggestions and next steps.

#### 1.2 Study the MCP Protocol Documentation

**Find pages in the MCP specification:**

1. Start with the sitemap to find the applicable pages: `https://modelcontextprotocol.io/sitemap.xml`
2. Fetch specific pages with the `.md` suffix to get markdown (for example, `https://modelcontextprotocol.io/specification/draft.md`).

Key pages to read:
- Specification overview and architecture
- Transport mechanisms (streamable HTTP, stdio)
- Tool, resource, and prompt definitions

#### 1.3 Study the Framework Documentation

**Recommended stack:**
- **Language**: TypeScript. The SDK support is high quality, and it is compatible with many execution environments (for example, MCPB). AI models also generate good TypeScript code because TypeScript is widely used and has static typing and good linting tools.
- **Transport**: Streamable HTTP for remote servers, with stateless JSON. Stateless JSON is easier to scale and maintain than stateful sessions and streaming responses. Use stdio for local servers.

**Load the framework documentation:**

Use the web fetch tool of your harness to load URLs (`WebFetch` in Claude Code). If the harness has no fetch tool, use `curl -sL <url>`.

- **MCP Best Practices**: [📋 View Best Practices](./reference/mcp_best_practices.md) - Core guidelines

**For TypeScript (recommended):**
- **TypeScript SDK**: Fetch `https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/README.md`
- [⚡ TypeScript Guide](./reference/node_mcp_server.md) - TypeScript patterns and examples

**For Python:**
- **Python SDK**: Fetch `https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md`
- [🐍 Python Guide](./reference/python_mcp_server.md) - Python patterns and examples

#### 1.4 Plan Your Implementation

**Understand the API:**
Read the API documentation of the service. Identify the key endpoints, the authentication requirements, and the data models. Use web search and web fetch when necessary.

**Tool Selection:**
Give priority to full API coverage. List the endpoints to implement. Start with the most frequent operations.

---

### Phase 2: Implementation

#### 2.1 Set Up the Project Structure

See the language-specific guides for project setup:
- [⚡ TypeScript Guide](./reference/node_mcp_server.md) - Project structure, package.json, tsconfig.json
- [🐍 Python Guide](./reference/python_mcp_server.md) - Module organization, dependencies

#### 2.2 Implement the Core Infrastructure

Create shared utilities:
- API client with authentication
- Error handling helpers
- Response formatting (JSON/Markdown)
- Pagination support

#### 2.3 Implement the Tools

Do these steps for each tool.

**Input Schema:**
- Use Zod (TypeScript) or Pydantic (Python).
- Include constraints and clear descriptions.
- Add examples in the field descriptions.

**Output Schema:**
- Define `outputSchema` where possible for structured data.
- Use `structuredContent` in tool responses (TypeScript SDK feature).
- The output schema helps clients understand and process tool outputs.

**Tool Description:**
- Concise summary of the function
- Parameter descriptions
- Return type schema

**Implementation:**
- Use async/await for I/O operations.
- Handle errors correctly, with actionable messages.
- Support pagination where applicable.
- With modern SDKs, return both text content and structured data.

**Annotations:**
- `readOnlyHint`: true/false
- `destructiveHint`: true/false
- `idempotentHint`: true/false
- `openWorldHint`: true/false

---

### Phase 3: Review and Test

#### 3.1 Code Quality

Review the code for these items:
- No duplicated code (DRY principle)
- Consistent error handling
- Full type coverage
- Clear tool descriptions

#### 3.2 Build and Test

**TypeScript:**
- Run `npm run build` to make sure that the code compiles.
- Test with MCP Inspector: `npx @modelcontextprotocol/inspector`

**Python:**
- Check the syntax: `python -m py_compile your_server.py`
- Test with MCP Inspector.

See the language-specific guides for detailed test procedures and quality checklists.

---

### Phase 4: Create Evaluations

After you implement your MCP server, create full evaluations to test how well it works.

**Load the [✅ Evaluation Guide](./reference/evaluation.md) for the full evaluation guidelines.**

#### 4.1 Understand the Purpose of Evaluations

Evaluations test if LLMs can use your MCP server to answer realistic, complex questions.

#### 4.2 Create 10 Evaluation Questions

Follow the process in the evaluation guide:

1. **Tool Inspection**: List the available tools and understand what they can do.
2. **Content Exploration**: Use READ-ONLY operations to explore the available data.
3. **Question Generation**: Create 10 complex, realistic questions.
4. **Answer Verification**: Solve each question yourself to verify the answers.

#### 4.3 Evaluation Requirements

Each question must be:
- **Independent**: It does not depend on other questions.
- **Read-only**: It needs only non-destructive operations.
- **Complex**: It needs many tool calls and deep exploration.
- **Realistic**: It comes from real use cases that are important to humans.
- **Verifiable**: It has one clear answer that a string comparison can verify.
- **Stable**: Its answer does not change over time.

#### 4.4 Output Format

Create an XML file with this structure:

```xml
<evaluation>
  <qa_pair>
    <question>Find discussions about AI model launches with animal codenames. One model needed a specific safety designation that uses the format ASL-X. What number X was being determined for the model named after a spotted wild cat?</question>
    <answer>3</answer>
  </qa_pair>
<!-- More qa_pairs... -->
</evaluation>
```

---

# Reference Files

## 📚 Documentation Library

Load these resources when you need them during development.

### Core MCP Documentation (Load First)
- **MCP Protocol**: Start with the sitemap at `https://modelcontextprotocol.io/sitemap.xml`. Then fetch specific pages with the `.md` suffix.
- [📋 MCP Best Practices](./reference/mcp_best_practices.md) - General MCP guidelines:
  - Server and tool naming conventions
  - Response format guidelines (JSON vs Markdown)
  - Pagination best practices
  - Transport selection (streamable HTTP vs stdio)
  - Security and error handling standards

### SDK Documentation (Load During Phase 1/2)
- **Python SDK**: Fetch from `https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md`
- **TypeScript SDK**: Fetch from `https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/README.md`

### Language-Specific Implementation Guides (Load During Phase 2)
- [🐍 Python Implementation Guide](./reference/python_mcp_server.md) - Full Python/FastMCP guide:
  - Server initialization patterns
  - Pydantic model examples
  - Tool registration with `@mcp.tool`
  - Complete working examples
  - Quality checklist

- [⚡ TypeScript Implementation Guide](./reference/node_mcp_server.md) - Full TypeScript guide:
  - Project structure
  - Zod schema patterns
  - Tool registration with `server.registerTool`
  - Complete working examples
  - Quality checklist

### Evaluation Guide (Load During Phase 4)
- [✅ Evaluation Guide](./reference/evaluation.md) - Full guide to create evaluations:
  - Question creation guidelines
  - Answer verification strategies
  - XML format specifications
  - Example questions and answers
  - How to run an evaluation with the provided scripts
