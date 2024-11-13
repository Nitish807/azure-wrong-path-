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
                    if image_path.startswith('/content/assets/images/'):
                        cleaned_image_path = image_path.split('/', 4)[-1]  # Remove '/content/assets/images/' prefix
                        if main_image_directory and main_image_directory not in cleaned_image_path:
                            mismatched_paths.append(f"{image_path}:{line_info.get(current_line, 'Line info not available')}")

            # Check for "Videos" key under 'videos'
            elif parent_key.lower() == 'videos':
                if 'src' in obj:
                    video_path = obj['src']
                    if video_path.startswith('/content/assets/videos/'):
                        cleaned_video_path = video_path.split('/', 4)[-1]  # Remove '/content/assets/videos/' prefix
                        if main_video_directory and main_video_directory not in cleaned_video_path:
                            mismatched_paths.append(f"{video_path}:{line_info.get(current_line, 'Line info not available')}")

            # Check for "keyLearningPoints"
            elif parent_key.lower() == 'keylearningpoints':
                if 'image' in obj:
                    if '/key learning point' not in obj['image']:
                        mismatched_paths.append(f"{obj['image']}:{line_info.get(current_line, 'Line info not available')}")

            # Check for "actionCards"
            elif parent_key.lower() == 'actioncards':
                if 'href' in obj:
                    if '/action card' not in obj['href']:
                        mismatched_paths.append(f"{obj['href']}:{line_info.get(current_line, 'Line info not available')}")

            # Check for "procedures"
            elif parent_key.lower() == 'procedures':
                if 'image' in obj:
                    if '/procedure' not in obj['image']:
                        mismatched_paths.append(f"{obj['image']}:{line_info.get(current_line, 'Line info not available')}")

            # Traverse nested dictionaries and lists
            for key, value in obj.items():
                if isinstance(value, (dict, list)):
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
                for path_info in mismatched_paths:
                    output_file.write(f"{path_info}\n")

    print('Processing completed.')

process_blob_storage()
