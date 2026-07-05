import time

from google import genai

client = genai.Client()

# 1. Path to your local audio file
local_audio_path = "sample_interview.mp3"

print("Uploading local file to temporary Gemini File API...")
# Supported audio formats include: audio/mp3, audio/wav, audio/m4a, audio/flac
audio_file = client.files.upload(file=local_audio_path)
print(f"Uploaded successfully. File URI: {audio_file.uri}")

# Wait for processing if the file is very large
while audio_file.state.name == "PROCESSING":
    print("Waiting for file processing...")
    time.sleep(2)
    audio_file = client.files.get(name=audio_file.name)

# 2. Test with Gemini 2.5 Pro (High Accuracy & Diarization)
print("\n--- Testing Gemini 2.5 Pro ---")
response_pro = client.models.generate_content(
    model="gemini-2.5-pro",
    contents=[
        audio_file,
        "Provide a complete transcript of this audio file. Separate speakers if multiple people are talking.",
    ],
)
print(response_pro.text)

# 3. Test with Gemini 2.5 Flash-Lite (Fast / Basic Transcription)
print("\n--- Testing Gemini 2.5 Flash-Lite ---")
response_lite = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    contents=[audio_file, "Provide a complete transcript of this audio file."],
)
print(response_lite.text)

# Clean up the file from the cloud environment early (Optional)
client.files.delete(name=audio_file.name)
