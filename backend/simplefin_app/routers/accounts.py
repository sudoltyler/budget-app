from ninja import Router
from ninja.errors import HttpError

from simplefin_app.models import SimpleFinConnection
from simplefin_app.simplefin import fetch_accounts, SimpleFinError

router = Router()


@router.get("/")
def list_accounts(request):
    connection = SimpleFinConnection.objects.first()
    if not connection:
        raise HttpError(400, "No SimpleFIN connection configured yet")

    try:
        data = fetch_accounts(connection.access_url)
    except SimpleFinError as e:
        raise HttpError(502, str(e))

    return data
