
# import os
# import json
# import re
# from azure.storage.blob import BlobServiceClient
# from dotenv import load_dotenv
# from collections import Counter

# # Load environment variables from .env file
# load_dotenv()

# # Get connection string from environment variables
# AZURE_CONNECTION_STRING = os.getenv("AZURE_CONNECTION_STRING")
# SOURCE_CONTAINER = os.getenv("SOURCE_CONTAINER")

# COMMON_VIDEO_PATH = "/content/assets/videos/"

# # Define a dictionary to dynamically handle keys
# DYNAMIC_KEYS = {
#     "videos": "src",
#     "procedures": "href",  # Previously "id"
#     "actionCards": "icon",
#     "keyLearningPoints": "image"
# }

# def get_description_mapping(container_client):
#     description_mapping = {}

#     # List blobs in the container (recursively)
#     blobs = container_client.list_blobs()

#     for blob in blobs:
#         if blob.name.endswith('bundle.json'):
#             print(f"Processing {blob.name} for description mapping...")
#             blob_client = container_client.get_blob_client(blob)
#             json_data = blob_client.download_blob().readall()
#             json_data = json.loads(json_data)

#             folder_name = os.path.dirname(blob.name)
#             if 'description' in json_data:
#                 description = json_data['description']
#                 description_mapping[folder_name] = description

#     return description_mapping

# def save_mapping_to_file(mapping, file_path):
#     with open(file_path, 'w', encoding='utf-8') as mapping_file:
#         for folder_name, description in mapping.items():
#             mapping_file.write(f"{folder_name}: {description}\n")

# def normalize_folder_name(folder_name):
#     return re.sub(r'[-\s]', '', folder_name.lower())

# def find_main_video_directory(data):
#     video_directories = []

#     def extract_video_directories(obj):
#         if isinstance(obj, dict):
#             for key, value in obj.items():
#                 # Use dynamic key for "videos" section
#                 video_key = DYNAMIC_KEYS.get("videos", "src")
#                 if key == video_key and isinstance(value, str) and value.startswith(COMMON_VIDEO_PATH):
#                     # Remove COMMON_VIDEO_PATH and get the directory after it
#                     relative_path = value[len(COMMON_VIDEO_PATH):]
#                     main_directory = relative_path.split('/')[0]
#                     video_directories.append(main_directory)
                
#                 if isinstance(value, (dict, list)):
#                     extract_video_directories(value)
#         elif isinstance(obj, list):
#             for item in obj:
#                 extract_video_directories(item)

#     extract_video_directories(data)
#     most_common_directory = Counter(video_directories).most_common(1)
#     return most_common_directory[0][0] if most_common_directory else None

# def validate_paths(data, folder_name, main_video_directory):
#     mismatched_paths = []
#     video_paths = []

#     def traverse(obj, parent_key=""):
#         if isinstance(obj, dict):
#             for key, value in obj.items():
#                 # Use dynamic keys for each parent section
#                 video_key = DYNAMIC_KEYS.get("videos", "src")
#                 procedure_key = DYNAMIC_KEYS.get("procedures", "href")
#                 action_card_key = DYNAMIC_KEYS.get("actionCards", "icon")
#                 key_learning_key = DYNAMIC_KEYS.get("keyLearningPoints", "image")

#                 # Check for mismatched video paths in 'src' for videos
#                 if parent_key == 'videos' and key == video_key:
#                     if value.startswith(COMMON_VIDEO_PATH) and main_video_directory not in value:
#                         video_paths.append((parent_key, key, value[len(COMMON_VIDEO_PATH):]))

#                 # Mismatched paths for keyLearningPoints
#                 elif parent_key == 'keyLearningPoints' and key == key_learning_key:
#                     if '/key learning point' not in value:
#                         mismatched_paths.append((parent_key, key, value))

#                 # Mismatched paths for procedures, excluding paths containing '/procedure'
#                 elif parent_key == 'procedures' and key == procedure_key:
#                     if '/procedures' not in value:
#                         mismatched_paths.append((parent_key, key, value))

