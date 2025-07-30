# MCP-Scan: An MCP Security Scanner

[<img src="https://devin.ai/assets/deepwiki-badge.png" alt="Ask DeepWiki.com" height="20"/>](https://deepwiki.com/invariantlabs-ai/mcp-scan)
<a href="https://discord.gg/dZuZfhKnJ4"><img src="https://img.shields.io/discord/1265409784409231483?style=plastic&logo=discord&color=blueviolet&logoColor=white" height=18/></a>

[Documentation](https://explorer.invariantlabs.ai/docs/mcp-scan)

MCP-Scan is a security scanning tool designed to both statically and dynamically scan and monitor your installed MCP servers and check them for common security vulnerabilities like [prompt injections](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks), [tool poisoning](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks) and [cross-origin escalations](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks).

## Features

- Scanning of Claude, Cursor, Windsurf, and other file-based MCP client configurations
- Scanning for prompt injection attacks in tools and [tool poisoning attacks](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks) using [Guardrails](https://github.com/invariantlabs-ai/invariant?tab=readme-ov-file#analyzer)
- Audit MCP calls in real-time using runtime monitoring of MCP traffic using [`mcp-scan proxy`](#proxy)
- Enforce guardrailing policies on tool calls and responses, including PII detection, secrets detection, tool restrictions and [entirely custom guardrailing policies](https://explorer.invariantlabs.ai/docs/mcp-scan/guardrails).
- Detect cross-origin escalation attacks (e.g. [tool shadowing](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks))
- Implements _tool pinning_ to detect and prevent [MCP rug pull attacks](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks), i.e. detects changes to MCP tools via hashing


## Quick Start
To run MCP-Scan statically, use the following command:

```bash
uvx mcp-scan@latest
```

or

```
npx mcp-scan@latest
```

### Example Run
[![demo](demo.svg)](https://asciinema.org/a/716858)

## How It Works

### Scanning

MCP-Scan `scan` searches through your configuration files to find MCP server configurations. It connects to these servers and retrieves tool descriptions.

It then scans tool descriptions, both with local checks and by invoking Invariant Guardrailing via an API. For this, tool names and descriptions are shared with invariantlabs.ai. By using MCP-Scan, you agree to the invariantlabs.ai [terms of use](https://explorer.invariantlabs.ai/terms) and [privacy policy](https://invariantlabs.ai/privacy-policy).

Invariant Labs is collecting data for security research purposes (only about tool descriptions and how they change over time, not your user data). Don't use MCP-scan if you don't want to share your tools.
You can run MCP-scan locally by using the `--local-only` flag. This will only run local checks and will not invoke the Invariant Guardrailing API, however it will not provide as accurate results as it just runs a local LLM-based policy check. This option requires an `OPENAI_API_KEY` environment variable to be set.

MCP-scan does not store or log any usage data, i.e. the contents and results of your MCP tool calls.

### Proxying

For runtime monitoring using `mcp-scan proxy`, MCP-Scan can be used as a proxy server. This allows you to monitor and guardrail system-wide MCP traffic in real-time. To do this, mcp-scan temporarily injects a local [Invariant Gateway](https://github.com/invariantlabs-ai/invariant-gateway) into MCP server configurations, which intercepts and analyzes traffic. After the `proxy` command exits, Gateway is removed from the configurations.

You can also configure guardrailing rules for the proxy to enforce security policies on the fly. This includes PII detection, secrets detection, tool restrictions, and custom guardrailing policies. Guardrails and proxying operate entirely locally using [Guardrails](https://github.com/invariantlabs-ai/invariant) and do not require any external API calls.

## CLI parameters

MCP-scan provides the following commands:

```
mcp-scan - Security scanner for Model Context Protocol servers and tools
```

### Common Options

These options are available for all commands:

```
--storage-file FILE    Path to store scan results and whitelist information (default: ~/.mcp-scan)
--base-url URL         Base URL for the verification server
--verbose              Enable detailed logging output
--print-errors         Show error details and tracebacks
--json                 Output results in JSON format instead of rich text
```

### Commands

#### scan (default)

Scan MCP configurations for security vulnerabilities in tools, prompts, and resources.

```
mcp-scan [CONFIG_FILE...]
```

Options:
```
--checks-per-server NUM       Number of checks to perform on each server (default: 1)
--server-timeout SECONDS      Seconds to wait before timing out server connections (default: 10)
--suppress-mcpserver-io BOOL  Suppress stdout/stderr from MCP servers (default: True)
--local-only BOOL             Only run verification locally. Does not run all checks, results will be less accurate (default: False)
```

#### proxy

Run a proxy server to monitor and guardrail system-wide MCP traffic in real-time. Temporarily injects [Gateway](https://github.com/invariantlabs-ai/invariant-gateway) into MCP server configurations, to intercept and analyze traffic. Removes Gateway again after the `proxy` command exits.

```
mcp-scan proxy [CONFIG_FILE...] [--pretty oneline|compact|full]
```

Options:
```
CONFIG_FILE...                  Path to MCP configuration files to setup for proxying.
--pretty oneline|compact|full   Pretty print the output in different formats (default: compact)
```


#### inspect

Print descriptions of tools, prompts, and resources without verification.

```
mcp-scan inspect [CONFIG_FILE...]
```

Options:
```
--server-timeout SECONDS      Seconds to wait before timing out server connections (default: 10)
--suppress-mcpserver-io BOOL  Suppress stdout/stderr from MCP servers (default: True)
```

#### whitelist

Manage the whitelist of approved entities. When no arguments are provided, this command displays the current whitelist.

```
# View the whitelist
mcp-scan whitelist

# Add to whitelist
mcp-scan whitelist TYPE NAME HASH

# Reset the whitelist
mcp-scan whitelist --reset
```

Options:
```
--reset                       Reset the entire whitelist
--local-only                  Only update local whitelist, don't contribute to global whitelist
```

Arguments:
```
TYPE                          Type of entity to whitelist: "tool", "prompt", or "resource"
NAME                          Name of the entity to whitelist
HASH                          Hash of the entity to whitelist
```

#### help

Display detailed help information and examples.

```
mcp-scan help
```

### Examples

```bash
# Scan all known MCP configs
mcp-scan

# Scan a specific config file
mcp-scan ~/custom/config.json

# Just inspect tools without verification
mcp-scan inspect

# View whitelisted tools
mcp-scan whitelist

# Whitelist a tool
mcp-scan whitelist tool "add" "a1b2c3..."
```

## Contributing

We welcome contributions to MCP-Scan. If you have suggestions, bug reports, or feature requests, please open an issue on our GitHub repository.

## Development Setup
To run this package from source, follow these steps:

```
uv run pip install -e .
uv run -m src.mcp_scan.cli
```

## Including MCP-scan results in your own project / registry

If you want to include MCP-scan results in your own project or registry, please reach out to the team via `mcpscan@invariantlabs.ai`, and we can help you with that.
For automated scanning we recommend using the `--json` flag and parsing the output.

## Further Reading
- [Introducing MCP-Scan](https://invariantlabs.ai/blog/introducing-mcp-scan)
- [MCP Security Notification Tool Poisoning Attacks](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks)
- [WhatsApp MCP Exploited](https://invariantlabs.ai/blog/whatsapp-mcp-exploited)
- [MCP Prompt Injection](https://simonwillison.net/2025/Apr/9/mcp-prompt-injection/)

## Changelog
See [CHANGELOG.md](CHANGELOG.md).
