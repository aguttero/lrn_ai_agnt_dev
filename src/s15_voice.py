import tempfile

import sounddevice as sd
import soundfile as sf

SAMPLE_RATE = 16000
MAX_DURATION = 10  # duration in seconds


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

    input()
    sd.stop()
    print("Recording stopped.")

    tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    sf.write(tmp.name, audio_data, SAMPLE_RATE)
    return tmp.name


tmp_name = record_audio()
print(tmp_name)
