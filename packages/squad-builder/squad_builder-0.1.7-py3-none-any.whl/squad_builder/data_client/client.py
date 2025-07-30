"""Main data client implementation for cloud storage access."""

import logging
import requests
from typing import Dict, List, Optional, Union, BinaryIO, IO
import io
from uuid import UUID
from datetime import datetime

logger = logging.getLogger(__name__)

class DataClient:
    """
    Client for interacting with cloud storage via pre-signed URLs.
    Supports file listing, downloading, streaming, and uploading operations.
    """
    
    def __init__(self, api_key: str, organization_id: UUID, environment: str, api_url: str = "https://api.example.com"):
        """
        Initialize the data client.
        
        Args:
            api_key: API key for authentication with the API
            organization_id: UUID of the organization
            environment: Environment name (e.g., 'dev', 'prod')
            api_url: Base URL of the storage API
        """
        self.api_key = api_key
        self.organization_id = organization_id
        self.environment = environment
        self.api_url = api_url
        self.headers = {"X-API-Key": self.api_key}
    
    def _request_presigned_url(self, endpoint: str, params: Dict = None) -> Dict:
        """
        Request a pre-signed URL from the API.
        
        Args:
            endpoint: API endpoint to call
            params: Additional parameters for the request
            
        Returns:
            Response data containing URL and metadata
        """
        url = f"{self.api_url}/storage/{endpoint}"
        # Add organization_id and environment to all requests
        request_params = {
            "organization_id": str(self.organization_id),
            "environment": self.environment
        }
        
        # Add any additional params
        if params:
            request_params.update(params)
            
        try:
            response = requests.get(url, headers=self.headers, params=request_params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Failed to get pre-signed URL for {endpoint}: {str(e)}")
            raise
    
    def list_files(self, prefix: Optional[str] = None) -> List[Dict]:
        """
        List files in storage.
        
        Args:
            prefix: Optional prefix to filter files by
            
        Returns:
            List of file objects with metadata
        """
        params = {}
        if prefix is not None:
            params["prefix"] = prefix
            
        response_data = self._request_presigned_url("list", params)
        
        try:
            list_url = response_data.get("list_url")
            if not list_url:
                logger.error("No list_url returned in response data")
                return []
                
            logger.debug(f"Making request to list_url: {list_url}")
            response = requests.get(list_url)
            response.raise_for_status()
            
            # Check if response has content before trying to parse
            if not response.content:
                logger.warning("Empty response content from list_url")
                return []
                
            # Check content type to determine how to parse the response
            content_type = response.headers.get('content-type', '')
            
            # Handle XML response (common for S3)
            if content_type.startswith('application/xml') or b'<?xml' in response.content[:100]:
                logger.info("Detected XML response, parsing accordingly")
                return self._parse_xml_list_response(response.content)
            
            # Handle JSON response
            elif content_type.startswith('application/json'):
                logger.info("Detected JSON response, parsing accordingly")
                return response.json()
            
            # Try JSON first for unknown content types, fall back to XML
            else:
                logger.info(f"Unknown content type: {content_type}, attempting JSON parse first")
                try:
                    return response.json()
                except requests.exceptions.JSONDecodeError:
                    logger.info("JSON parse failed, attempting XML parse")
                    return self._parse_xml_list_response(response.content)
                
        except requests.RequestException as e:
            logger.error(f"Failed to list files: {str(e)}")
            raise
    
    def _parse_xml_list_response(self, xml_content: bytes) -> List[Dict]:
        """
        Parse XML response from storage providers like S3.
        
        Args:
            xml_content: XML content to parse
            
        Returns:
            List of file objects with metadata
        """
        import xml.etree.ElementTree as ET
        try:
            # Parse the response content
            root = ET.fromstring(xml_content)
            
            # Get the namespace from the root tag
            namespace = ''
            if '{' in root.tag:
                namespace = root.tag.split('}')[0] + '}'
            
            logger.debug(f"XML root tag: {root.tag}")
            logger.debug(f"Using namespace: {namespace}")
            
            files = []
            
            # Find Contents elements (files) with namespace
            for contents in root.findall('.//' + namespace + 'Contents'):
                file_info = {}
                
                key_elem = contents.find('./' + namespace + 'Key')
                if key_elem is not None and key_elem.text:
                    # Skip empty directory markers (keys ending with /)
                    if key_elem.text.endswith('/'):
                        continue
                        
                    file_info["key"] = key_elem.text
                    
                    # Add additional metadata if available
                    size_elem = contents.find('./' + namespace + 'Size')
                    if size_elem is not None and size_elem.text:
                        file_info["size"] = int(size_elem.text)
                        
                    modified_elem = contents.find('./' + namespace + 'LastModified')
                    if modified_elem is not None and modified_elem.text:
                        file_info["last_modified"] = modified_elem.text
                        
                    files.append(file_info)
            
            # Also get any directories (CommonPrefixes)
            for prefix in root.findall('.//' + namespace + 'CommonPrefixes'):
                prefix_elem = prefix.find('./' + namespace + 'Prefix')
                if prefix_elem is not None and prefix_elem.text:
                    files.append({
                        "key": prefix_elem.text,
                        "is_directory": True
                    })
            
            # Get key count for debugging
            key_count_elem = root.find('./' + namespace + 'KeyCount')
            if key_count_elem is not None:
                logger.debug(f"KeyCount in XML: {key_count_elem.text}")
            
            logger.info(f"Successfully parsed XML response, found {len(files)} files")
            return files
        except Exception as xml_err:
            logger.error(f"Failed to parse XML response: {str(xml_err)}")
            logger.debug(f"Exception details: {type(xml_err).__name__}: {str(xml_err)}")
            return []
    
    def download_file(self, file_path: str, destination: str) -> str:
        """
        Download a file from storage to a local destination.
        
        Args:
            file_path: Path to the file in storage
            destination: Local path to save the file
            
        Returns:
            Path to the downloaded file
        """
        response_data = self._request_presigned_url("download", {"file_path": file_path})
        
        try:
            download_url = response_data.get("download_url")
            with requests.get(download_url, stream=True) as response:
                response.raise_for_status()
                with open(destination, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
            return destination
        except requests.RequestException as e:
            logger.error(f"Failed to download file {file_path}: {str(e)}")
            raise
    
    def stream_file(self, file_path: str) -> IO[bytes]:
        """
        Stream a file from storage.
        
        Args:
            file_path: Path to the file in storage
            
        Returns:
            File-like object for streaming
        """
        response_data = self._request_presigned_url("stream", {"file_path": file_path})
        
        try:
            stream_url = response_data.get("stream_url")
            response = requests.get(stream_url, stream=True)
            response.raise_for_status()
            # Create an in-memory bytes buffer
            buffer = io.BytesIO()
            for chunk in response.iter_content(chunk_size=8192):
                buffer.write(chunk)
            # Reset the buffer position to the beginning
            buffer.seek(0)
            return buffer
        except requests.RequestException as e:
            logger.error(f"Failed to stream file {file_path}: {str(e)}")
            raise
    
    def upload_file(self, file_path: str, file_obj: Union[str, BinaryIO], content_type: str = "application/octet-stream") -> Dict:
        """
        Upload a file to storage.
        
        Args:
            file_path: Target path in storage
            file_obj: File object or path to local file to upload
            content_type: Content type of the file (default: application/octet-stream)
            
        Returns:
            Metadata about the uploaded file
        """
        response_data = self._request_presigned_url("upload", {
            "file_path": file_path,
            "content_type": content_type
        })
        
        try:
            upload_url = response_data.get("upload_url")
            headers = {"Content-Type": content_type}
            
            # If file_obj is a string, treat it as a path and open the file
            if isinstance(file_obj, str):
                with open(file_obj, "rb") as f:
                    response = requests.put(upload_url, headers=headers, data=f)
                    response.raise_for_status()
            # Otherwise, treat it as a file-like object
            else:
                response = requests.put(upload_url, headers=headers, data=file_obj)
                response.raise_for_status()
            
            # Return metadata if the response contains it
            if response.headers.get("Content-Type") == "application/json":
                return response.json()
            return {
                "status": "success", 
                "file_path": response_data.get("file_path"),
                "bucket_name": response_data.get("bucket_name"),
                "provider_type": response_data.get("provider_type")
            }
        except requests.RequestException as e:
            logger.error(f"Failed to upload file to {file_path}: {str(e)}")
            raise 