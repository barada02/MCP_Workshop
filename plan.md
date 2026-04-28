# MCP (Model Context Protocol) Learning Plan & Project

## Objective
To understand the Model Context Protocol (MCP) in-depth by building a complete, functional MCP server from scratch. We will learn the core concepts (Tools, Resources, Prompts) and how AI models use them to interact with local systems or external APIs.

## Project Idea
We will build a **"System & Notes Assistant" MCP Server**. It will allow an AI to:
1. **Read/Write Notes (Resources/Tools):** Manage a local knowledge base.
2. **Execute Basic System Checks (Tools):** Get system stats (e.g., current time, OS info).
3. **Provide Formatting Templates (Prompts):** Provide predefined prompts for summarizing notes or generating reports.

*(We can use either Python or TypeScript. We will decide in Phase 1).*

## Step-by-Step Plan

### Phase 1: Setup and Basics
- [ ] Choose the language stack (Python or TypeScript).
- [ ] Initialize the project and install the official MCP SDK dependencies.
- [ ] Set up the basic MCP Server lifecycle (initialization, starting the stdio transport).

### Phase 2: Implementing Tools (Actions)
Tools allow the AI to perform actions (e.g., fetching live data, making calculations, or saving files).
- [ ] Define the tool schemas.
- [ ] Implement a tool to write/create a note.
- [ ] Implement a tool to get system information.

### Phase 3: Implementing Resources (Context)
Resources provide context and data to the model, like a file system or database.
- [ ] Expose the saved notes as readable MCP resources.
- [ ] Implement the `resources/list` and `resources/read` handlers.

### Phase 4: Implementing Prompts
Prompts are predefined templates that users can invoke to get specific AI behaviors.
- [ ] Create a prompt template for summarizing a specific note.
- [ ] Implement the `prompts/list` and `prompts/get` handlers.

### Phase 5: Testing and Inspector
- [ ] Use the official `@modelcontextprotocol/inspector` to test our server interactively.
- [ ] Debug any issues with the JSON-RPC communication.

### Phase 6: Integration (Bonus)
- [ ] Connect our new MCP server to a real client (like Claude Desktop or an MCP-compatible VS Code extension) to see it work in a real-world scenario.
