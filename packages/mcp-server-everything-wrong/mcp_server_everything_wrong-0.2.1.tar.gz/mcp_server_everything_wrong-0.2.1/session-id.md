# Session ID Leakage: Exposed Identifiers in MCP URLs

## Context

Every conversation between an AI agent and tools often has some form of session or conversation ID to maintain state. In MCP’s early design, these session identifiers are sometimes included in request URLs (for HTTP-based servers) or other visible channels. This practice can lead to **session ID leakage**, a classic web security issue now rearing its head in the MCP ecosystem.

Imagine an MCP server that uses a URL like `GET /messages?sessionId=<UUID>` to fetch the latest messages for a session. If that sessionId is a secret token (and in many cases it effectively is, allowing access to conversation state or acting as an auth), exposing it in the URL is risky. URLs can be logged by servers, stored in browser history, and even accidentally shared (for example, in referer headers when loading resources). An attacker who finds this ID in logs or shoulder-surfs it could potentially hijack the session – for instance, by using the sessionId to impersonate the client or fetch data they shouldn’t have.

In a real-world context, think of this like an online banking site putting your session token in the page URL – anyone who sees that URL could use your logged-in session. Similarly, an MCP client or server that isn’t careful with session IDs might leak conversation context identifiers that let others snoop or inject messages.

## Example

Our “everything-wrong” MCP server, if it were HTTP-based, might have endpoints that look like this (pseudo-code using a FastAPI-like syntax):

```python
from fastapi import FastAPI, Request

app = FastAPI()
active_sessions = {}  # dict to store session data

@app.get("/messages")
def get_messages(request: Request):
    session_id = request.query_params.get("sessionId")
    if session_id in active_sessions:
        return active_sessions[session_id].message_history
    else:
        return {"error": "Invalid session"}

# ... elsewhere, when creating a session:
new_session_id = str(uuid.uuid4())
active_sessions[new_session_id] = SessionData(...)
print(f"MCP session started. Retrieve messages at /messages?sessionId={new_session_id}")
```

In this snippet, when a new session starts, the server prints or logs a URL with the sessionId. That line is illustrative of what a developer might do for debugging or convenience. The sessionId is right there in a query parameter. If this were a real log or console output, anyone with access to those logs could copy that URL and potentially fetch the conversation (`message_history`).

Even without explicit logging, the fact that the API uses `?sessionId=` means the session token travels in the URL:

- It may show up in web server logs (which typically log the full path of requests).
- If the client is a browser or uses a web view, the URL could be stored in history or caches.
- If any networking monitoring is in place, the raw URLs might be observed.

The **MCP spec’s design choice** to use session IDs in URLs (as noted by Equixly’s analysis) is the root of this vulnerability. It violates a fundamental web security best practice: session identifiers or any sensitive tokens should be kept out of URLs (using headers or request bodies instead), precisely to avoid these accidental exposures.

To illustrate how easily this can leak, consider a user who screenshares or takes a screenshot of their agent’s debug console – the session UUID might be visible. Or if the MCP server is behind a proxy, the proxy logs contain that param. An attacker who cannot break the AI or the server might simply steal the session token and attach their own client to the session to inject malicious messages or read sensitive information (if the protocol doesn’t guard against that).

It’s worth noting that session hijacking via leaked tokens could allow an attacker to insert themselves as a “man-in-the-middle” in the AI conversation. They might replay API calls or fetch messages as if they were the legitimate client. Depending on how the MCP client authenticates messages, this could be devastating – the attacker might issue tool calls or read past communications without any prompt injection at all.

Our demonstration above is simplistic but drives home the point: **exposing session IDs in a query string or any public channel is a design flaw**. In MCP’s case, because it’s built on web tech, it inherited this web vuln when done naively. This is a reminder that not all MCP issues are fancy AI-specific attacks; some are classic web/app sec issues manifesting in the new context.

## Example (Real-World Reference)

It’s worth mentioning a real reference: the Vulnerable MCP Project notes that _“the MCP protocol specification mandates session identifiers in URLs... fundamentally violating security best practices”_. That is exactly what we’re demonstrating. This was flagged as a medium severity issue because, while it doesn’t let an attacker directly run code, it **makes other attacks easier** (session hijacking, as well as forensic tracing of user activity via logs).

## Remediation

_Remediation (e.g., move session tokens to headers or secure channels, avoid logging them, implement proper auth checks) – **to be added by the user**._

