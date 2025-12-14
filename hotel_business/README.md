# Система бронирования номеров в отеле "Кругосветка"


Система управления бронированием номеров в отеле с учетом
категорией номеров, дополнительных услуг и оснащения.

## Начало работы

Ниже представлено руководство по установке и настройке проекта
системы бронирования отеля. Эти инструкции помогут вам развернуть
копию проекта на локальном компьютере для целей разработки,
тестирования и ознакомления с функционалом системы.

### Необходимые условия

- Python 3.13.5 или выше
- Django 5.2 или выше
- Postgresql

```
# Установка Python
sudo apt update
sudo apt install python3.13

# Установка Django
pip install django==5.2

# Установка PostgreSQL
sudo apt install postgresql postgresql-contrib
```

### Установка

Пошаговое руководство по установке и запуску проекта

1. Клонирование репозитория
```
git clone [URL репозитория]
```

2. Активация виртуального окружения
```
# Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

3. Установите всё необходимое для работы проекта
```
pip install -r requirements.txt
```

4. Настройте базу данных
5. Примените миграции:
```
python manage.py makemigrations 
python manage.py migrate
```
6. Запуск сервера
```
python manage.py runserver
```
## Автор

* **Дарья Коробкова ☆(>ᴗ•)** - *Initial work* - [venttea(!)](https://github.com/venttea)