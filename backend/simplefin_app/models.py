from django.db import models


class SimpleFinConnection(models.Model):
    access_url = models.TextField()

    class Meta:
        verbose_name = "SimpleFIN Connection"


class Account(models.Model):
    """
    A financial account as returned by SimpleFIN.
    simplefin_id is SimpleFIN's stable identifier — used to avoid duplicates on re-sync.
    """

    simplefin_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    currency = models.CharField(max_length=10, default="USD")
    balance = models.DecimalField(max_digits=12, decimal_places=2)
    balance_date = models.DateTimeField()
    last_synced = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.balance} {self.currency})"


class Transaction(models.Model):
    """
    A single transaction within an account.
    amount is negative for debits, positive for credits (SimpleFIN convention).
    category is user-assigned, empty by default.
    """

    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="transactions"
    )
    simplefin_id = models.CharField(max_length=255, unique=True)
    posted = models.DateTimeField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.CharField(max_length=500)
    payee = models.CharField(max_length=255, blank=True, default="")
    memo = models.CharField(max_length=500, blank=True, default="")
    category = models.CharField(max_length=100, blank=True, default="")
    pending = models.BooleanField(default=False)

    class Meta:
        ordering = ["-posted"]

    def __str__(self):
        return f"{self.description}: {self.amount}"
