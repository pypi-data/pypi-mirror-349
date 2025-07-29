from __future__ import annotations

import asyncio
from typing import Awaitable, Callable, Tuple, List, Dict, Sequence, Any, Optional

import httpx
import logging
import json
import os
from httpx import Timeout, AsyncHTTPTransport

try:
    from rich.console import Console, Group
    from rich.live import Live
    from rich.panel import Panel
    from rich.columns import Columns
    from rich.progress import Progress, BarColumn, TimeElapsedColumn, TimeRemainingColumn

    _HAS_RICH = True
    _console = Console()
except ImportError:
    _HAS_RICH = False
    _console = None

__all__ = [
    "run_simulations",
]

_log = logging.getLogger(__name__)

_DEFAULT_JUDGE_MODEL = os.getenv("JANUS_JUDGE_MODEL", "openai/gpt-4.1-mini")

MAX_PARALLEL_SIMS: int = int(os.getenv("JANUS_MAX_PARALLEL_SIMS", "20"))

class JanusClient:
    """Async HTTP wrapper for the remote Janus API."""

    def __init__(
        self,
        base_url: str,
        api_key: str,
        *,
        _client: httpx.AsyncClient | None = None,
    ):
        """Create a new *logical* Janus client."""

        self._base = base_url.rstrip("/")
        self._headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        if _client is None:
            self._client = httpx.AsyncClient(
                headers=self._headers,
                timeout=Timeout(3600)
            )
            self._owns_client = True
        else:
            self._client = _client
            self._owns_client = False

    async def start(self, context: str, goal: str) -> Tuple[str, str]:
        """Begin a new conversation. Returns (conv_id, first_question)."""
        resp = await self._client.post(f"{self._base}/conv", json={
            "context": context,
            "goal": goal,
        })
        if resp.status_code != 200:
            # Surface structured error from Janus SaaS (if any)
            try:
                err_body = resp.json()
            except Exception:
                err_body = resp.text
            err_code = None
            try:
                if isinstance(err_body, dict):
                    err_code = err_body.get("error", {}).get("code")
            except Exception:
                err_code = None
            _log.error(
                f"JanusClient.start | HTTP {resp.status_code} | API_Code: {err_code} | body: {err_body}"
            )
        resp.raise_for_status()
        data = resp.json()
        return data["conv_id"], data["question"]

    async def turn(self, conv_id: str, answer: str) -> str:
        """Send *answer* and receive the next question (state handled server-side)."""
        resp = await self._client.post(f"{self._base}/conv/{conv_id}", json={
            "answer": answer,
        })
        if resp.status_code != 200:
            try:
                err_body = resp.json()
            except Exception:
                err_body = resp.text
            err_code = None
            try:
                if isinstance(err_body, dict):
                    err_code = err_body.get("error", {}).get("code")
            except Exception:
                err_code = None
            _log.error(
                f"JanusClient.turn | HTTP {resp.status_code} | API_Code: {err_code} | body: {err_body}"
            )
        resp.raise_for_status()
        data = resp.json()
        return data["question"]

    async def close(self):
        """Close the underlying :class:`httpx.AsyncClient` *if we own it*."""
        if self._owns_client:
            await self._client.aclose()

    # Context manager sugar
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()


async def _maybe_await(value):
    """Return ``value`` but await it first if it is awaitable."""
    if asyncio.iscoroutine(value):
        return await value
    return value


