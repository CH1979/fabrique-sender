import pytest
from django.test import Client
from rest_framework.reverse import reverse

from sender.models import Operator, Tag


@pytest.mark.django_db
class TestCustomer:
    """
    Тесты корректности работы API по эндпойнту 'customer-list'
    """
    url = reverse('customer-list')
    client = Client()

    def test_create_customer_success_1(self):
        """Тест успешного создания нового клиента с заданным полем 'tag' """
        data = {
            "phone_number": "79261234567",
            "timezone": "Europe/Moscow",
            "operator_code": "926",
            "tag": "tag_1"
        }

        response = self.client.post(
            self.url,
            data
        )
        data['id'] = 1
        assert response.status_code == 201
        assert response.json() == data

    def test_create_customer_success_2(self):
        """Тест успешного создания нового клиента с пустым полем 'tag' """
        data = {
            "phone_number": "79261234567",
            "timezone": "Europe/Moscow",
            "operator_code": "926",
            "tag": ""
        }

        response = self.client.post(
            self.url,
            data
        )
        data['id'] = 1
        data['tag'] = None

        assert response.status_code == 201
        assert response.json() == data
        assert len(Tag.objects.all()) == 0

    def test_create_customer_failure_1(self):
        """
        Тест отклоненной попытки создания нового клиента
        с пропущенным значение в поле 'operator_code'
        """
        response = self.client.post(
            self.url,
            {
                "phone_number": "79281234567",
                "timezone": "Europe/Moscow",
                "operator_code": "",
                "tag": "tag_1",
            }
        )
        assert response.status_code == 400

    def test_create_customer_failure_2(self):
        """
        Тест отклоненной попытки создания нового клиента
        с некорректным значением в поле 'operator_code'
        """
        response = self.client.post(
            self.url,
            {
                "phone_number": "79281234567",
                "timezone": "Europe/Moscow",
                "operator_code": "aaa",
                "tag": "tag_1",
            }
        )
        assert len(Operator.objects.filter(code__exact="aaa")) == 0
        assert response.status_code == 400

    def test_create_customer_failure_3(self):
        """
        Тест отклоненной попытки создания нового клиента
        с некорректным значением в поле 'phone_number'
        (мало цифр)
        """
        response = self.client.post(
            self.url,
            {
                "phone_number": "7928123456",
                "timezone": "Europe/Moscow",
                "operator_code": "928",
                "tag": "tag_1",
            }
        )
        assert response.status_code == 400

    def test_create_customer_failure_4(self):
        """
        Тест отклоненной попытки создания нового клиента
        с некорректным значением в поле 'phone_number'
        (много цифр)
        """
        response = self.client.post(
            self.url,
            {
                "phone_number": "792812345678",
                "timezone": "Europe/Moscow",
                "operator_code": "928",
                "tag": "tag_1",
            }
        )
        assert response.status_code == 400

    def test_create_customer_failure_5(self):
        """
        Тест отклоненной попытки создания нового клиента
        с некорректным значением в поле 'phone_number'
        (начинается не с 7)
        """
        response = self.client.post(
            self.url,
            {
                "phone_number": "38928123456",
                "timezone": "Europe/Moscow",
                "operator_code": "928",
                "tag": "tag_1",
            }
        )
        assert response.status_code == 400
