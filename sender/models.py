import pytz
from django.core.validators import RegexValidator
from django.db import models


class Operator(models.Model):
    """Мобильный оператор"""
    error_message = "Код оператора должен быть в формате XXX," \
                    " где X - цифра от 0 до 9"
    code_validator = RegexValidator(
        regex=r"^\d{3}$",
        message=error_message,
    )
    code = models.CharField(
        max_length=3,
        validators=[code_validator],
        primary_key=True,
        verbose_name="код мобильного оператора",
    )

    def __str__(self):
        return str(self.code)


class Tag(models.Model):
    """Тег"""
    name = models.CharField(
        max_length=30,
        primary_key=True,
        verbose_name="тег",
    )

    def __str__(self):
        return self.name


class Maillist(models.Model):
    """Рассылка"""
    start_at = models.DateTimeField(
        null=False,
        verbose_name="начало рассылки",
    )
    text = models.TextField(
        null=False,
        verbose_name="сообщение",
    )
    operator_code = models.ForeignKey(
        Operator,
        null=False,
        on_delete=models.CASCADE,
        verbose_name="код мобильного оператора",
    )
    tag = models.ForeignKey(
        Tag,
        null=False,
        on_delete=models.CASCADE,
        verbose_name="тег",
    )
    finish_at = models.DateTimeField(
        null=False,
        verbose_name="окончание рассылки",
    )


class Customer(models.Model):
    """Клиент"""
    error_message = "Номер телефона должен быть в формате 7XXXXXXXXXX," \
                    " где X - цифра от 0 до 9"
    phone_validator = RegexValidator(
        regex=r"^7\d{10}$",
        message=error_message,
    )
    phone_number = models.CharField(
        max_length=11,
        validators=[phone_validator],
        null=False,
        verbose_name="номер телефона",
    )

    operator_code = models.ForeignKey(
        Operator,
        null=False,
        on_delete=models.CASCADE,
        verbose_name="код мобильного оператора",
    )
    tag = models.ForeignKey(
        Tag,
        null=True,
        on_delete=models.CASCADE,
        verbose_name="тег",
    )

    TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))

    timezone = models.CharField(
        max_length=32,
        choices=TIMEZONES,
        default="Europe/Moscow",
        verbose_name="часовой пояс",
    )


class Message(models.Model):
    """Сообщение"""
    created_at = models.DateTimeField(
        null=False,
        auto_now_add=True,
        verbose_name="время создания (отправки)",
    )
    status = models.CharField(
        max_length=20,
        null=False,
        verbose_name="статус",
    )
    maillist = models.ForeignKey(
        Maillist,
        null=False,
        on_delete=models.CASCADE,
        verbose_name="рассылка",
    )
    customer = models.ForeignKey(
        Customer,
        null=False,
        on_delete=models.CASCADE,
        verbose_name="клиент",
    )
