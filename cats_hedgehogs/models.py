from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator


class User(AbstractUser):
    first_name = None
    last_name = None
    date_joined = None

    balance = models.IntegerField(default=0)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []


class Pet(models.Model):
    PET_TYPES = [('ct', 'Cat'), ('hh', 'Hedgehog'), ]

    pet_type = models.CharField(choices=PET_TYPES, max_length=2)
    breed = models.CharField(max_length=255)
    callsign = models.CharField(max_length=255)
    owner = models.ForeignKey(User, models.CASCADE)

    def __str__(self):
        return '%s (%s) of %s' % (self.pet_type, self.callsign, self.owner.username)


class Lot(models.Model):
    owner = models.ForeignKey(User, models.CASCADE, related_name='lots')
    start_price = models.IntegerField(validators=[MinValueValidator(0)])
    pet = models.ForeignKey(Pet, models.CASCADE)

    @property
    def finished(self):
        return self.bids.filter(accepted=True).exists()


class Bid(models.Model):
    value = models.IntegerField()
    owner = models.ForeignKey(User, models.CASCADE, related_name='bids')
    lot = models.ForeignKey(Lot, models.CASCADE, related_name='bids')
    accepted = models.BooleanField(default=False)

