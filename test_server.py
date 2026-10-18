"""Run: python test_server.py  (starts nothing; talks to the app in-process over Streamable HTTP)."""

import asyncio
import time

import httpx2 as httpx
from mcp.client.session import ClientSession
from mcp.client.streamable_http import streamable_http_client

from server import TASKS, app


async def main():
    async with app.router.lifespan_context(app):
        http = httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test")
        async with streamable_http_client("http://test/mcp", http_client=http) as (r, w, *_):
            async with ClientSession(r, w) as s:
                await s.initialize()

                async def call(name, **args):
                    t0 = time.perf_counter()
                    res = await s.call_tool(name, args)
                    ms = (time.perf_counter() - t0) * 1000
                    text = res.content[0].text
                    print(f"{name:18} {ms:5.1f} ms  {text}")
                    assert ms < 500, "Alexa+ needs < 500 ms"
                    return text

                names = {t.name for t in (await s.list_tools()).tools}
                assert names == {"create_task", "whats_pending", "mark_done", "snooze", "get_task_history"}

                assert "caught up" in await call("whats_pending")
                await call("create_task", title="DBMS assignment", deadline="2026-10-24T09:00:00+05:30")
                await call("create_task", title="Gym", repeat_every_minutes=120)
                assert "2 pending" in await call("whats_pending")
                for _ in range(3):
                    out = await call("snooze", task="dbms", minutes=10)
                assert "3 snoozes" in out
                assert "3 times" in await call("get_task_history", task="DBMS asignment")  # typo on purpose
                assert "done" in await call("mark_done", task="dbms assignment")
                assert "1 pending" in await call("whats_pending")
                assert "couldn't find" in await call("mark_done", task="taxes")
    assert len(TASKS) == 2
    print("OK")


asyncio.run(main())
