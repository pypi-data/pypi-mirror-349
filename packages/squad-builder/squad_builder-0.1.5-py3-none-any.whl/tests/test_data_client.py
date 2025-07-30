"""Tests for the DataClient class."""

import json
import unittest
from unittest.mock import MagicMock, patch

from squad_builder.data_client import DataClient, S3Provider, AzureBlobProvider, GCPStorageProvider

class TestDataClient(unittest.TestCase):
    """Test cases for the DataClient class."""
    
    @patch('requests.get')
    def test_init_and_s3_configuration(self, mock_get):
        """Test initialization with S3 provider configuration."""
        # Mock API response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "provider_type": "s3",
            "provider_config": {
                "access_key_id": "test_key",
                "secret_access_key": "test_secret",
                "region": "us-west-2",
                "bucket_name": "test-bucket"
            }
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response
        
        # Mock boto3 import and S3 provider
        with patch('squad_builder.data_client.client.S3Provider', autospec=True) as mock_s3_provider:
            # Create client
            client = DataClient(api_key="test_api_key")
            
            # Verify API call
            mock_get.assert_called_once()
            self.assertEqual(
                mock_get.call_args[1]['headers'],
                {"Authorization": "Bearer test_api_key"}
            )
            
            # Verify provider creation
            mock_s3_provider.assert_called_once()
            
    @patch('requests.get')
    def test_init_and_azure_configuration(self, mock_get):
        """Test initialization with Azure Blob provider configuration."""
        # Mock API response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "provider_type": "azure",
            "provider_config": {
                "connection_string": "test_connection_string",
                "container_name": "test-container"
            }
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response
        
        # Mock Azure provider
        with patch('squad_builder.data_client.client.AzureBlobProvider', autospec=True) as mock_azure_provider:
            # Create client
            client = DataClient(api_key="test_api_key")
            
            # Verify provider creation
            mock_azure_provider.assert_called_once()
            
    @patch('requests.get')
    def test_init_and_gcp_configuration(self, mock_get):
        """Test initialization with GCP Storage provider configuration."""
        # Mock API response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "provider_type": "gcp",
            "provider_config": {
                "bucket_name": "test-gcp-bucket"
            }
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response
        
        # Mock GCP provider
        with patch('squad_builder.data_client.client.GCPStorageProvider', autospec=True) as mock_gcp_provider:
            # Create client
            client = DataClient(api_key="test_api_key")
            
            # Verify provider creation
            mock_gcp_provider.assert_called_once()
            
    @patch('requests.get')
    def test_list_files(self, mock_get):
        """Test list_files method."""
        # Mock API response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "provider_type": "s3",
            "provider_config": {"bucket_name": "test-bucket"}
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response
        
        # Mock provider
        mock_provider = MagicMock()
        mock_provider.list_files.return_value = [
            {"name": "file1.txt", "size": 100, "last_modified": "2023-01-01T00:00:00", "provider": "s3"}
        ]
        
        with patch('squad_builder.data_client.client.S3Provider', return_value=mock_provider):
            client = DataClient(api_key="test_api_key")
            result = client.list_files(prefix="test/")
            
            # Verify list_files was called
            mock_provider.list_files.assert_called_once_with("test/")
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]["name"], "file1.txt")
            
    @patch('requests.get')
    def test_download_file(self, mock_get):
        """Test download_file method."""
        # Mock API response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "provider_type": "s3",
            "provider_config": {"bucket_name": "test-bucket"}
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response
        
        # Mock provider
        mock_provider = MagicMock()
        mock_provider.download_file.return_value = "/local/path/file.txt"
        
        with patch('squad_builder.data_client.client.S3Provider', return_value=mock_provider):
            client = DataClient(api_key="test_api_key")
            result = client.download_file("remote/path/file.txt", "/local/path/file.txt")
            
            # Verify download_file was called
            mock_provider.download_file.assert_called_once()
            self.assertEqual(result, "/local/path/file.txt")
            
    @patch('requests.get')
    def test_stream_file(self, mock_get):
        """Test stream_file method."""
        # Mock API response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "provider_type": "s3",
            "provider_config": {"bucket_name": "test-bucket"}
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response
        
        # Mock provider
        mock_provider = MagicMock()
        mock_stream = MagicMock()
        mock_provider.stream_file.return_value = mock_stream
        
        with patch('squad_builder.data_client.client.S3Provider', return_value=mock_provider):
            client = DataClient(api_key="test_api_key")
            result = client.stream_file("remote/path/file.txt")
            
            # Verify stream_file was called
            mock_provider.stream_file.assert_called_once()
            self.assertEqual(result, mock_stream)
            
    @patch('requests.get')
    def test_unsupported_provider(self, mock_get):
        """Test handling of unsupported provider type."""
        # Mock API response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "provider_type": "unsupported",
            "provider_config": {}
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response
        
        # Verify ValueError is raised
        with self.assertRaises(ValueError):
            client = DataClient(api_key="test_api_key")


if __name__ == '__main__':
    unittest.main() 