#                 # Mismatched paths for actionCards
#                 elif parent_key == 'actionCards' and key == action_card_key:
#                     if '/actioncard' not in value:
#                         mismatched_paths.append((parent_key, key, value))

#                 if isinstance(value, (dict, list)):
#                     traverse(value, parent_key=key if key in DYNAMIC_KEYS else parent_key)

#         elif isinstance(obj, list):
#             for item in obj:
#                 traverse(item, parent_key=parent_key)

#     traverse(data)
#     return video_paths + mismatched_paths

# def process_blob_storage():
#     blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
#     container_client = blob_servicelangID: fre-mczbv-78d, name: None
iption_mapping(container_client)
#     mapping_file_path = 'folder_descriptions.txt'
#     save_mapping_to_file(description_mapping, mapping_file_path)
langID: fre-mczbv-78d, name: None
dirname(blob.name)
#             langID = os.path.basename(folder_name)
#             description = description_mapping.get(folder_name, "No description found")

#             # Get main video directory
#             main_video_directory = find_main_video_directory(json_data)
#             print(f"The main video directory identified is: {main_video_directory}")

#             mismatched_paths = validate_paths(json_data, folder_name, main_video_directory)

#             mismatch_file_path = f'mismatched_paths_{langID}.txt'
#             with open(mismatch_file_path, 'w', encoding='utf-8') as output_file:
#                 output_file.write(f"langID: {langID}, name: {description}\n\n")
langID: fre-mczbv-78d, name: None
ath in mismatched_paths:
#                     output_file.write(f"Parent: {parent}, Key: {key}, Path: {path}\n")

#     print('Processing completed.')
#     print(f'Descriptions saved to {mapping_file_path} and mismatched paths saved to separate files.')

# process_blob_storage()
















# import os
# import json
# import re
# from azure.storage.blob import BlobServiceClient
# from dotenv import load_dotenv
# from collections import Counter

# # Load environment variables from .env file
# load_dotenv()

# # Get connection string from environment variables
# AZURE_CONNECTION_STRING = os.getenv("AZURE_CONNECTION_STRING")
# SOURCE_CONTAINER = os.getenv("SOURCE_CONTAINER")

# COMMON_VIDEO_PATH = "/content/assets/videos/"

# def get_description_mapping(container_client):
#     description_mapping = {}

#     # List blobs in the container (recursively)
#     blobs = container_client.list_blobs()

#     for blob in blobs:
#         if blob.name.endswith('bundle.json'):
#             print(f"Processing {blob.name} for description mapping...")
#             blob_client = container_client.get_blob_client(blob)
#             json_data = blob_client.download_blob().readall()
#             json_data = json.loads(json_data)

#             folder_name = os.path.dirname(blob.name)
#             if 'description' in json_data:
#                 description = json_data['description']
#                 description_mapping[folder_name] = description

#     return description_mapping

# def save_mapping_to_file(mapping, file_path):
#     with open(file_path, 'w', encoding='utf-8') as mapping_file:
#         for folder_name, description in mapping.items():
#             mapping_file.write(f"{folder_name}: {description}\n")

# def normalize_folder_name(folder_name):
#     return re.sub(r'[-\s]', '', folder_name.lower())

# def find_main_video_directory(data):
#     video_directories = []

#     def extract_video_directories(obj):
#         if isinstance(obj, dict):
#             for key, value in obj.items():
#                 # Process 'src' key under the COMMON_VIDEO_PATH
#                 if key == 'src' and isinstance(value, str) and value.startswith(COMMON_VIDEO_PATH):
#                     # Remove COMMON_VIDEO_PATH and get the directory after it
#                     relative_path = value[len(COMMON_VIDEO_PATH):]
#                     main_directory = relative_path.split('/')[0]
#                     video_directories.append(main_directory)
                
#                 if isinstance(value, (dict, list)):
#                     extract_video_directories(value)
#         elif isinstance(obj, list):
#             for item in obj:
#                 extract_video_directories(item)

