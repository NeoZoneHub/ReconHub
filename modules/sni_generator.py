from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

OPERATORS = {
    "cd": ["africell", "vodacom", "orange", "airtel"],
    "cm": ["orange", "mtn", "camtel"],
    "sn": ["orange", "free", "yas", "expresso"],
    "ci": ["orange", "mtn", "moov"],
    "ng": ["mtn", "glo", "airtel", "9mobile"],
    "gh": ["mtn", "vodafone", "airteltigo"],
    "ke": ["safaricom", "airtel", "telkom"],
    "za": ["vodacom", "mtn", "cellc", "telkom"],
    "fr": ["orange", "sfr", "bouygues", "free"],
    "ma": ["orange", "inwi", "iam"],
    "tn": ["orange", "ooredoo", "tunisie"],
    "dz": ["mobilis", "djezzy", "ooredoo"]
}

PREFIXES = [
    "internet",
    "web",
    "data",
    "wap",
    "mms",
    "portal",
    "mobile",
    "net",
    "connect",
    "forfaitepuise",
    "zero",
    "free",
    "unlimited"
]


def generate(country):

    results = []

    ops = OPERATORS.get(country.lower())

    if not ops:
        return results

    for op in ops:
        for prefix in PREFIXES:
            results.append(f"{prefix}.{op}.{country}")

    return results


def run():

    console.print(Panel("[cyan]SNI Generator Module[/cyan]", border_style="cyan"))

    console.print("\nAvailable countries:\n")
    console.print(", ".join(OPERATORS.keys()))

    country = console.input("\n[cyan]Country code > [/cyan]").lower().strip()

    results = generate(country)

    table = Table(title="Generated SNI", border_style="cyan")
    table.add_column("SNI", style="white")

    if results:
        for sni in results:
            table.add_row(sni)
    else:
        table.add_row("No data")

    console.print(table)

    console.print(
        Panel(f"[cyan]Total:[/cyan] {len(results)}", border_style="cyan")
    )

    console.input("\nPress ENTER to continue")