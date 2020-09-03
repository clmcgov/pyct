@echo off

docker build --tag pyct . || pause

cls

set /p username="gg username: "
set /p password="gg password: "

cls

docker run -it --rm --name pyct_test --env GRIN_USERNAME=%username% --env GRIN_PASSWORD=%password% --volume %cd%/code:/code pyct:test || pause

cls

docker exec pyct_test bash
