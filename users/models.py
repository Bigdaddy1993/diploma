from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    avatar = models.ImageField(upload_to='users/', verbose_name='изображение', **NULLABLE)
    phone = models.CharField(unique=True, max_length=35, verbose_name='телефон')
    comment = models.CharField(verbose_name='комментарий', help_text='Опишите чем вы занимаетесь', **NULLABLE)
    payment = models.OneToOneField('Payment', on_delete=models.CASCADE, verbose_name="подписка", **NULLABLE)
    owner = models.BooleanField(verbose_name='владелец', **NULLABLE)
    is_superuser = models.BooleanField(verbose_name='админ', default=False)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"

    def __str__(self):
        return f'{self.phone}'


class Payment(models.Model):
    date = models.DateTimeField(auto_now=True, verbose_name="дата оплаты")
    session_id = models.CharField(max_length=255, verbose_name="id сессии", **NULLABLE)
    link = models.URLField(max_length=400, verbose_name="ссылка на оплату", **NULLABLE)

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"

    def __str__(self):
        return self.link
