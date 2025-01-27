@echo off

:: create test user
curl -X POST "http://127.0.0.1:8000/api-auth/" ^
    -H "Authorization: Token 5822e9ba83420359c6af2f7765e690202cf92534" ^
    -H "Content-Type: application/json" ^
    -d "{ \"username\": \"test\", \"password\": \"test\", \"first_name\": \"test\", \"last_name\": \"test\", \"top_streak\": \"0\", \"current_streak\": \"0\" }"


:: create test2 user
curl -X POST "http://127.0.0.1:8000/api-auth/" ^
    -H "Authorization: Token 5822e9ba83420359c6af2f7765e690202cf92534" ^
    -H "Content-Type: application/json" ^
    -d "{ \"username\": \"test2\", \"password\": \"test2\", \"first_name\": \"test\", \"last_name\": \"test\", \"top_streak\": \"0\", \"current_streak\": \"0\" }"


:: create admin follow test
curl -X POST "http://127.0.0.1:8000/realationships/follow/1/2/" ^
    -H "Authorization: Token 5822e9ba83420359c6af2f7765e690202cf92534" ^
    -H "Content-Type: application/json" ^


:: create admin follow test2
curl -X POST "http://127.0.0.1:8000/realationships/follow/1/3/" ^
    -H "Authorization: Token 5822e9ba83420359c6af2f7765e690202cf92534" ^
    -H "Content-Type: application/json" ^
