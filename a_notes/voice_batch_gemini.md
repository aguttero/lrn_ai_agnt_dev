To test and compare both options locally, you do not need Google Cloud Storage (GCS) buckets for the standard real-time comparison. The Gemini File API allows you to upload local files directly into Google's temporary infrastructure for developer testing. [1, 2] 
However, for the Batch API, the architecture requires input and output data to be organized inside Google Cloud Storage (GCS) buckets or formatted into a .jsonl manifest file containing GCS pathways. [3] 
Both execution architectures use the unified google-genai Python library. [4] 
## Prerequisites
Install the required Google SDK libraries: [5, 6, 7] 

pip install google-genai google-cloud-storage

Set your API key as an environment variable: [8, 9] 

export GEMINI_API_KEY="your-api-key-here"

------------------------------
## Option 1: Standard Inference (Testing Local Files Directly)
This script uploads a local audio file to the temporary Gemini File API (where files are held for 48 hours for free) and requests an immediate transcript from both Gemini 2.5 Pro and Gemini 2.5 Flash-Lite: [1, 10, 11, 12, 13] 

import timefrom google import genai
client = genai.Client()
# 1. Path to your local audio filelocal_audio_path = "sample_interview.mp3" 

print("Uploading local file to temporary Gemini File API...")# Supported audio formats include: audio/mp3, audio/wav, audio/m4a, audio/flacaudio_file = client.files.upload(file=local_audio_path)
print(f"Uploaded successfully. File URI: {audio_file.uri}")
# Wait for processing if the file is very largewhile audio_file.state.name == "PROCESSING":
    print("Waiting for file processing...")
    time.sleep(2)
    audio_file = client.files.get(name=audio_file.name)
# 2. Test with Gemini 2.5 Pro (High Accuracy & Diarization)
print("\n--- Testing Gemini 2.5 Pro ---")response_pro = client.models.generate_content(
    model="gemini-2.5-pro",
    contents=[
        audio_file, 
        "Provide a complete transcript of this audio file. Separate speakers if multiple people are talking."
    ]
)
print(response_pro.text)
# 3. Test with Gemini 2.5 Flash-Lite (Fast / Basic Transcription)
print("\n--- Testing Gemini 2.5 Flash-Lite ---")response_lite = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    contents=[
        audio_file, 
        "Provide a complete transcript of this audio file."
    ]
)
print(response_lite.text)
# Clean up the file from the cloud environment early (Optional)
client.files.delete(name=audio_file.name)

