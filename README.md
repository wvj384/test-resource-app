# test-resource-app
Test resource python app

## Running in Docker

```
git clone <repo>
cd <repo>
docker compose -f Docker-compose.yaml build
docker compose -f Docker-compose.yaml create
docker compose -f Docker-compose.yaml start
docker compose -f Docker-compose.yaml stop
docker compose -f Docker-compose.yaml down

```

## Running locally

Start postgres locally according to storage parameters in the config.ini file

```
git clone <repo>
cd <repo>
pip install -r requirements.txt
cd src
uwsgi --ini wsgi.ini
```

## API call examples
```
Types

curl -X GET '127.0.0.1:3031/api/v1/types' | jq .
curl -X POST 127.0.0.1:3031/api/v1/types -H 'Content-Type: application/json' -d '{"name":"test","max_speed":100}' | jq .
curl -X GET '127.0.0.1:3031/api/v1/types?id=2&id=3' | jq .
curl -X PUT 127.0.0.1:3031/api/v1/types?id=3 -H 'Content-Type: application/json' -d '{"max_speed":80}' | jq .
curl -X DELETE '127.0.0.1:3031/api/v1/types?id=2&id=3' | jq .

Resources

curl -X GET '127.0.0.1:3031/api/v1/resources' | jq .
curl -X POST 127.0.0.1:3031/api/v1/resources -H 'Content-Type: application/json' -d '{"name":"test","type_id":1,"speed":110}' | jq .
curl -X PUT 127.0.0.1:3031/api/v1/resources?id=5 -H 'Content-Type: application/json' -d '{"speed":80}' | jq .
curl -X GET '127.0.0.1:3031/api/v1/resources?id=1&id=3&type_id=1' | jq .
curl -X DELETE '127.0.0.1:3031/api/v1/resources?id=2&id=3' | jq .
```
