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
        # Check if the blob name matches the specific JSON file
        if blob.name.endswith('bundle.json'):
            print(f"Processing {blob.name} for description mapping...")
            # Download the JSON file content
            blob_client = container_client.get_blob_client(blob)
            json_data = blob_client.download_blob().readall()
            json_data = json.loads(json_data)

            # Extract the folder name from the blob path
            folder_name = os.path.dirname(blob.name)  # Get the folder name

            # Check if 'description' exists in the JSON
            if 'description' in json_data:
                description = json_data['description']
                description_mapping[folder_name] = description

    return description_mapping

def save_mapping_to_file(mapping, file_path):
    with open(file_path, 'w', encoding='utf-8') as mapping_file:
        for folder_name, description in mapping.items():
            mapping_file.write(f"{folder_name}: {description}\n")

# Function to find the main directory from video paths, ignoring '/content/assets/videos/'
def find_main_video_directory(data):
    video_directories = []

    def extract_video_directories(obj, parent_key=""):
        if isinstance(obj, dict):
            for key, value in obj.items():
                # Collect video paths under the 'videos' key and look for 'src'
                if parent_key == 'videos' and key == 'src':
                    # Ignore the first three directories ('/content/assets/videos/')
                    path_parts = value.split('/')
                    if len(path_parts) > 3 and path_parts[1] == 'content' and path_parts[2] == 'assets' and path_parts[3] == 'videos':
                        main_directory = path_parts[4] if len(path_parts) > 4 else ""
                        if main_directory:
                            video_directories.append(main_directory)

                # Traverse nested dictionaries and lists
                if isinstance(value, (dict, list)):
                    extract_video_directories(value, parent_key=key if key == 'videos' else parent_key)

        elif isinstance(obj, list):
            for item in obj:
                extract_video_directories(item, parent_key=parent_key)

    extract_video_directories(data)

    # Find the most frequent base directory (main directory) for videos
    most_common_directory = Counter(video_directories).most_common(1)
    return most_common_directory[0][0] if most_common_directory else None

# Function to validate paths for specified parent keys
def validate_paths(data, line_info, main_video_directory):
    mismatched_paths = []
    mismatched_video_paths = []  # List to collect mismatched video paths

    def traverse(obj, parent_key="", current_line=0):
        if isinstance(obj, dict):
            # Check for "keyLearningPoints"
            if parent_key == 'keyLearningPoints':
                if 'image' in obj:
                    if '/key learning point' not in obj['image']:
                        mismatched_paths.append((parent_key, 'image', obj['image'], line_info.get(current_line, "Line info not available")))

            # Check for "procedures"
            elif parent_key == 'procedures':
                if 'icon' in obj:
                    if '/procedure' not in obj['icon']:
                        mismatched_paths.append((parent_key, 'icon', obj['icon'], line_info.get(current_line, "Line info not available")))

            # Check for "actionCards"
            elif parent_key == 'actionCards':
                if 'icon' in obj:
                    if '/actioncard' not in obj['icon']:
                        mismatched_paths.append((parent_key, 'icon', obj['icon'], line_info.get(current_line, "Line info not available")))

            # Check for video paths that do not contain the main video directory
            elif parent_key == 'videos':
                if 'src' in obj:
                    video_path = obj['src']
                    # Ignore '/content/assets/videos/' part when checking the path
                    if video_path.startswith('/content/assets/videos/'):
                        cleaned_video_path = video_path.split('/', 4)[-1]  # Remove '/content/assets/videos/'
                        if main_video_directory and main_video_directory not in cleaned_video_path:
                            mismatched_video_paths.append((parent_key, 'src', video_path, line_info.get(current_line, "Line info not available")))

            # Traverse nested dictionaries and lists
            for key, value in obj.items():
                if isinstance(value, (dict, list)):
                    traverse(value, parent_key=key if key in ['keyLearningPoints', 'procedures', 'actionCards', 'videos'] else parent_key, current_line=current_line)

                current_line += 1
        elif isinstance(obj, list):
            for index, item in enumerate(obj):
                traverse(item, parent_key=parent_key, current_line=current_line)
                current_line += 1

    traverse(data)
    return mismatched_paths, mismatched_video_paths  # Return both mismatched paths

def process_blob_storage():
    # Initialize Blob Service Client
    blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
    container_client = blob_service_client.get_container_client(SOURCE_CONTAINER)

    # Get the description mapping from JSON files
    description_mapping = get_description_mapping(container_client)

    # Save the mapping to a text file
    mapping_file_path = 'folder_descriptions.txt'
    save_mapping_to_file(description_mapping, mapping_file_path)

    # Process the specific JSON file for mismatches
    for blob in container_client.list_blobs():
        # Only process the specified JSON file
        if blob.name.endswith('bundle.json'):
            print(f"Processing {blob.name} for mismatches...")
            # Download the JSON file content
            blob_client = container_client.get_blob_client(blob)
            json_data = blob_client.download_blob().readall()
            json_data = json.loads(json_data)

            # Extract the folder name
            folder_name = os.path.dirname(blob.name)  # Get the folder path
            langID = os.path.basename(folder_name)  # Assuming langID is the folder name

            # Track line numbers
            json_data_lines = json.dumps(json_data, indent=4).splitlines()
            line_info = {i: line.strip() for i, line in enumerate(json_data_lines)}

            # Find the main video directory
            main_video_directory = find_main_video_directory(json_data)
            print(f"The main video directory identified is: {main_video_directory}")

            # Get the description for the current folder
            description = description_mapping.get(folder_name, "No description found")

            # Validate the image paths against the JSON data for keyLearningPoints, procedures, actionCards, and videos
            mismatched_paths, mismatched_video_paths = validate_paths(json_data, line_info, main_video_directory)

            # Create a folder-specific file named after the folder
            mismatch_file_path = f'mismatched_paths_{langID}.txt'
            with open(mismatch_file_path, 'w', encoding='utf-8') as output_file:
                # Write the langID and name at the top
                output_file.write(f"langID: {langID}, name: {description}\n\n")  # Include langID and description

                # Write mismatched image paths
                for parent, key, path, line in mismatched_paths:
                    output_file.write(f"Parent: {parent}, Key: {key}, Path: {path}, {line}\n")
                
                # Write mismatched video paths
                for parent, key, path, line in mismatched_video_paths:
                    output_file.write(f"Parent: {parent}, Key: {key}, Path: {path}, {line}\n")

    print('Processing completed.')
    print(f'Descriptions saved to {mapping_file_path} and mismatched paths saved to separate files.')

# Start processing from Azure Blob Storage
process_blob_storage()
