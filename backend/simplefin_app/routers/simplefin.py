from ninja import Router
from ninja import Schema
from ninja.errors import HttpError

from simplefin_app.models import SimpleFinConnection
from simplefin_app.simplefin import claim_setup_token, SimpleFinError

router = Router()


class ConnectRequest(Schema):
    setup_token: str


@router.post("/connect")
def connect(request, payload: ConnectRequest):
    try:
        access_url = claim_setup_token(payload.setup_token)
    except SimpleFinError as e:
        raise HttpError(400, str(e))

    # Single-connection app: replace any prior connection.
    SimpleFinConnection.objects.all().delete()
    SimpleFinConnection.objects.create(access_url=access_url)

    return {"status": "connected"}


@router.get("/status")
def status(request):
    connected = SimpleFinConnection.objects.exists()
    return {"connected": connected}
