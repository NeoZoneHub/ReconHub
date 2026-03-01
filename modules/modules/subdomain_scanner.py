import socket
import dns.resolver
from concurrent.futures import ThreadPoolExecutor, as_completed
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

WORDLIST = [
    "www","mail","webmail","ftp","cpanel","whm","ns1","ns2","dns","dns1","dns2",
    "mx","api","dev","test","stage","staging","beta","admin","portal","panel",
    "secure","server","vpn","m","mobile","blog","shop","store","app","dashboard",
    "auth","login","cloud","cdn","files","data","db","sql","gateway","node",
    "remote","client","support","help","docs","static","img","media","upload"
]


def resolve(host):
    try:
        answers = dns.resolver.resolve(host, "A", lifetime=3)
        return [r.to_text() for r in answers]
    except:
        return []


def scan(domain):

    found = []

    with ThreadPoolExecutor(max_workers=50) as executor:

        futures = {}

        for sub in WORDLIST:
            host = f"{sub}.{domain}"
            futures[executor.submit(resolve, host)] = host

        for future in as_completed(futures):

            host = futures[future]
            ips = future.result()

            if ips:
                found.append((host, ", ".join(ips)))

    return found


def run():

    console.print(Panel("[cyan]Subdomain Scanner Module[/cyan]", border_style="cyan"))

    domain = console.input("\n[cyan]Domain > [/cyan]").strip()

    if not domain:
        return

    console.print("\n[cyan]Scanning...[/cyan]\n")

    results = scan(domain)

    table = Table(title="Discovered Subdomains", border_style="cyan")
    table.add_column("Subdomain", style="cyan")
    table.add_column("IP", style="white")

    if results:
        for host, ip in sorted(results):
            table.add_row(host, ip)
    else:
        table.add_row("None found", "-")

    console.print(table)

    console.print(
        Panel(
            f"[cyan]Total Found:[/cyan] {len(results)}",
            border_style="cyan"
        )
    )

    console.input("\nPress ENTER to continue")