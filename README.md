# Запуск

Через Docker:
1. Клонируем проект
```
git clone https://github.com/sidikayfuy/friends_django
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
git clone https://github.com/sidikayfuy/friends_django
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

1. Регистрация 
![reg_request.png](https://sun9-69.userapi.com/impg/0Ahs2I-lH0N7m3XdIsjDyx8yToB4IpvJvuv_nQ/dTnlbxWOgyw.jpg?size=868x575&quality=96&sign=603f1320056a67fcfe4d766f49b4fa89&type=album)

   
2. Решено было сделать аутентификацию по Username для ограничения доступа к некоторым данным, поэтому все остальные запросы (кроме регистрационного), требуют авторизацию - наличие в headers заголовка с именем X-USERNAME и значением username зарегистрированного пользователя.
![auth_request.png](https://sun9-47.userapi.com/impg/DnMwPJk9h0VRHCKLH6o6BVCl2srDtrBo1qlayA/BCY5tNCbyTI.jpg?size=878x584&quality=96&sign=32bc90155c57c13a83ab2ba0d38d610b&type=album)
В Swagger можно авторизоваться через специальную форму
![auth_request_2.png](https://sun9-38.userapi.com/impg/tI_ZkzypDj24gppDmDHbr42fFGGn7ifKwoQISA/b-HNrppXjSU.jpg?size=1669x584&quality=96&sign=f5ca2e6adb639c643edb84f57506fa16&type=album)


3. Во всех запросах (кроме регистрации, получения информации о пользователе по id, получения списка друзей пользователя по id) доступны лишь данные которые принадлежат авторизированному пользователю. Таким образом авторизированный пользователь может смотреть только свои запросы, отправлять запросы где отправителем является только он, отвечать на запросы которые адресованы только ему и др.
4. Воспроизведем ситуацию:
    1) Зарегистрируем 6 пользователей c разными username для примера у каждого будет порядковый номер от 1 до 6
   
        ```POST(http://localhost:8000/api/v1/users), body: raw JSON({"username":"1(у каждого своё)"})```
   2) Пользователь №1 (авторизировавшись) оправляет запросы пользователю 2, 4, 5, 6.
       ```POST(http://localhost:8000/api/v1/friendRequests/1/2), headers: X-USERNAME: 1```
       ```POST(http://localhost:8000/api/v1/friendRequests/1/4), headers: X-USERNAME: 1```
       ```POST(http://localhost:8000/api/v1/friendRequests/1/5), headers: X-USERNAME: 1```
       ```POST(http://localhost:8000/api/v1/friendRequests/1/6), headers: X-USERNAME: 1```
   
       Пользователь №2 не отвечает
   
       Пользователь №4 (авторизировавшись) принимает
   
       ```POST(http://localhost:8000/api/v1/friendRequests/response/2/1), headers: X-USERNAME: 4```
       
       Пользователь №5 (авторизировавшись) отправляет запроса Пользователю №1 для проверки авто-добавления
   
       ```POST(http://localhost:8000/api/v1/friendRequests/5/1), headers: X-USERNAME: 5```
      
       Пользователь №6 (авторизировавшись) отклоняет
   
       ```POST(http://localhost:8000/api/v1/friendRequests/response/4/0), headers: X-USERNAME: 6```

   3) Пользователь №3 (авторизировавшись) отправляет запрос пользователю 1 (не отвечает)
   
       ```POST(http://localhost:8000/api/v1/friendRequests/3/1), headers: X-USERNAME: 3```
   4) После мы должны получить что Пользователь №1 имеет:
      1) Исходящий запрос Пользователю №2
      ```GET(http://localhost:8000/api/v1/users/friendStatus/1/2), headers: X-USERNAME: 1```
      
          ![request1.png](https://sun9-76.userapi.com/impg/c9WX9aFfINVjTrJlKP0SZM1O2FD9wajau2zSXw/fn2Cku5uH3M.jpg?size=866x704&quality=96&sign=50f5ea7447088f8005a93c44318033b7&type=album)
      
      2) Входящий запрос от Пользователя №3
      ```GET(http://localhost:8000/api/v1/users/friendStatus/1/3), headers: X-USERNAME: 1```
      
          ![request2.png](https://sun9-63.userapi.com/impg/kG95-v2dHsCpWlnYq83Nv0mGiFHupeKoWF0XxA/gmHlbxx_neM.jpg?size=868x668&quality=96&sign=1f0d77421c01ecb3f8135e5e53286d93&type=album)

         Или за один запрос
   
         ```GET(http://localhost:8000/api/v1/users/1/listOfFriendRequests), headers: X-USERNAME: 1```
      
          ![requests.png](https://sun9-23.userapi.com/impg/GTVPli-aNuH8C4TyFvU8n3D41hQBS_pp804o1w/kR3Jsu3km5Y.jpg?size=870x779&quality=96&sign=d2addfc76045071db62c3a81401b89b5&type=album)
      3) Друзей: Пользователя №4, Пользователя №5
      ```GET(http://localhost:8000/api/v1/users/friendStatus/1/4), headers: X-USERNAME: 1```
      
          ![friend1.png](https://sun9-77.userapi.com/impg/mZT9EayQ-ZE_vOqlyrX2tuiSJAoLHzVofHOH9Q/H716vVTsXZI.jpg?size=862x668&quality=96&sign=87fb18d1531839edfb5ab1511c6a6920&type=album)
      ```GET(http://localhost:8000/api/v1/users/friendStatus/1/5), headers: X-USERNAME: 1```
      
          ![friend2.png](https://sun9-64.userapi.com/impg/iK-nOGNiR5besD-CdOkt-RuSrrorsG1s81iEIA/6gv1kTbrnZk.jpg?size=870x684&quality=96&sign=5485f686c58e03c4b9684c65fd52da59&type=album)

         Или за один запрос
      
         ```GET(http://localhost:8000/api/v1/users/1/listOfFriends), headers: X-USERNAME: 1```
      ![friends.png](https://sun9-39.userapi.com/impg/pmWKV4F7BSQ_lhyA2nVTBo_IY8_mNGFdkYdtNg/geK_1GG8Ono.jpg?size=865x790&quality=96&sign=c4400fc83803284935770a9ba9949f4f&type=album)
      4) Никакой связи с Пользователем №6
      ```GET(http://localhost:8000/api/v1/users/friendStatus/1/6), headers: X-USERNAME: 1```
      
          ![status_nothing.png](https://sun9-62.userapi.com/impg/38NmHUr17CrvXbcyhzzsWeX7zd_oll7ZSczlKA/Or5r_BNXr-Y.jpg?size=876x645&quality=96&sign=df5e99af601d73fbef5eeae28fcdf0ff&type=album)
   5) Пользователь №1 удаляет из друзей Пользвоателя №5
   
      ```DELETE(http://localhost:8000/api/v1/users/1/relation/5), headers: X-USERNAME: 1```
      
      После этого дружественной связи с ним нет.
   
      ```GET(http://localhost:8000/api/v1/users/friendStatus/1/5), headers: X-USERNAME: 1```
      ![delete_friend.png](https://sun9-77.userapi.com/impg/3MSTd4mxB3NvlC8ga-ETJPpO1jVMEg8xEV2HCw/qvEdfGZTry0.jpg?size=850x665&quality=96&sign=8c732f3e0c7a07ba89901ce06cb7de35&type=album)
