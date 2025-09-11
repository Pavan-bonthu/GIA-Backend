import json, os, time, datetime as dt, re, sys
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from pathlib import Path

# ---- Third-party ----
from pydantic import BaseModel
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Prompt
import requests
from PyPDF2 import PdfReader

console = Console()
DATA_DIR = Path(__file__).parent / "data"
TASKS_PATH = DATA_DIR / "tasks.json"
JOURNAL_PATH = DATA_DIR / "journal.md"
INBOX_DIR = DATA_DIR / "inbox_pdfs"
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")
MODEL = os.environ.get("OLLAMA_MODEL", "llama3.1:8b")

DATA_DIR.mkdir(exist_ok=True)
INBOX_DIR.mkdir(parents=True, exist_ok=True)
if not TASKS_PATH.exists():
    TASKS_PATH.write_text("[]", encoding="utf-8")
if not JOURNAL_PATH.exists():
    JOURNAL_PATH.write_text("# Journal\n\n", encoding="utf-8")

# ----------------- Tools -----------------
def load_tasks() -> List[Dict[str, Any]]:
    try:
        return json.loads(TASKS_PATH.read_text(encoding="utf-8"))
    except Exception:
        return []

def save_tasks(tasks: List[Dict[str, Any]]):
    TASKS_PATH.write_text(json.dumps(tasks, indent=2), encoding="utf-8")

def add_task(title: str, due: Optional[str] = None, tags: Optional[List[str]] = None) -> str:
    tasks = load_tasks()
    tid = max([t["id"] for t in tasks], default=0) + 1
    tasks.append({
        "id": tid,
        "title": title.strip(),
        "due": due,  # ISO date string "2025-08-22" or None
        "tags": tags or [],
        "status": "todo",
        "created_at": dt.datetime.now().isoformat(timespec="seconds")
    })
    save_tasks(tasks)
    return f"Task #{tid} added."

def list_tasks(status: Optional[str] = None, tag: Optional[str] = None) -> str:
    tasks = load_tasks()
    filtered = tasks
    if status:
        filtered = [t for t in filtered if t["status"] == status]
    if tag:
        filtered = [t for t in filtered if tag in t.get("tags", [])]
    if not filtered:
        return "No tasks."
    lines = []
    for t in filtered:
        lines.append(f'#{t["id"]} [{t["status"]}] {t["title"]} ' +
                     (f'(due {t["due"]}) ' if t["due"] else "") +
                     (f'tags:{",".join(t["tags"])}' if t["tags"] else ""))
    return "\n".join(lines)

def complete_task(task_id: int) -> str:
    tasks = load_tasks()
    for t in tasks:
        if t["id"] == task_id:
            t["status"] = "done"
            save_tasks(tasks)
            return f"Task #{task_id} marked done."
    return f"Task #{task_id} not found."

def quick_plan(day: str = "today") -> str:
    # Very simple planner: selects TODOs and proposes a schedule block list.
    tasks = [t for t in load_tasks() if t["status"] == "todo"]
    day_date = dt.date.today() if day == "today" else dt.datetime.fromisoformat(day).date()
    start = dt.datetime.combine(day_date, dt.time(hour=9, minute=0))
    blocks = []
    for t in tasks[:6]:  # cap for brevity
        blocks.append((start.strftime("%H:%M"), (start + dt.timedelta(minutes=50)).strftime("%H:%M"), t["title"]))
        start += dt.timedelta(minutes=60)
    if not blocks:
        return "No TODOs to plan."
    return "\n".join([f"{s}-{e}  {title}" for s, e, title in blocks])

def summarize_pdf(filename: str) -> str:
    path = INBOX_DIR / filename
    if not path.exists():
        return f"File '{filename}' not found in inbox."
    try:
        reader = PdfReader(str(path))
        text = []
        for i, page in enumerate(reader.pages[:10]):  # limit pages for speed
            text.append(page.extract_text() or "")
        content = "\n".join(text).strip()
        if not content:
            return "Could not extract text."
        prompt = f"Summarize concisely in bullet points:\n\n{content[:6000]}"
        return local_llm(prompt)
    except Exception as e:
        return f"Error reading PDF: {e}"

