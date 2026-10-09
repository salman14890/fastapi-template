import socket

from fastapi import FastAPI

app = FastAPI(title="fastapi-template")


def get_ip_address() -> str:
    """Return this machine's primary IPv4 address."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.connect(("8.8.8.8", 80))
            return sock.getsockname()[0]
    except OSError:
        return "127.0.0.1"


@app.get("/")
def root() -> dict[str, str]:
    ip_address = get_ip_address()
    return {
        "ip": ip_address,
        "message": f"hello i am {ip_address}",
    }


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
