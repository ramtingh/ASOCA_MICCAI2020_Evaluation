call .\build.bat

docker volume create asoca-output

docker run --rm^
 --memory=4g^
 -v %~dp0\test\:/input/^
 -v asoca-output:/output/^
 asoca

docker run --rm^
 -v asoca-output:/output/^
 python:3.7-slim cat /output/metrics.json | python -m json.tool

docker volume rm asoca-output