#     extract_video_directories(data)
#     most_common_directory = Counter(video_directories).most_common(1)
#     return most_common_directory[0][0] if most_common_directory else None

# def validate_paths(data, folder_name, main_video_directory):
#     mismatched_paths = []
#     video_paths = []

#     def traverse(obj, parent_key=""):
#         if isinstance(obj, dict):
#             for key, value in obj.items():
#                 # Check for mismatched video paths in 'src' for videos
#                 if parent_key == 'videos' and key == 'src':
#                     if value.startswith(COMMON_VIDEO_PATH) and main_video_directory not in value:
#                         video_paths.append((parent_key, key, value[len(COMMON_VIDEO_PATH):]))

#                 # Mismatched paths for keyLearningPoints
#                 elif parent_key == 'keyLearningPoints' and key == 'image':
#                     if '/key learning point' not in value:
#                         mismatched_paths.append((parent_key, key, value))

#                 # Mismatched paths for procedures
#                 elif parent_key == 'procedures' and key == 'href':
#                     if '/procedures' not in value:
#                         mismatched_paths.append((parent_key, key, value))

#                 # Mismatched paths for actionCards
#                 elif parent_key == 'actionCards' and key == 'icon':
#                     if '/actioncard' not in value:
#                         mismatched_paths.append((parent_key, key, value))

#                 if isinstance(value, (dict, list)):
#                     traverse(value, parent_key=key if key in ['videos', 'keyLearningPoints', 'procedures', 'actionCards'] else parent_key)

#         elif isinstance(obj, list):
#             for item in obj:
#                 traverse(item, parent_key=parent_key)

#     traverse(data)
#     return video_paths + mismatched_paths

# def process_blob_storage():
#     blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
#     container_client = blob_service_client.get_container_client(SOURCE_CONTAINER)

#     description_mapping = get_description_mapping(container_client)
#     mapping_file_path = 'folder_descriptions.txt'
#     save_mapping_to_file(description_mapping, mapping_file_path)

#     for blob in container_client.list_blobs():
#         if blob.name.endswith('bundle.json'):
#             print(f"Processing {blob.name} for mismatches...")
#             blob_client = container_client.get_blob_client(blob)
#             json_data = blob_client.download_blob().readall()
#             json_data = json.loads(json_data)

#             folder_name = os.path.dirname(blob.name)
#             langID = os.path.basename(folder_name)
#             description = description_mapping.get(folder_name, "No description found")

#             # Get main video directory
#             main_video_directory = find_main_video_directory(json_data)
#             print(f"The main video directory identified is: {main_video_directory}")

#             mismatched_paths = validate_paths(json_data, folder_name, main_video_directory)

#             mismatch_file_path = f'mismatched_paths_{langID}.txt'
#             with open(mismatch_file_path, 'w', encoding='utf-8') as output_file:
#                 output_file.write(f"langID: {langID}, name: {description}\n\n")

#                 for parent, key, path in mismatched_paths:
#                     output_file.write(f"Parent: {parent}, Key: {key}, Path: {path}\n")

#     print('Processing completed.')
#     print(f'Descriptions saved to {mapping_file_path} and mismatched paths saved to separate files.')

# process_blob_storage()


























# isme procedure wagr ke saare path aa rhe h jab ki hame sird wrong  path chaheya
import os
import json
import re
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
from collections import Counter

# Load environment variables from .env file
load_dotenv()

# Get connection string and container from environment variables
AZURE_CONNECTION_STRING = os.getenv("AZURE_CONNECTION_STRING")
SOURCE_CONTAINER = os.getenv("SOURCE_CONTAINER")

# Define the common directory path
COMMON_VIDEO_PATH = "/content/assets/videos/"

