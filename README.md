# social-media-api
[Python API development course](https://www.youtube.com/watch?v=0sOvCWFmrtA)

- Project file structure
```
.
├── Dockerfile
├── LICENSE
├── Makefile
├── Procfile
├── README.md
├── docker-compose.yml
├── example.env
├── mypy.ini
├── poetry.lock
├── pyproject.toml
├── requirements.txt
└── src
    ├── __init__.py
    ├── config.py
    ├── database.py
    ├── main.py
    ├── oauth2.py
    ├── routers
    │   ├── __init__.py
    │   ├── auth.py
    │   ├── posts.py
    │   ├── users.py
    │   └── vote.py
    ├── schemas.py
    └── utils.py
```

### Setup using Docker
The API instance runs on `https://localhost:8000` using default values of Dockerfile.
```bash
> docker build -t fastapi .
> docker-compose up -d
```
