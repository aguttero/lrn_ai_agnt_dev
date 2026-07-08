import tempfile
import time

import sounddevice as sd
import soundfile as sf
from dotenv import dotenv_values
from google import genai

SAMPLE_RATE = 16000
MAX_DURATION = 10  # duration in seconds

config = dotenv_values(".env")
GOOGLE_API_KEY = config.get("GOOGLE_API_KEY")

client = genai.Client(api_key=GOOGLE_API_KEY)


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
    print(f"Uploaded successfully. File URI:\n{gcs_audio_file.uri}")

    # File state check
    print(f"audio_file state status= {gcs_audio_file.state.name}")

    # Wait for processing if the file is very large
    while gcs_audio_file.state.name == "PROCESSING":
        print("Waiting for file processing...")
        time.sleep(2)
        gcs_audio_file = client.files.get(name=gcs_audio_file.name)

    return gcs_audio_file


def transcribe(gcs_audio_file: str):
    """Send audio to Gemini API and return the transcript."""
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=[gcs_audio_file, "Provide a complete transcript of this audio file."],
    )
    print(response.text)


## ZAG - WIP
def delete_gcs_file(gcs_tmp_file_path):
    client.files.delete(name=gcs_tmp_file_path.name)
    print("File deleted from GCS")
    print(f"gcs file status= {gcs_tmp_file_path.state.name}")


def main():

    # Record Audio
    # tmp_audio_path = record_audio()
    # print("TMP audio file created:", tmp_audio_path)

    tmp_audio_path = "tmp/tmppjxarxf5.wav"

    # Upload audio to tmp GCS file
    gcs_file = upload_audio_file(tmp_audio_path)

    # Transcribe
    transcribe(gcs_file)
    print("TMP audio file transcribed:", tmp_audio_path)

    # Delte GCS file
    delete_gcs_file(gcs_file)

    return 0


if __name__ == "__main__":
    exit_code = main()
    print(f"exit code: {exit_code}")
