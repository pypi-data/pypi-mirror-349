"""
GitHub Actions tools for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional, List
from mcp.server.fastmcp import FastMCP

from services.github.service import GitHubServiceManager
from tools.github.base_tools import GitHubBaseTools
from utils.logging import setup_logger


class GitHubActionsTools(GitHubBaseTools):
    """Tools for GitHub Actions operations."""
    
    def __init__(self, mcp: FastMCP, github_service: Optional[GitHubServiceManager] = None):
        """
        Initialize GitHub Actions tools.
        
        Args:
            mcp: The MCP server instance
            github_service: The GitHub service manager instance (optional)
        """
        super().__init__(mcp, github_service)
        self.logger = setup_logger("devops_mcp_server.tools.github.actions")
        self._register_tools()
    
    def _register_tools(self) -> None:
        """Register GitHub Actions tools with the MCP server."""
        
        @self.mcp.tool()
        def list_github_workflows(repo_name: str) -> str:
            """
            List workflows in a GitHub repository.
            
            This tool lists workflows in a GitHub repository.
            
            Args:
                repo_name: Repository name (format: "owner/repo")
                
            Returns:
                List of workflows in JSON format
            """
            if not self._check_service_available():
                return self._format_error("GitHub service is not available")
            
            try:
                workflows = self.github_service.actions.list_workflows(repo_name)
                return self._format_response({"workflows": workflows, "count": len(workflows)})
            except Exception as e:
                self.logger.error(f"Error listing GitHub workflows: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_github_workflow(repo_name: str, workflow_id: int) -> str:
            """
            Get details of a workflow in a GitHub repository.
            
            This tool retrieves details of a workflow in a GitHub repository.
            
            Args:
                repo_name: Repository name (format: "owner/repo")
                workflow_id: Workflow ID
                
            Returns:
                Workflow details in JSON format
            """
            if not self._check_service_available():
                return self._format_error("GitHub service is not available")
            
            try:
                workflow = self.github_service.actions.get_workflow(repo_name, workflow_id)
                return self._format_response(workflow)
            except Exception as e:
                self.logger.error(f"Error getting GitHub workflow: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def list_github_workflow_runs(repo_name: str, workflow_id: int = None, 
                                   actor: str = None, branch: str = None,
                                   event: str = None, status: str = None,
                                   max_results: int = 100) -> str:
            """
            List workflow runs in a GitHub repository.
            
            This tool lists workflow runs in a GitHub repository.
            
            Args:
                repo_name: Repository name (format: "owner/repo")
                workflow_id: Workflow ID (optional)
                actor: Filter by actor login (optional)
                branch: Filter by branch (optional)
                event: Filter by event type (optional)
                status: Filter by status (optional)
                max_results: Maximum number of results to return (default: 100, max: 100)
                
            Returns:
                List of workflow runs in JSON format
            """
            if not self._check_service_available():
                return self._format_error("GitHub service is not available")
            
            # Validate max_results
            max_results = min(max(1, max_results), 100)
            
            try:
                runs = self.github_service.actions.list_workflow_runs(
                    repo_name, workflow_id, actor, branch, event, status, max_results
                )
                return self._format_response({"workflowRuns": runs, "count": len(runs)})
            except Exception as e:
                self.logger.error(f"Error listing GitHub workflow runs: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_github_workflow_run(repo_name: str, run_id: int) -> str:
            """
            Get details of a workflow run in a GitHub repository.
            
            This tool retrieves details of a workflow run in a GitHub repository.
            
            Args:
                repo_name: Repository name (format: "owner/repo")
                run_id: Run ID
                
            Returns:
                Workflow run details in JSON format
            """
            if not self._check_service_available():
                return self._format_error("GitHub service is not available")
            
            try:
                run = self.github_service.actions.get_workflow_run(repo_name, run_id)
                return self._format_response(run)
            except Exception as e:
                self.logger.error(f"Error getting GitHub workflow run: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def list_github_workflow_run_jobs(repo_name: str, run_id: int, 
                                       max_results: int = 100) -> str:
            """
            List jobs for a workflow run in a GitHub repository.
            
            This tool lists jobs for a workflow run in a GitHub repository.
            
            Args:
                repo_name: Repository name (format: "owner/repo")
                run_id: Run ID
                max_results: Maximum number of results to return (default: 100, max: 100)
                
            Returns:
                List of workflow run jobs in JSON format
            """
            if not self._check_service_available():
                return self._format_error("GitHub service is not available")
            
            # Validate max_results
            max_results = min(max(1, max_results), 100)
            
            try:
                jobs = self.github_service.actions.list_workflow_run_jobs(
                    repo_name, run_id, max_results
                )
                return self._format_response({"jobs": jobs, "count": len(jobs)})
            except Exception as e:
                self.logger.error(f"Error listing GitHub workflow run jobs: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def list_github_workflow_run_artifacts(repo_name: str, run_id: int, 
                                            max_results: int = 100) -> str:
            """
            List artifacts for a workflow run in a GitHub repository.
            
            This tool lists artifacts for a workflow run in a GitHub repository.
            
            Args:
                repo_name: Repository name (format: "owner/repo")
                run_id: Run ID
                max_results: Maximum number of results to return (default: 100, max: 100)
                
            Returns:
                List of workflow run artifacts in JSON format
            """
            if not self._check_service_available():
                return self._format_error("GitHub service is not available")
            
            # Validate max_results
            max_results = min(max(1, max_results), 100)
            
            try:
                artifacts = self.github_service.actions.list_workflow_run_artifacts(
                    repo_name, run_id, max_results
                )
                return self._format_response({"artifacts": artifacts, "count": len(artifacts)})
            except Exception as e:
                self.logger.error(f"Error listing GitHub workflow run artifacts: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_github_workflow_content(repo_name: str, workflow_id: int) -> str:
            """
            Get content of a workflow file in a GitHub repository.
            
            This tool retrieves content of a workflow file in a GitHub repository.
            
            Args:
                repo_name: Repository name (format: "owner/repo")
                workflow_id: Workflow ID
                
            Returns:
                Workflow file content in JSON format
            """
            if not self._check_service_available():
                return self._format_error("GitHub service is not available")
            
            try:
                content = self.github_service.actions.get_workflow_content(repo_name, workflow_id)
                return self._format_response(content)
            except Exception as e:
                self.logger.error(f"Error getting GitHub workflow content: {e}")
                return self._format_error(str(e))