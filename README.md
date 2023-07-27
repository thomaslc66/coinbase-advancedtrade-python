# Coinbase Advanced Trade Telegram BOT

This is the unofficial Python client for the Coinbase Advanced Trade API Fork. It allows users to interact with the API to manage their cryptocurrency trading activities on the Coinbase platform using a Telegram bot and command.

## NOTE

I've developed this small bot using this Coinbase wrapper to suit my needs and I will not continue it's development, so don't expect me to answer issues or pull requests. Feel free to fork it on work on it as you want though.

## Features

- Telegram bot base on the Conbaise Advanced Trade API wrapper
- Send command to bot to do action
- Possibility to create Reccuring buy order (DCA)

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

4.  Create a telegram bot and retrive the token for that: https://core.telegram.org/bots/features#creating-a-new-bot

- start a chat with @BotFather
- send `/newbot`
- then follow instruction and give your bot a name
- then follow instruction and select a username for your bot
- @BotFather will answer you and give you the token : <number>:<random_letter_and_number>
- Copy that token in .env or .env.docker
- if needed `/help` to see what you can do

## Usage

Here's an example of how to use the repository:
After cloning the repostitory you will have two files to edit.

#### To run it localy edit the .env file

all api key need to be between " "

```
# Set your API key and secret
API_KEY="api_key_example"
API_SECRET="api_secret_example"
TELEGRAM="telegram_bot_token_example"
```

Then you can call:

```cmd
python main.py
```

#### To run it using docker edit the .env.docker file

all api key need to be without " " and without space

```
# Set your API key and secret
API_KEY=api_key_example
API_SECRET=api_secret_example
TELEGRAM=telegram_bot_token_example
```

## Bot Commands

- List accounts
  ```bash
  /listAccounts
  ```
- Place BTC market order
  ```bash
  /buyBTC Currency Amount
  Example: /buyBTC EUR 10 -> Buy BTC for 10 EUR
  ```
- Place BTC Limit order
  ```bash
  /buyBTC Currency Amount Price
  Example: /buyBTC USD 0.0004 15000 -> Place a limit order to buy 0.0004 BTC when price hit 15000 USD
  ```
- Create a daily market order
  ```bash
  /setDCA <job_name> <currency> <amount>
  Example: /setDCA MY_DCA_JOB_NAME EUR 10 -> Place a daily market order for 10 EUR worth of Bitcoin
  ```
- Create a daily limit order
  ```bash
  /setDCA <job_name> <currency> <amount>
  Example: /setDCA MY_DCA_JOB_NAME USD 0.0004 15000 -> Place a daily limit order to buy 0.0004 BTC when price hit 15000 USD
  ```
- List all current DCA jobs
  ```bash
  /listJobs
  ```
- Remove specific DCA job name
  ```bash
  /unsetDCA <job_name>
  ```
- Possible to ask for help using bot command
  ```bash
  /help
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
