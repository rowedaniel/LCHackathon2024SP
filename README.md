## Installation

requires:
- docker
- python 3.9 (Though I used 3.11, so be warned)
- npm
- mysql

### python
From within ``backend'' directory:

Install python requirements (presumably within a virtual environment):
```sh
pip install -r requirements.txt
```

### docker
Docker image:
(you may have to start the docker daemon first)
To start image:
```sh
docker-compose -f docker-compose.yml up -d -V
```
To stop image and remove all caches/storage:
```sh
docker-compose -f docker-compose.yml down -v
```

To check to make sure it's working:
```sh
docker compose exec db_lchackathon2024sp mysql -u root -p
```
When prompted for a password, enter ``root''.
This should take you into a mysql shell.
```mysql
show databases;
```
should include ``mind''. 

To add tables to database:
```sh
alembic upgrade head
```


# Running
## Backend
```sh
uvicorn mind_api.main:app --reload
```
## Frontend
```sh
npm run dev
```


# Notes for Daniel:
to export requirements.txt:
```sh
poetry export > requirements.txt
```

