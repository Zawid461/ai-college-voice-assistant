from fastapi import FastAPI, Request
from fastapi.responses import Response
from twilio.twiml.voice_response import VoiceResponse

app = FastAPI()

@app.post("/voice")
async def voice(request: Request):

    response = VoiceResponse()

    response.say(
        "Hello. Welcome to Mailam Engineering College AI Assistant.",
        voice="alice"
    )

    response.say(
        "Our AI calling system is now working successfully.",
        voice="alice"
    )

    return Response(
        content=str(response),
        media_type="application/xml"
    )