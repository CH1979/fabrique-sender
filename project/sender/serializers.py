from itertools import count
from django.forms import ValidationError
from django.utils import timezone
from rest_framework import serializers

from .models import Customer, Maillist, Message, Operator, Tag


class OperatorSerializer(serializers.Serializer):
    code = serializers.RegexField(regex=r"^\d{3}$")


def get_or_create_code_and_tag(data):
    """
    Для кода мобильного оператора и тега делаем проверку по внешнему
    ключу и при необходимости создаем соответствующие записи.
    Для кода мобильного оператора дополнительно проводим валидацию
    содержимого.
    """
    if "operator_code" in data:
        serializer = OperatorSerializer(
            data={"code": data.get("operator_code", None)}
        )
        if serializer.is_valid():
            Operator.objects.get_or_create(code=data["operator_code"])
        else:
            raise serializers.ValidationError(serializer.errors)
    if "tag" in data:
        if data["tag"] != "":
            Tag.objects.get_or_create(name=data["tag"])
    return data


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["name"]


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"

    def to_internal_value(self, data):
        data = get_or_create_code_and_tag(data)
        return super().to_internal_value(data)


class MaillistSerializer(serializers.ModelSerializer):
    messages = serializers.StringRelatedField(many=True)

    class Meta:
        model = Maillist
        fields = (
            "id",
            "start_at",
            "text",
            "finish_at",
            "operator_code",
            "tag",
            "messages",
        )

    def validate(self, attrs):
        """
        Дополнительная валидация времени начала и окончания рассылки
        """
        if ("finish_at" in attrs) and ("start_at" in attrs):
            if attrs["finish_at"] <= attrs["start_at"]:
                raise ValidationError(
                    "Время окончания рассылки "
                    "должно быть больше времени начала"
                )
        if "finish_at" in attrs:
            if attrs["finish_at"] <= timezone.now():
                raise ValidationError(
                    "Время окончания рассылки "
                    "должно быть больше текущего времени"
                )
        return super().validate(attrs)

    def to_internal_value(self, data):
        data = get_or_create_code_and_tag(data)
        return super().to_internal_value(data)


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"


class MaillistListSerializer(serializers.ModelSerializer):
    status_failed = serializers.ReadOnlyField()
    status_pending = serializers.ReadOnlyField()
    status_success = serializers.ReadOnlyField()
    class Meta:
        model = Maillist
        fields = (
            'id',
            'start_at',
            'finish_at',
            'operator_code',
            'tag',
            'status_failed',
            'status_pending',
            'status_success'
        )
