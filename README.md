# Link Saver API

Link Saver API is a simple REST API for saving, managing and searching useful links.

The project was built as a backend practice project using FastAPI, PostgreSQL and Docker Compose.

## Features

- Create links
- Get all links
- Get one link by ID
- Update links
- Delete links
- Mark links as favorite
- Filter links by favorite status
- Search links by title or description
- Store data in PostgreSQL
- Run PostgreSQL with Docker Compose

## Tech Stack

- Python
- FastAPI
- SQLModel
- PostgreSQL
- Docker Compose
- Pydantic
- Uvicorn

## Project Structure

```text
link-saver/
  app/
    __init__.py
    main.py
    database.py
    models.py
    schemas.py
    routers/
      __init__.py
      links.py
  docker-compose.yml
  requirements.txt
  README.md
  .env.example
  .gitignore
