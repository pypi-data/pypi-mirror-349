# myzero/request.py

import json
from urllib.parse import parse_qs

def fix_padding(s):
    # Add missing base64 padding
    missing = len(s) % 4
    if missing:
        s += '=' * (4 - missing)
    return s

class Request:
    def __init__(self, method, path, headers, body, data=None):
        self.method = method       # HTTP method (GET, POST)
        self.path = path           # URL path
        self.headers = headers     # Parsed headers
        self.body = body           # Raw body bytes
        self.data = data           # Parsed JSON or form data


def parse_request(raw_data):
    try:
        raw_text = raw_data.decode('utf-8', errors='ignore')
        headers_end = raw_text.find("\r\n\r\n")

        if headers_end == -1:
            print("No headers/body separator found")
            return None

        header_part = raw_text[:headers_end]
        lines = header_part.split("\r\n")

        if len(lines) < 1:
            print("Malformed request line")
            return None

        method, path, _ = lines[0].split(" ", 2)

        headers = {}
        for line in lines[1:]:
            if ": " in line:
                key, value = line.split(": ", 1)
                headers[key.strip()] = value.strip()

        body_start = headers_end + 4
        body = raw_data[body_start:] if len(raw_data) > body_start else b""

        content_type = headers.get("Content-Type", "").lower()
        data = None

        if content_type == "application/json":
            try:
                decoded_body = body.decode('utf-8')
                data = json.loads(decoded_body)
                
                # If 'weights' field exists, fix its padding (for base64 strings)
                if isinstance(data, dict) and 'weights' in data:
                    data['weights'] = fix_padding(data['weights'])

            except json.JSONDecodeError as e:
                print(f"JSON decode error: {e} | Raw body: {decoded_body[:200]}...")
                data = None
            except UnicodeDecodeError as e:
                print(f"UTF-8 decode error: {e}")
                data = None

        elif content_type.startswith("application/x-www-form-urlencoded"):
            try:
                data = parse_qs(body.decode('utf-8'))
            except Exception as e:
                print(f"Form decode error: {e}")

        return Request(method, path, headers, body, data)

    except Exception as e:
        print(f"Request parsing error: {e}")
        return None