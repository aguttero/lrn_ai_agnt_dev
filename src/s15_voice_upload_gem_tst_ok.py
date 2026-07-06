import time

from dotenv import dotenv_values

# import tempfile
from google import genai

config = dotenv_values(".env")
GOOGLE_API_KEY = config.get("GOOGLE_FREE_API_KEY")

client = genai.Client(api_key=GOOGLE_API_KEY)

# 1. Path to your local audio file
# local_audio_path = "sample_interview.mp3"
local_audio_path = "tmp/tmphw5wk6pb.wav"

print("Uploading local file to temporary Gemini File API...")
# Supported audio formats include: audio/mp3, audio/wav, audio/m4a, audio/flac
audio_file = client.files.upload(file=local_audio_path)
print(f"Uploaded successfully. File URI: {audio_file.uri}")

# File state check
print(f"audio_file state status= {audio_file.state.name}")

# Wait for processing if the file is very large
while audio_file.state.name == "PROCESSING":  # status: PROCESSING, ACTIVE or FAILED
    print("Waiting for file processing...")
    time.sleep(2)
    audio_file = client.files.get(
        name=audio_file.name
    )  # Consulta al servidor info sobre file name=audio_file.name para refrescar .state y eventualmente salir del loop
    print("")

# 3. Test with Gemini 2.5 Flash-Lite (Fast / Basic Transcription)
print("\n--- Testing Gemini 2.5 Flash-Lite ---")
response_lite = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    contents=[audio_file, "Provide a complete transcript of this audio file."],
)
print(response_lite.text)

# Clean up the file from the cloud environment early (Optional)
client.files.delete(name=audio_file.name)
