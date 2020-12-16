# Jobbergate API

Jobbergate API facilitates handling web requests from the
[jobbergate-cli](https://github.com/omnivector-solutions/jobbergate-cli). The
business logic for rendering and tracking job scripts, submitting and
tracking jobs and registering applications is performed here.

---

## Development

### Install locally & in AWS

1. Create a python3 virtualenv, activate it, install packages.

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements/requirements.txt
    ```

1. In AWS Systems Manager/Parameter Store, you need to create some parameters.

    For each parameter, replace your_name with a new unique name (probably
    your name). These are the parameters you're creating:

    - /jobbergate-api/your_name/DATABASE_NAME
    - /jobbergate-api/your_name/DATABASE_PASS
    - /jobbergate-api/your_name/DATABASE_USER
    - /jobbergate-api/your_name/REGISTER_VERIFICATION_URL
    - /jobbergate-api/your_name/SENDGRID_API_KEY, and
    - /jobbergate-api/your_name/SENTRY_DSN

    For the most part you can copy these from `/jobbergate-api/staging/*`.

1. Install OpenVPN software, and confirm that you can succesfully connect to the `.ovpn` config.

   **Your development environment at https://jobbergate-api-YOURNAME.omnivector.solutions is NOT reachable without a VPN connection into AWS.**

1. Create a file under secrets/ with your correct stack info in it.
    ```bash
    cp secrets/staging.yaml secrets/<your_name>.yaml
    ```

    Edit <your_name>.yaml and change "staging" to your name, throughout.

1. (If necessary) Install docker.

    You can check by running `docker info`, an ERROR appears at the end if
    it's not running, and you will see `command not found` if it's not
    installed.

    - [Docker for Mac](https://docs.docker.com/docker-for-mac/install/)

1. Using serverless + cloudformation, deploy your instance to AWS:

    ```bash
    npx serverless deploy --stage your_name
    ```

    **IMPORTANT**: You must visit

    - https://us-west-2.console.aws.amazon.com/acm/home

    and finish the validation
    process by clicking "Create record in Route 53" for your pending certificate.

    **The deploy will *block* until you have done this.**

---

### Configure Django

To finish installation there are several steps that have to be run on Django's database.
The Django `manage.py` tool takes care of this, but you will need some environment variables
set so Django can find your cloud installation.

The steps are as follows:

```bash
# Note: make sure you have successfully used serverless deploy, above, or this will fail


# Set REQUIRED env vars, for this shell session
eval $(./scripts/serverlessenv.py your_name)


# Publish static files to the cloud
./manage.py collectstatic --noinput
npx serverless syncToS3 --stage your_name

# Prepare schema migration:
./manage.py migrate

# Create yourself a superuser
./manage.py createsuperuser
  # (you will be prompted for email & password x2)
```

### Other tips: changes to django models

As usual with Django, if you change models you must run `makemigrations` and `migrate` again.

The only difference: make sure to eval `serverlessenv.py` first, as shown above.


### Other tips: Create database object using django shell

```bash
$ eval $(scripts/serverlessenv.py your_name)
$ ./manage.py shell
```

```python
>>> from django.contrib.auth.models import User
>>> from apps.applications.models import Application
>>> u = User.objects.get()
>>> a = Application(application_name="rat name", application_description="rat desc", application_location="rat location", application_owner=u)
>>> a.save()
```

---

## API

### Endpoints and Methods

| Endpoint                | Method              |
| ----------------------- | ------------------- |
| `applications/`         | GET, POST           |
| `applications/<pk>/`    | GET, UPDATE, DELETE |
| `job-scripts/`          | GET, POST           |
| `job-scripts/<pk>/`     | GET, UPDATE, DELETE |
| `job-submissions/`      | GET, POST           |
| `job-submissions/<pk>/` | GET, UPDATE, DELETE |

### API Usage (localhost)

Run the API server locally like this.

_Important: The tools require environment
variables you can only get by running serverless, but the service itself will
run on your local machine. You must get your environment from `serverlessenv.py`
either way. To run in localhost mode there is one additional step below._


```bash
eval $(./scripts/serverlessenv.py your_name)
unset LAMBDA_TASK_ROOT  # when this is set -> management in the cloud.
                        # unset -> management is local.
./manage.py runserver 0:8080
```

(Install jq with `brew install jq` or `sudo snap install jq` .)

Open another terminal and try interacting with the API:

```bash
endpoint="http://127.0.0.1:8080"
# substitute your own superuser and password from "Configure Django"
django_superuser="bdx@bdx.com"
django_pass="bdx"
token=$(curl --silent -X POST -d "email=${django_superuser}&password=${django_pass}" "$endpoint/api-token-auth/" | jq -r '.token')
curl --silent -H "Authorization: JWT $token" "$endpoint/users/" | jq
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

- as json: `http://127.0.0.1:8080/swagger.json`

- as yaml: `http://127.0.0.1:8080/swagger.yaml`

- swagger UI: `http://127.0.0.1:8080/swagger/`

- redoc: `http://127.0.0.1:8080/redoc/`

### API Usage (serverless runtime)

Similar to the instructions above, but there's no need for `runserver`.

1. Connect through OpenVPN

2. Run similar curl commands

```bash
# Replace "yourname" with the actual name you gave your stack
endpoint="https://jobbergate-api-yourname.omnivector.solutions"
# substitute your own superuser and password from "Configure Django"
django_superuser="bdx@bdx.com"
django_pass="bdx"
token=$(curl --silent -X POST -d "email=${django_superuser}&password=${django_pass}" "$endpoint/api-token-auth/" | jq -r '.token')
curl --silent -H "Authorization: JWT $token" "$endpoint/users/" | jq
```

----

## Copyright

Copyright (c) 2020 OmniVector Solutions

License [MIT](LICENSE)

Web: [www.omnivector.solutions](https://www.omnivector.solutions)

Email: **<info@omnivector.solutions>**
