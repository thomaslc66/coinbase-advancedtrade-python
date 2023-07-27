# Coinbase Advanced Trade Telegram BOT

This is the unofficial Python client for the Coinbase Advanced Trade API Fork. It allows users to interact with the API to manage their cryptocurrency trading activities on the Coinbase platform using a Telegram bot and command.

## NOTE

I've developed this small bot using this Coinbase wrapper to suit my needs and I will not continue it's development, so don't expect me to answer issues or pull requests. Feel free to fork it on work on it as you want though.

## Features

- Telegram bot base on the Conbaise Advanced Trade API wrapper
- Possible to list accounts using bot command
  ```bash
  /listAccounts
  ```
- Possible to place BTC market order and limit order using bot command
  ```bash
  /buyBTC Currency Amount Price
  /buyBTC EUR 10 -> buy BTC for 10 EUR
  /buyBTC USD 0.0004 15000 -> place a limit order to buy 0.0004 BTC when price hit 15000USD
  ```
- Possible to ask for help using bot command
  ```bash
  /help
  ```

## TODO

- use the Telegram bot library to run daily bot command (usefull for DCA)
- create new bot command to match other API endpoint
- Update documentation to self host using docker or linux host

## Setup

1.  Clone this repository

    ```bash
       git clone https://github.com/thomaslc66/coinbase-advancedtrade-python.git

    ```

2.  Install the required Python packages:

    ```bash
       pip install -r requirements.txt

    ```

3.  Set your CoinBase API key and secret in config.py. To obtain your API key and secret, follow the steps below:
    - Log in to your Coinbase account.
    - Navigate to API settings.
    - Create a new API key with the appropriate permissions.
    - Copy the API key and secret to config.py.

## Usage

Here's an example of how to use the package:

- Go in the main.py files and update the Coinbase API_KEY, API_SECRET and TELEGRAM

```python
from telegram_bot import run_telegram_bot

if __name__ == '__main__':
    run_telegram_bot()
```

## Documentation

For more information about the Coinbase Advanced Trader API, consult the [official API documentation](https://docs.cloud.coinbase.com/advanced-trade-api/docs/rest-api-overview/).

## License

    This project is licensed under the MIT License. See the LICENSE file for more information.

## Author

    Rhett Reisman
    Fork and modification: Thomas
    Email: rhett@rhett.blog
    GitHub: https://github.com/rhettre/coinbase-advancedtrade-python

## Disclaimer

This project is not affiliated with, maintained, or endorsed by Coinbase. Use this software at your own risk. Trading cryptocurrencies carries a risk of financial loss. The developers of this software are not responsible for any financial losses or damages incurred while using this software.
