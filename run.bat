@echo off

docker-compose up --detach --build --force-recreate --remove-orphans || pause

docker-compose exec adapter bash || pause