def write_journal(entry: str) -> str:
    stamp = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    JOURNAL_PATH.write_text(JOURNAL_PATH.read_text(encoding="utf-8") + f"\n## {stamp}\n{entry}\n", encoding="utf-8")
    return "Journal updated."

def start_timer(minutes: int) -> str:
    # Non-blocking hint for user; real timers are OS-specific. Here we just simulate.
    end_time = dt.datetime.now() + dt.timedelta(minutes=minutes)
    return f"Timer set for {minutes} minutes (until {end_time.strftime('%H:%M')}). Keep this terminal open."

TOOLS = {
    "add_task": add_task,
    "list_tasks": list_tasks,
    "complete_task": complete_task,
    "quick_plan": quick_plan,
    "summarize_pdf": summarize_pdf,
    "write_journal": write_journal,
    "start_timer": start_timer,
}

# ----------------- LLM plumbing -----------------
SYS_PROMPT = """You are an efficient home desk agent. You can either reply to the user or call a tool.
Think step-by-step and keep things concise.

TOOLS you may call (one at a time):
- add_task(title: str, due: str|None, tags: list[str]|None)
- list_tasks(status: str|None, tag: str|None)
- complete_task(task_id: int)
- quick_plan(day: str)  # 'today' or ISO date 'YYYY-MM-DD'
- summarize_pdf(filename: str)  # file must be inside data/inbox_pdfs
- write_journal(entry: str)
- start_timer(minutes: int)

When you need a tool, output exactly:
TOOL: {"name": "<tool_name>", "args": {...}}

When you are done and want to answer the user, output:
FINAL: <your concise answer>

NEVER output anything else.
"""

def ollama_chat(messages: List[Dict[str, str]]) -> str:
    r = requests.post(f"{OLLAMA_URL}/api/chat", json={"model": MODEL, "messages": messages, "stream": False}, timeout=120)
    r.raise_for_status()
    return r.json()["message"]["content"]

def local_llm(prompt: str) -> str:
    r = requests.post(f"{OLLAMA_URL}/api/generate", json={"model": MODEL, "prompt": prompt, "stream": False}, timeout=120)
    r.raise_for_status()
    return r.json()["response"]

TOOL_RE = re.compile(r'^TOOL:\s*(\{.*\})\s*$', re.DOTALL)
FINAL_RE = re.compile(r'^FINAL:\s*(.*)$', re.DOTALL)

def run_agent():
    console.print(Panel.fit("Home Desk Agent (local, no paid APIs). Type 'exit' to quit.", title="Agent", border_style="cyan"))
    history = [{"role": "system", "content": SYS_PROMPT}]
    while True:
        user = Prompt.ask("[bold green]You[/]")
        if user.strip().lower() in {"exit", "quit"}:
            console.print("[bold]Bye![/]")
            break
        history.append({"role": "user", "content": user})
        # Agent loop (allow up to 4 tool calls per turn)
        for _ in range(4):
            reply = ollama_chat(history)
            m_tool = TOOL_RE.match(reply.strip())
            m_final = FINAL_RE.match(reply.strip())
            if m_final:
                answer = m_final.group(1).strip()
                console.print(Markdown(answer))
                history.append({"role": "assistant", "content": reply})
                break
            elif m_tool:
                try:
                    call = json.loads(m_tool.group(1))
                    name = call["name"]
                    args = call.get("args", {})
                    if name not in TOOLS:
                        observation = f"Unknown tool: {name}"
                    else:
                        observation = TOOLS[name](**args)
                except Exception as e:
                    observation = f"Tool error: {e}"
                history.append({"role": "assistant", "content": reply})
                history.append({"role": "user", "content": f"OBSERVATION: {observation}"})
            else:
                # If model responded oddly, show it and stop the turn
                console.print(Markdown(reply))
                history.append({"role": "assistant", "content": reply})
                break

if __name__ == "__main__":
    run_agent()