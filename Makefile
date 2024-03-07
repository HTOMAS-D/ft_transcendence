# Variables
include .env

SSL_FOLDER=./nginx/ssl
SSL_CERT=$(SSL_FOLDER)/certificate.pem
SSL_KEY=$(SSL_FOLDER)/key.key

# Commands
ECHO=echo -e
MKDIR=mkdir -p

# Colors
# Foreground Colors:
FG_BLACK=\033[30m # Black
FG_RED=\033[31m # Red
FG_GREEN=\033[32m # Green
FG_YELLOW=\033[33m # Yellow
FG_BLUE=\033[34m # Blue
FG_MAGENTA=\033[35m # Magenta
FG_CYAN=\033[36m # Cyan
FG_WHITE=\033[37m # White

# Background Colors:
BG_BLACK=\033[40m # Black
BG_RED=\033[41m # Red
BG_GREEN=\033[42m # Green
BG_YELLOW=\033[43m # Yellow
BG_BLUE=\033[44m # Blue
BG_MAGENTA=\033[45m # Magenta
BG_CYAN=\033[46m # Cyan
BG_WHITE=\033[47m # White

# Reset:
RESET=\033[0m # Reset to default (removes any previous color settings)

# Rules
all: up

# Generate files
$(SSL_FOLDER):
	@$(ECHO) "$(FG_GREEN)Creating ssl folder $(RESET)"
	@$(MKDIR) $(SSL_FOLDER)

$(SSL_CERT) $(SSL_KEY): | $(SSL_FOLDER)
	@$(ECHO) "$(FG_CYAN)Creating new SSL key$(RESET)"
	@openssl req -x509 -newkey rsa:4096 -keyout "$(SSL_KEY)" -out "$(SSL_CERT)" -sha256 -days 365 --passout pass:$(PEM_PASS)
	@touch $(SSL_FOLDER)/ssl_password
	@echo $(PEM_PASS) > $(SSL_FOLDER)/ssl_password

# Initial run setup
init: up
	@# Wait until docker container starts before migrating
	@until [ "`docker inspect -f {{.State.Running}} be_main`"=="true" ]; do\
    	sleep 0.1;\
	done;
	@make migrate

# Manually invoked rules
up: | $(SSL_CERT) $(SSL_KEY)
	docker compose up -d

down:
	docker compose down

migrate:
	@$(ECHO) "$(FG_GREEN)Migrating DB"
	@docker exec be_main python manage.py migrate

reload_nginx:
	@$(ECHO) "$(FG_CYAN)Reloading nginx$(RESET)"
	@docker exec nginx sh -c "/docker-entrypoint.d/20-envsubst-on-templates.sh" # Recompile docker file
	@docker exec nginx service nginx reload

.PHONY: up