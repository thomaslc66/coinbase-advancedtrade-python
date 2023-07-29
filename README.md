# Coinbase Advanced Trade Telegram BOT

This is a fork repository of the unofficial Python client for the Coinbase Advanced Trade API Fork. 
The Coinbase Advanced Trade Api will allow you to interact with coinbase advanced trading plateform and in this repository a layer was added in order to add basic functionalities and send command via a telegram chat bot.

## NOTE

I've developed this small telegram bot using this Coinbase wrapper to suit my needs and I will not continue developing new feature. I've already updated everything, also created a dockerfile that you can build and run directly, so don't expect me to answer issues or pull requests. Feel free to fork it and work on it as you want add new features and so on.

## Features

- Telegram bot, based on the Conbaise Advanced Trade API wrapper.
- Send command to bot to do action directly on Coinbase advanced trading plateform
- Possibility to create Reccuring buy order (DCA)
- 

## TODO

- create new bot command to match other API endpoint
- update /setDCA command to accept specific days and specific hours
- Update documentation to self host using docker or linux host (in progress)

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

4.  Create a telegram bot and retrive the token for that: https://core.telegram.org/bots/features#creating-a-new-bot

    - start a chat with @BotFather
    - send `/newbot`
    - then follow instruction and give your bot a name
    - then follow instruction and select a username for your bot
    - @BotFather will answer you and give you the token : <number>:<random_letter_and_number>
    - Copy that token in .env or .env.docker
    - if needed `/help` to see what you can do


5. Edit .evn.to.edit with all your API
   - Copy the Coinbase API key and secret to .env.to.edit and rename it as .env.
   - Copy your Telegram Bot Token and save
   - This file will be loaded and API KEY will not be exposed
     
7. Run it :
   ```bash
   python main.py
   ```

## Usage

Here's an example of how to use the repository:
After cloning the repostitory you will have two files to edit.

#### To run it localy edit the .env.to.edit file

all api key need to be between " "

```
# Set your API key and secret
API_KEY="api_key_example"
API_SECRET="api_secret_example"
TELEGRAM="telegram_bot_token_example"
```

rename the file from .env.to.edit to .env

Then you can call:

```cmd
python main.py
```

#### To run it using docker edit the .env.docker file

all api key need to be without the " " and without space in order for it to work in docker

```
# Set your API key and secret
API_KEY=api_key_example
API_SECRET=api_secret_example
TELEGRAM=telegram_bot_token_example
```

Then build and run the image like that:

passing the .env.docker as env file
```
docker build . -t coinbase-telegram
docker run --env-file ./.env.docker coinbase-telegram
```

## Bot Commands

### List accounts
  ```bash
  /listAccounts
  ```
  ![image](https://github.com/thomaslc66/coinbase-advancedtrade-python/assets/9827392/ada4f31f-d2a7-4c98-9975-405302c90628)

### Place BTC market order
  ```bash
  /buyBTC Currency Amount
  ```
  Example: /buyBTC EUR 10 -> Buy BTC for 10 EUR

  ![image](https://github.com/thomaslc66/coinbase-advancedtrade-python/assets/9827392/3f1dd366-23dd-4fa2-9d80-d644865b6e02)

### Place BTC Limit order
  Same as market order just set a price variable
  ```bash
  /buyBTC Currency Amount Price
  ```
  Example: /buyBTC USD 0.0004 15000 -> Place a limit order to buy 0.0004 BTC when price hit 15000 USD

  ![image](https://github.com/thomaslc66/coinbase-advancedtrade-python/assets/9827392/87189bf4-3768-4f24-b68a-9398a3785f1a)


### Create a daily market order
  ```bash
  /setDCA <job_name> <currency> <amount>
  ```
Example: /setDCA MY_DCA_JOB_NAME EUR 10 -> Place a daily market order for 10 EUR worth of Bitcoin

![image](https://github.com/thomaslc66/coinbase-advancedtrade-python/assets/9827392/550306ed-5565-48d6-9f92-17beb922b4df)

Then when order will be send at 12:30

![image](https://github.com/thomaslc66/coinbase-advancedtrade-python/assets/9827392/88d589af-eb5b-4d90-8838-20bf3ef8ec1b)

### Create a daily limit order
  ```bash
  /setDCA <job_name> <currency> <amount>
  ```
Example: /setDCA MY_DCA_JOB_NAME USD 0.0004 15000 -> Place a daily limit order to buy 0.0004 BTC when price hit 15000 USD

### Remove specific DCA job name
  ```bash
  /unsetDCA <job_name>
  ```
  ![image](https://github.com/thomaslc66/coinbase-advancedtrade-python/assets/9827392/fed34838-9ce6-462e-9012-9ae50f99abe4)

### List all current DCA jobs
  ```bash
  /listJobs
  ```
  ![image](https://github.com/thomaslc66/coinbase-advancedtrade-python/assets/9827392/7b8fc511-a629-40f1-9b6c-62d74d82feb4)

### Possible to ask for help using bot command
  ```bash
  /help
  ```
  ![image](https://github.com/thomaslc66/coinbase-advancedtrade-python/assets/9827392/75fb44c0-28ad-4979-92c9-3ff4760ec657)


## Documentation

For more information about the Coinbase Advanced Trader API, consult the [official API documentation](https://docs.cloud.coinbase.com/advanced-trade-api/docs/rest-api-overview/).

## License

    This project is licensed under the MIT License. See the LICENSE file for more information.

## Credit

    Coinbase advanced repo: Rhett Reisman
    Fork and modification with telegram bot: @thomaslc66
    GitHub: https://github.com/thomaslc66/coinbase-advancedtrade-python

## Disclaimer

This project is not affiliated with, maintained, or endorsed by Coinbase. 
Use this software at your own risk. 
Trading cryptocurrencies carries a risk of financial loss. The developers of this software are not responsible for any financial losses or damages incurred while using this software.
