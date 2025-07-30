"""
AWS CloudWatch Client.
"""
from typing import Dict, Any, List
import boto3
from botocore.exceptions import ClientError

from utils.logging import setup_logger


class CloudWatchClient:
    """Client for interacting with AWS CloudWatch."""

    def __init__(self, region_name: str = "us-east-1"):
        """
        Initialize CloudWatch client.

        Args:
            region_name: AWS region name
        """
        self.client = boto3.client("logs", region_name=region_name)
        self.logger = setup_logger("devops_mcp_server.services.aws.cloudwatch")

    def list_log_groups(self, limit: int = 50) -> List[Dict[str, Any]]:
        """
        List CloudWatch log groups.

        Args:
            limit: Maximum number of log groups to return

        Returns:
            List of log groups
        """
        try:
            log_groups = []
            paginator = self.client.get_paginator('describe_log_groups')
            page_iterator = paginator.paginate(PaginationConfig={'MaxItems': limit})
            for page in page_iterator:
                log_groups.extend(page.get("logGroups", []))
            self.logger.info(f"Successfully listed {len(log_groups)} CloudWatch log groups.")
            return log_groups
        except ClientError as e:
            self.logger.error(f"Error listing CloudWatch log groups: {e}")
            raise