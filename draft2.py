import os
import json
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get connection string from environment variables
AZURE_CONNECTION_STRING = os.getenv("AZURE_CONNECTION_STRING")
SOURCE_CONTAINER = os.getenv("SOURCE_CONTAINER")

# Load mapping sheet (assuming it's a JSON file)
def load_mapping_sheet(mapping_file_path='/home/nitish/nitish azure folder/mapingsheet.json'):
    with open(mapping_file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# Get description from the mapping sheet using langID
def get_description_from_mapping(langID, mapping_sheet):
    return mapping_sheet.get(langID, {}).get('description', 'Description not found')

# Function to validate paths for images, videos, keyLearningPoints, actionCards, and procedures
def validate_paths(data, line_info, main_image_directory, main_video_directory):
    mismatched_paths = []

    def traverse(obj, parent_key="", current_line=0):
        if isinstance(obj, dict):
            # Check for "Image" key under 'images'
            if parent_key.lower() == 'images':
                if 'src' in obj:
                    image_path = obj['src']
                    # Check if the path starts with the specified prefix and remove it
                    if image_path.startswith('/content/assets/images/'):
                        cleaned_image_path = image_path.split('/', 4)[-1]  # Remove '/content/assets/images/' prefix
                        if main_image_directory and main_image_directory not in cleaned_image_path:
                            mismatched_paths.append((parent_key, 'src', image_path, line_info.get(current_line, "Line info not available")))

            # Check for "Videos" key under 'videos'
            elif parent_key.lower() == 'videos':
                if 'src' in obj:
                    video_path = obj['src']
                    # Check if the path starts with the specified prefix and remove it
                    if video_path.startswith('/content/assets/videos/'):
                        cleaned_video_path = video_path.split('/', 4)[-1]  # Remove '/content/assets/videos/' prefix
                        if main_video_directory and main_video_directory not in cleaned_video_path:
                            mismatched_paths.append((parent_key, 'src', video_path, line_info.get(current_line, "Line info not available")))

            # Check for "keyLearningPoints"
            elif parent_key.lower() == 'keylearningpoints':
                if 'image' in obj:
                    if '/key learning point' not in obj['image']:
                        mismatched_paths.append((parent_key, 'image', obj['image'], line_info.get(current_line, "Line info not available")))

            # Check for "actionCards"
            elif parent_key.lower() == 'actioncards':
                if 'href' in obj:
                    if '/action card' not in obj['href']:
                        mismatched_paths.append((parent_key, 'href', obj['href'], line_info.get(current_line, "Line info not available")))

            # Check for "procedures"
            elif parent_key.lower() == 'procedures':
                if 'image' in obj:
                    if '/procedure' not in obj['image']:
                        mismatched_paths.append((parent_key, 'image', obj['image'], line_info.get(current_line, "Line info not available")))

            # Traverse nested dictionaries and lists
            for key, value in obj.items():
                if isinstance(value, (dict, list)):
                    # Properly set parent_key for "Image", "Videos", "keyLearningPoints", "actionCards", and "procedures"
                    traverse(value, parent_key=key if key.lower() in ['images', 'videos', 'keylearningpoints', 'actioncards', 'procedures'] else parent_key, current_line=current_line)

                current_line += 1
        elif isinstance(obj, list):
            for index, item in enumerate(obj):
                traverse(item, parent_key=parent_key, current_line=current_line)
                current_line += 1

    traverse(data)
    return mismatched_paths  # Return all mismatched paths

def process_blob_storage():
    # Load the mapping sheet
    mapping_sheet = load_mapping_sheet()

    # Initialize Azure Blob client
    blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
    container_client = blob_service_client.get_container_client(SOURCE_CONTAINER)

    for blob in container_client.list_blobs():
        if blob.name.endswith('bundle.json'):
            folder_name = os.path.dirname(blob.name)
            langID = os.path.basename(folder_name)  # Assuming langID is part of the folder name

            # Get description from mapping sheet
            description = get_description_from_mapping(langID, mapping_sheet)
            print(f"LangID: {langID}, Description: {description}")
            
            # Process the blob data
            blob_client = container_client.get_blob_client(blob)
            json_data = blob_client.download_blob().readall()
            json_data = json.loads(json_data)

            # Process video and image directories using the mapping sheet's asset version
            asset_versions = mapping_sheet.get(langID, {}).get('asset_version', '').split(', ')
            main_image_directory = asset_versions[0].strip() if len(asset_versions) > 0 else ""  # First value is for images
            main_video_directory = asset_versions[1].strip() if len(asset_versions) > 1 else ""  # Second value is for videos

            # Find mismatched paths for both videos, images, keyLearningPoints, actionCards, and procedures
            json_data_lines = json.dumps(json_data, indent=4).splitlines()
            line_info = {i: line.strip() for i, line in enumerate(json_data_lines)}
            mismatched_paths = validate_paths(
                json_data, line_info, main_image_directory, main_video_directory
            )

            # Save the mismatched paths for this langID in one file
            mismatch_file_path = f'mismatched_paths_{langID}.txt'
            with open(mismatch_file_path, 'w', encoding='utf-8') as output_file:
                output_file.write(f"LangID: {langID}, Description: {description}\n\n")
                for parent, key, path, line in mismatched_paths:
                    path_part = f"Parent: {parent}, Key: {key}, Path: {path}, Line: {line}\n"
                    output_file.write(path_part)

    print('Processing completed.')

process_blob_storage()
 
















# isme sab badiya hai image and videos kaa aa raha hai 
# import os
# import json
# from azure.storage.blob import BlobServiceClient
# from dotenv import load_dotenv

# # Load environment variables from .env file
# load_dotenv()

# # Get connection string from environment variables
# AZURE_CONNECTION_STRING = os.getenv("AZURE_CONNECTION_STRING")
# SOURCE_CONTAINER = os.getenv("SOURCE_CONTAINER")

# # Load mapping sheet (assuming it's a JSON file)
# def load_mapping_sheet(mapping_file_path='/home/nitish/nitish azure folder/mapingsheet.json'):
#     with open(mapping_file_path, 'r', encoding='utf-8') as file:
#         return json.load(file)

# # Get description from the mapping sheet using langID
# def get_description_from_mapping(langID, mapping_sheet):
#     return mapping_sheet.get(langID, {}).get('description', 'Description not found')

# # Function to validate paths for image and video directories
# def validate_paths(data, line_info, main_image_directory, main_video_directory):
#     mismatched_paths = []

#     def traverse(obj, parent_key="", current_line=0):
#         if isinstance(obj, dict):
#             # Check for "Image" key
#             if parent_key.lower() == 'images':
#                 if 'src' in obj:
#                     image_path = obj['src']
#                     # Check if the path starts with the specified prefix and remove it
#                     if image_path.startswith('/content/assets/images/'):
#                         cleaned_image_path = image_path.split('/', 4)[-1]  # Remove '/content/assets/images/' prefix
#                         if main_image_directory and main_image_directory not in cleaned_image_path:
#                             mismatched_paths.append((parent_key, 'src', image_path, line_info.get(current_line, "Line info not available")))

#             # Check for "videos" key
#             elif parent_key.lower() == 'videos':
#                 if 'src' in obj:
#                     video_path = obj['src']
#                     # Check if the path starts with the specified prefix and remove it
#                     if video_path.startswith('/content/assets/videos/'):
#                         cleaned_video_path = video_path.split('/', 4)[-1]  # Remove '/content/assets/videos/' prefix
#                         if main_video_directory and main_video_directory not in cleaned_video_path:
#                             mismatched_paths.append((parent_key, 'src', video_path, line_info.get(current_line, "Line info not available")))

#             # Traverse nested dictionaries and lists
#             for key, value in obj.items():
#                 if isinstance(value, (dict, list)):
#                     # Properly set parent_key for "Image" and "videos"
#                     traverse(value, parent_key=key if key.lower() in ['images', 'videos'] else parent_key, current_line=current_line)

#                 current_line += 1
#         elif isinstance(obj, list):
#             for index, item in enumerate(obj):
#                 traverse(item, parent_key=parent_key, current_line=current_line)
#                 current_line += 1

#     traverse(data)
#     return mismatched_paths  # Return all mismatched paths

# def process_blob_storage():
#     # Load the mapping sheet
#     mapping_sheet = load_mapping_sheet()

#     # Initialize Azure Blob client
#     blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
#     container_client = blob_service_client.get_container_client(SOURCE_CONTAINER)

#     for blob in container_client.list_blobs():
#         if blob.name.endswith('bundle.json'):
#             folder_name = os.path.dirname(blob.name)
#             langID = os.path.basename(folder_name)  # Assuming langID is part of the folder name

#             # Get description from mapping sheet
#             description = get_description_from_mapping(langID, mapping_sheet)
#             print(f"LangID: {langID}, Description: {description}")
            
#             # Process the blob data
#             blob_client = container_client.get_blob_client(blob)
#             json_data = blob_client.download_blob().readall()
#             json_data = json.loads(json_data)

#             # Process video and image directories using the mapping sheet's asset version
#             asset_versions = mapping_sheet.get(langID, {}).get('asset_version', '').split(', ')
#             main_image_directory = asset_versions[0].strip() if len(asset_versions) > 0 else ""  # First value is for images
#             main_video_directory = asset_versions[1].strip() if len(asset_versions) > 1 else ""  # Second value is for videos

#             # Find mismatched paths for both videos and images
#             json_data_lines = json.dumps(json_data, indent=4).splitlines()
#             line_info = {i: line.strip() for i, line in enumerate(json_data_lines)}
#             mismatched_paths = validate_paths(
#                 json_data, line_info, main_image_directory, main_video_directory
#             )

#             # Save the mismatched paths for this langID in one file
#             mismatch_file_path = f'mismatched_paths_{langID}.txt'
#             with open(mismatch_file_path, 'w', encoding='utf-8') as output_file:
#                 output_file.write(f"LangID: {langID}, Description: {description}\n\n")
#                 for parent, key, path, line in mismatched_paths:
#                     path_part = f"Parent: {parent}, Key: {key}, Path: {path}, Line: {line}\n"
#                     output_file.write(path_part)

#     print('Processing completed.')

# process_blob_storage()













# isme bhi sirf video wali file aa rahi h ye draft 2 hai neecha wala bhi code bhi same h bss ye backup code hai 
# import os
# import json
# from azure.storage.blob import BlobServiceClient
# from dotenv import load_dotenv

# # Load environment variables from .env file
# load_dotenv()

# # Get connection string from environment variables
# AZURE_CONNECTION_STRING = os.getenv("AZURE_CONNECTION_STRING")
# SOURCE_CONTAINER = os.getenv("SOURCE_CONTAINER")

# # Load mapping sheet (assuming it's a JSON file)
# def load_mapping_sheet(mapping_file_path='/home/nitish/nitish azure folder/mapingsheet.json'):
#     with open(mapping_file_path, 'r', encoding='utf-8') as file:
#         return json.load(file)

# # Get description from the mapping sheet using langID
# def get_description_from_mapping(langID, mapping_sheet):
#     return mapping_sheet.get(langID, {}).get('description', 'Description not found')

# # Function to validate paths for image and video directories
# def validate_paths(data, line_info, main_image_directory, main_video_directory):
#     mismatched_paths = []

#     def traverse(obj, parent_key="", current_line=0):
#         if isinstance(obj, dict):
#             # Check for "Image" key
#             if parent_key == 'Image':
#                 if 'src' in obj:
#                     image_path = obj['src']
#                     # Ignore '/content/assets/images/' part when checking the path
#                     if image_path.startswith('/content/assets/images/'):
#                         cleaned_image_path = image_path.split('/', 4)[-1]  # Remove '/content/assets/images/'
#                         if main_image_directory and main_image_directory not in cleaned_image_path:
#                             mismatched_paths.append((parent_key, 'src', image_path, line_info.get(current_line, "Line info not available")))

#             # Check for "videos" key
#             elif parent_key == 'videos':
#                 if 'src' in obj:
#                     video_path = obj['src']
#                     # Ignore '/content/assets/videos/' part when checking the path
#                     if video_path.startswith('/content/assets/videos/'):
#                         cleaned_video_path = video_path.split('/', 4)[-1]  # Remove '/content/assets/videos/'
#                         if main_video_directory and main_video_directory not in cleaned_video_path:
#                             mismatched_paths.append((parent_key, 'src', video_path, line_info.get(current_line, "Line info not available")))

#             # Traverse nested dictionaries and lists
#             for key, value in obj.items():
#                 if isinstance(value, (dict, list)):
#                     traverse(value, parent_key=key if key in ['Image', 'videos'] else parent_key, current_line=current_line)

#                 current_line += 1
#         elif isinstance(obj, list):
#             for index, item in enumerate(obj):
#                 traverse(item, parent_key=parent_key, current_line=current_line)
#                 current_line += 1

#     traverse(data)
#     return mismatched_paths  # Return all mismatched paths

# def process_blob_storage():
#     # Load the mapping sheet
#     mapping_sheet = load_mapping_sheet()

#     # Initialize Azure Blob client
#     blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
#     container_client = blob_service_client.get_container_client(SOURCE_CONTAINER)

#     for blob in container_client.list_blobs():
#         if blob.name.endswith('bundle.json'):
#             folder_name = os.path.dirname(blob.name)
#             langID = os.path.basename(folder_name)  # Assuming langID is part of the folder name

#             # Get description from mapping sheet
#             description = get_description_from_mapping(langID, mapping_sheet)
#             print(f"LangID: {langID}, Description: {description}")
            
#             # Process the blob data
#             blob_client = container_client.get_blob_client(blob)
#             json_data = blob_client.download_blob().readall()
#             json_data = json.loads(json_data)

#             # Process video and image directories using the mapping sheet's asset version
#             asset_versions = mapping_sheet.get(langID, {}).get('asset_version', '').split(', ')
#             main_image_directory = asset_versions[0] if len(asset_versions) > 0 else ""  # First value is for images
#             main_video_directory = asset_versions[1] if len(asset_versions) > 1 else ""  # Second value is for videos

#             # Find mismatched paths for both videos and images
#             json_data_lines = json.dumps(json_data, indent=4).splitlines()
#             line_info = {i: line.strip() for i, line in enumerate(json_data_lines)}
#             mismatched_paths = validate_paths(
#                 json_data, line_info, main_image_directory, main_video_directory
#             )

#             # Save the mismatched paths for this langID in one file
#             mismatch_file_path = f'mismatched_paths_{langID}.txt'
#             with open(mismatch_file_path, 'w', encoding='utf-8') as output_file:
#                 output_file.write(f"LangID: {langID}, Description: {description}\n\n")
#                 for parent, key, path, line in mismatched_paths:
#                     path_part = f"Parent: {parent}, Key: {key}, Path: {path}, Line: {line}\n"
#                     output_file.write(path_part)

#     print('Processing completed.')

# process_blob_storage()





























# ye sahi hai bass isme video wala kaam kar raha 
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

# # Load mapping sheet (assuming it's a JSON file)
# def load_mapping_sheet(mapping_file_path='/home/nitish/nitish azure folder/mapingsheet.json'):
#     with open(mapping_file_path, 'r', encoding='utf-8') as file:
#         return json.load(file)

# # Get description from the mapping sheet using langID
# def get_description_from_mapping(langID, mapping_sheet):
#     return mapping_sheet.get(langID, {}).get('description', 'Description not found')

# # Function to find the main directory from video paths, ignoring '/content/assets/videos/'
# def find_main_video_directory(data):
#     video_directories = []

#     def extract_video_directories(obj, parent_key=""):
#         if isinstance(obj, dict):
#             for key, value in obj.items():
#                 # Collect video paths under the 'videos' key and look for 'src'
#                 if parent_key == 'videos' and key == 'src':
#                     # Ignore the first three directories ('/content/assets/videos/')
#                     path_parts = value.split('/')
#                     if len(path_parts) > 3 and path_parts[1] == 'content' and path_parts[2] == 'assets' and path_parts[3] == 'videos':
#                         main_directory = path_parts[4] if len(path_parts) > 4 else ""
#                         if main_directory:
#                             video_directories.append(main_directory)

#                 # Traverse nested dictionaries and lists
#                 if isinstance(value, (dict, list)):
#                     extract_video_directories(value, parent_key=key if key == 'videos' else parent_key)

#         elif isinstance(obj, list):
#             for item in obj:
#                 extract_video_directories(item, parent_key=parent_key)

#     extract_video_directories(data)

#     # Find the most frequent base directory (main directory) for videos
#     most_common_directory = Counter(video_directories).most_common(1)
#     return most_common_directory[0][0] if most_common_directory else None

# # Function to validate paths for specified parent keys (videos and images)
# def validate_paths(data, line_info, main_video_directory, main_image_directory):
#     mismatched_paths = []
#     mismatched_video_paths = []  # List to collect mismatched video paths
#     mismatched_image_paths = []  # List to collect mismatched image paths

#     def traverse(obj, parent_key="", current_line=0):
#         if isinstance(obj, dict):
#             # Check for "Image" key (same logic as videos)
#             if parent_key == 'Image':
#                 if 'src' in obj:
#                     image_path = obj['src']
#                     # Ignore '/content/assets/images/' part when checking the path
#                     if image_path.startswith('/content/assets/images/'):
#                         cleaned_image_path = image_path.split('/', 4)[-1]  # Remove '/content/assets/images/'
#                         if main_image_directory and main_image_directory not in cleaned_image_path:
#                             mismatched_image_paths.append((parent_key, 'src', image_path, line_info.get(current_line, "Line info not available")))

#             # Check for "videos"
#             elif parent_key == 'videos':
#                 if 'src' in obj:
#                     video_path = obj['src']
#                     # Ignore '/content/assets/videos/' part when checking the path
#                     if video_path.startswith('/content/assets/videos/'):
#                         cleaned_video_path = video_path.split('/', 4)[-1]  # Remove '/content/assets/videos/'
#                         if main_video_directory and main_video_directory not in cleaned_video_path:
#                             mismatched_video_paths.append((parent_key, 'src', video_path, line_info.get(current_line, "Line info not available")))

#             # Traverse nested dictionaries and lists
#             for key, value in obj.items():
#                 if isinstance(value, (dict, list)):
#                     traverse(value, parent_key=key if key in ['Image', 'videos'] else parent_key, current_line=current_line)

#                 current_line += 1
#         elif isinstance(obj, list):
#             for index, item in enumerate(obj):
#                 traverse(item, parent_key=parent_key, current_line=current_line)
#                 current_line += 1

#     traverse(data)
#     return mismatched_paths, mismatched_video_paths, mismatched_image_paths  # Return all mismatched paths

# def process_blob_storage():
#     # Load the mapping sheet
#     mapping_sheet = load_mapping_sheet()

#     # Initialize Azure Blob client
#     blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
#     container_client = blob_service_client.get_container_client(SOURCE_CONTAINER)

#     for blob in container_client.list_blobs():
#         if blob.name.endswith('bundle.json'):
#             folder_name = os.path.dirname(blob.name)
#             langID = os.path.basename(folder_name)  # Assuming langID is part of the folder name

#             # Get description from mapping sheet
#             description = get_description_from_mapping(langID, mapping_sheet)
#             print(f"LangID: {langID}, Description: {description}")
            
#             # Process the blob data
#             blob_client = container_client.get_blob_client(blob)
#             json_data = blob_client.download_blob().readall()
#             json_data = json.loads(json_data)

#             # Process video and image directories using the mapping sheet's asset version
#             asset_versions = mapping_sheet.get(langID, {}).get('asset_version', '').split(', ')
#             main_video_directory = asset_versions[1] if len(asset_versions) > 1 else ""
#             main_image_directory = asset_versions[0] if len(asset_versions) > 0 else ""

#             # Find mismatched paths for both videos and images
#             json_data_lines = json.dumps(json_data, indent=4).splitlines()
#             line_info = {i: line.strip() for i, line in enumerate(json_data_lines)}
#             mismatched_paths, mismatched_video_paths, mismatched_image_paths = validate_paths(
#                 json_data, line_info, main_video_directory, main_image_directory
#             )

#             # Save the mismatched paths for this langID
#             mismatch_file_path = f'mismatched_paths_{langID}.txt'
#             with open(mismatch_file_path, 'w', encoding='utf-8') as output_file:
#                 output_file.write(f"LangID: {langID}, Description: {description}\n\n")
#                 for parent, key, path, line in mismatched_paths + mismatched_video_paths + mismatched_image_paths:
#                     path_part = f"Parent: {parent}, Key: {key}, Path: {path},\n"
#                     output_file.write(path_part)

#     print('Processing completed.')

# process_blob_storage()













# isme wo lang id or name bata raha h mapping sheet se leke 
# import os
# import json
# from azure.storage.blob import BlobServiceClient
# from dotenv import load_dotenv

# # Load environment variables from .env file
# load_dotenv()

# # Get connection string from environment variables
# AZURE_CONNECTION_STRING = os.getenv("AZURE_CONNECTION_STRING")
# SOURCE_CONTAINER = os.getenv("SOURCE_CONTAINER")

# # Load mapping sheet (assuming it's a JSON file)
# def load_mapping_sheet(mapping_file_path='/home/nitish/nitish azure folder/mapingsheet.json'):
#     with open(mapping_file_path, 'r', encoding='utf-8') as file:
#         return json.load(file)

# # Get description from the mapping sheet using langID
# def get_description_from_mapping(langID, mapping_sheet):
#     return mapping_sheet.get(langID, {}).get('description', 'Description not found')

# def process_blob_storage():
#     # Load the mapping sheet
#     mapping_sheet = load_mapping_sheet()

#     # Initialize Azure Blob client
#     blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
#     container_client = blob_service_client.get_container_client(SOURCE_CONTAINER)

#     for blob in container_client.list_blobs():
#         if blob.name.endswith('bundle.json'):
#             folder_name = os.path.dirname(blob.name)
#             langID = os.path.basename(folder_name)  # Assuming langID is part of the folder name

#             # Get description from mapping sheet
#             description = get_description_from_mapping(langID, mapping_sheet)
#             print(f"LangID: {langID}, Description: {description}")
            
#             # Proceed with further processing (validation of paths, etc.)
#             blob_client = container_client.get_blob_client(blob)
#             json_data = blob_client.download_blob().readall()
#             json_data = json.loads(json_data)

#             # Process the rest of your logic (such as validating paths, handling video and image sources, etc.)
#             # This part remains the same as in your initial code.

#     print('Processing completed.')

# process_blob_storage()
