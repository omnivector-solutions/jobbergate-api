# Jobbergate API

Jobbergate API facilitates hadling web requests from the [jobbergate-cli](https://github.com/omnivector-solutions/jobbergate-cli). The business logic for rendering and tracking job scripts, submitting and tracking jobs and registering applications is performaed here.

---

### Endpoints and Methods

| Endpoint                | Method              |
| ----------------------- | ------------------- |
| `applications/`         | GET, POST           |
| `applications/<pk>/`    | GET, UPDATE, DELETE |
| `job-scripts/`          | GET, POST           |
| `job-scripts/<pk>/`     | GET, UPDATE, DELETE |
| `job-submissions/`      | GET, POST           |
| `job-submissions/<pk>/` | GET, UPDATE, DELETE |

---

### Development

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
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('bdx@bdx.com', 'bdx')" | ./manage.py shell
```

#### Create database object using django shell

```
>>> from django.contrib.auth.models import User
>>> from apps.applications.models import Application
>>> u = User.objects.get()
>>> a = Application(application_name="rat name", application_description="rat desc", application_location="rat location", application_owner=u)
>>> a.save()
```

---

### API Usage

Run the api server locally:

```bash
./manage.py runserver 0.0.0.0:8080
```

Open another terminal and try interacting with the api:

```bash
# Install jq `brew install jq` `or sudo snap install jq`
TOKEN=`curl --silent -X POST -d "email=bdx@bdx.com&password=bdx" "http://127.0.0.1:8080/api-token-auth/" | jq -r '.token'`

curl --silent -H "Authorization: JWT $TOKEN" http://127.0.0.1:8080/users/ | jq
```

The response should look like:

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

You should now have access to the API docs:
• as json: `http://127.0.0.1:8080/swagger.json`
• as yaml: `http://127.0.0.1:8080/swagger.yaml`
• swagger UI: `http://127.0.0.1:8080/swagger/`
• redoc UI: `http://127.0.0.1:8080/redoc/`

Copyright (c) 2020 OmniVector Solutions

License [MIT](LICENSE)

Web: [www.omnivector.solutions](https://www.omnivector.solutions)

Email: **<info@omnivector.solutions>**
