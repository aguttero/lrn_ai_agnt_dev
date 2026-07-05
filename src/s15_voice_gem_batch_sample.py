import os

from google.cloud import storage

# Setup GCP variables
project_id = "your-gcp-project-id"
bucket_name = "gemini-batch-transcription-test-bucket"
local_file = "sample_interview.mp3"
gcs_blob_name = "audio/sample_interview.mp3"

# Initialize GCS Client
storage_client = storage.Client(project=project_id)

# Create the bucket
bucket = storage_client.create_bucket(bucket_name, location="us-central1")
print(f"Bucket {bucket.name} created.")

# Upload local audio file to the bucket
blob = bucket.blob(gcs_blob_name)
blob.upload_from_filename(local_file)
print(f"Uploaded {local_file} to gs://{bucket_name}/{gcs_blob_name}")
