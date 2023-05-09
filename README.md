# Запуск

Через Docker:
1. Клонируем проект
```
git clone
```
Или скачиваем данный репозиторий
2. Переходим в папку с проектом
3. Запускаем с помощью Docker
```
docker run -dp 8000:8000 -it $(docker build -q .)
```

Не через Docker:
1. Клонируем проект
```
git clone
```
Или скачиваем данный репозиторий
2. Переходим в папку с проектом
3. Создаем виртуальное окржуение
```
python3 -m venv venv
```
4. Активируем его
    
Windows
```
.\venv\Scripts\activate 
```
Linux
```
source .\venv\Scripts\activate 
```

5. Устанавливаем зависимости
```
pip install -r requrements.txt
```
6. Выполняем миграции
```
python3 manage.py migrate
```
7. Запускаем проект
```
python3 manage.py runserver --insecure
```

# Swagger

После успешного запуска по маршруту http://localhost:8000/docs/ будет доступен Swagger UI с его помощью можно протестировать разработанный сервис, основанный на спецификации расположенной: **/static/api.yaml**.

# Тесты
После успешного запуска в терминале контейнера можно запусить тесты командой:
```
python3 manage.py test
```
Файл с тестами: **/friends/tests.py**

# Примеры использования
