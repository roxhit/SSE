from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import json, uvicorn
from asyncio import sleep


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def hearbeat_generator():
    hearbeats = open('heartbeat.json')
    hearbeats = json.load(hearbeats)

    for heartbeat in hearbeats:
        data = json.dumps(heartbeat)
        yield f"event:heartbeatUpdate\ndata:{data} \n\n"
        await sleep(1)

@app.get("/get-heartbeats")
async def root():
    return StreamingResponse(hearbeat_generator(),media_type="text/event-stream")

    
