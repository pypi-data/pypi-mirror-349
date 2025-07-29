"""
AWS S3 tools for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional, List
from mcp.server.fastmcp import FastMCP

from services.aws.service import AWSServiceManager
from tools.aws.base_tools import AWSBaseTools
from utils.logging import setup_logger


class AWSS3Tools(AWSBaseTools):
    """Tools for AWS S3 operations."""
    
    def __init__(self, mcp: FastMCP, aws_service: Optional[AWSServiceManager] = None):
        """
        Initialize AWS S3 tools.
        
        Args:
            mcp: The MCP server instance
            aws_service: The AWS service manager instance (optional)
        """
        super().__init__(mcp, aws_service)
        self.logger = setup_logger("devops_mcp_server.tools.aws.s3")
        self._register_tools()
    
    def _register_tools(self) -> None:
        """Register AWS S3 tools with the MCP server."""
        
        @self.mcp.tool()
        def list_s3_buckets() -> str:
            """
            List S3 buckets.
            
            This tool lists all S3 buckets in your AWS account.
            
            Returns:
                List of S3 buckets in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            try:
                buckets = self.aws_service.s3.list_buckets()
                return self._format_response({"buckets": buckets, "count": len(buckets)})
            except Exception as e:
                self.logger.error(f"Error listing S3 buckets: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_s3_bucket(bucket: str) -> str:
            """
            Get details of an S3 bucket.
            
            This tool retrieves details of an S3 bucket.
            
            Args:
                bucket: Bucket name
                
            Returns:
                Bucket details in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            try:
                bucket_details = self.aws_service.s3.get_bucket(bucket)
                return self._format_response(bucket_details)
            except Exception as e:
                self.logger.error(f"Error getting S3 bucket: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def list_s3_objects(bucket: str, prefix: str = None, max_keys: int = 1000) -> str:
            """
            List objects in an S3 bucket.
            
            This tool lists objects in an S3 bucket, optionally filtered by prefix.
            
            Args:
                bucket: Bucket name
                prefix: Object key prefix (optional)
                max_keys: Maximum number of keys to return (default: 1000, max: 1000)
                
            Returns:
                List of S3 objects in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            # Validate max_keys
            max_keys = min(max(1, max_keys), 1000)
            
            try:
                objects = self.aws_service.s3.list_objects(bucket, prefix, max_keys)
                return self._format_response(objects)
            except Exception as e:
                self.logger.error(f"Error listing S3 objects: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_s3_object(bucket: str, key: str) -> str:
            """
            Get metadata of an S3 object.
            
            This tool retrieves metadata of an S3 object.
            
            Args:
                bucket: Bucket name
                key: Object key
                
            Returns:
                Object metadata in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            try:
                object_metadata = self.aws_service.s3.get_object(bucket, key)
                return self._format_response(object_metadata)
            except Exception as e:
                self.logger.error(f"Error getting S3 object: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_s3_object_url(bucket: str, key: str, expires_in: int = 3600) -> str:
            """
            Generate a presigned URL for an S3 object.
            
            This tool generates a presigned URL for an S3 object.
            
            Args:
                bucket: Bucket name
                key: Object key
                expires_in: URL expiration time in seconds (default: 3600, max: 604800)
                
            Returns:
                Presigned URL in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            # Validate expires_in
            expires_in = min(max(1, expires_in), 604800)  # Max 7 days
            
            try:
                url = self.aws_service.s3.get_object_url(bucket, key, expires_in)
                return self._format_response({"url": url, "expiresIn": expires_in})
            except Exception as e:
                self.logger.error(f"Error generating S3 object URL: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_s3_bucket_size(bucket: str, prefix: str = None) -> str:
            """
            Get the size of an S3 bucket.
            
            This tool calculates the size of an S3 bucket, optionally filtered by prefix.
            
            Args:
                bucket: Bucket name
                prefix: Object key prefix (optional)
                
            Returns:
                Bucket size information in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            try:
                size_info = self.aws_service.s3.get_bucket_size(bucket, prefix)
                return self._format_response(size_info)
            except Exception as e:
                self.logger.error(f"Error getting S3 bucket size: {e}")
                return self._format_error(str(e))