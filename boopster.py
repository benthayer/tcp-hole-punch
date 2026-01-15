from __future__ import annotations

# Step 1: Gather booping materials
# Step 2: Identity crisis
# Step 3: Call randy
# Step 4: Boop

import socket
import stun
import websockets
import asyncio
import json
from typing import TypedDict
from websockets import WebSocketClientProtocol

class Booper(TypedDict):
    ip: str
    port: int

def gather_booping_materials() -> tuple[socket.socket, int]:
    # Address family internet, TCP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Accept connections from anywhere, get a port
    sock.bind(('0.0.0.0', 0))
    # Our local port, basically irrelevant to anyone but us
    local_port = sock.getsockname()[1]
    return sock, local_port

RANDY = "wss://holepunch.apps.benthayer.com/"

def identity_crisis(local_port: int) -> tuple[str, int]:
    _nat_type, external_ip, external_port = stun.get_ip_info(source_port=local_port)
    return external_ip, external_port


async def call_randy(external_ip: str, external_port: int) -> WebSocketClientProtocol:
    ws = await websockets.connect(RANDY)
    await ws.send(json.dumps({"ip": external_ip, "port": external_port}))
    return ws

async def wait_for_boop_signal(ws: WebSocketClientProtocol) -> Booper:
    # We will eventually get booped
    message = await ws.recv()
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
    sock.connect((other_booper['ip'], other_booper['port']))

async def commence_booping(sock: socket.socket, other_booper: Booper) -> None:
    connect_to_other_booper(sock, other_booper)
    sock.setblocking(False)  # required for async socket ops
    await asyncio.gather(
        give_boops(sock),
        get_boops(sock)
    )

async def main() -> None:
    sock, local_port = gather_booping_materials()
    external_ip, external_port = identity_crisis(local_port)
    ws = await call_randy(external_ip, external_port)
    other_booper = await wait_for_boop_signal(ws)
    await commence_booping(sock, other_booper)

if __name__ == "__main__":
    asyncio.run(main())
