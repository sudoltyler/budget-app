from datetime import datetime, timedelta, timezone
from ninja import Router
from ninja.errors import HttpError

from simplefin_app.models import SimpleFinConnection, Account, Transaction
from simplefin_app.simplefin import fetch_accounts, SimpleFinError

router = Router()


@router.post("/")
def sync(request):
    connection = SimpleFinConnection.objects.first()
    if not connection:
        raise HttpError(400, "No SimpleFIN connection configured yet")

    # Only fetch transactions from the last 90 days
    start_date = int((datetime.now(timezone.utc) - timedelta(days=90)).timestamp())

    try:
        data = fetch_accounts(connection.access_url, start_date=start_date)
    except SimpleFinError as e:
        raise HttpError(502, str(e))

    accounts_synced = 0
    transactions_synced = 0

    for acct in data.get("accounts", []):
        # update_or_create uses simplefin_id to find existing rows,
        # then updates the fields in defaults — this is the upsert pattern.
        account, _ = Account.objects.update_or_create(
            simplefin_id=acct["id"],
            defaults={
                "name": acct["name"],
                "currency": acct.get("currency", "USD"),
                "balance": acct["balance"],
                "balance_date": datetime.fromtimestamp(
                    acct["balance-date"], tz=timezone.utc
                ),
            },
        )
        accounts_synced += 1

        for tx in acct.get("transactions", []):
            Transaction.objects.update_or_create(
                simplefin_id=tx["id"],
                defaults={
                    "account": account,
                    "posted": datetime.fromtimestamp(tx["posted"], tz=timezone.utc),
                    "amount": tx["amount"],
                    "description": tx.get("description", ""),
                    "payee": tx.get("payee", ""),
                    "memo": tx.get("memo", ""),
                    "pending": tx.get("pending", False),
                },
            )
            transactions_synced += 1

    return {
        "accounts_synced": accounts_synced,
        "transactions_synced": transactions_synced,
    }
