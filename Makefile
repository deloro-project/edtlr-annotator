# Variables
VENV           = .venv
VENV_BIN       = $(VENV)/bin
VENV_PYTHON    = $(VENV_BIN)/python
VENV_PIP       = $(VENV_BIN)/pip

SRC_DIR        = src
APP_NAME       = annotation
APP_DIR        = $(SRC_DIR)/$(APP_NAME)

# Recipes

# Initialize the development environment
init: requirements.txt
	if [ ! -d "$(VENV)" ]; then \
	    python -m venv $(VENV);\
	fi; \
	$(VENV_PIP) install -U pip;
	if [ -f requirements-dev.txt ]; then \
	    $(VENV_PIP) install -r requirements-dev.txt;\
	fi;\
	$(VENV_PIP) install -r requirements.txt;

# Create the Django app
app: init
	if [ ! -d $(SRC_DIR) ]; then \
	    $(VENV_BIN)/django-admin startproject config; \
	    mv config $(SRC_DIR); \
	fi; \
	if [ ! -d $(APP_DIR) ]; then \
	    cd $(SRC_DIR); \
	    ../$(VENV_PYTHON) manage.py startapp $(APP_NAME); \
	fi;

# Run the development server
start: init
	$(VENV_PYTHON) $(SRC_DIR)/manage.py runserver;

# Create or update the .po file containing the translation strings
messages: init
	if [ ! -d $(APP_DIR)/locale ]; then \
	    mkdir $(APP_DIR)/locale; \
	fi; \
	$(VENV_BIN)/django-admin makemessages --locale ro;

# Compile the translations
translations: messages
	$(VENV_BIN)/django-admin compilemessages;

# Make migrations
migrations: app
	$(VENV_PYTHON) $(SRC_DIR)/manage.py makemigrations;

# Apply migrations
schema: migrations
	$(VENV_PYTHON) $(SRC_DIR)/manage.py migrate;
	$(VENV_PYTHON) $(SRC_DIR)/manage.py migrate;
