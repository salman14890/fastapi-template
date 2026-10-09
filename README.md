# fastapi-template

FastAPI app with two endpoints:

- `GET /` returns this machine's IP address and the message `hello i am {ip}`
- `GET /health` returns `{"status": "ok"}`

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API is served at `http://127.0.0.1:8000`. Interactive docs are at `http://127.0.0.1:8000/docs`.

## Docker

```bash
docker build -t fastapi-template .
docker run --rm -p 8000:8000 fastapi-template
```

A container's own address is on Docker's private network and is often the same on every machine. `GET /` reports the machine's public IP instead.
