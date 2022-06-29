# Fabrique sender
### Тестовое задание на вакансию Python developer для ООО "Фабрика решений"
---
Для запуска
* Клонировать репозиторий командой:

`git clone https://github.com/CH1979/fabrique-sender`
* Сoздать в директории с репозиторием файлы:

`django_secret_key.txt`

`probe_server_url.txt`

`probe_server_token.txt`

cодержащие соответственно secret key для django, url внешнего сервиса и jwt-токен для доступа к внешнему сервису.
* Запустить сервис docker-контейнеры командой:
`docker-compose up -d --build`

API будет доступно по адресу: http://127.0.0.1:1337/api/v1/

Документация API: http://127.0.0.1:1337/docs/

Мониторинг задач Celery (Flower) по адресу: http://127.0.0.1:5555/
