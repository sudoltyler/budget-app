from django.contrib import admin
from .models import SimpleFinConnection, Account, Transaction


admin.site.register(SimpleFinConnection)
admin.site.register(Account)
admin.site.register(Transaction)
