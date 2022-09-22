from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=100,
        unique=True,
    )
    username = models.CharField(
        blank=False,
        verbose_name='Уникальный юзер',
        max_length=100,
        unique=True,
    )
    first_name = models.CharField(
        blank=False,
        verbose_name='Имя',
        max_length=50,
    )
    last_name = models.CharField(
        blank=False,
        verbose_name='Фамилия',
        max_length=50,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.email


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='user',
                             verbose_name='Подписчик')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='following',
                               verbose_name='Автор подписки')

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'author'],
                       name='unigue_subscriber')]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'{self.user} подписан на {self.author}'
