from enum import Enum
from datetime import datetime
import uuid
import json
from coinbase_advanced_trader.cb_auth import CBAuth
from coinbase_advanced_trader.config import API_KEY, API_SECRET, API_PATH

class Side(Enum):
    BUY = 1
    SELL = 0


class Method(Enum):
    POST = "POST"
    GET = "GET"


def generate_client_order_id():
    return str(uuid.uuid4())


cb_auth = CBAuth(API_KEY, API_SECRET)

def set_credentials(api_key, api_secret):
    global cb_auth
    cb_auth = CBAuth(api_key, api_secret)


def listAccounts(limit=49, cursor=None):
    return cb_auth(Method.GET.value, f'{API_PATH}/accounts', params={'limit': limit, 'cursor': cursor})

def listAccount():
    return cb_auth(Method.GET.value, f'{API_PATH}/accounts')

def getAccount(account_uuid):
    return cb_auth(Method.GET.value, f'{API_PATH}/accounts/{account_uuid}')


def createOrder(client_order_id, product_id, side, order_configuration):
    body = json.dumps({
        "client_order_id": client_order_id,
        "product_id": product_id,
        "side": side,
        "order_configuration": order_configuration
    })
    return cb_auth(Method.POST.value, f'{API_PATH}/orders', body)


def cancelOrders(order_ids):
    body = json.dumps({"order_ids": order_ids})
    return cb_auth(Method.POST.value, f'{API_PATH}/orders/batch_cancel', body)


def listOrders(**kwargs):
    return cb_auth(Method.GET.value, f'{API_PATH}/orders/historical/batch', params=kwargs)


def listFills(**kwargs):
    return cb_auth(Method.GET.value, f'{API_PATH}/orders/historical/fills', params=kwargs)


def getOrder(order_id):
    return cb_auth(Method.GET.value, f'{API_PATH}/orders/historical/{order_id}')


def listProducts(**kwargs):
    return cb_auth(Method.GET.value, f'{API_PATH}/products', params=kwargs)


def getProduct(product_id):
    return cb_auth(Method.GET.value, f'{API_PATH}/products/{product_id}')


def getProductCandles(product_id, start, end, granularity):
    params = {
        'start': start,
        'end': end,
        'granularity': granularity
    }
    return cb_auth(Method.GET.value, f'{API_PATH}/products/{product_id}/candles', params=params)


def getMarketTrades(product_id, limit):
    return cb_auth(Method.GET.value, f'{API_PATH}/products/{product_id}/ticker', params={'limit': limit})


def getTransactionsSummary(start_date, end_date, user_native_currency='USD', product_type='SPOT'):
    params = {
        'start_date': start_date.strftime('%Y-%m-%dT%H:%M:%SZ'),
        'end_date': end_date.strftime('%Y-%m-%dT%H:%M:%SZ'),
        'user_native_currency': user_native_currency,
        'product_type': product_type
    }
    return cb_auth(Method.GET.value, f'{API_PATH}/transaction_summary', params=params)
