start ::
	docker compose up -d

logs ::
	docker compose logs -t --tail=150

pgadmin ::
	python -m webbrowser "http://localhost:9055"

airflow ::
	python -m webbrowser "http://localhost:9054"

exec ::
	docker compose exec airflow bash

stop ::
	docker compose down --volumes --rmi all
	rm -rf pgadmin/sessions pgadmin/storage
