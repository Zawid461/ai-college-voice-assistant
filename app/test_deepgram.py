from deepgram import (
    DeepgramClient,
    PrerecordedOptions,
    FileSource,
)

from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv("app/.env")

# Get API key
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")

# Create Deepgram client
deepgram = DeepgramClient(DEEPGRAM_API_KEY)

# Read audio file
with open("app/test.mp3", "rb") as file:
    buffer_data = file.read()

# Prepare payload
payload: FileSource = {
    "buffer": buffer_data,
}

# Configure options
options = PrerecordedOptions(
    model="nova-2",
    smart_format=True,
)

# Transcribe audio
response = deepgram.listen.prerecorded.v("1").transcribe_file(
    payload,
    options
)

# Extract transcript
transcript = response.results.channels[0].alternatives[0].transcript

print("\nTRANSCRIPT:\n")
print(transcript)