from django.contrib.auth.models import AbstractUser
from django.db import models

from core.names import FIELDS


class User(AbstractUser):

    email = models.EmailField(
        verbose_name=FIELDS['USERS_EMAIL'],
        max_length=254,
        unique=True
    )
    first_name = models.CharField(
        verbose_name=FIELDS['USERS_FISRTNAME'],
        max_length=150
    )
    last_name = models.CharField(
        verbose_name=FIELDS['USERS_LASTNAME'],
        max_length=150
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name',)


    class Meta:
        ordering = ('username',)
        verbose_name = FIELDS['USER_NAME']
        verbose_name_plural = FIELDS['USERS_NAME']
    
    def __str__(self):
        return self.username[:20]
