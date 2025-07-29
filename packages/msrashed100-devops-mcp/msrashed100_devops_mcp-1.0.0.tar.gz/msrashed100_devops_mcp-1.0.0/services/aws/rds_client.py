"""
AWS RDS client for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional, List

from services.aws.client import AWSService


class AWSRDSClient:
    """Client for AWS RDS operations."""
    
    def __init__(self, aws_service: AWSService):
        """
        Initialize the AWS RDS client.
        
        Args:
            aws_service: The base AWS service
        """
        self.aws = aws_service
        self.logger = aws_service.logger
        self.client = None
    
    def _get_client(self):
        """Get the RDS client."""
        if self.client is None:
            self.client = self.aws.get_client('rds')
        return self.client
    
    def list_db_instances(self, max_records: int = 100) -> List[Dict[str, Any]]:
        """
        List RDS DB instances.
        
        Args:
            max_records: Maximum number of records to return
            
        Returns:
            List of DB instances
        """
        try:
            client = self._get_client()
            
            response = client.describe_db_instances(MaxRecords=min(max_records, 100))
            instances = response.get('DBInstances', [])
            
            return instances
        except Exception as e:
            self.aws._handle_error("list_db_instances", e)
    
    def get_db_instance(self, db_instance_identifier: str) -> Dict[str, Any]:
        """
        Get details of an RDS DB instance.
        
        Args:
            db_instance_identifier: DB instance identifier
            
        Returns:
            DB instance details
        """
        try:
            client = self._get_client()
            
            response = client.describe_db_instances(DBInstanceIdentifier=db_instance_identifier)
            instances = response.get('DBInstances', [])
            
            if not instances:
                raise ValueError(f"DB instance '{db_instance_identifier}' not found")
            
            return instances[0]
        except Exception as e:
            self.aws._handle_error(f"get_db_instance({db_instance_identifier})", e)
    
    def list_db_clusters(self, max_records: int = 100) -> List[Dict[str, Any]]:
        """
        List RDS DB clusters.
        
        Args:
            max_records: Maximum number of records to return
            
        Returns:
            List of DB clusters
        """
        try:
            client = self._get_client()
            
            response = client.describe_db_clusters(MaxRecords=min(max_records, 100))
            clusters = response.get('DBClusters', [])
            
            return clusters
        except Exception as e:
            self.aws._handle_error("list_db_clusters", e)
    
    def get_db_cluster(self, db_cluster_identifier: str) -> Dict[str, Any]:
        """
        Get details of an RDS DB cluster.
        
        Args:
            db_cluster_identifier: DB cluster identifier
            
        Returns:
            DB cluster details
        """
        try:
            client = self._get_client()
            
            response = client.describe_db_clusters(DBClusterIdentifier=db_cluster_identifier)
            clusters = response.get('DBClusters', [])
            
            if not clusters:
                raise ValueError(f"DB cluster '{db_cluster_identifier}' not found")
            
            return clusters[0]
        except Exception as e:
            self.aws._handle_error(f"get_db_cluster({db_cluster_identifier})", e)
    
    def list_db_parameter_groups(self, max_records: int = 100) -> List[Dict[str, Any]]:
        """
        List RDS DB parameter groups.
        
        Args:
            max_records: Maximum number of records to return
            
        Returns:
            List of DB parameter groups
        """
        try:
            client = self._get_client()
            
            response = client.describe_db_parameter_groups(MaxRecords=min(max_records, 100))
            parameter_groups = response.get('DBParameterGroups', [])
            
            return parameter_groups
        except Exception as e:
            self.aws._handle_error("list_db_parameter_groups", e)
    
    def get_db_parameter_group(self, db_parameter_group_name: str) -> Dict[str, Any]:
        """
        Get details of an RDS DB parameter group.
        
        Args:
            db_parameter_group_name: DB parameter group name
            
        Returns:
            DB parameter group details
        """
        try:
            client = self._get_client()
            
            response = client.describe_db_parameter_groups(DBParameterGroupName=db_parameter_group_name)
            parameter_groups = response.get('DBParameterGroups', [])
            
            if not parameter_groups:
                raise ValueError(f"DB parameter group '{db_parameter_group_name}' not found")
            
            return parameter_groups[0]
        except Exception as e:
            self.aws._handle_error(f"get_db_parameter_group({db_parameter_group_name})", e)
    
    def list_db_parameters(self, db_parameter_group_name: str, source: Optional[str] = None, 
                         max_records: int = 100) -> List[Dict[str, Any]]:
        """
        List parameters in an RDS DB parameter group.
        
        Args:
            db_parameter_group_name: DB parameter group name
            source: Parameter source (user, system, engine-default)
            max_records: Maximum number of records to return
            
        Returns:
            List of parameters
        """
        try:
            client = self._get_client()
            
            params = {
                'DBParameterGroupName': db_parameter_group_name,
                'MaxRecords': min(max_records, 100)
            }
            if source:
                params['Source'] = source
            
            response = client.describe_db_parameters(**params)
            parameters = response.get('Parameters', [])
            
            return parameters
        except Exception as e:
            self.aws._handle_error(f"list_db_parameters({db_parameter_group_name})", e)
    
    def list_db_subnet_groups(self, max_records: int = 100) -> List[Dict[str, Any]]:
        """
        List RDS DB subnet groups.
        
        Args:
            max_records: Maximum number of records to return
            
        Returns:
            List of DB subnet groups
        """
        try:
            client = self._get_client()
            
            response = client.describe_db_subnet_groups(MaxRecords=min(max_records, 100))
            subnet_groups = response.get('DBSubnetGroups', [])
            
            return subnet_groups
        except Exception as e:
            self.aws._handle_error("list_db_subnet_groups", e)
    
    def get_db_subnet_group(self, db_subnet_group_name: str) -> Dict[str, Any]:
        """
        Get details of an RDS DB subnet group.
        
        Args:
            db_subnet_group_name: DB subnet group name
            
        Returns:
            DB subnet group details
        """
        try:
            client = self._get_client()
            
            response = client.describe_db_subnet_groups(DBSubnetGroupName=db_subnet_group_name)
            subnet_groups = response.get('DBSubnetGroups', [])
            
            if not subnet_groups:
                raise ValueError(f"DB subnet group '{db_subnet_group_name}' not found")
            
            return subnet_groups[0]
        except Exception as e:
            self.aws._handle_error(f"get_db_subnet_group({db_subnet_group_name})", e)
    
    def list_db_snapshots(self, db_instance_identifier: Optional[str] = None, 
                        snapshot_type: Optional[str] = None, max_records: int = 100) -> List[Dict[str, Any]]:
        """
        List RDS DB snapshots.
        
        Args:
            db_instance_identifier: DB instance identifier (optional)
            snapshot_type: Snapshot type (optional)
            max_records: Maximum number of records to return
            
        Returns:
            List of DB snapshots
        """
        try:
            client = self._get_client()
            
            params = {'MaxRecords': min(max_records, 100)}
            if db_instance_identifier:
                params['DBInstanceIdentifier'] = db_instance_identifier
            if snapshot_type:
                params['SnapshotType'] = snapshot_type
            
            response = client.describe_db_snapshots(**params)
            snapshots = response.get('DBSnapshots', [])
            
            return snapshots
        except Exception as e:
            self.aws._handle_error("list_db_snapshots", e)
    
    def get_db_snapshot(self, db_snapshot_identifier: str) -> Dict[str, Any]:
        """
        Get details of an RDS DB snapshot.
        
        Args:
            db_snapshot_identifier: DB snapshot identifier
            
        Returns:
            DB snapshot details
        """
        try:
            client = self._get_client()
            
            response = client.describe_db_snapshots(DBSnapshotIdentifier=db_snapshot_identifier)
            snapshots = response.get('DBSnapshots', [])
            
            if not snapshots:
                raise ValueError(f"DB snapshot '{db_snapshot_identifier}' not found")
            
            return snapshots[0]
        except Exception as e:
            self.aws._handle_error(f"get_db_snapshot({db_snapshot_identifier})", e)
    
    def list_db_cluster_snapshots(self, db_cluster_identifier: Optional[str] = None, 
                                snapshot_type: Optional[str] = None, 
                                max_records: int = 100) -> List[Dict[str, Any]]:
        """
        List RDS DB cluster snapshots.
        
        Args:
            db_cluster_identifier: DB cluster identifier (optional)
            snapshot_type: Snapshot type (optional)
            max_records: Maximum number of records to return
            
        Returns:
            List of DB cluster snapshots
        """
        try:
            client = self._get_client()
            
            params = {'MaxRecords': min(max_records, 100)}
            if db_cluster_identifier:
                params['DBClusterIdentifier'] = db_cluster_identifier
            if snapshot_type:
                params['SnapshotType'] = snapshot_type
            
            response = client.describe_db_cluster_snapshots(**params)
            snapshots = response.get('DBClusterSnapshots', [])
            
            return snapshots
        except Exception as e:
            self.aws._handle_error("list_db_cluster_snapshots", e)
    
    def get_db_cluster_snapshot(self, db_cluster_snapshot_identifier: str) -> Dict[str, Any]:
        """
        Get details of an RDS DB cluster snapshot.
        
        Args:
            db_cluster_snapshot_identifier: DB cluster snapshot identifier
            
        Returns:
            DB cluster snapshot details
        """
        try:
            client = self._get_client()
            
            response = client.describe_db_cluster_snapshots(
                DBClusterSnapshotIdentifier=db_cluster_snapshot_identifier
            )
            snapshots = response.get('DBClusterSnapshots', [])
            
            if not snapshots:
                raise ValueError(f"DB cluster snapshot '{db_cluster_snapshot_identifier}' not found")
            
            return snapshots[0]
        except Exception as e:
            self.aws._handle_error(f"get_db_cluster_snapshot({db_cluster_snapshot_identifier})", e)