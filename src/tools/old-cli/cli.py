import rich_click as click
click.rich_click.USE_MARKDOWN = True
import sys
import os

from src.core import SourceCore

@click.group()
def cli():
    """
    My amazing tool does _**all the things**_.
    This is a `minimal example` based on documentation from the [_click_ package](https://click.palletsprojects.com/).
    > Remember:
    >  - You can try using --help at the top level
    >  - Also for specific group subcommands.
    """
    pass

@cli.command()  # @cli, not @click!
@click.option('-c','--config', required=True)#, help='config.ini file ')
@click.argument('asset')
def source(asset,config):
    click.echo('Starting sourcing core ')
    SC = SourceCore(asset,config)
    print(SC.company)
    SC.run()



import rich_click as click

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
