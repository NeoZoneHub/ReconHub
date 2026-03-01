#!/usr/bin/env python3

import os
import sys
import time
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.align import Align

console = Console()

VERSION = "1.0"

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

def loading(text="Initializing"):

    with console.status(f"[cyan]{text}...[/cyan]"):
        time.sleep(1.2)

def menu():

    table = Table(show_header=False, box=None, padding=(0,2))

    table.add_row("[cyan][01][/cyan]", "DNS Lookup")
    table.add_row("[cyan][02][/cyan]", "IP Tracker")
    table.add_row("[cyan][03][/cyan]", "Domain Intelligence")
    table.add_row("[cyan][04][/cyan]", "Username Search")
    table.add_row("[cyan][05][/cyan]", "Subdomain Scanner")
    table.add_row("[cyan][06][/cyan]", "Port Scanner")
    table.add_row("[cyan][07][/cyan]", "Phone Lookup")
    table.add_row("[cyan][00][/cyan]", "Exit")

    console.print(Panel(table, border_style="cyan", title="[white]Modules[/white]"))

def pause():
    input("\nPress ENTER to continue")

def not_ready(name):
    console.print(f"\n[yellow]{name} module not installed[/yellow]")
    pause()

def main():

    while True:

        clear()
        banner()
        menu()

        choice = console.input("\n[cyan]ReconHub > [/cyan]").strip()

        if choice == "1" or choice == "01":
            not_ready("DNS Lookup")

        elif choice == "2" or choice == "02":
            not_ready("IP Tracker")

        elif choice == "3" or choice == "03":
            not_ready("Domain Intelligence")

        elif choice == "4" or choice == "04":
            not_ready("Username Search")

        elif choice == "5" or choice == "05":
            not_ready("Subdomain Scanner")

        elif choice == "6" or choice == "06":
            not_ready("Port Scanner")

        elif choice == "7" or choice == "07":
            not_ready("Phone Lookup")

        elif choice == "0" or choice == "00":
            console.print("\n[cyan]Exiting ReconHub[/cyan]\n")
            sys.exit()

        else:
            console.print("\n[red]Invalid option[/red]")
            time.sleep(1)


if __name__ == "__main__":
    try:
        loading()
        main()
    except KeyboardInterrupt:
        console.print("\n\n[red]Interrupted[/red]")