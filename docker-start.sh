#!/usr/bin/env bash

# Create .env if it doesn't exist
[ -f .env ] || touch .env

# Run docker compose with any arguments
docker compose up --build "$@"
