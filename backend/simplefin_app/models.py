from django.db import models


class SimpleFinConnection(models.Model):
    """
    Stores the permanent SimpleFIN access URL after a setup token has been claimed.
    The access URL contains embedded Basic Auth credentials, e.g.
    https://user:pass@bridge.simplefin.org/simplefin

    Treat this like a password — don't expose it to the frontend, don't log it.
    """

    access_url = models.TextField()

    class Meta:
        # Only ever one connection row in a single-user app.
        # If you add multi-user auth later, add a OneToOneField to User here.
        verbose_name = "SimpleFIN Connection"
