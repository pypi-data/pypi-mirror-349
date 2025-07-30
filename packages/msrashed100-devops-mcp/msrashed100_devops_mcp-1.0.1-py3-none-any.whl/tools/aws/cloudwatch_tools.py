"""
AWS CloudWatch tools for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional

from mcp.server.fastmcp import FastMCP
from services.aws.service import AWSServiceManager
from utils.logging import setup_logger


class AWSCloudWatchTools:
    """Tools for interacting with AWS CloudWatch."""

    def __init__(self, mcp: FastMCP, aws_service: AWSServiceManager):
        """
        Initialize AWS CloudWatch tools.

        Args:
            mcp: The MCP server instance.
            aws_service: The AWS service manager instance.
        """
        self.mcp = mcp
        self.aws_service = aws_service
        self.logger = setup_logger("devops_mcp_server.tools.aws.cloudwatch")
        self._register_tools()

    def _register_tools(self) -> None:
        """Register CloudWatch tools with the MCP server."""

        @self.mcp.tool()
        def list_cloudwatch_log_groups(limit: int = 50) -> Dict[str, Any]:
            """
            List CloudWatch log groups.

            Args:
                limit: Maximum number of log groups to return (default: 50, max: 50 for now)
            
            Returns:
                List of log groups in JSON format
            """
            self.logger.info(f"Listing CloudWatch log groups with limit: {limit}")
            try:
                log_groups = self.aws_service.cloudwatch.list_log_groups(limit=limit)
                return {"log_groups": log_groups, "count": len(log_groups)}
            except Exception as e:
                self.logger.error(f"Error listing CloudWatch log groups: {e}")
                # Consider re-raising or returning an error structure
                return {"error": str(e)}

        self.logger.info("AWS CloudWatch tools registered successfully")