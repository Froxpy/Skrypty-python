#!/usr/bin/env python3

import os
from google.cloud import storage
from google.api_core.exceptions import Conflict
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm  # pip install tqdm

BUCKET_NAME = "zdjecia-damiana"
LOCATION = "europe-west1"
MAX_WORKERS = 8  # Możesz dostosować do CPU / łącza

def create_bucket_if_not_exists(bucket_name, location):
    client = storage.Client()
    try:
        bucket = storage.Bucket(client, name=bucket_name)
        bucket.location = location
        bucket = client.create_bucket(bucket)
        print(f"✅ Bucket '{bucket_name}' utworzony.")
    except Conflict:
        print(f"ℹ️ Bucket '{bucket_name}' już istnieje.")

def should_upload(blob, local_path):
    if blob.exists():
        blob.reload()
        local_size = os.path.getsize(local_path)
        return blob.size != local_size
    return True

def upload_file(bucket, full_path, blob_path, relative_path):
    blob = bucket.blob(blob_path)

    if not should_upload(blob, full_path):
        return f"⏭️  Pominięto (już istnieje): {relative_path}"

    try:
        blob.upload_from_filename(full_path, timeout=600)
        return f"📤 Wysłano: {relative_path} → gs://{bucket.name}/{blob_path}"
    except Exception as e:
        return f"❌ Błąd przy wysyłaniu {relative_path}: {e}"

def upload_all_from_folder(folder_path, bucket_name):
    client = storage.Client()
    bucket = client.bucket(bucket_name)

    upload_tasks = []

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            full_path = os.path.join(root, file)
            relative_path = os.path.relpath(full_path, folder_path)
            blob_path = relative_path.replace("\\", "/")  # Windows → Unix
            upload_tasks.append((full_path, blob_path, relative_path))

    print(f"🔄 Rozpoczynam równoległe przesyłanie ({len(upload_tasks)} plików)...")

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {
            executor.submit(upload_file, bucket, full_path, blob_path, relative_path): relative_path
            for full_path, blob_path, relative_path in upload_tasks
        }

        for future in tqdm(as_completed(futures), total=len(futures), desc="📤 Postęp"):
            print(future.result())

if __name__ == "__main__":
    folder_path = os.getcwd()
    print(f"🔎 Przesyłam pliki z folderu: {folder_path}")

    create_bucket_if_not_exists(BUCKET_NAME, LOCATION)
    upload_all_from_folder(folder_path, BUCKET_NAME)
