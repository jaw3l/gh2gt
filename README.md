# GitHub to Gitea Mirror

[![BCH compliance](https://bettercodehub.com/edge/badge/jaw3l/gh2gt?branch=master)](https://bettercodehub.com/)

gh2gt (GitHub to Gitea) is a simple tool that mirrors your **own** repositories and **starred** repositories to Gitea.

## Installation

- Install depencies with `pip install -r requirements.txt`
- Fill the `src/secrets.py` file
- If you want to ignore a repo add it to `src/settings.py`
- Run the python script `py main.py`

## Features

- Migrates your own repos to Gitea
- Migrates your starred repos to Gitea
- Ignore repos as you like

## Gitea Configuration

You might want to change your Gitea configuration if you have more than 50 starred or own repositories. Because Gitea's default configuration only lists 50 items for each request. To do that:

- Open `gitea/conf/app.ini`
- Add `[api]` header (I don't know if it is necessary)
- Below the header add `MAX_RESPONSE_ITEMS` varibale and the number you desire as value. Example: `MAX_RESPONSE_ITEMS=100`

`app.ini` should look like this

```ini
...

[api]
MAX_RESPONSE_ITEMS=100

...
```

You can find more information at [official documentation](https://docs.gitea.io/en-us/config-cheat-sheet/#api-api).

## ToDo

- Ease the code
- Shorten the code
- Add tests
- Add Docker support
- Add crontab support
- Remove GitHubPy dependency and make requests with requests package
- Make migration process two sided (sync between github and gitea)
- Add an option to mirroring process (like: do you want to mirror your own repos?)
- Take command-line arguments

## MightDo

- Intractive mode (wait user input for every repo)

## Sources

<https://pygithub.readthedocs.io/en/latest/introduction.html>

<https://jpmens.net/2019/04/15/i-mirror-my-github-repositories-to-gitea/>
