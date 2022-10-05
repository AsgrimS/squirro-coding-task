install:
	cp ./git-hooks/* .git/hooks/
	docker compose build fastapi

reinstall:
	docker compose build --no-cache fastapi

run:
	docker compose up fastapi

shell:
	docker compose run --rm fastapi sh -c "poetry shell"

add_dependency:
	docker compose run --rm fastapi poetry add $$name

add_dev_dependency:
	docker compose run --rm fastapi poetry add --dev $$name

lint:
	docker compose run --rm fastapi sh -c "poetry run black . && \
	poetry run isort --overwrite-in-place app && \
	poetry run flake8 && \
	poetry run pytype app"

lint_check:
	docker compose run --rm fastapi sh -c "poetry run flake8 && \
	poetry run black --check . && \
	poetry run pytype app"