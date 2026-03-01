import requests
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

API = "https://aryanx-apisx.onrender.com/tikstalk?username={}"


def fetch(username):
    try:
        r = requests.get(API.format(username), timeout=15)
        return r.json()
    except:
        return None


def run():

    console.print(Panel("[cyan]TikTok Intelligence Module[/cyan]", border_style="cyan"))

    username = console.input("\n[cyan]TikTok username > [/cyan]").strip().replace("@","")

    if not username:
        return

    console.print("\n[cyan]Fetching data...[/cyan]\n")

    data = fetch(username)

    if not data or not data.get("username"):
        console.print(Panel("User not found", border_style="red"))
        console.input("\nPress ENTER to continue")
        return


    nickname = data.get("nickname")
    username = data.get("username")
    avatar = data.get("avatarLarger")
    bio = data.get("signature")
    verified = data.get("verified")

    followers = data.get("followerCount")
    following = data.get("followingCount")
    likes = data.get("heartCount")
    videos = data.get("videoCount")
    relation = data.get("relation")

    profile = Table(title="Profile", border_style="cyan")
    profile.add_column("Field", style="cyan")
    profile.add_column("Value", style="white")

    profile.add_row("Nickname", str(nickname))
    profile.add_row("Username", f"@{username}")
    profile.add_row("Verified", "Yes" if verified else "No")
    profile.add_row("Bio", bio if bio else "None")
    profile.add_row("Avatar", avatar if avatar else "None")

    stats = Table(title="Statistics", border_style="cyan")
    stats.add_column("Metric", style="cyan")
    stats.add_column("Value", style="white")

    stats.add_row("Followers", str(followers))
    stats.add_row("Following", str(following))
    stats.add_row("Likes", str(likes))
    stats.add_row("Videos", str(videos))
    stats.add_row("Relation", str(relation))


    raw = Table(title="Raw Intelligence", border_style="cyan")
    raw.add_column("Key", style="cyan")
    raw.add_column("Value", style="white")

    for k, v in data.items():
        raw.add_row(str(k), str(v))


    console.print(profile)
    console.print(stats)
    console.print(raw)

    console.input("\nPress ENTER to continue")