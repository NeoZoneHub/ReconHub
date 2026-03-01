import socket
import requests
import subprocess
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


def resolve_target(target):
    try:
        return socket.gethostbyname(target)
    except:
        return None


def ip_info(ip):
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}?fields=status,message,continent,country,regionName,city,zip,lat,lon,timezone,isp,org,as,reverse,query", timeout=10)
        return r.json()
    except:
        return None


def reverse_dns(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except:
        return "Not found"


def scan_ports(ip):
    ports = [21,22,23,25,53,80,110,139,143,443,445,3306,3389,8080]
    open_ports = []

    for port in ports:
        try:
            sock = socket.socket()
            sock.settimeout(0.5)
            result = sock.connect_ex((ip, port))
            sock.close()
            if result == 0:
                open_ports.append(port)
        except:
            pass

    return open_ports


def run():

    console.print(Panel("[cyan]IP Intelligence Module[/cyan]", border_style="cyan"))

    target = console.input("\n[cyan]IP or Host > [/cyan]").strip()

    if not target:
        return

    ip = resolve_target(target) if not target.replace(".", "").isdigit() else target

    if not ip:
        console.print(Panel("Invalid target", border_style="red"))
        console.input("\nPress ENTER to continue")
        return

    data = ip_info(ip)

    table = Table(title="IP Information", border_style="cyan")
    table.add_column("Field", style="cyan")
    table.add_column("Value", style="white")

    if data and data.get("status") == "success":

        table.add_row("IP", data.get("query",""))
        table.add_row("Reverse", data.get("reverse") or reverse_dns(ip))
        table.add_row("Country", data.get("country",""))
        table.add_row("Region", data.get("regionName",""))
        table.add_row("City", data.get("city",""))
        table.add_row("ZIP", data.get("zip",""))
        table.add_row("Timezone", data.get("timezone",""))
        table.add_row("ISP", data.get("isp",""))
        table.add_row("Organization", data.get("org",""))
        table.add_row("ASN", data.get("as",""))
        table.add_row("Coordinates", f'{data.get("lat","")}, {data.get("lon","")}')

        maps = f"https://www.google.com/maps?q={data.get('lat')},{data.get('lon')}"
        table.add_row("Google Maps", maps)

    else:

        table.add_row("IP", ip)
        table.add_row("Reverse", reverse_dns(ip))

    console.print(table)

    ports = scan_ports(ip)

    port_table = Table(title="Common Open Ports", border_style="cyan")
    port_table.add_column("Port", style="cyan")
    port_table.add_column("Status", style="white")

    if ports:
        for p in ports:
            port_table.add_row(str(p), "OPEN")
    else:
        port_table.add_row("-", "No common ports open")

    console.print(port_table)

    console.input("\nPress ENTER to continue")