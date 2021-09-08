# MAKEFILE

download-files:
	python3 download.py

build-test:
	docker-compose -f docker-compose-test.yml up -d postgres
	docker-compose -f docker-compose-test.yml run modelvpf alembic upgrade head

run-test:
	docker-compose -f docker-compose-test.yml run modelvpf

clean-test:
	docker-compose -f docker-compose-test.yml exec postgres psql -U postgres -c 'DROP DATABASE modelvpf;'
	docker-compose -f docker-compose-test.yml down
	sudo docker volume prune -f
	docker rmi tfginformatica_modelvpf


build-app:
	docker-compose -f docker-compose.yml up -d postgres
	docker-compose -f docker-compose.yml run modelvpf alembic upgrade head

run-app:
	docker-compose -f docker-compose.yml run modelvpf

clean-app:
	docker-compose -f docker-compose.yml exec postgres psql -U postgres -c 'DROP DATABASE modelvpf;'
	docker-compose -f docker-compose.yml down
	sudo docker volume prune -f
	docker rmi tfginformatica_modelvpf
