import asyncio
import sys
import os
import shutil

import microcore as mc
import async_typer
import typer
from .ai_code_review import Report
from .project_config import ProjectConfig
from git import Repo

from .ai_code_review import review
from .constants import ENV_CONFIG_FILE
from .bootstrap import bootstrap


app = async_typer.AsyncTyper(
    pretty_exceptions_show_locals=False,
)


if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


@app.callback(invoke_without_command=True)
def cli(ctx: typer.Context, filter = ""):
    if ctx.invoked_subcommand != 'setup':
        bootstrap()
    if not ctx.invoked_subcommand:
        asyncio.run(review(filter=filter))



@app.async_command(help="Configure LLM for local usage interactively")
async def setup():
    mc.interactive_setup(ENV_CONFIG_FILE)

@app.async_command()
async def render(format: str = Report.Format.MARKDOWN):
    print(Report.load().render(format=format))

@app.async_command(help="Review remote code")
async def remote(url=typer.Option(), branch=typer.Option()):
    if os.path.exists("reviewed-repo"):
        shutil.rmtree("reviewed-repo")
    Repo.clone_from(url, branch=branch, to_path="reviewed-repo")
    os.chdir("reviewed-repo")
    await review()
    os.chdir("../")
