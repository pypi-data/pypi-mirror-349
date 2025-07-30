import decimal
from dataclasses import dataclass
from datetime import datetime


@dataclass
class TransferBudget:
    accountNumber: str
    cuit: str
    currency: str
    cbu: str
    bankAccountNumber: str
    amount: decimal
