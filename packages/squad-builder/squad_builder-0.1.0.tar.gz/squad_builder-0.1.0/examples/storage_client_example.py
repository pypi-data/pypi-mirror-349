"""
Example demonstrating the use of the Squad Builder SDK DataClient for storage operations.
"""

import uuid
import os
from squad_builder import DataClient

def main():
    # Initialize the client with all required parameters
    client = DataClient(
        api_key="bodra-123",
        organization_id=uuid.UUID("113a06a8-6ae9-46dd-be95-9d7ae2ee0338"),
        environment="dev",
        api_url="http://localhost:8000"
    )
    
    # List files with a prefix
    print("Listing files...")
    files = client.list_files(prefix="")
    print(f"Found {len(files)} files")
    if files:
        print("First few files:")
        for file in files[:5]:
            print(f"  {file}")
    
    # Download a file
    file_path = "ikigai.jpeg"
    destination = "/Users/gbodra/Desktop/ikigai.jpeg"
    print(f"Downloading {file_path} to {destination}...")
    client.download_file(file_path=file_path, destination=destination)
    print(f"Successfully downloaded to {destination}")
    
    # Upload a file
    upload_path = "uploaded.txt"
    local_file = "local_file_to_upload.txt"
    
    # Create a simple file if it doesn't exist
    if not os.path.exists(local_file):
        with open(local_file, "w") as f:
            f.write("This is a test file for upload.")
    
    print(f"Uploading {local_file} to {upload_path}...")
    result = client.upload_file(
        file_path=upload_path, 
        file_obj=local_file,
        content_type="text/plain"
    )
    print(f"Upload result: {result}")
    
    # Stream a file
    stream_path = "ikigai.jpeg"
    print(f"Streaming {stream_path}...")
    stream = client.stream_file(file_path=stream_path)
    content = stream.read()
    print(f"Streamed content length: {len(content)} bytes")
    
    # Clean up
    if os.path.exists(local_file):
        os.remove(local_file)

if __name__ == "__main__":
    main() 