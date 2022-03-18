import pytz
from django.db import models


class Operator(models.Model):
    """Мобильный оператор"""
    code = models.IntegerField(
        max_length=3,
        primary_key=True,
        verbose_name="код мобильного оператора",
    )


class Tag(models.Model):
    """Тег"""
    name = models.CharField(
        max_length=30,
        primary_key=True,
        verbose_name="тег",
    )


class Maillist(models.Model):
    """Рассылка"""
    start_at = models.DateTimeField(
        null=False,
        verbose_name="начало рассылки",
    )
    message = models.TextField(
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


class Client(models.Model):
    """Клиент"""
    phone_number = models.IntegerField(
        max_length=11,
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
        null=False,
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


class Status(models.Model):
    text = models.CharField(
        max_length=20,
        primary_key=True,
        verbose_name="статус"
    )


class Message(models.Model):
    """Сообщение"""
    created_at = models.DateTimeField(
        null=False,
        verbose_name="время создания (отправки)",
    )
    status = models.ForeignKey(
        Status,
        null=False,
        on_delete=models.CASCADE,
        verbose_name="статус",
    )
    maillist = models.ForeignKey(
        Maillist,
        null=False,
        on_delete=models.CASCADE,
        verbose_name="рассылка",
    )
    client = models.ForeignKey(
        Client,
        null=False,
        on_delete=models.CASCADE,
        verbose_name="клиент",
    )
