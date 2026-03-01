#!/usr/bin/env python3

import os
import sys
import time
import importlib
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.align import Align

console = Console()

VERSION = "1.0"
MODULE_DIR = "modules"


def clear():
    os.system("clear" if os.name == "posix" else "cls")


def banner():

    title = """
██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗██╗  ██╗██╗   ██╗██████╗
██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║██║  ██║██║   ██║██╔══██╗
██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║███████║██║   ██║██████╔╝
██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║██╔══██║██║   ██║██╔══██╗
██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║██║  ██║╚██████╔╝██████╔╝
╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝
"""

    panel = Panel(
        Align.center(f"[cyan]{title}[/cyan]\n[white]Digital Crew OSINT Framework[/white]\n[dim]Version {VERSION}[/dim]"),
        border_style="cyan",
        padding=(1,2)
    )

    console.print(panel)


def loading():
    with console.status("[cyan]Loading modules...[/cyan]"):
        time.sleep(1)


def load_modules():

    modules = []

    if not os.path.exists(MODULE_DIR):
        return modules

    for file in sorted(os.listdir(MODULE_DIR)):

        if file.endswith(".py") and not file.startswith("_"):

            name = file[:-3]

            try:
                module = importlib.import_module(f"{MODULE_DIR}.{name}")

                if hasattr(module, "run"):
                    modules.append({
                        "name": name.replace("_", " ").title(),
                        "function": module.run
                    })

            except:
                pass

    return modules


def show_menu(modules):

    table = Table(show_header=False, box=None, padding=(0,2))

    for i, mod in enumerate(modules, 1):
        table.add_row(f"[cyan][{str(i).zfill(2)}][/cyan]", mod["name"])

    table.add_row("[cyan][00][/cyan]", "Exit")

    console.print(Panel(table, border_style="cyan", title="[white]Modules[/white]"))


def main():

    modules = load_modules()

    while True:

        clear()
        banner()
        show_menu(modules)

        choice = console.input("\n[cyan]ReconHub > [/cyan]").strip()

        if choice in ["0", "00"]:
            sys.exit()

        if choice.isdigit():

            index = int(choice) - 1

            if 0 <= index < len(modules):
                clear()
                modules[index]["function"]()

        console.input("")


if __name__ == "__main__":
    try:
        loading()
        main()
    except KeyboardInterrupt:
        sys.exit()