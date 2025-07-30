# gatenet 🛰️

##### BETA (0.1.0)

## Installation

```zsh
pip install gatenet
```

## Features
- [x] [TCP Server](#tcp-server) for raw socket data
- [x] [UDP Server & Client](#udp-server--client)
- [x] [HTTP Server](#http-server-get--post)
    - [x] Route-based handling
    - [x] JSON responses
    - [x] POST support
- Minimal, composable, Pythonic design

## TCP Server

```python
from gatenet.socket.tcp import TCPServer

server = TCPServer(host='127.0.0.1', port=8000)

@server.on_receive
def handle_data(data, addr):
    print(f"[TCP] {addr} sent: {data}")
    return f"Echo: {data}"

server.start()
```

## UDP Server & Client

### UDP Server

```python
from gatenet.socket.udp import UDPServer

server = UDPServer(host="127.0.0.1", port=9000)

@server.on_receive
def handle_udp(data, addr):
    print(f"[UDP] {addr} sent: {data}")
    return f"Got your message: {data}"

server.start()
```

### UDP Client

```python
from gatenet.socket.udp import UDPClient

client = UDPClient(host="127.0.0.1", port=9000)
response = client.send("Hello, UDP!")
print(response)
```

## HTTP Server (GET + POST)

```python
from gatenet.http.base import HTTPServerComponent

server = HTTPServerComponent(host="127.0.0.1", port=8080)

@server.route("/status", method="GET")
def status(_req):
    return {
        "ok": True
    }

@server.route("/echo", method="POST")
def echo(_req, data):
    return {
        "received": data
    }

server.start()
```

### Send a POST request

```python
import requests

res = requests.post("http://127.0.0.1:8080/echo", json={"msg": "hi"})
print(res.json()) # {'received': {'msg': 'hi'}}
```

## Tests

```bash
pytest
```

[![codecov](https://codecov.io/gh/clxrityy/gatenet/branch/main/graph/badge.svg)](https://codecov.io/gh/clxrityy/gatenet)