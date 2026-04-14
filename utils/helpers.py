import datetime
import random


def generate_order_id():
    now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    rand = random.randint(100, 999)
    return f"ORD{now}{rand}"


def format_price(value):
    try:
        return int(str(value).replace(",", ""))
    except:
        return 0


def safe_get(data, key, default=""):
    return data.get(key, default)