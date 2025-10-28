@echo off

REM Create .env if it doesn't exist
if not exist ".env" type NUL > .env

REM Run docker compose with any arguments
docker compose up --build %*
