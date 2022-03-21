from datetime import timedelta

import pytest
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework.reverse import reverse

from sender.models import Operator, Tag


@pytest.mark.django_db
class TestCustomer:
    """
    Тесты корректности работы API по эндпойнту 'customer-list'
    """
    url = reverse('customer-list')
    client = APIClient()

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

    def test_update_customer(self):
        """Тест обновления атрибутов клиента"""
        # Создаем клиента
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
        # Проверяем успешность создания
        data["id"] = 1
        assert response.status_code == 201
        assert response.json() == data
        
        # Проверяем метод PUT/update
        url = f"{self.url}1/"
        response = self.client.put(
            url,
            {
                "phone_number": "79260000000",
                "timezone": "UTC",
                "operator_code": "926",
                "tag": "tag_2"
            }
        )
        assert response.status_code == 200

        # Проверяем метод PATCH/partial_update
        response = self.client.patch(
            url,
            {"tag": "tag_3"}
        )
        assert response.status_code == 200

    def test_delete_customer_success(self):
        """Тест удаления клиента"""
        # Создаем клиента
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
        # Проверяем успешность создания
        data["id"] = 1
        assert response.status_code == 201
        assert response.json() == data

        url = f"{self.url}1/"
        # Проверяем удаление
        response = self.client.delete(url)
        assert response.status_code == 204


@pytest.mark.django_db
class TestMaillist:
    """
    Тесты корректности работы API по эндпойнту 'maillist-list'
    """
    url = reverse("maillist-list")
    client = APIClient()

    def test_create_maillist_success_1(self):
        """Тест успешного создания рассылки"""
        data = {
            "start_at": timezone.now(),
            "text": "Hello!",
            "operator_code": "926",
            "tag": "tag_1",
            "finish_at": timezone.now() + timedelta(minutes=5),
        }
        response = self.client.post(
            self.url,
            data
        )

        assert response.status_code == 201

    def test_create_maillist_failure_1(self):
        """Тест валидации времени (начало позже окочания)"""
        data = {
            "start_at": timezone.now() + timedelta(minutes=10),
            "text": "Hello!",
            "operator_code": "926",
            "tag": "tag_1",
            "finish_at": timezone.now() + timedelta(minutes=5),
        }
        response = self.client.post(
            self.url,
            data
        )

        assert response.status_code == 400

    def test_create_maillist_failure_2(self):
        """Тест валидации времени (окочание в прошлом)"""
        data = {
            "start_at": timezone.now() - timedelta(minutes=10),
            "text": "Hello!",
            "operator_code": "926",
            "tag": "tag_1",
            "finish_at": timezone.now() - timedelta(minutes=5),
        }
        response = self.client.post(
            self.url,
            data
        )

        assert response.status_code == 400

    def test_update_maillist(self):
        # Создаем новую рассылку
        data = {
            "start_at": timezone.now(),
            "text": "Hello!",
            "operator_code": "926",
            "tag": "tag_1",
            "finish_at": timezone.now() + timedelta(minutes=5),
        }
        response = self.client.post(
            self.url,
            data
        )
        assert response.status_code == 201
        
        # Проверяем метод PUT/update
        data["finish_at"] = timezone.now() + timedelta(minutes=5)
        url = f"{self.url}1/"
        response = self.client.put(
            url,
            data
        )
        assert response.status_code == 200
        
        # Проверяем метод PATCH/partial_update
        response = self.client.patch(
            url,
            {"tag": "tag_2"}
        )
        assert response.status_code == 200

    def test_delete_maillist(self):
        # Создаем новую рассылку
        data = {
            "start_at": timezone.now(),
            "text": "Hello!",
            "operator_code": "926",
            "tag": "tag_1",
            "finish_at": timezone.now() + timedelta(minutes=5),
        }
        response = self.client.post(
            self.url,
            data
        )
        assert response.status_code == 201
        
        # Удаляем
        url = f"{self.url}1/"
        response = self.client.delete(
            url
        )
        assert response.status_code == 204
