from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import F, Q

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


class Follow(models.Model):
    """Модель подписки содержит поля:
    - user - подписчик;
    - author - автор интересующий подписчика;
    - функция __str__ переопределена.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followers',
        verbose_name=FIELDS['FOLLOWER_NAME']
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='authors',
        verbose_name=FIELDS['AUTHOR_NAME'],
        null=True
    )

    class Meta:
        ordering = ('-author',)
        verbose_name = FIELDS['FOLLOWER_NAME']
        verbose_name_plural = FIELDS['FOLLOWERS_NAME']
        constraints = [
            models.CheckConstraint(check=~Q(user=F('author')),
                                   name='disable_self-folowing'),
            models.UniqueConstraint(fields=('user', 'author'),
                                    name='unique_folowing')
        ]

    def __str__(self):
        return(f'{self.user} => {self.author}')