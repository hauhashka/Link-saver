# Link Saver API

Link Saver API is a simple REST API for saving, managing, and searching useful links.

This project was built as a backend practice project using FastAPI, PostgreSQL, SQLModel, and Docker Compose.

## Features

* Create links
* Get all links
* Get one link by ID
* Update links
* Delete links
* Mark links as favorite
* Filter links by favorite status
* Search links by title or description
* Store data in PostgreSQL
* Run PostgreSQL with Docker Compose

## Tech Stack

* Python
* FastAPI
* SQLModel
* PostgreSQL
* Docker Compose
* Pydantic
* Uvicorn

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
```

## API Endpoints

| Method | Endpoint           | Description        |
| ------ | ------------------ | ------------------ |
| GET    | `/health`          | Health check       |
| GET    | `/links`           | Get all links      |
| POST   | `/links`           | Create a new link  |
| GET    | `/links/{link_id}` | Get one link by ID |
| PUT    | `/links/{link_id}` | Update a link      |
| DELETE | `/links/{link_id}` | Delete a link      |

## Query Parameters

`GET /links` supports optional query parameters:

| Parameter  | Example                | Description                    |
| ---------- | ---------------------- | ------------------------------ |
| `favorite` | `/links?favorite=true` | Filter favorite links          |
| `search`   | `/links?search=python` | Search by title or description |

You can combine them:

```text
/links?favorite=true&search=python
```

## Example Request

```json
{
  "title": "FastAPI Docs",
  "url": "https://fastapi.tiangolo.com",
  "description": "Official FastAPI documentation",
  "is_favorite": true
}
```

## How to Run

Clone the repository:

```bash
git clone https://github.com/hauhashka/Link-saver.git
cd link-saver
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment.

Windows:

```bash
venv\Scripts\activate
```

macOS / Linux:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file from the example:

```bash
cp .env.example .env
```

Start PostgreSQL:

```bash
docker compose up -d
```

Run the app:

```bash
uvicorn app.main:app --reload
```

Open API docs:

```text
http://127.0.0.1:8000/docs
```

## Environment Variables

Example `.env`:

```env
DATABASE_URL=postgresql+psycopg://link_saver_user:link_saver_password@localhost:5432/link_saver
```

## Future Improvements

* Add automated tests
* Add full Docker setup for API and database
* Add `created_at` and `updated_at` fields
* Add user authentication
* Add tags for links
* Add frontend
* Add deployment
