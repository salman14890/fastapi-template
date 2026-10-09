import ipaddress
import os
import socket
import urllib.request
from functools import lru_cache

from fastapi import FastAPI

app = FastAPI(title="fastapi-template")


def _interface_ip() -> str:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.connect(("8.8.8.8", 80))
            return sock.getsockname()[0]
    except OSError:
        return "127.0.0.1"


def _public_ip() -> str | None:
    request = urllib.request.Request(
        "https://api.ipify.org",
        headers={"User-Agent": "fastapi-template"},
    )
    try:
        with urllib.request.urlopen(request, timeout=3) as response:
            ip_address = response.read().decode().strip()
        ipaddress.ip_address(ip_address)
    except (OSError, ValueError):
        return None
    return ip_address


@lru_cache(maxsize=1)
def get_ip_address() -> str:
    """Return this machine's address.

    Inside Docker the interface address is a private bridge IP, often the same
    on every machine. Use the public IP in that case.
    """
    ip_address = _interface_ip()
    if os.path.exists("/.dockerenv"):
        return _public_ip() or ip_address
    return ip_address


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
