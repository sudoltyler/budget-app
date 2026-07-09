from ninja import NinjaAPI
from simplefin_app.routers.simplefin import router as simplefin_router
from simplefin_app.routers.accounts import router as accounts_router
from simplefin_app.routers.sync import router as sync_router

api = NinjaAPI(title="Budget App API")

api.add_router("/simplefin/", simplefin_router)
api.add_router("/accounts/", accounts_router)
api.add_router("/sync/", sync_router)


@api.get("/health")
def health(request):
    return {"status": "ok"}
