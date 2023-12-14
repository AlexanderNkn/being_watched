#!/bin/bash

# prepare .env files
cp envs/.env.sample envs/.env
cp envs/.db.env.sample envs/.db.env

# build images
docker compose build
docker compose up -d links-db

# add schema to links db
echo "Waiting for links-db..."
ping -c 1 localhost 5432 &> /dev/null
echo "Links db started"

export PGPASSWORD=1234
psql -U postgres -h localhost -p 5432 -f apps/links/data/links_db.sql -d links_database

# remove containers
docker compose down
