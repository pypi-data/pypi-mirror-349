"""
GitHub tools for the DevOps MCP Server.
"""
from typing import Optional
from mcp.server.fastmcp import FastMCP

from services.github.service import GitHubServiceManager
from tools.github.repo_tools import GitHubRepoTools
from tools.github.issue_tools import GitHubIssueTools
from tools.github.pr_tools import GitHubPRTools
from tools.github.actions_tools import GitHubActionsTools
from utils.logging import setup_logger


class GitHubTools:
    """Tools for interacting with GitHub."""
    
    def __init__(self, mcp: FastMCP, github_service: Optional[GitHubServiceManager] = None):
        """
        Initialize GitHub tools.
        
        Args:
            mcp: The MCP server instance
            github_service: The GitHub service manager instance (optional)
        """
        self.mcp = mcp
        self.github_service = github_service or GitHubServiceManager()
        self.logger = setup_logger("devops_mcp_server.tools.github")
        
        # Initialize specialized tools
        self.repo_tools = GitHubRepoTools(mcp, self.github_service)
        self.issue_tools = GitHubIssueTools(mcp, self.github_service)
        self.pr_tools = GitHubPRTools(mcp, self.github_service)
        self.actions_tools = GitHubActionsTools(mcp, self.github_service)
        
        self._register_tools()
        
        self.logger.info("GitHub tools initialized successfully")
    
    def _register_tools(self) -> None:
        """Register GitHub tools with the MCP server."""
        
        @self.mcp.tool()
        def get_github_rate_limit() -> str:
            """
            Get GitHub API rate limit information.
            
            This tool retrieves GitHub API rate limit information.
            
            Returns:
                Rate limit information in JSON format
            """
            try:
                rate_limit = self.github_service.get_rate_limit()
                return {
                    "core": {
                        "limit": rate_limit["core"]["limit"],
                        "remaining": rate_limit["core"]["remaining"],
                        "reset": rate_limit["core"]["reset"]
                    },
                    "search": {
                        "limit": rate_limit["search"]["limit"],
                        "remaining": rate_limit["search"]["remaining"],
                        "reset": rate_limit["search"]["reset"]
                    },
                    "graphql": {
                        "limit": rate_limit["graphql"]["limit"],
                        "remaining": rate_limit["graphql"]["remaining"],
                        "reset": rate_limit["graphql"]["reset"]
                    }
                }
            except Exception as e:
                self.logger.error(f"Error getting GitHub rate limit: {e}")
                return {"error": str(e)}