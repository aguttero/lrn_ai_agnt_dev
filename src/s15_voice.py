import tempfile
import time
import sounddevice as sd
import soundfile as sf
from google import genai
from dotenv import dotenv_values


SAMPLE_RATE = 16000
MAX_DURATION = 10  # duration in seconds

config = dotenv_values(".env")
GOOGLE_API_KEY = config.get("GOOGLE_API_KEY")

client = genai.Client()

def record_audio() -> str:
    """Record from microphone, return path to temp WAV file."""
    input("Press Enter to start recording...")
    print("Recording... Press Enter to stop.")

    audio_data = sd.rec(
        int(MAX_DURATION * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="float64",
    )

    input()  # Trick to waits for an enter input to execute next line
    sd.stop()
    print("Recording stopped.")

    tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    sf.write(tmp.name, audio_data, SAMPLE_RATE)
    print(f"Saved audio to {tmp.name} successfully!")
    return tmp.name

# --- Upload to GCS
# Supported audio formats include: audio/mp3, audio/wav, audio/m4a, audio/flac
def upload_audio_file(local_audio_path: str):
    """Upload audio file to temp Google Cloud Storage"""
    print("Uploading local file to temporary Gemini File API...")
    gcs_audio_file = client.files.upload(file=local_audio_path)
    print(f"Uploaded successfully. File URI: {gcs_audio_file.uri}")

    # File state check
    print(f"audio_file state status= {gcs_audio_file.state.name}")

    # Wait for processing if the file is very large
    while gcs_audio_file.state.name == "PROCESSING":
        print("Waiting for file processing...")
        time.sleep(2)
        gcs_audio_file = client.files.get(name=gcs_audio_file.name)

    return gcs_audio_file

def transcribe (audio_path: str)
    """Send audio to Gemini API and return the transcript."""
    with open(audio_path, "rb") as f:
        return client.audio.transcriptions.create(
            model="whisper-1",
            file=f,
            response_format="text",
        )

## ZAG - WIP
def delete_gcs_file(gcs_tmp_file_path):
    client.files.delete(name=gcs_tmp_file_path.name)
    print (f"gcs file status= {}")


def main ():

    # Record Audio
    tmp_audio_path = record_audio()
    print("TMP audio file created:", tmp_audio_path)

    # Upload audio to tmp GCS file
    gcs_file = upload_audio_file(tmp_audio_path)

    transcribe(gcs_file)
    print("TMP audio file transcribed:", tmp_audio_path)
