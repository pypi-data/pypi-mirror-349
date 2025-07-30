import decimal
from dataclasses import dataclass
from datetime import datetime


@dataclass
class EstimateBonds:
    ticker: str
    date: datetime
    quantityType: str
    price: decimal
    quantity: decimal = None
    amountOfMoney: decimal = None
    exchangeRate: decimal = None
    equityRate: decimal = None
    exchangeRateAmortization: decimal = None
    rateAdjustmentAmortization: decimal = None