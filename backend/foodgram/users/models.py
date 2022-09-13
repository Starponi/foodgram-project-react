from django.contrib.auth.models import AbstractUser
from django.db import models


class MyUser(AbstractUser):
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=100,
        unique=True,
    )
    username = models.CharField(
        verbose_name='Уникальный юзер',
        max_length=100,
        unique=True,
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=50,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=50,
    )
    password = models.CharField(
        verbose_name='Пароль',
        max_length=255,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.email


class Follow(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE,
                             related_name='Подписчик',
                             verbose_name='Подписчик')
    following = models.ForeignKey(MyUser, on_delete=models.CASCADE,
                                  related_name='following',
                                  verbose_name='Автор подписки')

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'following'],
                       name='unique_following')]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
    
    def __str___(self):
        return f'{self.user} {self.following}'
