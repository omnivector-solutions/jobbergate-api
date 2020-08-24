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
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('bdx', 'bdx@bdx.com', 'bdx')" | ./manage.py shell
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

#### Authentication:

1. ##### Run the api server locally:

```bash
./manage.py runserver 0.0.0.0:8080
```

2. ##### Get a token pair:

```bash
curl
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"username": "bdx", "password": "bdx"}' http://localhost:8080/token/

...
{
"refresh":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTU5ODM4MzQwNiwianRpIjoiYzdlYmFmMjIxMTg5NGVjYTkxM2NhMzczOWY3Yzc2Y2YiLCJ1c2VyX2lkIjoxfQ.0ZRA0oV6xEeg8imXbi65GBw9TD77AqwqBVrfDOP-4MI",

"access":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTk4Mjk3MzA2LCJqdGkiOiJlMDAwMGIxNWY4NTQ0NmQ1ODNmOTcxYmVhYzU5MGI5YSIsInVzZXJfaWQiOjF9.XGNjATlCROEpk8nB0zAyo_vt2IPw35g8afy6DRBdxAU"
}
```

3. ##### Use the returned access token to prove authentication for a protected view:

```bash
curl \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiY29sZF9zdHVmZiI6IuKYgyIsImV4cCI6MTIzNDU2LCJqdGkiOiJmZDJmOWQ1ZTFhN2M0MmU4OTQ5MzVlMzYyYmNhOGJjYSJ9.NHlztMGER7UADHZJlxNG0WSi22a2KaYSfd1S-AuT7lU" \
  http://localhost:8080/users/
```

4. ##### When the access token expires, you can use the refresh token to get a new access token:

```bash
curl
-X POST
-H "Content-Type: application/json"
-d '{"refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImNvbGRfc3R1ZmYiOiLimIMiLCJleHAiOjIzNDU2NywianRpIjoiZGUxMmY0ZTY3MDY4NDI3ODg5ZjE1YWMyNzcwZGEwNTEifQ.aEoAYkSJjoWH1boshQAaTkf8G3yn0kapko6HFRt7Rh4"}'
http://localhost:8080/token/refresh/

...
{"access":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiY29sZF9zdHVmZiI6IuKYgyIsImV4cCI6MTIzNTY3LCJqdGkiOiJjNzE4ZTVkNjgzZWQ0NTQyYTU0NWJkM2VmMGI0ZGQ0ZSJ9.ekxRxgb9OKmHkfy-zs1Ro_xs1eMLXiR17dIDBVxeT-w"}
```

Copyright (c) 2020 OmniVector Solutions

License [MIT](LICENSE)

Web: [www.omnivector.solutions](https://www.omnivector.solutions)

Email: **<info@omnivector.solutions>**
