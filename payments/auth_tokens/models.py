from django.db import models

from django.utils import timezone
from payments.users.models import User

from django.conf import settings
from datetime import timedelta
import binascii
import os

EXPIRING_TOKEN_DURATION = getattr(
    settings, 'EXPIRING_TOKEN_DURATION', timedelta(days=1))



class Token(models.Model):

    objects = models.Manager()

    class Meta:
        db_table = 'expiring_authtoken'

    key = models.CharField(max_length=50, primary_key=True)
    user = models.OneToOneField(User, related_name='auth_token',
                                on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expires = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()

        self.expires = timezone.now() + EXPIRING_TOKEN_DURATION
        return super(Token, self).save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(25)).decode()

    def __str__(self):
        return self.key
