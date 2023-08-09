# Simple referal

## How to run project
1. Copy repository with:
`git clone git@github.com:maursu/simple_referal.git`

2. Create and run virtual enviroment:
`python3 -m venv venv`
`source venv/bin/activate`

3. Install dependencies:
`pip install -r requirments.txt`

4. Create and fill .env file (you can look for variables in .env.template file)

5. Run project in docker:
`docker-compose up`

## Using without Docker
To run project without Docker after steps 1-4 in "How to run project" you need:

1. To fill DATABASES constant in config/settings-dev.py
(you can use os.getenv method to fill it from .env file, but it sometimes couse some issues with connection to databases with celery)

2. Create database in Postgresql with name and user you defined in settings or .env

3. Then type this commands in your terminal:
    `make migrate`
    `make run`
    or this if you dont have makefile extension in your IDE:
    `python manage.py makemigrations`
    `python manage.py migrate`
    `python manage.py runserver --settings='config.settings-dev'`

4. Open one more terminal and type:
    `celery -A config worker -l INFO`

## Project functions
1. "host"/api/v1/authorize - sends login code to users phone number (expires after 30 seconds). Creates user and profile instances at first authorization.

2. "host"/api/v1/login - completes suthorizstion with login code.

3. "host"/api/v1/profile - returns data of authorized user profile. You can put other users invite code to define user you refered by.

4. "host"/api/v1/docs - Redoc API documentation for more information about API handlers
