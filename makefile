install:
	cp ./git-hooks/* .git/hooks/
	docker compose build fastapi

reinstall:
	docker compose down
	docker compose build --no-cache fastapi

run:
	docker compose up fastapi -d

stop:
	docker compose stop

test:
	docker compose up mongo_test -d
	docker compose run --rm fastapi sh -c "pytest --verbose"

clean:
	docker compose run --rm fastapi sh -c "rm -rf mongo_data"
	docker compose down -v

attach:
	docker attach squirro_fastapi

shell:
	docker compose run --rm fastapi sh -c "poetry shell"

add_dependency:
	docker compose run --rm fastapi poetry add $$name

add_dev_dependency:
	docker compose run --rm fastapi poetry add -G dev $$name

remove_dependency:
	docker compose run --rm fastapi poetry remove $$name

lint:
	docker compose run --rm fastapi sh -c "poetry run black . && \
	poetry run isort --overwrite-in-place app tests && \
	poetry run flake8"

lint_check:
	docker compose run --rm fastapi sh -c "poetry run flake8 && \
	poetry run black --check ."