from typing import List, Dict, Optional, TypedDict, Any, Union
import os
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

# Type definitions
class PermissionResponse(TypedDict):
    hasPermission: bool

class BulkPermissionResponse(TypedDict):
    allow: bool
    permission: str
    scope: str

class PermissionInput(TypedDict):
    permission: str
    scope: str

class PermissionResult(TypedDict):
    allow: bool
    permission: str
    scope: str

# Constants
ENTITY_TYPES = {
    'team': 'team',
    'billingAccount': 'billingAccount',
    'project': 'project',
    'workspace': 'workspace',
    'knowledgeBase': 'knowledgeBase',
    'newsLetter': 'newsLetter',
    'plan': 'plan',
    'supportTicket': 'supportTicket',
    'workflow': 'workflow',
    'bot': 'bot'
}

DEFAULT_PERMISSIONS = {
    'create': 'create',
    'read': 'read',
    'update': 'update',
    'delete': 'delete',
    'all': 'all'
}

DEFAULT_PERMISSION_BASE_STRING = 'https://permissions.burdenoff.com'

class PermissionClient:
    def __init__(self, graphql_endpoint: str, permission_base_string: Optional[str] = None):
        """
        Initialize the Permission client with a GraphQL endpoint and optional permission base string.
        
        Args:
            graphql_endpoint (str): The GraphQL endpoint URL
            permission_base_string (str, optional): The base string for permissions. 
                                                  Defaults to 'https://permissions.burdenoff.com'
        """
        self.graphql_endpoint = graphql_endpoint
        self.permission_base_string = permission_base_string or DEFAULT_PERMISSION_BASE_STRING

    def get_client(self, token: str) -> Client:
        """Create and return a GraphQL client with the given token."""
        transport = RequestsHTTPTransport(
            url=self.graphql_endpoint,
            headers={'Authorization': f'{token}'}
        )
        return Client(transport=transport, fetch_schema_from_transport=True)

    async def create_permissions(
        self,
        entity_id: str,
        entity_type: str,
        scope_name: str,
        token: str,
        child_entity_types: Optional[List[str]] = None,
        custom_permissions: Optional[List[str]] = None,
        workspace_id: Optional[str] = None
    ) -> Optional[Dict]:
        """
        Create permissions for an entity.
        
        Args:
            entity_id (str): The ID of the entity
            entity_type (str): The type of entity (should be one of ENTITY_TYPES)
            scope_name (str): The name of the scope
            token (str): Authentication token
            child_entity_types (List[str], optional): List of child entity types
            custom_permissions (List[str], optional): List of custom permissions
            workspace_id (str, optional): The workspace ID if applicable
            
        Returns:
            Optional[Dict]: The created permission or None if failed
        """
        try:
            client = self.get_client(token)
            mutation = gql("""
                mutation createPermission(
                    $childEntityTypes: [String!]
                    $customPermissions: [String!]
                    $entityID: ID!
                    $entityType: String!
                    $scopeName: String!
                ) {
                    createPermission(
                        entityID: $entityID
                        scopeName: $scopeName
                        childEntityTypes: $childEntityTypes
                        customPermissions: $customPermissions
                        entityType: $entityType
                    )
                }
            """)
            
            variables = {
                'entityID': entity_id,
                'scopeName': scope_name,
                'childEntityTypes': child_entity_types,
                'customPermissions': custom_permissions,
                'entityType': entity_type
            }
            
            result = client.execute(mutation, variable_values=variables)
            return result
        except Exception as e:
            print(f"Create permission failed: {str(e)}")
            return None

    async def check_permission(
        self,
        permission: str,
        scope: str,
        token: str
    ) -> PermissionResponse:
        """
        Check if a permission is allowed for a specific scope.
        
        Args:
            permission (str): The permission to check
            scope (str): The scope to check the permission in
            token (str): Authentication token
            
        Returns:
            PermissionResponse: Dictionary with hasPermission field indicating if permission is allowed
        """
        try:
            client = self.get_client(token)
            query = gql("""
                query hasPermission($permission: String!, $scope: String!) {
                    hasPermission(permission: $permission, scope: $scope)
                }
            """)
            
            variables = {
                'permission': permission,
                'scope': scope
            }
            
            result = client.execute(query, variable_values=variables)
            return result
        except Exception as e:
            print(f"Permission check error: {str(e)}")
            return {'hasPermission': False}

    async def check_permission_bulk(
        self,
        permission_inputs: List[PermissionInput],
        token: str
    ) -> List[PermissionResult]:
        """
        Verify multiple permissions in bulk.
        
        Args:
            permission_inputs (List[PermissionInput]): List of permission inputs, each containing
                                                     permission and scope to verify
            token (str): Authentication token
            
        Returns:
            List[PermissionResult]: List of dictionaries containing allow status, permission,
                                  and scope for each input
        """
        try:
            client = self.get_client(token)
            query = gql("""
                query verifyPermissions($input: [PermissionInput!]!) {
                    verifyPermission(input: $input) {
                        allow
                        permission
                        scope
                    }
                }
            """)
            
            variables = {
                'input': permission_inputs
            }
            
            result = client.execute(query, variable_values=variables)
            return result.get('verifyPermission', [
                {
                    'allow': False,
                    'permission': input_item['permission'],
                    'scope': input_item['scope']
                }
                for input_item in permission_inputs
            ])
        except Exception as e:
            print(f"Permission verification failed: {str(e)}")
            return [
                {
                    'allow': False,
                    'permission': input_item['permission'],
                    'scope': input_item['scope']
                }
                for input_item in permission_inputs
            ]

    async def get_scopes_ids_by_user_and_scope_name(
        self,
        permission: str,
        scope_type: str,
        token: str
    ) -> List[str]:
        """
        Get all scope IDs for a user and scope type.
        
        Args:
            permission (str): The permission to check
            scope_type (str): The type of scope
            token (str): Authentication token
            
        Returns:
            List[str]: List of scope IDs
        """
        try:
            client = self.get_client(token)
            query = gql("""
                query getAllScopesByUserAndScopeType(
                    $permission: String!
                    $permissionBaseString: String!
                    $scopeType: String!
                ) {
                    getAllScopesByUserAndScopeType(
                        permission: $permission
                        permissionBaseString: $permissionBaseString
                        scopeType: $scopeType
                    )
                }
            """)
            
            variables = {
                'permission': permission,
                'scopeType': scope_type,
                'permissionBaseString': self.permission_base_string
            }
            
            result = client.execute(query, variable_values=variables)
            return result.get('getAllScopesByUserAndScopeType', [])
        except Exception as e:
            print(f"Error getting scopes: {str(e)}")
            return []

    async def create_visibility(
        self,
        permission: str,
        scope: str,
        visibility: str,
        visibility_id: str,
        token: str
    ) -> Optional[Dict]:
        """
        Create a visibility entry.
        
        Args:
            permission (str): The permission to set visibility for
            scope (str): The scope of the visibility
            visibility (str): The visibility value
            visibility_id (str): The ID for the visibility
            token (str): Authentication token
            
        Returns:
            Optional[Dict]: The created visibility entry or None if failed
        """
        try:
            client = self.get_client(token)
            mutation = gql("""
                mutation CreateVisibility(
                    $permission: String!,
                    $scope: String!,
                    $visibility: String!,
                    $visibility_id: String!
                ) {
                    createVisibility(
                        input: {
                            visibility: $visibility,
                            visibility_id: $visibility_id,
                            permission: $permission,
                            scope: $scope
                        }
                    ) {
                        id
                    }
                }
            """)
            
            variables = {
                'permission': permission,
                'scope': scope,
                'visibility': visibility,
                'visibility_id': visibility_id
            }
            
            result = client.execute(mutation, variable_values=variables)
            return result.get('createVisibility')
        except Exception as e:
            print(f"Error creating visibility: {str(e)}")
            return None

