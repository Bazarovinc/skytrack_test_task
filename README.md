# REST-API microservice
## Start service
To start running the service just run `start.sh`
```
>./start.sh
```
## Manual start
* Run docker-compose to start PostgreSQL
```
>docker-compose up -d postgres
```
* Then you need to create virtual environment and install all needed dependencies
```
>./install_dependencies.sh
```
* Activate virtual environment
```
>source .venv/bin/activate
```
* Set alembic head
```
>alembic upgrade head
```
* Run python script to fill data into database
```
./fill_database.py
```
* Run server localy
```
python3 main.py
```
You can check the docs for service use `http://0.0.0.0:8000/docs`
# Test
You can run local tests
* Activate virtual environment
```
>source .venv/bin/activate
```
* Run pytest
```
>pytest tests/tests.py
```
