start ::
	@docker compose up -d

logs ::
	@docker compose logs -t --tail=150

pgadmin ::
	@until $$(curl --output /dev/null --silent --head --fail http://localhost:9055); do echo "Waiting for pgadmin to start..." && sleep 10; done
	@python -m webbrowser "http://localhost:9055"

airflow ::
	@until $$(curl --output /dev/null --silent --head --fail http://localhost:9054); do echo "Waiting for Airflow to start..." && sleep 10; done
	@python -m webbrowser "http://localhost:9054"

exec ::
	@docker compose exec airflow bash

stop ::
	@docker compose down --volumes --rmi all
	@rm -rf pgadmin/sessions pgadmin/storage
