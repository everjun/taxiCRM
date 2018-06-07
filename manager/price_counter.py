from .models import PriceRule
from decimal import *

getcontext().prec=2


class PriceCounter:

    def count_price(self, path):
        try:
            pr = PriceRule.objects.last()
            return Decimal(path).quantize(Decimal('.01'), rounding=ROUND_DOWN)*pr.price_for_km + pr.price_for_sit
        except:
            return None