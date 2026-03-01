import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

SITES = {
    "GitHub": "https://github.com/{}",
    "Telegram": "https://t.me/{}",
    "Instagram": "https://instagram.com/{}",
    "Twitter": "https://twitter.com/{}",
    "TikTok": "https://www.tiktok.com/@{}",
    "YouTube": "https://www.youtube.com/@{}",
    "Reddit": "https://www.reddit.com/user/{}",
    "Pinterest": "https://www.pinterest.com/{}",
    "Snapchat": "https://www.snapchat.com/add/{}",
    "LinkedIn": "https://www.linkedin.com/in/{}",
    "Medium": "https://medium.com/@{}",
    "Vimeo": "https://vimeo.com/{}",
    "SoundCloud": "https://soundcloud.com/{}",
    "GitLab": "https://gitlab.com/{}",
    "Bitbucket": "https://bitbucket.org/{}",
    "Twitch": "https://www.twitch.tv/{}",
    "Steam": "https://steamcommunity.com/id/{}",
    "DeviantArt": "https://www.deviantart.com/{}",
    "About.me": "https://about.me/{}",
    "Flickr": "https://www.flickr.com/people/{}"
}


HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def check(site, url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=8)
        if r.status_code == 200 and len(r.text) > 500:
            return site, url, True
        return site, url, False
    except:
        return site, url, False


def run():

    console.print(Panel("[cyan]Username Intelligence Module[/cyan]", border_style="cyan"))

    username = console.input("\n[cyan]Username > [/cyan]").strip()

    if not username:
        return

    table = Table(title="Results", border_style="cyan")
    table.add_column("Platform", style="cyan")
    table.add_column("Status")
    table.add_column("URL", style="white")

    found_count = 0

    with ThreadPoolExecutor(max_workers=20) as executor:

        futures = []

        for site, url in SITES.items():
            futures.append(executor.submit(check, site, url.format(username)))

        for future in as_completed(futures):

            site, url, found = future.result()

            if found:
                table.add_row(site, "[green]FOUND[/green]", url)
                found_count += 1
            else:
                table.add_row(site, "[red]NOT FOUND[/red]", url)

    console.print(table)

    console.print(
        Panel(
            f"[cyan]Total Found:[/cyan] {found_count} / {len(SITES)}",
            border_style="cyan"
        )
    )

    console.input("\nPress ENTER to continue")