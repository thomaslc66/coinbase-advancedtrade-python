import logging
import html
import json
import logging
import traceback
import datetime, pytz
from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )

from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
from telegram.constants import ParseMode
from coinbase import buy_xx_amount_bitcoin, listAccounts
from coinbase_advanced_trader.config import TELEGRAM

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

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
            "/buyBTC <currency>* <amount>* price - Currency and Amount params are required, Price is for a limit order\n"
            "Example:\n"
            "/buyBTC EUR 10 -> Market order of 10€ worth of BTC\n"
            "/buyBTC USD 0.001 15000 -> Limit order to buy 0.001 BTC when the value hits 15000 USD"
            "/setDCA <DCA_NAME>* <currency>* <amount>* <price> -> same logic as /buyBTC command but to place a daily (12:30) recurring order"
            "/unsetDCA <DCA_NAME>* -> to remove the recurring order already in place"
            "/listJobs -> will list all the recurring job in place"
)

async def telegram_buy_btc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for the Telegram command /buyBTC <currency>* <amount>* <price>.

    Buys Bitcoin with the specified amount and currency.

    Args:
        update (Update): The incoming update from Telegram.
        context (ContextTypes.DEFAULT_TYPE): The context for the Telegram message.

    This handler processes the /buyBTC command, allowing the user to buy Bitcoin
    with the specified amount and currency. If the price is provided, it will
    execute a limit order; otherwise, it will execute a market order. The handler
    sends a message with the order result and details to the Telegram chat.

    Examples:
        /buyBTC EUR 10 -> Market order of 10€ worth of BTC
        /buyBTC USD 0.001 15000 -> Limit order to buy 0.001 BTC when the value hits 15000 USD
    """

    # Function implementation
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


#
# TODO - give possibility to user to set specific day and time
# TODO - set hour, minutes and timezone as variable
#
async def set_dca(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler for the Telegram command /setDCA.

    Adds a job to the job queue for Dollar-Cost Averaging Scheduling job (DCA).

    Args:
        update (Update): The incoming update from Telegram.
        context (ContextTypes.DEFAULT_TYPE): The context for the Telegram message.

    This handler processes the /setDCA command, which allows the user to schedule
    Dollar-Cost Averaging (DCA) with the specified DCA name, currency, amount, and
    optional price. The DCA job will be repeated daily at a fixed interval and
    execute the specified DCA strategy. The handler responds with a confirmation
    message if the DCA is successfully set.

    Usage:
        /setDCA <dca_name>* <currency>* <amount>* <price> (Price is optional)
    """
    
    # Function implementation
    chat_id = update.effective_message.chat_id

    try:
        # DCA will always be daily
        price = None
        if len(context.args) > 3:
            price = context.args[3]
        dca_name = context.args[0]
        dca_name = dca_name if dca_name else "DCA_SCHEDULED"
        currency = context.args[1]
        amount = context.args[2]


        context.job_queue.run_daily(dca_job, datetime.time(hour=12, minute=30, tzinfo=pytz.timezone('Europe/Zurich')),
                                days=(0, 1, 2, 3, 4, 5, 6), chat_id=chat_id, name=dca_name, data=[dca_name, currency, amount, price])
        text = "DCA successfully set!"
        await update.effective_message.reply_text(text)

    except (IndexError, ValueError):
        await update.effective_message.reply_text("Usage: /setDCA <dca_name>* <currency>* <amount>* <price>")

async def dca_job(context: ContextTypes.DEFAULT_TYPE) -> None:
    """ Execute the dca job each selected day.

    will call be call daily
    
    """
    job = context.job
    dca_name,currency,amount,price = job.data

    response = buy_xx_amount_bitcoin(amount, currency, price)
    response = await extract_order_info(response)
    text='Order requested:\n'
    text+=f'Limit Order to buy {amount} of BTC when the price is equal to {price} {currency}' if price else f'Market Order to buy {amount} {currency} of BTC'
    await context.bot.send_message(job.chat_id, text=f"\nResponse: {response}\n\n{text}\n\nJob Name: {dca_name}")

#
#
#
async def unset_dca(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    try:
        name = context.args[0]
        if name:
            current_jobs = context.job_queue.get_jobs_by_name(name)
            if not current_jobs:
                await update.effective_message.reply_text(f'No job with the name: {name}')
            else:
                for job in current_jobs:
                    job.schedule_removal()
                await update.effective_message.reply_text(f'Removed all jobs with the name: {name}')
    except (IndexError, ValueError):
        await update.effective_message.reply_text("Usage: /unsetDCA <name>\n/listJobs will give you the jobs name")

#
#
#
async def list_job(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        current_jobs = context.job_queue.jobs()
        list_str = ""
        for job in current_jobs:
            name=job.name
            chat=job.chat_id
            data=job.data
            list_str += f'Name: {name}\nChatId: {chat}\nData: {data}'
        await update.effective_message.reply_text(f'{list_str if list_str else "No jobs scheduled"}')

# Unkown command handler
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command. Use /help to check available commands")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log the error and send a telegram message to notify the developer."""
    # Log the error before we do anything else, so we can see it even if something breaks.
    logger.error("Exception while handling an update:", exc_info=context.error)

    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb_string = "".join(tb_list)

    # Build the message with some markup and additional information about what happened.
    # You might need to add some logic to deal with messages longer than the 4096 character limit.
    update_str = update.to_dict() if isinstance(update, Update) else str(update)
    message = (
        f"An exception was raised while handling an update\n"
        f"<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}"
        "</pre>\n\n"
        f"<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n"
        f"<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n"
        f"<pre>{html.escape(tb_string)}</pre>"
    )

    # Finally, send the message
    await context.bot.send_message(
        chat_id=368708033, text=message, parse_mode=ParseMode.HTML
    )

# Running Telegram bot
def run_telegram_bot():
    application = ApplicationBuilder().token(TELEGRAM).build()

    # Adding all handlers
    application.add_handler(CommandHandler('help', telegram_help))
    application.add_handler(CommandHandler('listAccounts', telegram_listAccount))
    application.add_handler(CommandHandler('buyBTC', telegram_buy_btc))
    application.add_handler(CommandHandler('listJobs', list_job))
    application.add_handler(CommandHandler('setDCA', set_dca))
    application.add_handler(CommandHandler('unsetDCA', unset_dca))
    application.add_handler(MessageHandler(filters.COMMAND, unknown))
    # ...and the error handler
    application.add_error_handler(error_handler)
    application.run_polling(allowed_updates=Update.ALL_TYPES)
