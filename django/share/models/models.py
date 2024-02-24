from django.db import models
from pathlib import Path

DEFAULT_PFP_PATH = Path(__file__).parent / 'default_pfp.txt'
DEFAULT_PFP = None

with DEFAULT_PFP_PATH.open() as file:
    DEFAULT_PFP = file.read()

# Create your models here.
class User(models.Model):
    # User might not be logged in via 42 OAUTH so this can be NULL
    intra_id = models.IntegerField(unique=True, null=True)
    # Sha256 of password stored as hexadecimal, might be null if logged in via 42 OAUTH
    password = models.CharField(max_length=64)
    email = models.CharField(max_length=128, unique=True)
    username = models.CharField(max_length=16, unique=True)
    pfp = models.TextField(null=False, default=DEFAULT_PFP)
    totp_secret = models.CharField(max_length=16) # Base 32 random 80 bit string

    class Meta:
        db_table = 'User'
        # This makes the database app the 'owner' of this model
        app_label = 'database'