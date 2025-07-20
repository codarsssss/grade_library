# Django Library Project 📚

## 📖 Описание

**Django Library Project** — это веб-приложение для управления библиотекой.  
Позволяет пользователям добавлять книги, просматривать их, фильтровать по жанру, автору и дате публикации, а также осуществлять поиск.

В проекте используются:

- **Django + Django REST Framework** — для API и веб-интерфейса  
- **PostgreSQL** — в качестве СУБД  
- **Docker + Docker Compose** — для контейнеризации  
- **Makefile** — для удобного управления проектом  
- **Silk** — мониторинг SQL-запросов и производительности  
- **Pillow** — обработка изображений  
- **Black + isort + flake8** — поддержка кода в едином стиле  

---

## 🚀 Функционал

✅ CRUD для книг, авторов и жанров  
✅ REST API  
✅ Поиск и фильтрация книг по автору, жанру и дате  
✅ Загрузка и ресайз обложек книг  
✅ Импорт книг из CSV в админке  
✅ UI для просмотра каталога книг  
✅ Страницы авторов и жанров  
✅ Поддержка AJAX и динамической фильтрации  
✅ Мониторинг медленных SQL-запросов через Silk  
✅ Логирование всех запросов и действий  

---

## ⚙️ Установка и запуск проекта

### 1️⃣ Клонируйте репозиторий

```bash
git clone git@github.com:codarsssss/grade_library.git
cd grade_library
```

### 2️⃣ Создайте `.env` файл

```bash
cp .env.example .env
```

Пример содержимого:

```env
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

### 3️⃣ Запустите контейнеры

```bash
make up
```

### 4️⃣ Примените миграции и создайте суперпользователя

```bash
make migrate
make createsuperuser
```

### 5️⃣ Откройте приложение

```
http://localhost:8000/
```

---

## 🛠 Управление проектом через Makefile

| Команда               | Описание                                      |
|-----------------------|----------------------------------------------|
| `make up`            | Запуск контейнеров (в фоне)                   |
| `make up-logs`       | Запуск контейнеров с логами                   |
| `make down`          | Остановка контейнеров                         |
| `make restart`       | Перезапуск                                   |
| `make migrations`    | Создание миграций                             |
| `make migrate`       | Применение миграций                           |
| `make createsuperuser` | Создание суперпользователя                  |
| `make shell`         | Django shell                                 |
| `make container-shell` | Терминал в контейнере                       |
| `make logs`          | Логи веб-приложения                           |
| `make collectstatic` | Сборка статики                                |
| `make clean`         | Очистка (volumes, images, orphans)            |
| `make style`         | Форматирование и линтинг                      |
| `make format`        | Black + isort                                 |
| `make lint`          | flake8                                        |

---

## 🛡 Дополнительно

- 📂 **Импорт CSV** — доступен через Django Admin (`/admin/import_csv/`)
- 📊 **Silk-панель мониторинга** — доступна по адресу `/silk/`
- 🖼 **Обложки книг** автоматически ресайзятся при загрузке
- ⚙️ Все ключевые модули покрыты логированием
