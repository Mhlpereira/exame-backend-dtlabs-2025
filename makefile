API_URL=http://127.0.0.1:8000
SERVER_ID=01JN4HCDW7ZF0TFMXWKRFV06GG

docker:
	docker compose up -d

start-server: 
	uvicorn app.main:app --reload &

seed-db:
	python -m app.script.seed

register-user:
	@USER_ID=$$(curl -s -X POST "$(API_URL)/auth/register" \
		-H "Content-Type: application/json" \
		-d '{"email": "example2@example.com", "password": "example", "confirm_password": "example"}' | jq -r '.id'); \
	echo $$USER_ID > .id; \
	echo "User id is ready!!"

login:
	@echo "Log in..."
	@RESPONSE=$$(curl -s -X POST "$(API_URL)/auth/login" \
	-H "Content-Type: application/json" \
		-d '{"email": "example2@example.com", "password": "example"}'); \
		TOKEN=$$(echo $$RESPONSE | jq -r '.access_token'); \
		echo $$TOKEN > .token; \
		echo "Token generated!"; \


create-server:
	@echo "Creating server..."
	@RESPONSE=$$(curl -s -X POST "$(API_URL)/create-server" \
		-H "Authorization: Bearer $$(cat .token)" \
		-H "Content-Type: application/json" \
		-d '{"name": "Dolly#3"}'); \


10-register-data:
	@echo "Starting..."
	@START=$$(date +%s); \
	for i in $$(seq 1 10); do \
	  curl -X POST "$(API_URL)/data" \
	  -H "Content-Type: application/json" \
	  -d "{\"server_ulid\": \"$(SERVER_ID)\"}" \
	  -s -o /dev/null -w "Requisition $$i: %{time_total}s\n"; \
	done; \
	END=$$(date +%s); \
	echo "Total time: $$((END - START)) secs"

test:
	pytest