# Function for finding the main directory for videos
def find_main_directory_in_videos(data):
    video_directories = []

    def extract_video_directories(obj):
        if isinstance(obj, dict):
            for key, value in obj.items():
                if key == 'src' and isinstance(value, str) and value.startswith(COMMON_VIDEO_PATH):
                    # Extract the part after the common path
                    relative_path = value[len(COMMON_VIDEO_PATH):]
                    # Split the relative path and get the first directory
                    main_directory = relative_path.split('/')[0]
                    video_directories.append(main_directory)

                if isinstance(value, (dict, list)):
                    extract_video_directories(value)
        elif isinstance(obj, list):
            for item in obj: 
                extract_video_directories(item)

    extract_video_directories(data)

    # Find the most common directory
    most_common_directory = Counter(video_directories).most_common(1)
    return most_common_directory[0][0] if most_common_directory else None

# Function to map descriptions from JSON files
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

# Function for writing mismatched paths
def traverse_and_write_mismatched_paths(data, main_directory, output_file, langID):
    def traverse(obj, parent_key=""):
        if isinstance(obj, dict):
            for key, value in obj.items():
                if key == 'src' and isinstance(value, str) and value.startswith(COMMON_VIDEO_PATH):
                    relative_path = value[len(COMMON_VIDEO_PATH):]
                    directory_in_path = relative_path.split('/')[0]

                    # Check if directory in the path matches the main directory
                    if directory_in_path != main_directory:
                        output_file.write(f"Mismatched: {relative_path} : {langID}\n")

                if isinstance(value, (dict, list)):
                    traverse(value)
        elif isinstance(obj, list):
            for item in obj:
                traverse(item)

    traverse(data)

# Function for validating `keyLearningPoints`, `procedures`, and `actionCards` for specific mismatches
def validate_paths(data, output_file, langID):
    def traverse(obj, parent_key=""):
        if isinstance(obj, dict):
            for key, value in obj.items():
                # Validation for `keyLearningPoints`
                if parent_key == 'keyLearningPoints' and key == 'image':
                    if '/key learning point' not in value:
                        output_file.write(f"Mismatch - keyLearningPoints: {value} : {langID}\n")

                # Validation for `procedures`
                elif parent_key == 'procedures' and key == 'href':
                    if '/procedure' not in value:
                        output_file.write(f"Mismatch - procedures: {value} : {langID}\n")

                # Validation for `actionCards`
                elif parent_key == 'actionCards' and key == 'icon':
                    if '/actioncard' not in value:
                        output_file.write(f"Mismatch - actionCards: {value} : {langID}\n")

                if isinstance(value, (dict, list)):
                    traverse(value, parent_key=key if key in ['keyLearningPoints', 'procedures', 'actionCards'] else parent_key)

        elif isinstance(obj, list):
            for item in obj:
                traverse(item, parent_key=parent_key)

    traverse(data)

# Function for processing blob storage
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

            # Find the main directory for videos
            main_directory = find_main_directory_in_videos(json_data)
            print(f"The main directory for videos is: {main_directory}")

            mismatch_file_path = f'mismatched_paths_{langID}.txt'
            with open(mismatch_file_path, 'w', encoding='utf-8') as output_file:
                output_file.write(f"langID: {langID}, name: {description}\n\n")

                # Write mismatched video paths
                traverse_and_write_mismatched_paths(json_data, main_directory, output_file, langID)

                # Write mismatched paths for `keyLearningPoints`, `procedures`, and `actionCards`
                validate_paths(json_data, output_file, langID)

    print('Processing completed.')
    print(f'Descriptions saved to {mapping_file_path} and mismatched paths saved to separate files.')

process_blob_storage()



























# import os
# import json
# import re
# from azure.storage.blob import BlobServiceClient
# from dotenv import load_dotenv
# from collections import Counter

# # Load environment variables from .env file
# load_dotenv()

# # Get connection string and container from environment variables
# AZURE_CONNECTION_STRING = os.getenv("AZURE_CONNECTION_STRING")
# SOURCE_CONTAINER = os.getenv("SOURCE_CONTAINER")

# # Define the common directory path
# COMMON_VIDEO_PATH = "/content/assets/videos/"

