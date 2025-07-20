DOCKER_COMPOSE = docker compose
WEB_SERVICE = web

.PHONY: up up-logs build down restart migrate migrations createsuperuser startapp shell logs test collectstatic clean

# Поднять контейнеры в фоновом режиме
up:
	$(DOCKER_COMPOSE) up -d --build

# Поднять контейнеры с логами (foreground)
up-logs:
	$(DOCKER_COMPOSE) up --build

# Остановить контейнеры
down:
	$(DOCKER_COMPOSE) down

# Перезапуск контейнеров
restart: down up

# Создать миграции
migrations:
	$(DOCKER_COMPOSE) exec $(WEB_SERVICE) python manage.py makemigrations

# Применить миграции
migrate:
	$(DOCKER_COMPOSE) exec $(WEB_SERVICE) python manage.py migrate

# Создать суперпользователя
createsuperuser:
	$(DOCKER_COMPOSE) exec $(WEB_SERVICE) python manage.py createsuperuser

# Создать новое приложение, указав переменную app (например: make app=books startapp)
startapp:
	$(DOCKER_COMPOSE) exec $(WEB_SERVICE) python manage.py startapp $(app)

# Войти в Django shell
shell:
	$(DOCKER_COMPOSE) exec $(WEB_SERVICE) python manage.py shell

# Войти в контейнер через sh
container-shell:
	$(DOCKER_COMPOSE) exec $(WEB_SERVICE) sh

# Посмотреть логи контейнеров
logs:
	$(DOCKER_COMPOSE) logs -f $(WEB_SERVICE)

# Собрать статику
collectstatic:
	$(DOCKER_COMPOSE) exec $(WEB_SERVICE) python manage.py collectstatic --no-input

# Очистить неиспользуемые контейнеры, образы и тома
clean:
	$(DOCKER_COMPOSE) down -v --rmi all --remove-orphans

# Останавливает контейнеры, собирает из гита, пересобирает и запускает контейнеры, применяет миграции, собирает статику
deploy:
	git pull origin main
	$(DOCKER_COMPOSE) down
	$(DOCKER_COMPOSE) pull
	$(DOCKER_COMPOSE) build
	$(DOCKER_COMPOSE) up -d --remove-orphans
	$(DOCKER_COMPOSE) exec $(WEB_SERVICE) python manage.py migrate
	$(DOCKER_COMPOSE) exec $(WEB_SERVICE) python manage.py collectstatic --noinput

# Форматирование кода black + isort
format:
	$(DOCKER_COMPOSE) exec $(WEB_SERVICE) poetry run black .
	$(DOCKER_COMPOSE) exec $(WEB_SERVICE) poetry run isort .

# Линтинг с flake8
lint:
	$(DOCKER_COMPOSE) exec $(WEB_SERVICE) poetry run flake8 .

# Проверка кода
style: format lint

# Создание .po файлов для всех языков
makemessages:
	$(DOCKER_COMPOSE) exec $(WEB_SERVICE) python manage.py makemessages -l ru -l en

# Компиляция переводов
compilemessages:
	$(DOCKER_COMPOSE) exec $(WEB_SERVICE) python manage.py compilemessages
