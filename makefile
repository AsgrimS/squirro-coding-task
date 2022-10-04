install:
	docker compose build fastapi

reinstall:
	docker compose build --no-cache fastapi

run:
	docker compose up fastapi