------------------------------
## Option 2: No-Rush Batch Inference (Using GCP GCS Buckets)
For the [Batch API](https://ai.google.dev/gemini-api/docs/batch-api), you must stage the structural requests in a .jsonl (JSON Lines) file. Each line in this file corresponds to an individual transcription job that points directly to a persistent file location. [3, 14, 15, 16] 
## Step A: Prepare your GCP Storage Bucket
Run this quick automation script to create your test bucket and upload your local files to Google Cloud Storage:

```python
import os
from google.cloud import storage
# Setup GCP variables
project_id = "your-gcp-project-id"bucket_name = "gemini-batch-transcription-test-bucket"local_file = "sample_interview.mp3"gcs_blob_name = "audio/sample_interview.mp3"

# Initialize GCS Client
storage_client = storage.Client(project=project_id)

# Create the bucket
bucket = storage_client.create_bucket(bucket_name, location="us-central1")
print(f"Bucket {bucket.name} created.")
# Upload local audio file to the bucket
blob = bucket.blob(gcs_blob_name)
blob.upload_from_filename(local_file)
print(f"Uploaded {local_file} to gs://{bucket_name}/{gcs_blob_name}")
```

## Step B: Execute the Batch Job via Python
Once your files sit inside GCS, create a .jsonl request manifest file, upload that manifest using the File API, and kick off the automated batch processing pipeline: [3] 

```python
import json
from google import genai
from google.genai import types
client = genai.Client()

# 1. Define the GCS paths
gcs_audio_uri = "gs://gemini-batch-transcription-test-bucket/audio/sample_interview.mp3"manifest_filename = "batch_requests.jsonl"

# 2. Build the structural JSONL manifest file
# # Each line contains the contents prompt mapping to your cloud file path
request_data = {
    "contents": [
        {"parts": [{"text": "Provide a complete transcript of this audio file."}]},
        {"parts": [{"file_data": {"mime_type": "audio/mp3", "file_uri": gcs_audio_uri}}]}
    ]
}
with open(manifest_filename, "w") as f:
    f.write(json.dumps(request_data) + "\n")

# 3. Upload the manifest file itself to the Gemini File API
print("Uploading manifest to Gemini...")uploaded_manifest = client.files.upload(
    file=manifest_filename, 
    config={'mime_type': 'application/jsonl'}
)

# 4. Initialize the Batch Pipeline with the 50% discount model
print("Submitting low-cost Batch Job...")
batch_job = client.batches.create(
    model="gemini-2.5-flash-lite",
    src=uploaded_manifest.name,
    config=types.CreateBatchJobConfig(display_name="audio_transcription_batch_01")
)

print(f"Batch Job ID Created: {batch_job.name}")
print(f"Current Execution State: {batch_job.state}") # Will start as PENDING / RUNNING
```

## Step C: Monitor and Pull Results
Batch jobs execute in the background. You can check on their execution status and access completed logs using this monitoring hook: [17] 

```python
# Check job status using the Job ID string from Step B (e.g., 'batches/123456789')
job_status = client.batches.get(name="YOUR_BATCH_JOB_ID_STRING")
print(f"Job Status: {job_status.state}")
if job_status.state.name == "SUCCEEDED":
    # Download and print results
    print(f"Output files are ready. Metadata: {job_status.output_info}")
```
# calling a file already in GCS with known URI
To transcribe an audio file directly from a Google Cloud Storage (GCS) URI using the Google GenAI SDK, you use types.Part.from_uri(). [1, 2] 
This allows Gemini to stream the file directly from your gs:// bucket path without downloading it to your local machine. [2] 
## Implementation
Ensure you have the current SDK installed:

bash:
pip install google-genai

Pass the gs:// URI inside the contents list using the code below:
```python
from google import genai
from google.genai import types

def transcribe_gcs_audio(gcs_uri: str, mime_type: str):
    # Initializes the client using the GEMINI_API_KEY environment variable
    client = genai.Client()
    
    response = client.models.generate_content(
        model="gemini-2.5-flash", # Use gemini-2.5-pro for complex audio or multi-speaker analysis
        contents=[
            types.Part.from_uri(
                file_uri=gcs_uri,
                mime_type=mime_type
            ),
            "Provide a clean, word-for-word transcription of this audio file."
        ]
    )
    
    return response.text
# Example Usage
if __name__ == "__main__":
    # Define your exact GCS path and audio format
    MY_GCS_URI = "gs://your-bucket-name/folder/audio_file.mp3"
    AUDIO_MIME = "audio/mp3" # e.g., audio/wav, audio/ogg, audio/m4a
    
    transcript = transcribe_gcs_audio(MY_GCS_URI, AUDIO_MIME)
    print("--- Transcript ---")
    print(transcript)
```

## Key Considerations

* Authentication: Your environment must have permissions to read from that GCS bucket. If running locally or outside GCP, set your service account path via export GOOGLE_APPLICATION_CREDENTIALS="path/to/key.json". [3, 4] 
* Supported Formats: Gemini natively parses common formats including audio/mp3, audio/wav, audio/ogg, audio/flac, and audio/m4a. [5] 
* File Size and Length: Large files up to 2GB are supported. For files longer than approximately 2 hours, output token limits apply to full transcriptions. [6] 

Would you like to add timestamps to the text, or does the audio require speaker diarization (identifying who is talking)? [6] 

[1] [https://googleapis.github.io](https://googleapis.github.io/python-genai/genai.html)
[2] [https://github.com](https://github.com/567-labs/instructor/issues/1647)
[3] [https://www.youtube.com](https://www.youtube.com/watch?v=n43Td-mU7oA&t=2)
[4] [https://medium.com](https://medium.com/google-cloud/delivering-private-gcs-content-via-gcp-cloud-cdn-using-hmac-authentication-7d8c210e5f33)
[5] [https://docs.cloud.google.com](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/capabilities/audio-understanding)
[6] [https://www.youtube.com](https://www.youtube.com/watch?v=LMhe2egLsrQ)