# # Your original function for finding the main directory for videos
# def find_main_directory_in_videos(data):
#     video_directories = []

#     def extract_video_directories(obj):
#         if isinstance(obj, dict):
#             for key, value in obj.items():
#                 if key == 'src' and isinstance(value, str) and value.startswith(COMMON_VIDEO_PATH):
#                     # Extract the part after the common path
#                     relative_path = value[len(COMMON_VIDEO_PATH):]
#                     # Split the relative path and get the first directory
#                     main_directory = relative_path.split('/')[0]
#                     video_directories.append(main_directory)

#                 if isinstance(value, (dict, list)):
#                     extract_video_directories(value)
#         elif isinstance(obj, list):
#             for item in obj:
#                 extract_video_directories(item)

#     extract_video_directories(data)

#     # Find the most common directory
#     most_common_directory = Counter(video_directories).most_common(1)
#     return most_common_directory[0][0] if most_common_directory else None

# # Original code from 2nd function
# def get_description_mapping(container_client):
#     description_mapping = {}

#     # List blobs in the container (recursively)
#     blobs = container_client.list_blobs()

#     for blob in blobs:
#         if blob.name.endswith('bundle.json'):
#             print(f"Processing {blob.name} for description mapping...")
#             blob_client = container_client.get_blob_client(blob)
#             json_data = blob_client.download_blob().readall()
#             json_data = json.loads(json_data)

#             folder_name = os.path.dirname(blob.name)
#             if 'description' in json_data:
#                 description = json_data['description']
#                 description_mapping[folder_name] = description

#     return description_mapping

# def save_mapping_to_file(mapping, file_path):
#     with open(file_path, 'w', encoding='utf-8') as mapping_file:
#         for folder_name, description in mapping.items():
#             mapping_file.write(f"{folder_name}: {description}\n")

# def normalize_folder_name(folder_name):
#     return re.sub(r'[-\s]', '', folder_name.lower())

# # Function for writing mismatched paths
# def traverse_and_write_mismatched_paths(data, main_directory, output_file, langID):
#     def traverse(obj, parent_key=""):
#         if isinstance(obj, dict):
#             for key, value in obj.items():
#                 if key == 'src' and isinstance(value, str) and value.startswith(COMMON_VIDEO_PATH):
#                     relative_path = value[len(COMMON_VIDEO_PATH):]
#                     directory_in_path = relative_path.split('/')[0]

#                     # Check if directory in the path matches the main directory
#                     if directory_in_path != main_directory:
#                         output_file.write(f"Mismatched: {relative_path} : {langID}\n")

#                 if isinstance(value, (dict, list)):
#                     traverse(value)
#         elif isinstance(obj, list):
#             for item in obj:
#                 traverse(item)

#     traverse(data)

# # Function for validating `keyLearningPoints`, `procedures`, and `actionCards`
# def validate_paths(data, output_file, langID):
#     mismatched_paths = []

#     def traverse(obj, parent_key=""):
#         if isinstance(obj, dict):
#             for key, value in obj.items():
#                 # Validation for keyLearningPoints
#                 if parent_key == 'keyLearningPoints' and key == 'image':
#                     if '/key learning point' not in value:
#                         mismatched_paths.append((parent_key, key, value))
#                         output_file.write(f"Mismatch - keyLearningPoints: {value} : {langID}\n")

#                 # Validation for procedures
#                 elif parent_key == 'procedures' and key == 'href':
#                     if '/procedure' not in value:
#                         mismatched_paths.append((parent_key, key, value))
#                         output_file.write(f"Mismatch - procedures: {value} : {langID}\n")

#                 # Validation for actionCards
#                 elif parent_key == 'actionCards' and key == 'href':
#                     if '/actioncard' not in value:
#                         mismatched_paths.append((parent_key, key, value))
#                         output_file.write(f"Mismatch - actionCards: {value} : {langID}\n")

#                 if isinstance(value, (dict, list)):
#                     traverse(value, parent_key=key if key in ['keyLearningPoints', 'procedures', 'actionCards'] else parent_key)

