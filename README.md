# GitHub to Gitea Mirror

gh2gt (GitHub to Gitea) is a simple tool that mirrors your own repositories and starred repositories to Gitea.

## Installation

- Install depencies with `pip install -r requirements.txt`
- Fill the `src/secrets.py` file
- If you want to ignore a repo add it to `src/settings.py`
- Run the python script `py main.py`

## Features

- Migrates your own repos to Gitea
- Migrates your starred repos to Gitea
- Ignore repos as you like

## ToDo

- Ease the code
- Shorten the code
- Add Docker support
- Add crontab support
- Remove GitHubPy dependency and make requests with requests package
- Make migration process two sided (sync between github and gitea)
- Add an option to mirroring process (like: do you want to mirror your own repos?)
- Take command-line arguments

## MightorMightNotDo

- Intractive mode (wait user input for every repo)

## Sources

<https://pygithub.readthedocs.io/en/latest/introduction.html>

<https://jpmens.net/2019/04/15/i-mirror-my-github-repositories-to-gitea/>
