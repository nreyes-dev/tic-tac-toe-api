# tic-tac-toe-api
REST API for playing Noughts and Crosses (a.k.a Tic-tac-toe), built for Ethyca’s Technical Challenge

## Instructions on how to run this locally:

Make sure you have Docker installed and running in your system, then do:
```shell
cp .env.example .env
docker compose -f docker-compose.dev.yaml up --build -d
```

You can look at the logs by doing:
```shell
docker compose -f docker-compose.dev.yaml logs api -f
```


