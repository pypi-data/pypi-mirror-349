# Secrets in the Wind: Environment Variables, URLs, and the Leaky Abstractions

## Context

In the evolving landscape of MCP servers and AI agents, a new category of risk is emerging: **sensitive data exposure through dynamic access mechanisms**. We're talking about secrets not statically written to disk, but **fetched on demand** — via environment variables, command-line outputs, or even remote HTTP URLs.

At first glance, this looks like progress. You're no longer writing secrets to plain text config files. Instead, your server gets its credentials at runtime, maybe through an environment variable like `AWS_SECRET_ACCESS_KEY`, a shell command like `gcloud auth print-access-token`, or a “magic” URL like `http://169.254.169.254/latest/meta-data/iam/security-credentials/`.

But here's the catch: **many MCP agents blindly expose this information** in their tool outputs, logs, or debug traces. Worse, they might even return these secrets to user queries that are only loosely scoped. You ask an agent to “check configuration,” and suddenly it's dumped your full environment, including credentials, to the front-end.

This isn’t hypothetical. Consider the following common tools MCP agents provide:

### `env_var`: The Fastest Way to Spill Your Secrets

```python
@mcp.tool()
def env_var() -> str:
    """Use this tool to display environment variables."""
    out = ""
    for key, value in os.environ.items():
        out += f"{key}={value}\n"
    return out
```

This innocent-looking tool is a **data breach in disguise**. Run it in an agent that has access to real credentials — and it will happily print them all. `AWS_ACCESS_KEY_ID`, `GITHUB_TOKEN`, maybe even `OPENAI_API_KEY`.

You think “this is safe because only developers use it,” but agents can be unpredictable. A prompt like “diagnose system state” might trigger `env_var` under the hood. Now imagine this being returned to the user — or worse, logged.

### `fetch`: Remote Secrets Just a URL Away

```python
@mcp.tool()
def fetch(url: str) -> str:
    """Use this tool to get remote URL data."""
    with httpx.Client(timeout=10.0) as client:
        response = client.get(url)
        response.raise_for_status()
        return response.text
```

This one’s deceptively powerful. The intention is to fetch documentation or user-provided URLs. But agents often build or infer URLs programmatically. On a cloud VM? You might hit the instance metadata service:

```
fetch("http://169.254.169.254/latest/meta-data/iam/security-credentials/")
```

And just like that, you’re holding temporary AWS credentials in plain text.

This isn’t just about EC2. GCP and Azure have similar endpoints. Any code that allows an agent to make HTTP requests becomes a **secret exfiltration vector** unless it understands what not to fetch.

### `run_command`: A Trojan Horse

```python
@mcp.tool()
def run_command(command: str, args: List[str]) -> str:
    """Run a command with given arguments and return its stdout as text."""
    completed = subprocess.run(
        [command] + args, capture_output=True, text=True, check=True
    )
    return completed.stdout
```

What happens when an agent is told to “check AWS config”? It might call:

```
run_command("aws", ["configure", "list"])
```

Or even worse:

```
run_command("gcloud", ["auth", "print-access-token"])
```

These tools are fantastic for automation — but disastrous if their outputs are dumped into logs, returned to a user, or passed between agents without redaction.

## Why This Happens

AI agents are **greedy**. They try to fulfill the intent of a user prompt, and often go too far. Developers, meanwhile, are trying to give them powerful tools — but forget that these tools can access sensitive system-level data.

The fundamental problem is this: **agents operate with authority, but not discretion**. You give them keys to the kingdom and ask them to “get information,” and they do — sometimes more than you bargained for.

## 🛡️ Remediation

To safeguard against **sensitive data leakage**, whether through environment variables, metadata endpoints, command output, or misconfigured tools, **Acuvity provides a robust Rego policy suite** designed to enforce deep inspection and **real-time redaction** of secrets at runtime.

These policies are specifically engineered to protect against **credential spills, token exposures, and unintentional leaks** during agent execution, even when the agent is operating over dynamic, inferred, or user-directed toolchains.

### ✅ Acuvity’s Built-In Redaction with ARC

Acuvity’s **ARC (Agent Runtime Controller)** includes a comprehensive Rego policy layer activated via the `GUARDRAILS` environment variable. These policies apply across **tool execution, environment introspection, and remote fetches**, and include powerful redaction capabilities:

- **Secret Pattern Redaction**
  Detects and redacts common secret formats **before** responses reach users or logs, including:

  - API keys (GitHub, Slack, OpenAI, etc.)
  - Cloud credentials (AWS access keys, GCP tokens)
  - OAuth tokens, Bearer tokens, JWTs

- **Environment Leakage Protection**
  Scrubs environment dumps of sensitive keys like:

  - `AWS_ACCESS_KEY_ID`, `OPENAI_API_KEY`, `DATABASE_URL`, etc.
  - Custom patterns defined by workspace policies

- **Metadata Endpoint Detection**
  Blocks or sanitizes content retrieved from metadata URLs such as:

  - `http://169.254.169.254` (AWS/GCP/Azure instance credentials)
  - `/latest/meta-data/iam/` and similar high-risk endpoints

- **Output Surface Scrubbing**
  Applies redaction rules recursively to:

  - Tool outputs
  - Command results
  - HTTP fetch results
  - Agent response serialization

- **Sensitive File Reference Detection**
  Prevents exposure of file paths and contents from:

  - `.env`, `.ssh/`, `config.json`, `id_rsa`, etc.
  - Files containing credential-like strings

Enable these protections with:

```bash
REGO_POLICY_RUNTIME_GUARDRAILS="secrets-redaction sensitive-pattern-detection"
```

![image](./redaction.png)

### 🔐 Minibridge + ARC: Unified Redaction Enforcement

**Minibridge**, Acuvity’s intelligent agent router, **natively integrates with ARC** to apply redaction policies at every stage of agent interaction:

- **Pre-call Filtering**
  Intercepts sensitive or high-risk parameters **before tools are executed**

- **Post-call Scrubbing**
  Sanitizes outputs containing secret tokens, environment leaks, or metadata fetches

- **Runtime Surface Control**
  Applies policy constraints across:

  - Tool descriptions
  - Agent output serialization
  - Error traces and debug logs

> **ARC sanitizes the flow. Minibridge routes it safely. Together, they ensure no secret slips through.**

With ARC and Minibridge, every environment variable, fetched resource, and command output is treated as **potentially sensitive** and rigorously redacted according to Acuvity’s best-in-class runtime security model.

By enforcing these protections, Acuvity ensures that your MCP agents — no matter how dynamic or powerful — operate within strict boundaries that **respect the confidentiality of your systems and secrets**.
