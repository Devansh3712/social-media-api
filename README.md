# social-media-api
[Python API development course](https://www.youtube.com/watch?v=0sOvCWFmrtA)

- Project file structure
```
.
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

- Building a new image
```bash
> docker build -t <tag-name> .
> docker-compose up -d
```

- Pulling the existing image
```bash
> docker pull devansh3712/social-media-api
```
