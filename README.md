# Starship Telegram Client

Starship is a text action Telegram game in which the main target of player is to consistently upgrade his starship and compete in combats with other ones.

This repository provides source code of the Starsihp Telegram bot receiving and handling Starship players' requests gracefully piping them to [Starship Core](https://github.com/starship-crew/starship-core).

Technical specification for the project can be found [here](https://docs.google.com/document/d/1G6URBOew1XY_o6vuwBBKnyhgYMWYWzp2tFedxSK1CeE/edit?usp=sharing).

To run the project, install sqlite3 shared library on your system and run these commands within the repository root:
```bash
export TELEGRAM_BOT_TOKEN="*YOUR_TELEGRAM_BOT_TOKEN*"
poetry install
poetry run python main.py
```
