import os
import json
import re
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
from collections import Counter

# Load environment variables from .env file
load_dotenv()

# Get connection string from environment variables
AZURE_CONNECTION_STRING = os.getenv("AZURE_CONNECTION_STRING")
SOURCE_CONTAINER = os.getenv("SOURCE_CONTAINER")

def get_description_mapping(container_client):
    description_mapping = {}

    # List blobs in the container (recursively)
    blobs = container_client.list_blobs()

    for blob in blobs:
        if blob.name.endswith('bundle.json'):
            print(f"Processing {blob.name} for description mapping...")
            blob_client = container_client.get_blob_client(blob)
            json_data = blob_client.download_blob().readall()
            json_data = json.loads(json_data)

            folder_name = os.path.dirname(blob.name)
            if 'description' in json_data:
                description = json_data['description']
                description_mapping[folder_name] = description

    return description_mapping

def save_mapping_to_file(mapping, file_path):
    with open(file_path, 'w', encoding='utf-8') as mapping_file:
        for folder_name, description in mapping.items():
            mapping_file.write(f"{folder_name}: {description}\n")

def normalize_folder_name(folder_name):
    return re.sub(r'[-\s]', '', folder_name.lower())

def find_main_video_directory(data):
    video_directories = []

    def extract_video_directories(obj, parent_key=""):
        if isinstance(obj, dict):
            for key, value in obj.items():
                if parent_key == 'videos' and key == 'id':
                    base_directory = value.split('/')[1] if len(value.split('/')) > 1 else ""
                    if base_directory:
                        video_directories.append(base_directory)
                if isinstance(value, (dict, list)):
                    extract_video_directories(value, parent_key=key if key == 'videos' else parent_key)
        elif isinstance(obj, list):
            for item in obj:
                extract_video_directories(item, parent_key=parent_key)

    extract_video_directories(data)
    most_common_directory = Counter(video_directories).most_common(1)
    return most_common_directory[0][0] if most_common_directory else None

def validate_paths(data, folder_name, main_video_directory):
    mismatched_paths = []
    video_paths = []

    def traverse(obj, parent_key=""):
        if isinstance(obj, dict):
            for key, value in obj.items():
                if parent_key == 'videos' and key == 'id':
                    if main_video_directory not in value:
                        video_paths.append((parent_key, key, value))

                elif parent_key == 'keyLearningPoints' and key == 'image':
                    if '/key learning point' not in value:
                        mismatched_paths.append((parent_key, key, value))

                elif parent_key == 'procedures' and key == 'href':
                    if '/procedures' not in value:
                        mismatched_paths.append((parent_key, key, value))

                elif parent_key == 'actionCards' and key == 'icon':
                    if '/actioncard' not in value:
                        mismatched_paths.append((parent_key, key, value))

                if isinstance(value, (dict, list)):
                    traverse(value, parent_key=key if key in ['videos', 'keyLearningPoints', 'procedures', 'actionCards'] else parent_key)

        elif isinstance(obj, list):
            for item in obj:
                traverse(item, parent_key=parent_key)

    traverse(data)
    return video_paths + mismatched_paths

def process_blob_storage():
    blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
    container_client = blob_service_client.get_container_client(SOURCE_CONTAINER)

    description_mapping = get_description_mapping(container_client)
    mapping_file_path = 'folder_descriptions.txt'
    save_mapping_to_file(description_mapping, mapping_file_path)

    for blob in container_client.list_blobs():
        if blob.name.endswith('bundle.json'):
            print(f"Processing {blob.name} for mismatches...")
            blob_client = container_client.get_blob_client(blob)
            json_data = blob_client.download_blob().readall()
            json_data = json.loads(json_data)

            folder_name = os.path.dirname(blob.name)
            langID = os.path.basename(folder_name)
            description = description_mapping.get(folder_name, "No description found")

            main_video_directory = find_main_video_directory(json_data)
            print(f"The main video directory identified is: {main_video_directory}")

            mismatched_paths = validate_paths(json_data, folder_name, main_video_directory)

            mismatch_file_path = f'mismatched_paths_{langID}.txt'
            with open(mismatch_file_path, 'w', encoding='utf-8') as output_file:
                output_file.write(f"langID: {langID}, name: {description}\n\n")

                for parent, key, path in mismatched_paths:
                    output_file.write(f"Parent: {parent}, Key: {key}, Path: {path}\n")

    print('Processing completed.')
    print(f'Descriptions saved to {mapping_file_path} and mismatched paths saved to separate files.')

process_blob_storage()



