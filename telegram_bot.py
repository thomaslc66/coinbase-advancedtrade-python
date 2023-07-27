import logging
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
from coinbase import buy_xx_amount_bitcoin, listAccounts, setCredentials
from coinbase_advanced_trader.config import TELEGRAM

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Extracting amount information to send formated answer to telgram
async def extract_account_info(json_data):
    # Initialize an empty string to store the account information
    account_info_str = ""

    # Extract required information from each account in the array
    for account in json_data["accounts"]:
        uuid = account["uuid"]
        name = account["name"]
        value = account["available_balance"]["value"]
        currency = account["available_balance"]["currency"]

        # Append the account information to the string
        account_info_str += f"UUID: {uuid}\nName: {name}\nValue: {value} {currency}\n\n"

    return account_info_str

#
# Extracting order result information
# to send back to the telegram bot
#
async def extract_order_info(data):
    # Initialize the order_str
    order_str = ""

    # Check if the response was successful
    if "success" in data and data["success"]:
        success_response = data["success_response"]
        product_id = success_response["product_id"]
        order_id = success_response["order_id"]
        order_str = f"Order success: True\nProduct ID: {product_id}\nOrder ID: {order_id}"
    elif "success" in data and not data["success"]:
        error_response = data["error_response"]
        error_message = error_response["message"]
        error_details = error_response["error_details"]
        order_str = f"Order success: False\nFailure Reason: {error_message}\nFailure Details:{error_details}"
    else:
        error_response = data["error"]
        error_message = data["message"]
        error_details = data["error_details"]
        order_str = f"Order success: False\nFailure Reason: {error_message}\nFailure Details:{error_details}"

    return order_str

#
# Handler for telegram command /listAccounts
# call CB advanced API and list account with currency
# Then send formated answer in telegram
#
async def telegram_listAccount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = listAccounts()
    response = await extract_account_info(response)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=response)

#
# Handler for telegram command /help
# Will send a list of command available to the bot chat
#
async def telegram_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="You can use the following commands:\n"
            "/help - to get help on the command\n"
            "/listAccounts - to list all your accounts and the amount\n"
            "/buyBTC currency* amount* price - Currency and Amount params are required, Price is for a limit order\n"
            "Example:\n"
            "/buyBTC EUR 10 -> Market order of 10€ worth of BTC\n"
            "/buyBTC USD 0.001 15000 -> Limit order to buy 0.001 BTC when the value hits 15000 USD"
)

#
# Handler for telegram command /buyBTC currency amount price
# Will send a list of command available to the bot chat
#
async def telegram_buy_btc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2 or len(context.args) > 3:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Currency and Amount params are required, Price is for a limit order\n'
                'Example:\n'
                '/buyBTC EUR 10 -> Market order of 10€ worth of BTC\n'
                '/buyBTC USD 0.001 15000 -> Limit order to buy 0.001 BTC when the value hits 15000 USD'
        )
    else:
        if len(context.args) == 2:
            currency_param = context.args[0].upper()
            amount_param = context.args[1]
            price_param = None
        elif len(context.args) == 3:
            currency_param = context.args[0].upper()
            amount_param = context.args[1]
            price_param = context.args[2]

        response = buy_xx_amount_bitcoin(amount_param, currency_param, price_param)
        response = await extract_order_info(response)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f'{response}\nCurrency:{currency_param}\nAmount:{amount_param}\nPrice:{price_param}')

# Unkown command handler
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command. Use /help to check available commands")


# Application setup
def setup_telegram_handlers(application):
    # Help Handler
    help_handler = CommandHandler('help', telegram_help)
    # Account Handler
    listAccount_handler = CommandHandler('listAccounts', telegram_listAccount)
    # Buy BTC handler
    buyBTC_handler = CommandHandler('buyBTC', telegram_buy_btc)
    # Other handlers
    unknown_handler = MessageHandler(filters.COMMAND, unknown)

    # Adding all handlers
    application.add_handler(help_handler)
    application.add_handler(listAccount_handler)
    application.add_handler(buyBTC_handler)
    application.add_handler(unknown_handler)

# Application building
def create_telegram_application(token):
    application = ApplicationBuilder().token(token).build()
    setup_telegram_handlers(application)
    return application

# Running Telegram bot
def run_telegram_bot():
    telegram_application = create_telegram_application(TELEGRAM)
    telegram_application.run_polling()