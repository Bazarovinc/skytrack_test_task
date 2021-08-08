#!/bin/bash
docker-compose up -d postgres
./install_dependencies.sh
alembic upgrade head
./fill_database.py
python3 main.py