async def arun_simulations(
    *,
    num_simulations: int,
    context: str,
    goal: str,
    agent_factory: Callable[[], Callable[[str], Awaitable[str] | str]],
    base_url: str,
    api_key: str,
    max_turns: int,
    debug: bool = False,
    # --- Judge configuration -------------------------------------------------
    enabled_judges: Sequence[str] | None = ("rule",),
    rules: Sequence[str] | None = None,
    num_judges: int = 3,
    judge_model: str = _DEFAULT_JUDGE_MODEL,
    judge_kwargs: Dict[str, Any] | None = None,
) -> List[dict]:


    column_width: int = 80  # Default column width for plain text logs
    live_ctx: Live | None = None

    use_rich = debug and _HAS_RICH

    # Concurrency gate – shared across all simulation tasks spawned below.
    sem = asyncio.Semaphore(MAX_PARALLEL_SIMS)

    # Lightweight shared client used *only* for judge / hallucination calls.
    shared_client = httpx.AsyncClient(
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        limits=httpx.Limits(
            max_connections=MAX_PARALLEL_SIMS,
            max_keepalive_connections=MAX_PARALLEL_SIMS,
            keepalive_expiry=30.0,
        ),
        transport=AsyncHTTPTransport(retries=3),
        timeout=Timeout(3600),
    )

    try:
        sim_progress: Progress | None = None # Renamed from conv_progress
        sim_task_id = None # Renamed from conv_task_id

        if use_rich:
            sim_progress = Progress( # Renamed from conv_progress
                "[progress.description]{task.description}",
                BarColumn(),
                "[progress.completed]{task.completed}/{task.total}",
                TimeElapsedColumn(),
                TimeRemainingColumn(),
                console=_console,
                transient=True,
            )
            sim_task_id = sim_progress.add_task("Running Simulations...", total=num_simulations) # Renamed description


            def _render_live_display():
                elements: list[Any] = []

                if sim_progress: # Renamed from conv_progress
                    elements.append(sim_progress)

                return Group(*elements)

            live_ctx = Live(_render_live_display(), refresh_per_second=8, console=_console)
            live_ctx.__enter__()
        else:
            live_ctx = None  # type: ignore

        async def _one_sim(sim_idx: int) -> dict:
            """Run a **single** simulation under a concurrency semaphore.

            Each simulation gets its own short-lived :class:`httpx.AsyncClient`
            so a stale keep-alive cannot impact any other simulation.  A
            transport-level retry layer masks transient mid-stream resets on
            idempotent calls.
            """

            async with sem:
                transport = AsyncHTTPTransport(retries=3)
                async with httpx.AsyncClient(
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json",
                    },
                    limits=httpx.Limits(
                        max_connections=5,
                        max_keepalive_connections=5,
                        keepalive_expiry=30.0,
                    ),
                    transport=transport,
                    timeout=Timeout(3600),
                ) as _session:
                    client = JanusClient(base_url, api_key, _client=_session)
                    agent = agent_factory()

                    def _log(role: str, text: str):
                        return # Completely disable Q/A output
                        
                        # Original code left here but unreachable
                        if not debug or use_rich:  
                            return
                        
                        indent = " " * (sim_idx * column_width)
                        prefix = f"{role}{sim_idx}: "
                        snippet = text.replace("\n", " ")
                        print(f"{indent}{prefix}{snippet}")
                        print(f"{indent}{'-' * (column_width - 2)}")

                    # Start the conversation
                    conv_id, question = await client.start(context, goal)

                    qa: List[Dict[str, str]] = []

                    # Run the conversation loop
                    for turn_idx in range(max_turns):
                        _log("Q", question)
                        answer = await _maybe_await(agent(question))
                        _log("A", answer)

                        # Record the Q/A pair
                        qa.append({
                            "idx": turn_idx,
                            "q": question,
                            "a": answer,
                        })

                        # Advance the conversation
                        question = await client.turn(conv_id, answer)

                    _log("End", "Conversation finished")

                    try:
                        await _session.post(
                            f"{base_url.rstrip('/')}/conversation",
                            json={"conv_id": conv_id, "transcript": qa},
                        )
                    except Exception as exc_conv:
                        _log.warning("/conversation POST failed – %s", exc_conv)

                    if sim_progress and sim_task_id is not None:
                        sim_progress.update(sim_task_id, advance=1)
                        if live_ctx:
                            live_ctx.update(_render_live_display())

                    return {
                        "sim_id": sim_idx,
                        "conv_id": conv_id,
                        "qa": qa,
                    }
        aggregated = await asyncio.gather(*(_one_sim(i) for i in range(num_simulations)))

        if enabled_judges:

            answers_by_question: Dict[str, List[str]] = {}
            for sim in aggregated:
                for qa in sim["qa"]:
                    answers_by_question.setdefault(qa["q"], []).append(qa["a"])

            async def _rule_verdict(question: str, answer: str, conv_id: str) -> None:
                """Fire-and-forget: enqueue a judge job but *do not* poll for completion."""

                if not rules:
                    return

                payload = {
                    "question": question,
                    "answer": answer,
                    "rules": list(rules),
                    "num_judges": num_judges,
                    "judge_model": judge_model,
                    "judge_kwargs": judge_kwargs or {},
                    "enabled_judges": ["rule"],
                    "conv_id": conv_id,
                }

                try:
                    await shared_client.post(f"{base_url.rstrip('/')}/judge", json=payload)
                except Exception as exc:
                    _log.error("Rule judge HTTP error (enqueue only): %s", exc)

            rule_jobs: list[asyncio.Task] = []
            from typing import Tuple
            job_targets: list[Tuple[dict, str]] = []

            if enabled_judges and "rule" in enabled_judges and rules:
                for sim in aggregated:
                    for qa in sim["qa"]:
                        # create task
                        task = asyncio.create_task(_rule_verdict(qa["q"], qa["a"], sim["conv_id"]))
                        rule_jobs.append(task)
                        job_targets.append((qa, qa["q"]))

            if rule_jobs:
                await asyncio.gather(*rule_jobs, return_exceptions=True)
            if enabled_judges and "hallucination" in enabled_judges:
                async def _hallucination_metrics(answer: str, peers: list[str]) -> Dict[str, Any]:
                    payload = {
                        "answer": answer,
                        "other_answers": peers,
                    }
                    resp = await shared_client.post(f"{base_url.rstrip('/')}/hallucination", json=payload)
                    try:
                        resp.raise_for_status()
                        return resp.json().get("scores", {})
                    except Exception as exc:
                        _log.error("Hallucination HTTP error: %s", exc)
                        return {}

                hallu_tasks: list[asyncio.Task] = []
                hallu_targets: list[tuple[dict, list[str]]] = []

                for sim in aggregated:
                    for qa in sim["qa"]:
                        peers = [a for a in answers_by_question.get(qa["q"], []) if a != qa["a"]]
                        task = asyncio.create_task(_hallucination_metrics(qa["a"], peers))
                        hallu_tasks.append(task)
                        hallu_targets.append((qa, peers))

                if hallu_tasks:
                    hallu_results = await asyncio.gather(*hallu_tasks)
                    for (qa_dict, _), res in zip(hallu_targets, hallu_results):
                        qa_dict.setdefault("judgments", {})["hallucination"] = res

    finally:
        await shared_client.aclose()
        if use_rich and live_ctx is not None:
            live_ctx.__exit__(None, None, None)

    return aggregated