#         elif isinstance(obj, list):
#             for item in obj:
#                 traverse(item, parent_key=parent_key)

#     traverse(data)
#     return mismatched_paths

# # Merged process_blob_storage function
# def process_blob_storage():
#     blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
#     container_client = blob_service_client.get_container_client(SOURCE_CONTAINER)

#     description_mapping = get_description_mapping(container_client)
#     mapping_file_path = 'folder_descriptions.txt'
#     save_mapping_to_file(description_mapping, mapping_file_path)

#     for blob in container_client.list_blobs():
#         if blob.name.endswith('bundle.json'):
#             print(f"Processing {blob.name} for mismatches...")
#             blob_client = container_client.get_blob_client(blob)
#             json_data = blob_client.download_blob().readall()
#             json_data = json.loads(json_data)

#             folder_name = os.path.dirname(blob.name)
#             langID = os.path.basename(folder_name)
#             description = description_mapping.get(folder_name, "No description found")

#             # Your video directory function
#             main_directory = find_main_directory_in_videos(json_data)
#             print(f"The main directory for videos is: {main_directory}")

#             mismatch_file_path = f'mismatched_paths_{langID}.txt'
#             with open(mismatch_file_path, 'w', encoding='utf-8') as output_file:
#                 output_file.write(f"langID: {langID}, name: {description}\n\n")

#                 # Your traversal function for video mismatches
#                 traverse_and_write_mismatched_paths(json_data, main_directory, output_file, langID)

#                 # Traverse JSON to extract and write other mismatched paths
#                 mismatched_paths = validate_paths(json_data, output_file, langID)

#     print('Processing completed.')
#     print(f'Descriptions saved to {mapping_file_path} and mismatched paths saved to separate files.')

# process_blob_storage()
























# import os
# import json
# import re
# from azure.storage.blob import BlobServiceClient
# from dotenv import load_dotenv
# from collections import Counter

# # Load environment variables from .env file
# load_dotenv()

# # Get connection string and container from environment variables
# AZURE_CONNECTION_STRING = os.getenv("AZURE_CONNECTION_STRING")
# SOURCE_CONTAINER = os.getenv("SOURCE_CONTAINER")

# # Define the common directory path
# COMMON_VIDEO_PATH = "/content/assets/videos/"

# # Your original function for finding the main directory for videos
# def find_main_directory_in_videos(data):
#     video_directories = []

#     def extract_video_directories(obj):
#         if isinstance(obj, dict):
#             for key, value in obj.items():
#                 if key == 'src' and isinstance(value, str) and value.startswith(COMMON_VIDEO_PATH):
#                     # Extract the part after the common path
#                     relative_path = value[len(COMMON_VIDEO_PATH):]
#                     # Split the relative path and get the first directory
#                     main_directory = relative_path.split('/')[0]
#                     video_directories.append(main_directory)

#                 if isinstance(value, (dict, list)):
#                     extract_video_directories(value)
#         elif isinstance(obj, list):
#             for item in obj:
#                 extract_video_directories(item)

#     extract_video_directories(data)

#     # Find the most common directory
#     most_common_directory = Counter(video_directories).most_common(1)
#     return most_common_directory[0][0] if most_common_directory else None

# # Original code from 2nd function
# def get_description_mapping(container_client):
#     description_mapping = {}

#     # List blobs in the container (recursively)
#     blobs = container_client.list_blobs()

#     for blob in blobs:
#         if blob.name.endswith('bundle.json'):
#             print(f"Processing {blob.name} for description mapping...")
#             blob_client = container_client.get_blob_client(blob)
#             json_data = blob_client.download_blob().readall()
#             json_data = json.loads(json_data)

#             folder_name = os.path.dirname(blob.name)
#             if 'description' in json_data:
#                 description = json_data['description']
#                 description_mapping[folder_name] = description

#     return description_mapping

