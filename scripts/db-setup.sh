#!/bin/sh

export PGUSER="postgres"

psql -c "CREATE DATABASE ocharm"

psql ocharm -c "CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";"