# Development Guide

## Prerequisites

- Python 3.8+
- git

## Local Setup

```bash
git clone https://github.com/RP38/SomNotiFy.git
cd SomNotiFy
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` with your credentials, then start the server:

```bash
python3 server.py
```

## Project Structure

```
.
├── server.py            # HTTP server entry point
├── backends/
│   ├── __init__.py      # Backend auto-discovery and registry
│   ├── log.py           # Log backend (prints to stdout, useful for testing)
│   └── pushover.py      # Pushover notification backend
├── scripts/
│   └── install.sh       # Production installer
├── .env.example         # Template for environment variables
└── requirements.txt     # Python dependencies
```

## Adding a Backend

Create a new file in `backends/`, for example `backends/myservice.py`:

```python
import os
from backends import register

@register("myservice")
class MyServiceBackend:
    def __init__(self):
        self.api_key = os.environ.get("MYSERVICE_API_KEY", "")

    def send(self, msg):
        # msg contains: email, pass, numero, message
        print(f"Sending via MyService: {msg['message']}")
```

The backend is automatically discovered at startup. Set `BACKEND=myservice` in `.env` to use it.

## Configuration Reference

All configuration is done via the `.env` file:

| Variable             | Description                         | Default   |
|----------------------|-------------------------------------|-----------|
| `BACKEND`            | Notification backend to use         | `log`     |
| `LISTEN_HOST`        | Server listen address               | `0.0.0.0` |
| `LISTEN_PORT`        | Server listen port                  | `80`      |
| `PUSHOVER_TOKEN`     | Pushover application token          | —         |
| `PUSHOVER_USER_KEY`  | Pushover user key                   | —         |
