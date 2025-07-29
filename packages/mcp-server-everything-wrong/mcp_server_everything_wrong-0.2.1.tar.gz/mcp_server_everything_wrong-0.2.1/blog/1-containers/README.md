# MCP Server: The Danger of "Plug-and-Play" Code

Running Model Context Protocol (MCP) servers using local executables like Node’s `npx`, Astral’s `uvx`, or downloaded binaries might be convenient, but it carries serious security risks. When you run an MCP server locally, you grant untrusted code your user’s full permissions. This means the code can:

- Access any file your user can read or modify
- Scrape sensitive environment variables
- Open network connections and more

Security researcher Bob Dickinson warned, "the code that is then run on your machine has root access — it can see your entire machine, environment variables, the file system. It can open ports to listen or to exfiltrate data" [^3].

Each time you use `npx` (or `uvx`), you’re downloading the latest code published by the author without any built-in auditing or sandboxing. This is similar to the notorious "curl | bash" anti-pattern—with no pinning, signing, or checksum verification for code integrity [^2].

## Supply Chain Risks

Because MCP servers are community-contributed, there’s little assurance of safe practices. A malicious actor could:

- Publish a package that mimics a popular tool’s name (typosquatting)
- Inject harmful code in a once-trusted project (a "rug pull")

With auto-update defaults, you might pull a compromised version immediately. The risk increases further if the MCP tool is distributed as a compiled binary with no easy way to inspect its behavior [^2].

## The Safer Path: Docker Container Isolation

Using Docker or Podman to containerize MCP servers significantly mitigates these risks. Here’s why:

- **Isolated Execution:**
  Containers confine the tool to a restricted filesystem and process space. The MCP code only accesses files and directories you explicitly allow, keeping your system safe even in the presence of malicious code [^3].

- **Non-Root by Default:**
  Container best practices run processes as non-root users, or if as root, within a namespaced environment. This reduces potential damage from exploits, aligning with Kubernetes’ Pod Security Policies [^2].

- **Immutable Runtime:**
  Docker images offer a fixed filesystem snapshot that doesn’t change at runtime. Unlike `npx`, which fetches the latest code every time, a container runs a specific tagged or digest image. This ensures that updates occur only when you decide to update and review the changes [^4].

- **Version Pinning & Vulnerability Scanning:**
  You can pin container versions and use security tools to scan images for known vulnerabilities before deployment. Official images on Docker Hub are often digitally signed, adding an extra layer of trust [^5].

- **SBOM and Provenance:**
  Container builds can generate a Software Bill of Materials (SBOM) and cryptographic provenance attestations. This transparency helps verify that the tool hasn’t been tampered with [^6].

## A Cautionary Example: "Everything Wrong" Local Execution Demo

Imagine a not so fictive MCP tool server called **`mcp-server-everything-wrong`**. This insecure MCP server:

- Reads private files
- Dumps environment secrets
- Makes unauthorized network requests

For example, a debug tool like `env_var` might be harmless in a secure setting, but in the wrong hands, it could send sensitive API keys or credentials to an attacker. Running this server with `npx` or as a local binary gives it full control of your user permissions—handing over your secrets without your consent.

<div style="display: flex; justify-content: space-around; align-items: flex-start; gap: 20px;">
  <figure style="text-align: center;">
    <img src="from-desktop.png" alt="Unrestricted access" style="width: 400px; object-fit: contain;"/>
    <figcaption style="margin-top: 8px;">Server with full user access</figcaption>
  </figure>
  <figure style="text-align: center;">
    <img src="from-container.png" alt="Isolated environment" style="width: 400px; object-fit: contain;"/>
    <figcaption style="margin-top: 8px;">Server in an isolated container</figcaption>
  </figure>
</div>

An exploit like this can occur without your knowledge, as the tool may trigger harmful actions automatically [^3] [^8] [^9].

---

## A Better Approach: Containerize and Govern with ARC & MiniBridge

Security experts recommend containerizing MCP servers. This is why at Acuvity, we built ARC (Acuvity Runtime Container) to offer a hardened runtime:[^1] [^4]

- Isolated Execution: Run securely in isolated containers, preventing lateral movement.
- Non-root by Default: Minimize risks by enforcing least-privilege.
- Immutable Runtime: Read-only file system ensures tamper-proof operations.
- Version Pinning & CVE Scanning: Consistent and secure deployments with proactive vulnerability detection (via Docker Scout).
- SBOM & Provenance: Traceable builds for complete supply chain transparency.

Acuvity also pairs ARC with **MiniBridge**[^10], a specialized opensource lightweight proxy enhancing security and governance. MiniBridge supports policy engines (like Open Policy Agent with Rego policies) to enforce fine-grained runtime security. Together, ARC and MiniBridge form a robust defense that limits damage even if an exploit occurs.

---

Remember, just because a tool is listed in an MCP registry doesn’t mean it’s safe. The safest approach—especially for handling sensitive data—is to self-host MCP tools in containers on trusted infrastructure with strict security policies.

---

[^1]: Acuvity. **"Securing MCP Servers."** _Acuvity_ (web article), 2025. [https://acuvity.ai/securing-mcp-servers/](https://acuvity.ai/securing-mcp-servers/)

[^2]: Rami McCarthy. **"Research Briefing: MCP Security."** _Wiz Blog_. April 17, 2025. [https://www.wiz.io/blog/mcp-security-research-briefing](https://www.wiz.io/blog/mcp-security-research-briefing)

[^3]: Bob Dickinson. **"Stop Running Your MCP Tools via npx/uvx Right Now."** _Medium_. May 2025. [https://medium.com/@scalablecto/stop-running-your-mcp-tools-via-npx-uvx-right-now-380d1ab99d3f](https://medium.com/@scalablecto/stop-running-your-mcp-tools-via-npx-uvx-right-now-380d1ab99d3f)

[^4]: Sudeep Padiyar. **"Securing Anthropic MCP with Acuvity."** _Acuvity Blog_. May 16, 2025. [https://acuvity.ai/securing-anthropic-mcp-with-acuvity/](https://acuvity.ai/securing-anthropic-mcp-with-acuvity/)

[^5]: Acuvity. **"MCP Security."** _Acuvity_ (product page), 2025. [https://acuvity.ai/mcp-security/](https://acuvity.ai/mcp-security/)

[^6]: Docker Docs. **"Explore Analysis in Docker Scout."** _Docker Documentation_. [https://docs.docker.com/scout/explore/analysis/#](https://docs.docker.com/scout/explore/analysis/#)

[^7]: GitHub MCP Registry. _toolsdk-ai/awesome-mcp-registry_. [https://github.com/toolsdk-ai/awesome-mcp-registry](https://github.com/toolsdk-ai/awesome-mcp-registry)

[^8]: Repello AI. **"MCP Tool Poisoning to RCE."** _Repello Blog_, 2025. [https://repello.ai/blog/mcp-tool-poisoning-to-rce](https://repello.ai/blog/mcp-tool-poisoning-to-rce)

[^9]: Repello AI. **"MCP Exploit Demo."** _GitHub Repository_, 2025. [https://github.com/Repello-AI/mcp-exploit-demo](https://github.com/Repello-AI/mcp-exploit-demo)

[^10]: Minibridge: "Make your MCP servers secure and production ready" GitHub Repository, 2025. [https://github.com/acuvity/minibridge](https://github.com/acuvity/minibridge)
