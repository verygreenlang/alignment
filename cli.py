import rich_click as click

click.rich_click.USE_MARKDOWN = True
import sys
import os

from src import SourceCore
from src import GlobalSourceCore


@click.group()
def cli():
    """
    Welcome to FINGREEN AI CLI
    > Remember:
    >  - You can try using --help at the top level
    >  - Ask the [code](https://github.com/fingreen-ai/alignment/), or for your peers for help
    """
    pass


@cli.command()
@click.option("-c", "--config", default="config.ini",required=False)  # , help='config.ini file ')
@click.option("-d", "--dconfig", required=True)  # , help='config.ini file ')
@click.argument("asset")
def source(asset, config, dconfig):
    click.echo("Starting sourcing core ")
    SC = SourceCore(asset, config, dconfig)
    SC.run()


@cli.command()
@click.option("-c", "--config", "config.ini",required=False)  # , help='config.ini file ')
def sourceall(config):
    click.echo("Starting sourcing core globaly ")
    GSC = GlobalSourceCore(config)
    GSC.run()


# Use Markdown (bit of a ridiculous example!)


# @click.command()
# @click.option(
#     "--input",
#     type=click.Path(),
#     help="Input **file**. _[default: a custom default]_",
# )
# @click.option(
#     "--type",
#     default="files",
#     show_default=True,
#     help="Type of file to sync",
# )
# @click.option("--all", is_flag=True, help="Sync\n 1. all\n 2. the\n 3. things?")
# @click.option(
#     "--debug/--no-debug",
#     "-d/-n",
#     default=False,
#     help="# Enable `debug mode`",
# )
# def cli(input, type, all, debug):
#     """
#     My amazing tool does _**all the things**_.
#     This is a `minimal example` based on documentation from the [_click_ package](https://click.palletsprojects.com/).
#     > Remember:
#     >  - You can try using --help at the top level
#     >  - Also for specific group subcommands.
#     """
#     print(f"Debug mode is {'on' if debug else 'off'}")
#

if __name__ == "__main__":
    cli()
