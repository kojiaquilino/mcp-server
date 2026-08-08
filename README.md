# mcp-server

A Model Context Protocol (MCP) server built from scratch in Python — without relying on the official `mcp` SDK.

## What is this?

This project implements the MCP protocol from the ground up. Instead of using Anthropic's `mcp` library, it builds:

- JSON-RPC 2.0 message parsing and serialization
- STDIO transport for stdin/stdout communication
- MCP protocol handshake and lifecycle
- Dynamic tool registry and dispatcher
- Security-controlled portfolio tools

## Project Structure

```
mcp-server/
├── protocol.py       # JSON-RPC 2.0 data models
├── docs/             # Project documentation
│   └── DEVELOPMENT.md  # (make later)
```

## Status

**Work in progress.** Currently has the protocol data layer.

- JSON-RPC 2.0 data models (Request, Response, Notification, Error)
- Raw JSON parser (`parse_message`)
- STDIO transport layer
- Protocol handshake & lifecycle
- Tool registry & dispatcher
- Portfolio tools (SQLite inspector, log tailer)
- End-to-end testing with MCP inspector

## Running Locally

```powershell
to be added
```

## Learning Outcomes

This project is a deep dive into:
- Protocol implementation from scratch
- JSON-RPC 2.0 specifications
- Async I/O and stream isolation
- MCP protocol lifecycle
- Input validation and security controls
- End-to-end protocol testing
