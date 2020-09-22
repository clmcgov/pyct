@echo off

set /p GRIN_USER="gg username: "
set /p GRIN_PASSWORD="gg password: "
cls

docker-compose up --detach --force-recreate --build --remove-orphans || pause