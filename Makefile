isort = poetry run isort .
black = poetry run black .
###############
# Environment #
###############
.PHONY: pkg
pkg: ;
	# Install system package dependencies

.PHONY: pkg_dev
pkg_dev:
	# Install development tools
	pip3 install poetry -U --user

.PHONY: venv
venv: pkg
	# Setup the virtual environment
	poetry install

.PHONY: dev_env
dev_env: pkg pkg_dev venv
	# Setup the whole development setup: package dependencies, dev tools and venv

.PHONY: clean
clean:
	# Clean up
	find . -type f -name "*.pyc" | xargs rm -fr
	find . -type d -name __pycache__ | xargs rm -fr
	find . -type d -name "*egg-info" | xargs rm -fr
	rm -rf *dist-info/ *egg-info/ linux/ *.xml dist/ .coverage .pytest_cache .mypy_cache htmlcov/ site/

.PHONY: clean-venv
clean-venv:
	# Clean up only the virtual environment
	poetry env remove "$$(poetry env list | awk '{print $$1}')"

#########
# Build #
#########
.PHONY: wheel
wheel:
	# Build the App wheel
	poetry build

.PHONY: build
build:
	earthly +build

.PHONY: upload
upload:
	earthly +upload

################
# Test Targets #
################
.PHONY: test
test:
	poetry run pytest
.PHONY: coverage
coverage:
	@echo "-----------------------"
	@echo "- 🧪 Test Coverage 🧪 -"
	@echo "-----------------------"
	poetry run pytest \
		--cov=src/kalimera/ \
		--cov-report term-missing:skip-covered \
		--cov-report html

################
# Code Quality #
################
.PHONY: format
format:
	@echo "-------------------"
	@echo "- 🎨 Formating 🎨 -"
	@echo "-------------------"

	$(isort)
	$(black)

	@echo ""

.PHONY: lint
lint:
	@echo "-----------------"
	@echo "- 🚨 Linting 🚨 -"
	@echo "-----------------"

	poetry run pylint -j 4 -f colorized src/ tests/
	poetry run mypy src/ tests/
	$(isort) --check-only --df
	$(black) --check --diff

	@echo ""

.PHONY: mypy
mypy:
	@echo "-----------------------"
	@echo "- ✅ Type checking ✅ -"
	@echo "-----------------------"

	poetry run mypy src/ tests/

	@echo ""

########
# Docs #
########
.PHONY: docs
docs:
	@echo "--------------"
	@echo "- 📚 Docs 📚 -"
	@echo "--------------"

	poetry run mkdocs build

	@echo ""

.PHONY: docs-serve
docs-serve:
	@echo "--------------"
	@echo "- 📚 Docs 📚 -"
	@echo "--------------"

	poetry run mkdocs serve

	@echo ""

##############
# Migrations #
##############
.PHONY: migrations
migrations:
	@echo "------------------"
	@echo "- ⛃ Migrations ⛃ -"
	@echo "------------------"

	@read -p "Message: " message; \
	poetry run alembic revision --autogenerate -m "$$message"

.PHONY: migrate
migrate:
	@echo "---------------"
	@echo "- ⛃ Migrate ⛃ -"
	@echo "---------------"

	poetry run alembic upgrade head

#######
# Run #
#######
.PHONY: run
run:
	poetry run uvicorn --factory --host 0.0.0.0 --reload sqlalchemy_multi_tenant.main:main
