## Installation

requires:
- docker
- python3.8
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



# Notes for Daniel:
to export requirements.txt:
```sh
poetry export > requirements.txt
```

