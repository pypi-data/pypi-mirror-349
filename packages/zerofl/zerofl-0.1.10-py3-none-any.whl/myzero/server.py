# myzero/server.py

import socket
import threading
import asyncio
from .request import parse_request, fix_padding  # Make sure fix_padding is imported
from .response import build_response

def run_server(app, host="127.0.0.1", port=8000):
    def _handle_client(conn, addr, app):
        data = b""
        try:
            # Step 1: Read headers completely first
            while b"\r\n\r\n" not in data:
                chunk = conn.recv(4096)
                if not chunk:
                    break
                data += chunk

            if b"\r\n\r\n" not in data:
                print("Headers incomplete")
                return

            # Step 2: Parse Content-Length
            content_length = 0
            header_end = data.find(b"\r\n\r\n") + 4
            header_part = data[:header_end].decode('utf-8', errors='ignore')

            for line in header_part.split("\r\n"):
                if line.lower().startswith("content-length"):
                    _, value = line.split(": ", 1)
                    content_length = int(value.strip())
                    break

            # Step 3: Read full body based on Content-Length
            while len(data) < header_end + content_length:
                chunk = conn.recv(4096)
                if not chunk:
                    break
                data += chunk

            # Step 4: Now parse the full request
            request = parse_request(data)
            if not request:
                conn.sendall(b"HTTP/1.1 400 Bad Request\r\n\r\n")
                return

            loop = asyncio.new_event_loop()
            response_data = loop.run_until_complete(app.handle_request(request))
            conn.sendall(build_response(response_data))

        except Exception as e:
            print(f"Server error: {e}")
        finally:
            conn.close()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((host, port))
        sock.listen(100)
        print(f"Server running on http://{host}:{port}")

        while True:
            conn, addr = sock.accept()
            thread = threading.Thread(target=_handle_client, args=(conn, addr, app))
            thread.start()