# How to collaborate in this repository

I am using poetry if you don't have one follow this [guide](#poetry-guide) and come back later on.

## How to start a bot

You can either use make or `python bot.py` beware that you should be inside virtual enviroment by activate it with `poetry shell`

## How do I define enviroment variables?

You can use `.env` file by 

```bash
ENVIROMENT_VARIABLE=VALUE
```

then you can access it with

```py
from dotenv import load_dotenv
load_dotenv()
import os
os.environ["ENVIROMENT_VARIABLE"] # or os.getenv
```

.env files is not committed to actual repo directly and it isn't couraged to edit `config/config.py` by yourself

## How can I add dependencies?

You can add them by `poetry add <package>`

## Poetry guide

1. Install poetry

```bash
pip install poetry
```

2. Install dependencies with poetry

```bash
poetry install
```

3. Access virtual enviroment

```bash
poetry shell
```

4. If you want to add intellisense for your VSCode then follow this [issue on github](https://github.com/microsoft/vscode-python/issues/8372) or [this one on stackoverflow](https://stackoverflow.com/questions/59882884/vscode-doesnt-show-poetry-virtualenvs-in-select-interpreter-option)
