// Randy the rendezvous server
import express from "express";
import { WebSocketServer, WebSocket } from "ws";
import { createServer } from "http";

const app = express();
const server = createServer(app);
const wss = new WebSocketServer({ server });

type Someone = {
    ip: string,
    port: number,
}

const boopMap: Map<WebSocket, Someone> = new Map()

function boop() {
    if (boopMap.size <= 1) return;
    for (const outerBooper of boopMap.keys()) {
        for (const innerBooper of boopMap.keys()) {
            if (innerBooper !== outerBooper) {
                outerBooper.send(JSON.stringify(boopMap.get(innerBooper)))
            }
        }
    }
    boopMap.clear()
}

wss.on("connection", (ws) => {
  console.log("Client connected");

  ws.on("message", (data) => {
    const person: Someone = JSON.parse(data.toString());
    boopMap.set(ws, person);
    boop()
  });

  ws.on("close", () => {
    console.log("Client disconnected");
  });
});

const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
  console.log(`Randy listening on port ${PORT}`);
});

