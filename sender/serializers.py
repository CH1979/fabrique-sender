from pyexpat import model
from django.test import tag
from rest_framework import serializers

from .models import Customer, Maillist, Message, Operator, Tag


class OperatorSerializer(serializers.Serializer):
    code = serializers.RegexField(regex=r"^\d{3}$")


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

    def to_internal_value(self, data):
        """
        Для кода мобильного оператора и тега делаем проверку по внешнему
        ключу и при необходимости создаем соответствующие записи.
        Для кода мобильного оператора дополнительно проводим валидацию
        содержимого.
        """
        serializer = OperatorSerializer(data={'code': data['operator_code']})
        if serializer.is_valid():
            Operator.objects.get_or_create(code=data['operator_code'])
        else:
            raise serializers.ValidationError(serializer.errors) 
        if data['tag'] != "":
            Tag.objects.get_or_create(name=data['tag'])
        return super().to_internal_value(data)


class MaillistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maillist
        fields = '__all__'
