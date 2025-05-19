#!/usr/bin/env python3

import os, socket, mimetypes, logging
from datetime import datetime, timezone

HOST, PORT     = "localhost", 8080
BASE_DIR       = "./www"
ERROR_404_FILE = os.path.join(BASE_DIR, "404.html")
LOG_FILE       = "access.log"

# Logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Helper
def build_header(status: str, mime: str, length: int) -> bytes:
    """Genera l'header HTTP con data UTC-aware e Content-Length."""
    now_utc = datetime.now(timezone.utc)
    date_str = now_utc.strftime("%a, %d %b %Y %H:%M:%S GMT")
    return (
        f"HTTP/1.1 {status}\r\n"
        f"Date: {date_str}\r\n"
        f"Server: MiniPython/0.3\r\n"
        f"Content-Type: {mime}\r\n"
        f"Content-Length: {length}\r\n\r\n"
    ).encode()

def serve_client(conn: socket.socket, addr):
    """Gestisce una richiesta GET."""
    try:
        request = conn.recv(1024).decode(errors="ignore")
        if not request:
            return

        method, path, _ = request.splitlines()[0].split()
        logging.info("%s %s %s", addr[0], method, path)

        if method != "GET":
            conn.sendall(b"HTTP/1.1 405 Method Not Allowed\r\n\r\n")
            return

        if ".." in path:
            conn.sendall(b"HTTP/1.1 400 Bad Request\r\n\r\n")
            return

        if path == "/":
            path = "/index.html"

        file_path = os.path.join(BASE_DIR, path.lstrip("/"))

        if os.path.isfile(file_path):
            mime = mimetypes.guess_type(file_path)[0] or "application/octet-stream"
            with open(file_path, "rb") as f:
                content = f.read()
            conn.sendall(build_header("200 OK", mime, len(content)) + content)
        else:
            with open(ERROR_404_FILE, "rb") as f:
                content = f.read()
            conn.sendall(build_header("404 Not Found", "text/html", len(content)) + content)

    finally:
        conn.close()

# Main loop
def main():
    print(f"Server attivo su http://{HOST}:{PORT}")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()

        while True:
            conn, addr = s.accept()
            serve_client(conn, addr)

if __name__ == "__main__":
    main()
