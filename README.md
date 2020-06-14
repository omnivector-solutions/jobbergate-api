# Jobbergate API
Jobbergate API facilitates hadling web requests from the jobbergate-cli. The business logic for rendering and tracking job scripts, submitting and tracking jobs and registering applications is performaed here.


## Endpoints and Methods

Endpoint                  | Method
------------------------- | -------------------
`applications/`           | GET, POST
`applications/<pk>/`      | GET, UPDATE, DELETE
`job-scripts/`            | GET, POST
`job-scripts/<pk>/`       | GET, UPDATE, DELETE
`job-submissions/`        | GET, POST
`job-submissions/<pk>/`   | GET, UPDATE, DELETE


## Development
#### Local Install
Create a python3 virtualenv, activate it, install packages.
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements/requirements.txt
```

#### Setup
Following the install steps, run these commands to create and apply and migrations.
```bash
# Make migrations
./manage.py makemigrations

# Migrate schema
./manage.py migrate

# Collect static files
./manage.py collectstatic --noinput

# Create superuser
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('bdx', 'bdx@bdx.com', 'bdx')" | ./manage.py shell
```

#### API Usage
Run the api server locally:
```bash
./manage.py runserver 0.0.0.0:8080
```
Open another terminal and try interacting with the api:
```bash
# Install jq `brew install jq` `or sudo snap install jq`
TOKEN=`curl --silent -X POST -d "username=bdx&password=bdx" "http://127.0.0.1:8080/api-token-auth/" | jq -r '.token'`

curl --silent -H "Authorization: Bearer $TOKEN" http://127.0.0.1:8080/users/ | jq
```
The response shoudl look like:
```json
[
  {
    "url": "http://127.0.0.1:8080/users/1/",
    "username": "bdx",
    "email": "bdx@bdx.com",
    "is_staff": true
  }
]
```


### Docker

### License
* [MIT](LICENSE)

### Copyright
* Copyright (c) 2020 OmniVector Solutions <admin@omnivector.solutions>
