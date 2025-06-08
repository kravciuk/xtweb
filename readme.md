Bild container:
    docker build -t xtweb:latest .

Run docker containter:
    docker run -it --rm --name xtweb -v .:/app -p 80:8000 xtweb:latest /bin/bash

docker compose up --force-recreate --build

docker exec -it 5bfe20b3c5af /bin/bash


docker build -t test . && docker run -p 22:22 --rm test
