# test-resource-app
Test resource python app

## Running locally
```
git clone <repo>
cd <repo>
pip install virtualenv
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
uwsgi --ini wsgi.ini
```

To check
```
curl -X GET 127.0.0.1:3031/types | jq .
curl -X GET 127.0.0.1:3031/resources | jq .

curl -X POST 127.0.0.1:3031/types -H 'Content-Type: application/json' -d '{"name":"test","max_speed":"100"}'
```
