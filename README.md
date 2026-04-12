# GitHub Gists API

A simple HTTP API that returns a GitHub user's public Gists, built with Python and Flask.

## Prerequisites

- Python 3.12+
- Docker
- Make

## Quick Start with Docker

```bash
make build
make run
```

The API will be available at `http://localhost:8080`

## API Endpoints

| Endpoint | Description |
|---|---|
| `GET /health` | Health check |
| `GET /<username>` | List public Gists for a GitHub user |

### Example

```bash
curl http://localhost:8080/octocat
curl http://localhost:8080/health
```

## Running Tests

```bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
make test
```

## Running Locally Without Docker

```bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
flask --app app run --port 8080
```