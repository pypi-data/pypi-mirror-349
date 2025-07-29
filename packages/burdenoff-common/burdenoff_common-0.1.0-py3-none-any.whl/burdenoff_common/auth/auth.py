from typing import Dict, Optional, Any, List, Tuple, Union
import requests


class Auth:
    """
    Authentication operations for the Burdenoff Server.
    Handles JWT verification.
    """
    
    def __init__(self, client):
        """
        Initialize Auth module.
        
        Args:
            client: WorkspaceClient instance
        """
        self.client = client
    
    def verify_jwt(self, token: str) -> bool:
        """
        Verify if a JWT token is valid by calling the verify-jwt endpoint.
        
        Args:
            token: JWT token to verify
            
        Returns:
            Boolean indicating if token is valid
        """
        # Extract the base URL from the GraphQL endpoint to call the REST verify-jwt endpoint
        base_url = self.client.endpoint.rsplit('/graphql', 1)[0]
        verify_endpoint = f"{base_url}/verify-jwt"
        
        # Pass token as a query parameter instead of in the Authorization header
        params = {
            "token": token
        }
        
        try:
            response = requests.get(verify_endpoint, params=params)
            return response.status_code == 200
        except Exception as e:
            return False
            
    def set_token(self, token: str) -> None:
        """
        Set authentication token in the client.
        
        Args:
            token: JWT authentication token
        """
        self.client.set_token(token) 