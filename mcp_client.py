"""
Calling an MCP tool from your agent. ← UNIT 4

This is the plumbing, and it's given to you. Connecting over stdio and turning
the protocol's response back into a Python value is fiddly and it isn't the
lesson. What *is* the lesson is on the other side, in `mcp_server.py`: writing
a tool description and typed inputs that something other than your own code can
read.

Use it like this, in `run_agent()`:

    from mcp_client import call_tool

    results = call_tool("search_listings", {
        "description": "graphic tee",
        "max_price": 30,
    })

`results` comes back as the same list of dicts `search_listings` returned when
you called it directly. **That's the promise: the call changes shape, the
return value does not.** If it does change, that difference is information —
usually it means your tool was returning something you hadn't noticed.

Every call starts the server, asks, and stops it again. That's slower than
holding a connection open and it is much easier to reason about, which is the
right trade for one unit.
"""

import asyncio
import json
import sys
from pathlib import Path
from time import perf_counter

import atexit
from concurrent.futures import Future
from queue import Queue, Empty
from threading import Thread

SERVER = Path(__file__).parent / "mcp_server.py"


class MCPError(RuntimeError):
    """The server couldn't be reached, or it refused the call."""


class MCPConnection:
    """One worker that keeps an MCP connection open between calls."""

    def __init__(self):
        self.requests = Queue()
        self.failure = None
        self.thread = Thread(target=self._run, daemon=True)
        self.thread.start()

    def _run(self):
        try:
            asyncio.run(self._serve())
        except Exception as exc:
            self.failure = MCPError(f"MCP connection failed: {exc}")

            # Release any caller waiting for a response.
            while True:
                try:
                    request = self.requests.get_nowait()
                except Empty:
                    break

                if request is not None:
                    _, _, future = request
                    future.set_exception(self.failure)

    async def _serve(self):
        from mcp import ClientSession, StdioServerParameters
        from mcp.client.stdio import stdio_client

        params = StdioServerParameters(
            command=sys.executable,
            args=[str(SERVER)],
        )

        started = perf_counter()

        async with stdio_client(params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                available = {
                    tool.name
                    for tool in (await session.list_tools()).tools
                }

                print(
                    f"[MCP] connection ready in "
                    f"{perf_counter() - started:.3f}s",
                    file=sys.stderr,
                )

                while True:
                    request = await asyncio.to_thread(self.requests.get)

                    if request is None:
                        break

                    name, arguments, future = request

                    try:
                        if name not in available:
                            raise MCPError(
                                f"The server doesn't offer '{name}'. "
                                "Check its registration in mcp_server.py."
                            )

                        result = await session.call_tool(name, arguments)

                        if getattr(result, "isError", False):
                            raise MCPError(
                                f"The tool '{name}' returned an error: "
                                f"{_text(result)}"
                            )

                        future.set_result(_unwrap(result))
                    except Exception as exc:
                        future.set_exception(
                            MCPError(f"Couldn't call '{name}' over MCP: {exc}")
                        )

    def call(self, name, arguments):
        if self.failure:
            raise self.failure

        if not self.thread.is_alive():
            raise MCPError("The MCP connection has closed.")

        future = Future()
        self.requests.put((name, arguments, future))

        try:
            return future.result(timeout=60)
        except TimeoutError as exc:
            raise MCPError(
                "MCP did not respond within 60 seconds. "
                "Restart the application and check mcp_server.py."
            ) from exc

    def close(self):
        if self.thread.is_alive():
            self.requests.put(None)
            self.thread.join(timeout=5)


_connection = None


def call_tool(name: str, arguments: dict):
    """Start the connection on the first call, then reuse it."""

    """ The first call starts the server and connects. Later calls reuse that
connection until the program exits."""

    global _connection

    if _connection is None:
        _connection = MCPConnection()

    return _connection.call(name, arguments)


def close_connection():
    """Close the shared connection when the program finishes."""
    if _connection is not None:
        _connection.close()


atexit.register(close_connection)

def _unwrap(result):
    """
    Turn an MCP response back into the value the tool actually returned.

    MCP hands back content blocks rather than Python objects, so a tool that
    returned a list of dicts arrives as text containing JSON. This puts it
    back. Without this step your agent would start seeing strings where it used
    to see lists, and every downstream branch would quietly stop working.
    """
    structured = getattr(result, "structuredContent", None)
    if isinstance(structured, dict):
        # FastMCP wraps a bare (non-dict) return value under "result".
        if set(structured) == {"result"}:
            return structured["result"]
        return structured

    text = _text(result)
    if text == "":
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return text


def _type_of(spec: dict) -> str:
    """Read a type out of a JSON schema entry, including optional ones."""
    if "type" in spec:
        return spec["type"]
    options = spec.get("anyOf") or spec.get("oneOf") or []
    names = [o.get("type") for o in options if o.get("type") and o.get("type") != "null"]
    return " or ".join(names) if names else "?"


def _text(result) -> str:
    parts = []
    for block in getattr(result, "content", []) or []:
        value = getattr(block, "text", None)
        if value:
            parts.append(value)
    return "\n".join(parts).strip()


# ── check it works ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Asking mcp_server.py what it offers…\n")

    async def _list():
        from mcp import ClientSession, StdioServerParameters
        from mcp.client.stdio import stdio_client

        params = StdioServerParameters(command=sys.executable, args=[str(SERVER)])
        async with stdio_client(params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                return (await session.list_tools()).tools

    try:
        tools = asyncio.run(_list())
    except Exception as exc:  # noqa: BLE001
        print(f"Couldn't reach the server: {exc}")
        sys.exit(1)

    if not tools:
        print("The server is running but offers no tools yet.")
        print("Register one in mcp_server.py — that's Milestone 1.")
        sys.exit(0)

    for tool in tools:
        print(f"  {tool.name}")
        print(f"    {tool.description or '(no description — write one)'}")
        schema = tool.inputSchema or {}
        required = set(schema.get("required", []))
        for key, spec in schema.get("properties", {}).items():
            kind = _type_of(spec)
            mark = "" if key in required else "  (optional)"
            print(f"    - {key}: {kind}{mark}")
        print()
