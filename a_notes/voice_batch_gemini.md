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

------------------------------
Would you like help writing a Python loop to automatically generate the .jsonl manifest for dozens of local audio files at once, or do you need assistance configuring Application Default Credentials (ADC) to authenticate your script with GCP? [18] 

[1] [https://ai.google.dev](https://ai.google.dev/gemini-api/docs/file-input-methods)
[2] [https://python.useinstructor.com](https://python.useinstructor.com/examples/multi_modal_gemini/)
[3] [https://dev.to](https://dev.to/googleai/benchmarking-on-a-budget-running-massive-evals-for-50-less-with-the-gemini-batch-api-5d1j)
[4] [https://docs.cloud.google.com](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/quickstart-sdk)
[5] [https://www.youtube.com](https://www.youtube.com/watch?v=vH2iMV2Y3dI&t=128)
[6] [https://medium.com](https://medium.com/@frenzur007/how-to-set-up-google-gemini-2-5-locally-with-litellm-243ebb02d910)
[7] [https://mayankgpt50.medium.com](https://mayankgpt50.medium.com/setting-up-gcp-account-with-local-system-unlocking-bigquery-and-cloud-storage-using-jupyter-8b13435118c4)
[8] [https://www.youtube.com](https://www.youtube.com/watch?v=-Qqj7Bftqg4)
[9] [https://medium.com](https://medium.com/@petitpois24_12726/getting-started-with-googles-gemini-cli-1de2251448ab)
[10] [https://ai.google.dev](https://ai.google.dev/gemini-api/docs/models/gemini-2.5-flash-lite)
[11] [https://colab.research.google.com](https://colab.research.google.com/github/google-gemini/cookbook/blob/main/quickstarts/File_API.ipynb)
[12] [https://medium.com](https://medium.com/@pankaj_pandey/google-gemini-2-5-pro-pushing-the-limits-of-ai-reasoning-and-multimodality-32c085bb7045)
[13] [https://www.youtube.com](https://www.youtube.com/watch?v=2pGx9sOAKf8&t=138)
[14] [https://ai.google.dev](https://ai.google.dev/api/batch-api)
[15] [https://medium.com](https://medium.com/google-cloud/scaling-language-detection-a-million-messages-with-geminis-batch-api-flash-lite-baccc197a1c2)
[16] [https://apidog.com](https://apidog.com/blog/gemini-api-batch-mode/)
[17] [https://www.youtube.com](https://www.youtube.com/watch?v=qcM3tdB6H0o)
[18] [https://github.com](https://github.com/jakobap/aaron)
