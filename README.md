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
uwsgi --ini application.ini
```

To check
```
curl -X GET 127.0.0.1:3031/types | jq .
curl -X GET 127.0.0.1:3031/resources | jq .
```

