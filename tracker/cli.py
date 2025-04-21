from typing import Iterable
import click

from tracker.query.base import TrendingTimeframe
from tracker.query.model import Show
from tracker.query.tvshows import TVShowAdapter, TelevisionDB


@click.group()
def main():
    pass


@main.group("tv")
@click.pass_context
def tvshow(ctx: click.Context):
    ctx.obj = TVShowAdapter(TelevisionDB())


def render_tvshows(shows: Iterable[Show]):
    output = []
    for show in shows:
        output.append(
            f"{show.name} ({show.length.seasons} seasons, {show.length.episodes} episodes)"
        )
        output.append(f"{show.description}")
        output.append(f"Genre: {', '.join(show.genres)}")
        output.append(f"Networks: {', '.join(show.networks)}")
        output.append("---")
    click.echo_via_pager("\n".join(output))


# tracker tvshow trending
@tvshow.command("trending")
@click.argument("timeframe", type=click.Choice(TrendingTimeframe))
@click.pass_obj
def trending_tv(obj: TVShowAdapter, timeframe: TrendingTimeframe):
    trending_shows = obj.trending(timeframe)
    render_tvshows(trending_shows)


@tvshow.command("search")
@click.argument("query", nargs=-1)
@click.pass_obj
def search_tv(obj: TVShowAdapter, query: str):
    query = " ".join(query)
    results = obj.search(query)
    render_tvshows(results)


if __name__ == "__main__":
    main()
