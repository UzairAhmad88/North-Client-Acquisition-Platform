up:
	docker compose up -d
down:
	docker compose down
logs:
	docker compose logs -f
ps:
	docker compose ps
test:
	cd backend && python -m pytest
lint:
	cd backend && ruff check .
format:
	cd backend && ruff format .
migrate:
	cd backend && alembic upgrade head
