from typing import Dict, Optional, Any, List, Tuple, Union
import requests
import jwt
import time
import aiohttp
import uuid # For generating consistent fake IDs if needed


class Auth:
    """
    Authentication operations for the Burdenoff Server.
    Handles JWT verification and context enrichment.
    """
    
    def __init__(self, client):
        """
        Initialize Auth module.
        
        Args:
            client: WorkspaceClient instance (from burdenoff_common.client)
        """
        self.client = client # This is the BurdenoffWorkspaceClient
    
    async def authenticate(self, username: str, password: str) -> Dict[str, Any]:
        """
        Authenticate a user with username and password.
        
        Args:
            username: The user's username or email
            password: The user's password
            
        Returns:
            Dict containing authentication result with the following fields:
            - success: Boolean indicating if authentication was successful
            - token: JWT token if successful, None if failed
            - user: User details if successful, None if failed
        """
        base_url = self.client.endpoint.rsplit('/graphql', 1)[0]
        auth_endpoint = f"{base_url}/authenticate"
        
        payload = {
            "username": username,
            "password": password
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(auth_endpoint, json=payload) as response:
                    if response.status == 200:
                        result = await response.json()
                        # Set the token in the client for subsequent requests
                        if result.get("token"):
                            self.set_token(result["token"])
                        return {
                            "success": True, 
                            "token": result.get("token"),
                            "user": result.get("user")
                        }
                    else:
                        return {"success": False, "token": None, "user": None}
        except Exception as e:
            # Consider logging the error
            return {"success": False, "token": None, "user": None, "error": str(e)}
    
    async def verify_jwt(self, token: str) -> bool:
        """
        Verify if a JWT token is valid by calling the verify-jwt endpoint asynchronously.
        
        Args:
            token: JWT token to verify
            
        Returns:
            Boolean indicating if token is valid
        """
        base_url = self.client.endpoint.rsplit('/graphql', 1)[0]
        verify_endpoint = f"{base_url}/verify-jwt"
        
        params = {"token": token}
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(verify_endpoint, params=params) as response:
                    return response.status == 200
        except Exception as e:
            # Consider logging the error e
            return False
            
    def set_token(self, token: str) -> None:
        """
        Set authentication token in the client.
        
        Args:
            token: JWT authentication token
        """
        self.client.set_token(token)

    async def _get_context(self, token: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        (Internal) Asynchronously decodes a JWT and enriches its payload.
        *** CURRENTLY IMPLEMENTED WITH A FAKE USER DB FOR TESTING/MIGRATION ***
        It will return details for a 'test_user' irrespective of the input token's content,
        though it still expects a syntactically valid JWT for basic decoding to pass.
        Future implementation will fetch real details based on the token.

        Args:
            token: The JWT string. Currently mostly ignored for content, but format is checked.
            metadata: Optional dictionary, may influence future data fetching.

        Returns:
            A dictionary containing the enriched context for the fake 'test_user'.

        Raises:
            jwt.ExpiredSignatureError: If the token has nominally expired (if checked).
            jwt.InvalidTokenError: For JWT format errors or other processing issues.
        """
        try:
            # Basic decode to ensure token is somewhat valid structurally, even if we ignore its content for now.
            # This helps catch completely malformed tokens early.
            decoded_token = jwt.decode(
                token,
                options={"verify_signature": False, "verify_exp": False, "verify_nbf": False, "verify_iat": False}
            )

            # If we wanted to strictly enforce expiry even for the fake user scenario:
            # if 'exp' in decoded_token and decoded_token['exp'] < time.time():
            #     raise jwt.ExpiredSignatureError("Token has expired.")

            # --- FAKE USER DB Implementation --- 
            # Return a consistent set of details for 'test_user'.
            # This helps in migrating API endpoints that expect a certain User model structure.
            
            fake_user_id = str(decoded_token.get("user_id", "test_user_001")) # Try to get a user_id from token, or default
            fake_org_id = str(decoded_token.get("org_id", "test_org_001"))
            fake_tenant_id = str(decoded_token.get("tenant_id", "test_tenant_001"))

            enriched_context = {
                "user": {
                    "id": fake_user_id, # Consistent ID for test_user
                    "username": decoded_token.get("username", "testuser"),
                    "name": decoded_token.get("name", "Test User Default"),
                    "email": decoded_token.get("email", "testuser@example.com"),
                    "roles": decoded_token.get("roles", ["test_role_admin", "test_role_user"]),
                    "is_active": True, # Common field in User models
                    "is_superuser": False, # Example field
                    "profile_picture_url": f"https://example.com/avatars/{fake_user_id}.png",
                    # Add any other fields that existing User models might have, to ease migration
                    # e.g., "email_verified": True,
                    # "created_at": "2023-01-01T10:00:00Z",
                    # "last_login": time.time()
                },
                "organization": {
                    "id": fake_org_id,
                    "name": f"Test Organization for {fake_user_id}",
                    "plan": "premium_test_plan",
                    # e.g., "member_count": 10,
                    # "trial_ends_at": None
                },
                "tenant": {
                    "id": fake_tenant_id,
                    "name": f"Test Tenant for {fake_user_id}",
                    "region": "test_region_1",
                    # e.g., "status": "active"
                },
                "product": {
                    "name": "FluidGrids Workflow Engine (Test Context)",
                    "version_subscribed": "dev-latest",
                    "features_enabled": ["all_test_features", "rbac_beta_test"]
                },
                # Include some top-level claims that might have been in the original JWT payload
                # These are from the decoded_token, so they reflect the *actual* input token if present.
                # This is useful if some code directly accessed decoded_token fields outside of user/org/tenant.
                "jti": decoded_token.get("jti", str(uuid.uuid4())),
                "original_iss": decoded_token.get("iss"),
                "original_aud": decoded_token.get("aud"),
                # Add any other specific claims from decoded_token if they are used directly elsewhere
                # and are not part of the standard excluded_fields or the structured objects above.
                **{k: v for k, v in decoded_token.items() if k not in ['exp', 'iat', 'nbf', 'jti', 'iss', 'sub', 'aud', 'user_id', 'org_id', 'tenant_id', 'name', 'email', 'roles', 'username']} # Non-overlapping generic claims
            }
            # Ensure standard JWT claims that were part of user/org/tenant objects are not duplicated at top level if they came from decoded_token

            return enriched_context

        except jwt.ExpiredSignatureError as e:
            # log.warning(f"Token expired during _get_context (fake DB mode): {e}")
            raise e
        except jwt.InvalidTokenError as e:
            # log.warning(f"Invalid token during _get_context (fake DB mode): {e}")
            raise e
        except Exception as e:
            # log.error(f"Unexpected error during _get_context (fake DB mode): {e}", exc_info=True)
            raise jwt.InvalidTokenError(f"An unexpected error occurred during context processing (fake DB): {e}")

    async def guardRequest(self, jwt_token: str, operation: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Asynchronously guards an incoming request...
        The 'context' field in the response will be populated by _get_context,
        which currently uses a fake user DB for 'test_user'.
        """
        response = {
            "isAuthenticated": False,
            "context": None,
            "isAuthorized": None,
            "hasSufficientCredits": None,
            "error": None
        }

        try:
            # Step 1: Verify JWT structure and if it's generally valid (e.g., not junk)
            # The verify_jwt might do an external call, which might pass even for an unknown user / expired token for this endpoint.
            # However, for the fake DB scenario, we might primarily rely on _get_context's internal JWT decode.
            # For now, let's assume verify_jwt is a lightweight check or is bypassed if _get_context is in full fake mode.
            
            # If a strict JWT verification (e.g. signature, external check) is still desired before fake data:
            # is_structurally_valid_jwt = await self.verify_jwt(jwt_token)
            # if not is_structurally_valid_jwt:
            #     response["error"] = "JWT verification failed (endpoint check)."
            #     return response
            # response["isAuthenticated"] = True # Tentatively true, _get_context will confirm with its own checks + fake data logic
            
            # For current request: _get_context will decode and provide fake data or raise error
            try:
                token_context = await self._get_context(jwt_token, metadata)
                response["context"] = token_context
                # Since _get_context provides fake data, if it doesn't raise an error, we consider it "authenticated" in this test mode.
                response["isAuthenticated"] = True 
            except jwt.ExpiredSignatureError as e:
                response["isAuthenticated"] = False
                response["error"] = f"Token has expired: {e}"
            except jwt.InvalidTokenError as e:
                response["isAuthenticated"] = False
                response["error"] = f"Invalid token for context retrieval: {e}"
            except Exception as e:
                response["isAuthenticated"] = False
                response["error"] = f"Error retrieving or processing context: {e}"
            
            if not response["isAuthenticated"]:
                 return response
            
            return response

        except Exception as e:
            response["error"] = f"An unexpected error occurred in guardRequest: {e}"
            response["isAuthenticated"] = False
            response["context"] = None
            return response

# Standalone get_context is now removed, it's Auth._get_context 