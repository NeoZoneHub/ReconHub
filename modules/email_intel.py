import re
import socket
import requests
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import dns.resolver

console = Console()

HIBP_API = ""  # optionnel : vous pouvez ajouter votre api Key pour la recherche de breaches, vous devez créer une clé API HaveIBeenPwned et la mettre entre " ".


def valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)


def resolve_mx(domain):
    try:
        answers = dns.resolver.resolve(domain, 'MX', lifetime=5)
        return [r.exchange.to_text() for r in answers]
    except:
        return []


def gravatar(email):
    import hashlib
    hash_email = hashlib.md5(email.lower().encode()).hexdigest()
    return f"https://www.gravatar.com/avatar/{hash_email}"


def check_breach(email):
    if not HIBP_API:
        return "API key missing"
    try:
        r = requests.get(f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}",
                         headers={"hibp-api-key": HIBP_API}, timeout=10)
        if r.status_code == 200:
            breaches = [b["Name"] for b in r.json()]
            return ", ".join(breaches) if breaches else "None"
        elif r.status_code == 404:
            return "None"
        else:
            return "Error"
    except:
        return "Error"


def run():

    console.print(Panel("[cyan]Email Intelligence Module[/cyan]", border_style="cyan"))

    email = console.input("\n[cyan]Email > [/cyan]").strip()

    if not email or not valid_email(email):
        console.print(Panel("Invalid email", border_style="red"))
        console.input("\nPress ENTER to continue")
        return

    domain = email.split("@")[1]

    table = Table(title="Email Information", border_style="cyan")
    table.add_column("Field", style="cyan")
    table.add_column("Value", style="white")

    table.add_row("Email", email)
    table.add_row("Domain", domain)
    table.add_row("Gravatar", gravatar(email))

    mx_records = resolve_mx(domain)
    table.add_row("MX Records", ", ".join(mx_records) if mx_records else "None")

    breaches = check_breach(email)
    table.add_row("Breaches", breaches)

    console.print(table)

    console.input("\nPress ENTER to continue")