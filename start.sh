#!/bin/bash
docker-compose up -d postgres
./install_dependencies.sh
source .venv/bin/activate
alembic upgrade head
./fill_database.py
python3 main.py