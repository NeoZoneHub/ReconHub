import socket
import whois
import dns.resolver
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


def resolve_ip(domain):
    try:
        return socket.gethostbyname(domain)
    except:
        return "Unknown"


def get_ns(domain):
    try:
        answers = dns.resolver.resolve(domain, "NS", lifetime=5)
        return [r.to_text() for r in answers]
    except:
        return []


def run():

    console.print(Panel("[cyan]Domain Intelligence Module[/cyan]", border_style="cyan"))

    domain = console.input("\n[cyan]Domain > [/cyan]").strip()

    if not domain:
        return

    try:
        w = whois.whois(domain)
    except:
        console.print(Panel("WHOIS lookup failed", border_style="red"))
        console.input("\nPress ENTER to continue")
        return


    table = Table(title="Domain Information", border_style="cyan")
    table.add_column("Field", style="cyan")
    table.add_column("Value", style="white")

    table.add_row("Domain", str(w.domain_name))
    table.add_row("Registrar", str(w.registrar))
    table.add_row("Creation Date", str(w.creation_date))
    table.add_row("Expiration Date", str(w.expiration_date))
    table.add_row("Updated Date", str(w.updated_date))
    table.add_row("Status", str(w.status))
    table.add_row("Emails", str(w.emails))
    table.add_row("Org", str(getattr(w, "org", "Unknown")))
    table.add_row("Country", str(getattr(w, "country", "Unknown")))

    console.print(table)


    ns = get_ns(domain)

    ns_table = Table(title="Name Servers", border_style="cyan")
    ns_table.add_column("Server", style="white")

    if ns:
        for server in ns:
            ns_table.add_row(server)
    else:
        ns_table.add_row("None")

    console.print(ns_table)


    ip = resolve_ip(domain)

    ip_table = Table(title="Resolved IP", border_style="cyan")
    ip_table.add_column("IP Address", style="white")
    ip_table.add_row(ip)

    console.print(ip_table)


    console.input("\nPress ENTER to continue")