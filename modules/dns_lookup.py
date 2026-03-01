import socket
import dns.resolver
import dns.reversename
import dns.zone
import dns.query
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

def resolve(domain, rtype):
    try:
        answers = dns.resolver.resolve(domain, rtype, lifetime=5)
        return [r.to_text() for r in answers]
    except:
        return []

def get_ip(domain):
    try:
        return socket.gethostbyname(domain)
    except:
        return None

def reverse(ip):
    try:
        addr = dns.reversename.from_address(ip)
        answers = dns.resolver.resolve(addr, "PTR")
        return [r.to_text() for r in answers]
    except:
        return []

def zone_transfer(domain):
    results = []
    try:
        ns_servers = resolve(domain, "NS")
        for ns in ns_servers:
            try:
                z = dns.zone.from_xfr(dns.query.xfr(ns, domain, lifetime=5))
                for name, node in z.nodes.items():
                    for rdataset in node.rdatasets:
                        if rdataset.rdtype == 1:
                            for rdata in rdataset:
                                results.append((str(name), rdata.to_text()))
            except:
                pass
    except:
        pass
    return results

def run():

    console.print(Panel("[cyan]DNS Intelligence Module[/cyan]", border_style="cyan"))

    domain = console.input("\n[cyan]Domain > [/cyan]").strip()

    if not domain:
        return

    table = Table(title="DNS Records", border_style="cyan")
    table.add_column("Type", style="cyan")
    table.add_column("Value", style="white")

    record_types = ["A","AAAA","MX","NS","TXT","CNAME","SOA"]

    found = False

    for r in record_types:
        values = resolve(domain, r)
        for v in values:
            table.add_row(r, v)
            found = True

    if found:
        console.print(table)
    else:
        console.print(Panel("No DNS records found", border_style="red"))

    ip = get_ip(domain)

    if ip:
        ptrs = reverse(ip)

        ptr_table = Table(title="Reverse DNS", border_style="cyan")
        ptr_table.add_column("IP")
        ptr_table.add_column("Host")

        if ptrs:
            for host in ptrs:
                ptr_table.add_row(ip, host)
        else:
            ptr_table.add_row(ip, "Not found")

        console.print(ptr_table)

    zone = zone_transfer(domain)

    if zone:
        ztable = Table(title="Zone Transfer", border_style="cyan")
        ztable.add_column("Host")
        ztable.add_column("IP")

        for host, ipaddr in zone:
            ztable.add_row(host, ipaddr)

        console.print(ztable)
    else:
        console.print(Panel("Zone transfer not allowed", border_style="yellow"))

    console.input("\nPress ENTER to continue")