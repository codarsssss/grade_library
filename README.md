# Django Library Project 📚

## 📖 Описание
Django Library Project — это веб-приложение для управления библиотекой.  
Позволяет пользователям добавлять книги, просматривать их, фильтровать по жанру, автору и дате публикации, а также осуществлять поиск.

В проекте используются:
- **Django + Django REST Framework** для API
- **PostgreSQL** как база данных
- **Docker + Docker Compose** для контейнеризации
- **Makefile** для удобного управления проектом

---

## 🚀 Функционал
✅ **CRUD** для книг, авторов и жанров  
✅ **REST API** для управления библиотекой  
✅ **Поиск и фильтрация** книг по автору, жанру и дате публикации  
✅ **Docker + PostgreSQL** для удобного развертывания  
✅ **Makefile** для автоматизации команд
✅ **Админ-панель Django**  

---

## ⚙️ Установка и запуск проекта

### 1️⃣ Клонируйте репозиторий:
```bash
git git@github.com:codarsssss/grade_library.git
cd grade_library
```

### 2️⃣ Создайте `.env` файл:
Скопируйте `.env.example` в `.env`:
```bash
cp .env.example .env
```
Пример `.env` файла:
```ini
PROJECT_NAME=library
DEBUG=True
DB_HOST=db
DB_PORT=5432
POSTGRES_USER=myuser
POSTGRES_PASSWORD=mypassword
POSTGRES_DB=mydatabase
SECRET_KEY=your-secret-key
EXTERNAL_PORT=8000
EXTERNAL_DB_PORT=5432
```

### 3️⃣ Запустите контейнеры Docker:
```bash
make up
```

### 4️⃣ Создайте суперпользователя (если требуется):
Если вам нужен доступ в Django Admin, создайте суперпользователя:
```bash
make createsuperuser
```

### 5️⃣ Откройте приложение в браузере:
```
http://localhost:8000
```

---

## 🛠 Управление проектом с помощью Makefile

| Команда               | Описание                                      |
|-----------------------|----------------------------------------------|
| `make up`            | Запуск контейнеров в фоновом режиме          |
| `make up-logs`       | Запуск контейнеров с выводом логов           |
| `make down`          | Остановка контейнеров                        |
| `make restart`       | Перезапуск контейнеров                       |
| `make migrations`    | Создание миграций                            |
| `make migrate`       | Применение миграций                          |
| `make createsuperuser` | Создание суперпользователя                 |
| `make startapp app=books` | Создание нового Django-приложения        |
| `make shell`         | Открытие Django shell                        |
| `make container-shell` | Вход в контейнер через `sh`                |
| `make logs`          | Просмотр логов контейнера                    |
| `make collectstatic` | Сборка статических файлов                     |
| `make clean`         | Полная очистка контейнеров, образов и томов |

---

## 🛡 Технологии и инструменты

- **Django** — веб-фреймворк
- **Django REST Framework** — API
- **PostgreSQL** — база данных
- **Docker & Docker Compose** — контейнеризация
- **Gunicorn** — WSGI-сервер
- **Makefile** — автоматизация команд

## В админ-панели реализован импорт CSV