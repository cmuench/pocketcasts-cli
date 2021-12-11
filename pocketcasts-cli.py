import click
import json

from pycketcasts import PocketCast
from pycketcasts.pocketcasts import Episode, Category


class PocketcastsJsonEncode(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Category):
            data = {
                "name": obj.name,
                "source": obj.source,
                "icon": obj.icon
            }
            return data

        if isinstance(obj, Episode):
            url = obj.url
            if hasattr(obj, "episode_url"):
                url = obj.episode_url

            data = {
                "uuid": obj.uuid,
                "title": obj.title,
                "size": obj.size,
                "url": url,
                "duration": obj.duration,
                "file_type": obj.file_type,
                "starred": obj.starred,
                "deleted": obj.deleted,
                "podcast_uuid": obj.podcast_uuid,
                "podcast_title": obj.podcast_title,
                "season": obj.season,
                "number": obj.number,
                "playing_status": obj.playing_status,
                "current_position": obj.current_position,
            }
            return data
        return json.JSONEncoder.default(self, obj)


@click.group("cli")
@click.pass_context
@click.option("-e", "--email", is_flag=False, help="Email for login")
@click.option("-p", "--password", is_flag=False, help="Password for login")
def cli(ctx, email: str, password: str):
    if email == "":
        print("Email option is required")
        exit(1)

    if password == "":
        print("Password option is required")
        exit(1)

    _dict = {
        "email": email,
        "password": password
    }
    ctx.obj = _dict


@cli.command("starred")
@click.option("--use-pocketcasts-url", is_flag=True, help="Replace original url to episode with a link to pocketcasts.")
@click.pass_context
def starred(ctx, use_pocketcasts_url=False):
    """List starred episodes"""
    pc = PocketCast(ctx.obj["email"], ctx.obj["password"])

    if use_pocketcasts_url:
        data = pc.starred
        for episode in data:
            episode.__dict__["episode_url"] = "https://pca.st/episode/" + episode.uuid
    else:
        data = pc.starred

    print(json.dumps(data, cls=PocketcastsJsonEncode, indent=4))


@cli.command("categories")
@click.pass_context
def starred(ctx):
    """List all categories"""
    pc = PocketCast(ctx.obj["email"], ctx.obj["password"])
    print(json.dumps(pc.categories, cls=PocketcastsJsonEncode, indent=4))


def main():
    """Unofficial PocketCasts CLI"""
    cli(prog_name="cli")


if __name__ == '__main__':
    main()
