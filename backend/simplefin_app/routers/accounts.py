from ninja import Router
from ninja.errors import HttpError
from ninja import Schema
from datetime import datetime
from decimal import Decimal

from simplefin_app.models import Account

router = Router()


class TransactionOut(Schema):
    id: int
    simplefin_id: str
    posted: datetime
    amount: Decimal
    description: str
    payee: str
    memo: str
    category: str
    pending: bool


class AccountOut(Schema):
    id: int
    simplefin_id: str
    name: str
    currency: str
    balance: Decimal
    balance_date: datetime
    last_synced: datetime
    transactions: list[TransactionOut]


@router.get("/", response=list[AccountOut])
def list_accounts(request):
    accounts = Account.objects.prefetch_related("transactions").all()
    if not accounts.exists():
        raise HttpError(404, "No accounts found — try syncing first")
    return accounts
