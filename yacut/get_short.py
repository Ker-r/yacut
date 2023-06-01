import random
import string

from .models import URLMap

def get_unique_short_id():
    symbol = string.ascii_letters + string.digits
    short_link = ''.join(random.choice(symbol) for i in range(6))
    if URLMap.query.filter_by(short=short_link).first():
        short_link = get_unique_short_id()
    return short_link