def run_simulations(
    *,
    num_simulations: int,
    context: str,
    goal: str,
    agent_factory: Callable[[], Callable[[str], Awaitable[str] | str]],
    base_url: str,
    api_key: str,
    max_turns: int = 10,
    debug: bool = False,
    # Judge parameters (see async variant for docstring)
    enabled_judges: Sequence[str] | None = ("rule",),
    rules: Sequence[str] | None = None,
    num_judges: int = 3,
    judge_model: str = _DEFAULT_JUDGE_MODEL,
    judge_kwargs: Dict[str, Any] | None = None,
):
    """Blocking wrapper that hides ``asyncio`` details and runs the async
    :pyfunc:`arun_simulations` helper.
    """

    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(
            arun_simulations(
                num_simulations=num_simulations,
                context=context,
                goal=goal,
                agent_factory=agent_factory,
                base_url=base_url,
                api_key=api_key,
                max_turns=max_turns,
                debug=debug,
                enabled_judges=enabled_judges,
                rules=rules,
                num_judges=num_judges,
                judge_model=judge_model,
                judge_kwargs=judge_kwargs,
            )
        )
    else:
        return loop.create_task(
            arun_simulations(
                num_simulations=num_simulations,
                context=context,
                goal=goal,
                agent_factory=agent_factory,
                base_url=base_url,
                api_key=api_key,
                max_turns=max_turns,
                debug=debug,
                enabled_judges=enabled_judges,
                rules=rules,
                num_judges=num_judges,
                judge_model=judge_model,
                judge_kwargs=judge_kwargs,
            )
        )
