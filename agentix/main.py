import asyncio
import nest_asyncio
import subprocess
import os
from datetime import datetime
from pydantic import BaseModel

from agents import Agent, Runner, set_default_openai_key
from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

# --------------------
# Setup
# --------------------
nest_asyncio.apply()
set_default_openai_key("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")

console = Console()
HISTORY_FILE = "history.md"

# --------------------
# Command schema
# --------------------
class Command(BaseModel):
    command: list[str]   # MULTI-COMMAND SUPPORT

# --------------------
# Utility functions
# --------------------
def auto_newline(text: str, limit: int = 10) -> str:
    words = text.split()
    return "\n".join(
        " ".join(words[i:i + limit])
        for i in range(0, len(words), limit)
    )

def save_history(user_input: str, commands: list[str]):
    with open(HISTORY_FILE, "a", encoding="utf-8") as f:
        f.write(f"## {datetime.now().isoformat()}\n")
        f.write("**User Prompt:**\n")
        f.write(f"```\n{user_input}\n```\n")
        f.write("**Commands:**\n")
        f.write("```\n" + "\n".join(commands) + "\n```\n\n")

# --------------------
# CLI App
# --------------------
async def cli():
    agent = Agent(
        name="Agentix OS CLI Agent",
        instructions=(
            "You are an operating system CLI agent.\n"
            "Convert the user's natural language request into SAFE shell commands.\n"
            "If multiple tasks are requested, return commands in correct sequence.\n"
            "Return ONLY a list of shell commands.\n"
            "Do not explain anything."
        ),
        model="gpt-5-nano",
        output_type=Command
    )

    session = PromptSession(
        style=Style.from_dict({"prompt": "#00ffcc bold"})
    )

    console.print(
        Panel.fit(
            "[bold cyan]Agentix CLI[/bold cyan]\n"
            "[dim]Default: AI mode • Ctrl+C = exit[/dim]\n"
            "[dim]Use /cli <command> for raw shell[/dim]",
            border_style="cyan"
        )
    )

    # 🔥 THIS FIXES YOUR BUG
    current_dir = os.getcwd()

    while True:
        try:
            raw_input = session.prompt(" Agentix ❯ ").strip()
            if not raw_input:
                continue

            # --------------------
            # RAW SHELL MODE
            # --------------------
            if raw_input.lower().startswith("/cli "):
                shell_cmd = raw_input[5:].strip()
                if shell_cmd:
                    subprocess.run(shell_cmd, shell=True, cwd=current_dir)
                continue

            # --------------------
            # AI MODE (DEFAULT)
            # --------------------
            user_input = auto_newline(raw_input)
            result = await Runner.run(agent, user_input)
            commands = result.final_output.command

            if not commands:
                console.print("[red]No commands generated[/red]")
                continue

            for cmd in commands:
                cmd = cmd.strip()
                if not cmd:
                    continue

                console.print(Text(cmd, style="bold green"))
                input("Press Enter to Allow…")

                # 🔥 HANDLE `cd` MANUALLY
                if cmd.startswith("cd "):
                    path = cmd[3:].strip()
                    new_path = os.path.abspath(
                        os.path.join(current_dir, path)
                    )

                    if os.path.isdir(new_path):
                        current_dir = new_path
                        console.print(
                            f"[cyan]Directory changed to:[/cyan] {current_dir}"
                        )
                    else:
                        console.print(
                            f"[red]Directory not found:[/red] {path}"
                        )
                    continue

                subprocess.run(cmd, shell=True, cwd=current_dir)

            save_history(raw_input, commands)

        except KeyboardInterrupt:
            console.print("\n[bold cyan]Goodbye from Agentix 👋[/bold cyan]")
            break

# --------------------
# Entry
# --------------------
if __name__ == "__main__":
    asyncio.run(cli())
