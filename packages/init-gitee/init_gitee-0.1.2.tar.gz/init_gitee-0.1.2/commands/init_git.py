import os

import click


@click.command(
    name="init-git",
    context_settings={"help_option_names": ["--help", "-h"]},
)
@click.argument("path", required=True)
def init_git(path):
    url = f"https://gitee.com/{path}.git"
    commands = [
        "git init",
        "touch README.md",
        "git add README.md",
        "git commit -m 'init'",
        "git remote add origin {url}",
        "git config --global user.name birds",
        "git config --global user.email cg626@163.com",
        "git config --global credential.helper store",
    ]
    for command in commands:
        os.system(command)
