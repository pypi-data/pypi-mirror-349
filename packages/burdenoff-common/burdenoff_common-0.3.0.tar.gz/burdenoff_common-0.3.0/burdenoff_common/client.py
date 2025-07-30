from typing import Dict, Optional, Any, List, Union

from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport
import jwt

from burdenoff_common.auth import Auth
from burdenoff_common.workspace import Workspace
from burdenoff_common.project import Project
from burdenoff_common.billing.payment import Payment
from burdenoff_common.billing.quota import Quota
from burdenoff_common.billing.usage import Usage
from burdenoff_common.billing.plan import Plan
from burdenoff_common.billing.addon import Addon
from burdenoff_common.billing.billing import Billing
from burdenoff_common.permissions import permissions


class WorkspaceClient:
    """
    Main client for the Burdenoff Common SDK.
    Handles authentication and provides access to all services.
    """
    
    def __init__(self, endpoint: str, api_key: Optional[str] = None, token: Optional[str] = None):
        """
        Initialize the Workspace client.
        
        Args:
            endpoint: GraphQL API endpoint URL
            api_key: Optional API key for authentication
            token: Optional JWT token for authentication
        """
        self.endpoint = endpoint
        self.api_key = api_key
        self.token = token
        self._client = None
        self._headers = {}
        
        # Set up authentication headers if provided
        if api_key:
            self._headers["X-API-Key"] = api_key
        if token:
            self._headers["Authorization"] = f"Bearer {token}"
            
        # Initialize service modules
        self.auth = Auth(self)
        self.workspace = Workspace(self)
        self.project = Project(self)
        
        # Initialize billing modules
        self.payment = Payment(self)
        self.quota = Quota(self)
        self.usage = Usage(self)
        self.plan = Plan(self)
        self.addon = Addon(self)
        self.billing = Billing(self)
        
        # Initialize permissions module
        self.permissions = permissions.initialize(endpoint)
        
    @property
    def client(self) -> Client:
        """
        Returns the GQL client with current authentication.
        Lazy-loads the client when needed.
        """
        if not self._client:
            transport = RequestsHTTPTransport(
                url=self.endpoint,
                headers=self._headers,
                use_json=True,
            )
            self._client = Client(transport=transport, fetch_schema_from_transport=True)
        return self._client
    
    def set_token(self, token: str) -> None:
        """
        Set authentication token and update headers.
        
        Args:
            token: JWT authentication token
        """
        self.token = token
        self._headers["Authorization"] = f"{token}"
        # Reset client to apply new headers
        self._client = None
        
    def execute(self, query: str, variables: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Execute a GraphQL query or mutation.
        
        Args:
            query: GraphQL query or mutation string
            variables: Optional variables for the query
            
        Returns:
            Dict containing the GraphQL response
        """
        if variables is None:
            variables = {}
            
        # Convert query string to gql object
        gql_query = gql(query)
        
        # Execute query
        result = self.client.execute(gql_query, variable_values=variables)
        return result
    
    def is_authenticated(self) -> bool:
        """
        Check if client has valid authentication token.
        
        Returns:
            Boolean indicating if client is authenticated
        """
        if not self.token:
            return False
            
        try:
            # Decode token to check if it's valid
            # This only checks format, not if the token is actually valid on the server
            payload = jwt.decode(self.token, options={"verify_signature": False})
            # Check if token is expired
            if "exp" in payload and payload["exp"] > 0:
                return True
            return False
        except:
            return False 