# def save_mapping_to_file(mapping, file_path):
#     with open(file_path, 'w', encoding='utf-8') as mapping_file:
#         for folder_name, description in mapping.items():
#             mapping_file.write(f"{folder_name}: {description}\n")

# def normalize_folder_name(folder_name):
#     return re.sub(r'[-\s]', '', folder_name.lower())

# # Your function for traversing JSON and validating mismatches
# def traverse_and_write_mismatched_paths(data, main_directory, output_file, langID):
#     def traverse(obj, parent_key=""):
#         if isinstance(obj, dict):
#             for key, value in obj.items():
#                 if key == 'src' and isinstance(value, str) and value.startswith(COMMON_VIDEO_PATH):
#                     relative_path = value[len(COMMON_VIDEO_PATH):]
#                     directory_in_path = relative_path.split('/')[0]

#                     # Check if directory in the path matches the main directory
#                     if directory_in_path != main_directory:
#                         output_file.write(f"Mismatched: {relative_path} : {langID}\n")

#                 if isinstance(value, (dict, list)):
#                     traverse(value)
#         elif isinstance(obj, list):
#             for item in obj:
#                 traverse(item)

#     traverse(data)

# # Original validate_paths function, excluding the video processing
# def validate_paths(data, folder_name, main_video_directory):
#     mismatched_paths = []

#     def traverse(obj, parent_key=""):
#         if isinstance(obj, dict):
#             for key, value in obj.items():
#                 # Excluding video validation from the second function
#                 if parent_key == 'keyLearningPoints' and key == 'image':
#                     if '/key learning point' not in value:
#                         mismatched_paths.append((parent_key, key, value))

#                 elif parent_key == 'procedures' and key == 'href':
#                     if '/procedure' not in value:
#                         mismatched_paths.append((parent_key, key, value))

#                 elif parent_key == 'actionCards' and key == 'icon':
#                     if '/actioncard' not in value:
#                         mismatched_paths.append((parent_key, key, value))

#                 if isinstance(value, (dict, list)):
#                     traverse(value, parent_key=key if key in ['keyLearningPoints', 'procedures', 'actionCards'] else parent_key)

#         elif isinstance(obj, list):
#             for item in obj:
#                 traverse(item, parent_key=parent_key)

#     return mismatched_paths

# # Merged process_blob_storage function
# def process_blob_storage():
#     blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
#     container_client = blob_service_client.get_container_client(SOURCE_CONTAINER)

#     description_mapping = get_description_mapping(container_client)
#     mapping_file_path = 'folder_descriptions.txt'
#     save_mapping_to_file(description_mapping, mapping_file_path)

#     for blob in container_client.list_blobs():
#         if blob.name.endswith('bundle.json'):
#             print(f"Processing {blob.name} for mismatches...")
#             blob_client = container_client.get_blob_client(blob)
#             json_data = blob_client.download_blob().readall()
#             json_data = json.loads(json_data)

#             folder_name = os.path.dirname(blob.name)
#             langID = os.path.basename(folder_name)
#             description = description_mapping.get(folder_name, "No description found")

#             # Your video directory function
#             main_directory = find_main_directory_in_videos(json_data)
#             print(f"The main directory for videos is: {main_directory}")

#             mismatch_file_path = f'mismatched_paths_{langID}.txt'
#             with open(mismatch_file_path, 'w', encoding='utf-8') as output_file:
#                 output_file.write(f"langID: {langID}, name: {description}\n\n")

#                 # Your traversal function for video mismatches
#                 traverse_and_write_mismatched_paths(json_data, main_directory, output_file, langID)

#                 # Traverse JSON to extract and write other mismatched paths
#                 mismatched_paths = validate_paths(json_data, folder_name, main_directory)
#                 for parent, key, path in mismatched_paths:
#                     output_file.write(f"Parent: {parent}, Key: {key}, Path: {path}\n")

#     print('Processing completed.')
#     print(f'Descriptions saved to {mapping_file_path} and mismatched paths saved to separate files.')

# process_blob_storage()