# Create convenience functions that use a default client
_default_client = None

def initialize(graphql_endpoint: str, permission_base_string: Optional[str] = None):
    """
    Initialize the default client with the GraphQL endpoint and optional permission base string.
    
    Args:
        graphql_endpoint (str): The GraphQL endpoint URL
        permission_base_string (str, optional): The base string for permissions. 
                                              Defaults to 'https://permissions.burdenoff.com'
    """
    global _default_client
    _default_client = PermissionClient(graphql_endpoint, permission_base_string)

def get_client() -> PermissionClient:
    """Get the default permission client."""
    if _default_client is None:
        raise RuntimeError("Permission client not initialized. Call initialize() first.")
    return _default_client

# Convenience functions that use the default client
async def create_permissions(*args, **kwargs):
    return await get_client().create_permissions(*args, **kwargs)

async def check_permission(*args, **kwargs):
    return await get_client().check_permission(*args, **kwargs)

async def check_permission_bulk(*args, **kwargs):
    return await get_client().check_permission_bulk(*args, **kwargs)

async def get_scopes_ids_by_user_and_scope_name(*args, **kwargs):
    return await get_client().get_scopes_ids_by_user_and_scope_name(*args, **kwargs)

async def create_visibility(*args, **kwargs):
    return await get_client().create_visibility(*args, **kwargs) 