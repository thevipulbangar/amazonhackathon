# FollowThrough

Today Alexa reminds you at a set time. FollowThrough makes Alexa keep at it until the task is actually done.

An Alexa+ MCP server (Streamable HTTP, `/mcp`) built for students juggling deadlines. Built during the Build, Ship, Shape: Amazon Developer Hackathon (Oct 2026).

## Tools
| Tool | What it does |
|---|---|
| `create_task(title, deadline?, repeat_every_minutes?)` | Reminds you again and again until you mark it done |
| `whats_pending()` | Short spoken summary, soonest deadline first |
| `mark_done(task)` | Stops the reminders (task names are fuzzy-matched) |
| `snooze(task, minutes)` | Pushes the next reminder back and counts the snoozes |
| `get_task_history(task)` | "That's due Friday. You've snoozed it 3 times." |

## Run locally
```sh
python -m venv .venv && .venv/Scripts/pip install -r requirements.txt   # bin/ on macOS/Linux
.venv/Scripts/python server.py          # http://localhost:8000/mcp
.venv/Scripts/python test_server.py     # end-to-end self-check with latency numbers
npx @modelcontextprotocol/inspector     # connect to http://localhost:8000/mcp
```

## License
MIT
