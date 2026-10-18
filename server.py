"""FollowThrough: an Alexa+ MCP server for reminders that keep going until the task is done."""

import difflib
import os
import uuid
from datetime import datetime, timedelta, timezone

from mcp.server.mcpserver import MCPServer

mcp = MCPServer(
    "FollowThrough",
    instructions="Reminders that repeat until the user confirms the task is done. Keep spoken replies short.",
)

# ponytail: in-memory, single user, lost on restart. Swap for DynamoDB keyed by user id on Day 2.
TASKS: dict[str, dict] = {}


def now() -> datetime:
    return datetime.now(timezone.utc)


def find(name: str) -> dict | None:
    """Match a spoken task name to a pending task: substring first, then fuzzy."""
    pending = [t for t in TASKS.values() if not t["done"]]
    name = name.lower().strip()
    for t in pending:
        if name in t["title"].lower():
            return t
    titles = {t["title"].lower(): t for t in pending}
    best = difflib.get_close_matches(name, titles, n=1, cutoff=0.5)
    return titles[best[0]] if best else None


def when(iso: str | None) -> str:
    if not iso:
        return "no deadline"
    return "due " + datetime.fromisoformat(iso).strftime("%a %d %b, %I:%M %p")


@mcp.tool()
def create_task(title: str, deadline: str | None = None, repeat_every_minutes: int = 60) -> str:
    """Create a task that Alexa keeps reminding about until it is marked done.

    deadline: ISO 8601 datetime, e.g. 2026-10-24T09:00:00+05:30. repeat_every_minutes: nag interval.
    """
    if deadline:
        datetime.fromisoformat(deadline)  # reject garbage early
    tid = uuid.uuid4().hex[:8]
    TASKS[tid] = {
        "id": tid,
        "title": title,
        "deadline": deadline,
        "repeat_every_minutes": max(5, repeat_every_minutes),
        "next_nag": (now() + timedelta(minutes=repeat_every_minutes)).isoformat(),
        "done": False,
        "history": [{"at": now().isoformat(), "event": "created"}],
    }
    return f"Got it. I'll keep reminding you about {title}, every {repeat_every_minutes} minutes, until you tell me it's done."


@mcp.tool()
def whats_pending() -> str:
    """Short spoken summary of all unfinished tasks, soonest deadline first."""
    pending = [t for t in TASKS.values() if not t["done"]]
    if not pending:
        return "You're all caught up. Nothing pending."
    pending.sort(key=lambda t: t["deadline"] or "9999")
    parts = [f"{t['title']}, {when(t['deadline'])}" for t in pending[:3]]
    extra = f", and {len(pending) - 3} more" if len(pending) > 3 else ""
    return f"You have {len(pending)} pending: " + "; ".join(parts) + extra + "."


@mcp.tool()
def mark_done(task: str) -> str:
    """Mark a task as done so the reminders stop. task: the task name as the user said it."""
    t = find(task)
    if not t:
        return f"I couldn't find a pending task called {task}."
    t["done"] = True
    t["history"].append({"at": now().isoformat(), "event": "done"})
    return f"Nice work. {t['title']} is done, I'll stop reminding you."


@mcp.tool()
def snooze(task: str, minutes: int = 30) -> str:
    """Push the next reminder for a task back by some minutes."""
    t = find(task)
    if not t:
        return f"I couldn't find a pending task called {task}."
    t["next_nag"] = (now() + timedelta(minutes=minutes)).isoformat()
    t["history"].append({"at": now().isoformat(), "event": "snoozed", "minutes": minutes})
    n = sum(e["event"] == "snoozed" for e in t["history"])
    nudge = f" That's {n} snoozes so far." if n >= 3 else ""
    return f"Okay, I'll remind you about {t['title']} in {minutes} minutes.{nudge}"


@mcp.tool()
def get_task_history(task: str) -> str:
    """What has happened with a task: when it was created, how often it was snoozed, its deadline."""
    t = find(task)
    if not t:
        return f"I couldn't find a pending task called {task}."
    n = sum(e["event"] == "snoozed" for e in t["history"])
    return f"{t['title']} is {when(t['deadline'])}. You've snoozed it {n} time{'s' if n != 1 else ''}."


app = mcp.streamable_http_app(stateless_http=True, json_response=True, host="0.0.0.0")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
