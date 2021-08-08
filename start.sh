#!/bin/bash
docker-compose up -d postgres
./install_dependencies.sh
./fill_database.py
python3 main.py
