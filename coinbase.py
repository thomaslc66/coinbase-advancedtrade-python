from coinbase_advanced_trader import coinbase_client
from coinbase_advanced_trader.coinbase_client import Side

def setCredentials(api_key, api_secret):
    return coinbase_client.set_credentials(api_key, api_secret)

def listAccounts():
    return coinbase_client.listAccount()

def buy_xx_amount_bitcoin(amount, currency="USD", price=None):
    product_id = f"BTC-{currency}"

    if price:
        order_configuration = {
            "limit_limit_gtc": {
                "base_size": str(amount),
                "limit_price": str(price)
            }
        }
    else:
        order_configuration = {
            "market_market_ioc": {
                "quote_size": str(amount),
            }
        }

    client_order_id = coinbase_client.generate_client_order_id()
    side = Side.BUY.name

    response = coinbase_client.createOrder(
        client_order_id=client_order_id,
        product_id=product_id,
        side=side,
        order_configuration=order_configuration
    )

    return response