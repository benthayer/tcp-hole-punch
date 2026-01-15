from __future__ import annotations

# Step 1: Gather booping materials
# Step 2: Identity crisis
# Step 3: Call randy
# Step 4: Boop

import socket
import websockets
import asyncio
import json
from typing import TypedDict, Any

class Booper(TypedDict):
    ip: str
    port: int

def gather_booping_materials() -> tuple[socket.socket, int]:
    # Address family internet, TCP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Accept connections from anywhere, get a port
    sock.bind(('0.0.0.0', 0))
    # Our local port, basically irrelevant to anyone but us
    local_port = sock.getsockname()[1]
    return sock, local_port

RANDY_WS = "wss://holepunch.apps.benthayer.com/"
RANDY_HOST = "holepunch.apps.benthayer.com"
RANDY_PORT = 443

def identity_crisis(sock: socket.socket) -> tuple[str, int]:
    # Raw HTTPS is hard, let's use the stdlib
    import ssl
    import http.client
    
    local_port = sock.getsockname()[1]
    sock.close()  # Release the port
    
    # Create SSL connection from same port
    conn = http.client.HTTPSConnection(RANDY_HOST, RANDY_PORT, source_address=('0.0.0.0', local_port))
    conn.request("GET", "/randypleasehelpwhoami")
    response = conn.getresponse()
    data = json.loads(response.read())
    conn.close()
    
    print(f"I am {data['ip']}:{data['port']}")
    return data['ip'], data['port']


async def call_randy(external_ip: str, external_port: int) -> Any:
    print(f"Connecting to Randy...")
    ws = await websockets.connect(RANDY_WS)
    await ws.send(json.dumps({"ip": external_ip, "port": external_port}))
    print("Waiting for peer...")
    return ws

async def wait_for_boop_signal(ws: Any) -> Booper:
    message = await ws.recv()
    print(f"Randy says: {message}")
    other_booper: Booper = json.loads(str(message))
    return other_booper

async def give_boops(sock: socket.socket) -> None:
    loop = asyncio.get_event_loop()
    while True:
        await loop.sock_sendall(sock, b"boop")
        await asyncio.sleep(1)

async def get_boops(sock: socket.socket) -> None:
    loop = asyncio.get_event_loop()
    while True:
        data = await loop.sock_recv(sock, len(b"boop"))
        print(data)

def connect_to_other_booper(sock: socket.socket, other_booper: Booper) -> None:
    print(f"Connecting to peer {other_booper['ip']}:{other_booper['port']}...")
    sock.connect((other_booper['ip'], other_booper['port']))
    print("Connected! Commencing boops.")

async def commence_booping(sock: socket.socket, other_booper: Booper) -> None:
    connect_to_other_booper(sock, other_booper)
    sock.setblocking(False)  # required for async socket ops
    await asyncio.gather(
        give_boops(sock),
        get_boops(sock)
    )

async def main() -> None:
    sock, local_port = gather_booping_materials()
    external_ip, external_port = identity_crisis(sock)  # closes sock
    
    # Rebind to same port for hole punch
    import time
    time.sleep(0.1)  # Let the port fully release
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    sock.bind(('0.0.0.0', local_port))
    
    ws = await call_randy(external_ip, external_port)
    other_booper = await wait_for_boop_signal(ws)
    await commence_booping(sock, other_booper)

if __name__ == "__main__":
    asyncio.run(main())
