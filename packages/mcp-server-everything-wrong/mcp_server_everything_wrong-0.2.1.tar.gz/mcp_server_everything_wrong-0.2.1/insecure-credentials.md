# Insecure Credential Storage: API Keys Under the Doormat

## Context

Many MCP servers need credentials to access external services (APIs, databases, etc.). For example, a server that integrates with AWS needs AWS keys; one that queries a database might need a connection string. A major issue observed in the wild is that these credentials are often stored **in plaintext on disk** by the MCP servers, sometimes with weak file permissions. This means if an attacker compromises the machine (even briefly, or via another vulnerability), they can easily harvest these keys. Even without a live attack, backups or other users on the system could inadvertently expose the keys if they are world-readable files.

Think of it this way: you install an MCP server for GitHub issues. It asks for a GitHub Personal Access Token, and you provide it (maybe via a config file or an environment variable). The server then writes this token to a config file in your home directory, like `~/.mcp/github_server/config.json`. If that file is not secured, any malware or curious user on your system can open it and see your token, gaining access to your GitHub account. Or if you sync your home directory somewhere, you’ve now leaked an API key.

This problem is not unique to MCP, but MCP makes it more likely because a lot of rapid development is happening, and not every server developer is following best practices like using OS keychains or at least file permission locks. The **Trail of Bits research** highlighted that numerous official and third-party MCP servers were storing keys in plaintext – including for services like GitLab, Postgres, Google Maps, etc.. It’s an ecosystem-wide issue.

## Example

In our “everything wrong” server, let’s demonstrate poor credential storage. Suppose our server integrates with a fictional “MegaCloud” storage service and needs an API key:

```python
MEGACLOUD_API_KEY = None

def init(megacloud_api_key: str):
    global MEGACLOUD_API_KEY
    MEGACLOUD_API_KEY = megacloud_api_key
    # Save the key to a file for persistence (insecurely)
    config_path = os.path.expanduser("~/.mcp/everything_wrong_config.txt")
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    with open(config_path, "w") as f:
        f.write(f"MEGACLOUD_API_KEY={megacloud_api_key}\n")
    print(f"[Info] Saved MegaCloud API key to {config_path}")

class UploadToMegaCloud:
    """Upload a file to MegaCloud storage."""
    def __call__(self, filename: str, data: bytes):
        if MEGACLOUD_API_KEY is None:
            return "Error: No API key configured."
        # (Pretend to upload using the API key...)
        return f"File '{filename}' uploaded to MegaCloud."
```

Several red flags in this code:

- We write the API key in plaintext to `~/.mcp/everything_wrong_config.txt`. The file isn’t encrypted, and we didn’t set any file permission (it will likely be 644 by default, meaning readable by other users on the system in many OS configurations).
- We printed the path and fact we saved it, which might tip off an attacker scanning logs or simply confirm the location.
- The key is also stored in a global variable `MEGACLOUD_API_KEY` in memory. If our process or another tool had a way to dump memory, it’s accessible. This is somewhat unavoidable while in use, but worth noting.

Now, if an attacker gains a foothold on this machine via another MCP vulnerability or any malware, the first thing they might do is look into `~/.mcp/` directory (a logical place for config). There they find `everything_wrong_config.txt` with `MEGACLOUD_API_KEY=...`. With that key, they can now access the user’s MegaCloud account outside of MCP entirely (a completely different vector of attack).

Even without active attack, consider multi-user systems: if this file’s permissions are not restricted, any user on the system could read it. Or if the user checks this into source control by accident (since it’s just a text file in home directory) or backs it up, the key could leak.

Many MCP servers probably do something similar: writing config to the user directory. The proper way would be to at least chmod the file to 600 (user-only) and ideally encrypt or use a secure credential store. But our server is doing it the wrong way – as many did in early MCP examples – to keep things simple.

Another example is storing credentials inside code or notebooks that users might share. For instance, someone might paste their API key into a notebook to initialize an MCP server (as seen in some tutorials), then share that notebook forgetting the key is in there.

The **severity** of this issue is high because API keys often have broad access. If an AI agent’s key for a cloud service leaks, an attacker might not even need to bother with AI – they directly log into the cloud account and wreak havoc.

## Example: World-Readable Key

To simulate how bad it can be, let’s say our config file was created with default perms (644). On a Unix system, that’s world-readable. We can check this (if we were to run it):

_(Imagine running the server then doing `ls -l ~/.mcp/everything_wrong_config.txt`)_:

```
-rw-r--r-- 1 user user 50 Sep 1 12:00 everything_wrong_config.txt
```

The `rw-r--r--` means owner can read/write, group can read, others can read. If this is a shared machine or if an attacker gets a low-privileged account, they can read that file.

Even on single-user machines, some paths might be synced to cloud backups (OneDrive, Dropbox, etc.), and those could be compromised or accessed by others (say, an IT admin or a hacker who got into your cloud storage).

The Trail of Bits snippet from April 30, 2025, points out _“many examples of MCP software store API keys in plaintext, often world-readable… leaving users one file disclosure away from having their API keys stolen”_. Our example is exactly that: one file disclosure (that config) away from disaster.

## Remediation

_Remediation (e.g., use secure credential vaults, never store secrets unencrypted, enforce file permission, rotate keys) – **to be added by the user**._

