
# Подключение к удаленной базе данных PostgreSQL через DBeaver

### Задача

**_Основные данные_**
- надо достучаться с:               хоста
- посредством админа БД:            DBeaver
- к базе данных:                    pg_bd_star,
- которая развернута в контейнере   postgres
- на удаленной виртуальной машине,
- вход на которую ->                ssh <owner>@192.168.08.108
- с юзером:                         <owner>
- и паролем:                        <!27pass72>

**_Дополнительные данные_**
- В pg_db_star базе есть таблица: public.users


### Исходные данные задачи

**_Удаленный сервер_**
  - IP адрес: 192.168.08.108
  - Port SSH: 22
  - Username: <owner>
  - Password: <!27pass72>

**_Connection Settings to DB_**:
  - Host: localhost
  - Port: 5432
  - Database: pg_db_star
  - Username: <!27pass72>
  - Password: <27pass72>

 #### Решение посредством входа из терминала по SSH
 
 1. Подключение к удаленной виртуальной машине через SSH:
    <br>ssh <owner>@192.168.08.108
    <br>ввод пароля <!27pass72>  
 2. Запуск контейнера с PostgreSQL на удаленной виртуальной машине
    <br>docker run --name postgres -e POSTGRES_PASSWORD=<27pass72> -d -p 5432:5432 postgres
    <br>или так: ./restart.sh , где в файле restart.sh указаны команды:
```
#!/bin/bash
docker-compose down
docker-compose up -d
```
 1. Вход в контейнер с PostgreSQL:
```
docker exec -it postgres bash
```
 1. Подключение к базе данных pg_db_star внутри контейнера:
```
psql -U <owner> -d pg_db_star
```
 1. Выполнение SQL-запроса для вывода таблицы users:
```
SELECT * FROM users;
```
 1. Выход из БД, а затем из контейнера:
```
\q
```
```
exit
```

#### Решение посредством DBeaver

**_Шаг 1: Настройка SSH-туннеля_**
- Откройте DBeaver и откройте окно настроек подключения.
- Нажмите на кнопку "New Database Connection"
  <br> (или используйте меню "Database" -> "New Database Connection").
- В списке доступных баз данных выберите "PostgreSQL" и нажмите "Next".
- введите следующие параметры подключения:
```
Host:       localhost (SSH-туннель для перенаправления трафика)
Port:       5432
Database:   pg_db_star
Username:   <owner>
Password:   <27pass72>
```
- Перейдите на вкладку "SSH" и включите опцию "Use SSH tunnel".
  <br>Введите следующие параметры SSH:
```  
Host:       192.168.08.108
Port:       22
Username:   <owner>
Password:   <!27pass72>
```
- Сохраните и подключитесь:
``` 
Нажмите "Test Connection" для проверки подключения.
Если тест прошел успешно, нажмите "Finish" для сохранения подключения.
```

**_Шаг 2: Проверка подключения_**
- Проверьте подключение:
``` 
После настройки, DBeaver должен автоматически подключиться к базе данных.
Вы должны увидеть базу данных pg_db_star в левой панели DBeaver.
```
