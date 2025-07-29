// ... existing code ...
### login(email, password)

Authenticates a user with their email and password.

**Parameters:**
- `email` (str): The user's email address
- `password` (str): The user's password

**Returns:**
- JWT token string if successful, None if failed

**Example:**

```python
# Request
token = await client.auth.login("user@example.com", "your-secure-password")

# Example Response (Success)
# "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"

# Example Response (Failure)
# None
```

### refresh_token(token)

Refreshes an existing authentication token.

**Parameters:**
- `token` (str): Current authentication token

**Returns:**
- New JWT token string if successful, None if failed

**Example:**

```python
# Request
# Assuming client.token holds a valid, refreshable token
new_token = await client.auth.refresh_token(client.token)

# Example Response (Success)
# "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJleHAiOjE1MTYyNDI2MjJ9.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"

# Example Response (Failure)
# None
```

### logout(token)

Invalidates an authentication token.

**Parameters:**
- `token` (str): Authentication token to invalidate

**Returns:**
- Boolean indicating success

**Example:**

```python
# Request
# Assuming client.token holds a valid token
success = await client.auth.logout(client.token)

# Example Response (Success)
# True

# Example Response (Failure - e.g., token already invalid)
# False
```

### verify_jwt(token)

Verifies if a token is valid by asynchronously calling an external verification endpoint.

**Parameters:**
- `token` (str): Authentication token to verify

**Returns:**
- `bool`: Indicating if token is valid

**Note:** This method is now asynchronous and must be called with `await`. It uses an underlying asynchronous HTTP client (e.g., `aiohttp`).

**Example:**

```python
import asyncio

# Presuming client is an initialized WorkspaceClient with an async-capable Auth class
# async def main():
#     is_valid = await client.auth.verify_jwt("some_jwt_token_string")
#     print(f"Token is valid: {is_valid}")
#
# asyncio.run(main())

# Example Response (Valid Token)
# True

# Example Response (Invalid Token)
# False
```

### ~~get_context(token, metadata=None)~~ (Now an internal method `_get_context` used by `guardRequest`)

~~Asynchronously decodes a JWT and returns its payload...~~
This function has been refactored into an internal method `_get_context` within the `Auth` class. It's used by `guardRequest` to decode the JWT and enrich it with additional user, organization, tenant, and product information. The enriched context is then made available through the `context` field in the `guardRequest` response.

### guardRequest(jwt_token, operation, metadata=None)

This is a central asynchronous method designed to be invoked for every operation that requires protection. It performs initial authentication (via `verify_jwt`) and then retrieves an enriched context (via an internal `_get_context` call). It includes placeholders for future authorization (RBAC) and billing checks.

**Note:** This method is asynchronous and must be called with `await`.

**Parameters:**
- `jwt_token` (str): The JWT string to validate.
- `operation` (str): A string identifying the operation being attempted. This will be used for future RBAC checks (e.g., "create_document", "read_user_profile").
- `metadata` (Optional[Dict[str, Any]]): An optional dictionary for passing additional data. This can influence what details are fetched for the context (e.g., `{"fetch_product_info": True}`) or be used by future RBAC/billing logic.

**Returns:**
- `Dict[str, Any]`: A dictionary containing the results of the checks:
    - `isAuthenticated` (bool): `True` if the `jwt_token` is successfully verified, `False` otherwise.
    - `context` (Optional[Dict[str, Any]]): If `isAuthenticated` is `True` and context retrieval is successful, this field contains an **enriched dictionary**.
        - **Note on Current Implementation (Fake User DB for Migration):** For development and migration purposes, the `_get_context` method (called internally by `guardRequest`) currently returns a **predefined context for a 'test_user'**, largely irrespective of the input token's actual content (though the token must be a syntactically valid JWT). This ensures API endpoints can be refactored to use the new context structure without immediately requiring live backend services for user/org/tenant data. This fake data includes illustrative user, organization, tenant, and product details.
        - In a future production state, this context will be dynamically built based on the validated JWT and real-time calls to backend services for enrichment.
        - The structure includes:
            - Core claims from the JWT (excluding standard JWT-specific claims like `exp`, `iat`).
            - **User Details**: (e.g., `context['user'] = {'id': 'test_user_001', 'name': 'Test User Default', 'email': 'testuser@example.com', 'roles': ['test_role_admin'], 'is_active': True}`).
            - **Organization Details**: (e.g., `context['organization'] = {'id': 'test_org_001', 'name': 'Test Organization for test_user_001', 'plan': 'premium_test_plan'}`).
            - **Tenant Details**: (e.g., `context['tenant'] = {'id': 'test_tenant_001', 'name': 'Test Tenant for test_user_001', 'region': 'test_region_1'}`).
            - **Product/Service Details**: (e.g., `context['product'] = {'name': 'FluidGrids Workflow Engine (Test Context)', 'version_subscribed': 'dev-latest'}`).
        This field is `None` if authentication fails or if context processing encounters an unrecoverable error.
    - `isAuthorized` (Optional[bool]): Placeholder for future RBAC checks. Currently always `None`.
    - `hasSufficientCredits` (Optional[bool]): Placeholder for future billing checks. Currently always `None`.
    - `error` (Optional[str]): A string describing any error encountered.

**Behavior:**
1. Asynchronously calls `await self.verify_jwt(jwt_token)`.
2. If `verify_jwt` fails, `isAuthenticated` is `False`.
3. If `verify_jwt` succeeds, it then asynchronously calls an internal `await self._get_context(jwt_token, metadata)` method.
   - `_get_context` decodes the JWT and currently provides a predefined 'test_user' context with enriched user, organization, tenant, and product details.
   - If `_get_context` fails (e.g., `jwt.ExpiredSignatureError`, `jwt.InvalidTokenError`, or issues during data fetching), `isAuthenticated` may be set to `False`, and an `error` message is populated. The `context` will likely be `None`.

**Example Usage (within the SDK, assuming `client.auth` is an instance of `Auth`):**

```python
import asyncio

# async def main():
#     # Presuming client is an initialized WorkspaceClient
#     # burdenoff_auth_service = client.auth
#     # jwt_token = "your_jwt_token_string"
#     # operation_name = "access_sensitive_data"
#
#     guard_response = await burdenoff_auth_service.guardRequest(jwt_token, operation_name)
#
#     if guard_response["isAuthenticated"] and guard_response["context"] is not None:
#         print(f"User authenticated.")
#         user_info = guard_response["context"].get("user")
#         org_info = guard_response["context"].get("organization")
#         if user_info:
#             print(f"  User ID: {user_info.get('id')}, Name: {user_info.get('name')}")
#         if org_info:
#             print(f"  Organization ID: {org_info.get('id')}, Plan: {org_info.get('plan')}")
#         
#         # Hypothetical check for future RBAC/Billing
#         # if guard_response["isAuthorized"] is not False and guard_response["hasSufficientCredits"] is not False:
#         #      print("Operation can proceed.")
#         # else:
#         #     print(f"Operation cannot proceed. Authz: {guard_response['isAuthorized']}, Credits: {guard_response['hasSufficientCredits']}")
#     else:
#         print(f"Authentication or context processing failed: {guard_response['error']}")
#
# # asyncio.run(main())
```

## FastAPI Integration (FluidGrids Workflow Engine Example)

The `burdenoff-common` SDK, particularly its `Auth` class with `guardRequest`, can be integrated into a FastAPI application to protect endpoints. The `context` provided by `guardRequest` will be enriched as described above.

### 1. Initialization 
(Example for `app.py` lifespan remains largely the same - it initializes `BurdenoffAuth` which now has the enhanced `_get_context` internally.)
```python
# In your FastAPI app.py or similar
# ... (imports and lifespan setup as previously documented) ...
# app.state.burdenoff_auth_service = BurdenoffAuth(client=burdenoff_client)
# ...
```

### 2. Authentication Middleware
(The middleware example remains the same. It populates `request.state.user_context` with the `context` from `guardRequest`.)
```python
# In your middleware/burdenoff_auth_middleware.py
# ... (middleware code as previously documented) ...
# request.state.user_context = guard_response.get("context") 
# ...
```
The `user_context` stored in `request.state.user_context` will now be the richer context object.

### 3. FastAPI Dependencies
(Dependencies remain structurally the same, but the type/content of `user_context` they provide access to is richer.)

**Example (`dependencies.py`):**
```python
# ... (imports as previously documented) ...

# async def get_current_user_context(request: Request) -> Optional[Dict[str, Any]]:
#     # This will now return the enriched context or None
#     return getattr(request.state, 'user_context', None)

# async def require_burdenoff_user_context(request: Request) -> Dict[str, Any]:
#     # This will now return the enriched context or raise an error
#     # ... (logic as previously documented)
#     user_context = getattr(request.state, 'user_context', None)
#     # ... (validation logic)
#     return user_context
```

### 4. Using Dependencies in Routes
Your route handlers can now access the more detailed information from the context.

**Example Route:**
```python
from fastapi import APIRouter, Depends, FastAPI
from typing import Dict, Any, Optional # For type hints

# Assume dependencies are defined as shown previously and imported
# async def require_burdenoff_user_context(request: Request) -> Dict[str, Any]: ...
# async def get_current_user_context(request: Request) -> Optional[Dict[str, Any]]: ...


# app = FastAPI() # Assuming app is defined with lifespan and middleware
# router = APIRouter()

# @router.get("/my-protected-resource")
# async def get_protected_resource(
#     # user_ctx is the enriched context
#     user_ctx: Dict[str, Any] = Depends(require_burdenoff_user_context) 
# ):
#     user_details = user_ctx.get("user", {})
#     org_details = user_ctx.get("organization", {})
#     
#     return {
#         "message": "Hello, this is a protected resource!", 
#         "user_id": user_details.get("id"),
#         "user_email": user_details.get("email"),
#         "organization_name": org_details.get("name"),
#         "raw_jwt_custom_claim": user_ctx.get("custom_claim_from_jwt") # If present
#     }

# @router.get("/my-optional-auth-resource")
# async def get_optional_resource(
#     # user_ctx is the enriched context if user is authenticated
#     user_ctx: Optional[Dict[str, Any]] = Depends(get_current_user_context)
# ):
#     if user_ctx and user_ctx.get("user"):
#         return {
#             "message": "Hello, authenticated user!", 
#             "user_id": user_ctx.get("user").get("id"),
#             "tenant_id": user_ctx.get("tenant", {}).get("id")
#         }
#     return {"message": "Hello, guest! This resource is accessible to all."}

# app.include_router(router, prefix="/api/v1/app") # Example prefix
```

This enriched context allows for more fine-grained decisions and data availability directly after authentication, streamlining access to common user, organization, and tenant information within your API endpoints.

# Example Route (Illustrating access to fake context structure):
# ...
# async def get_protected_resource(
#     user_ctx: Dict[str, Any] = Depends(require_burdenoff_user_context) 
# ):
#     user_details = user_ctx.get("user", {})
#     org_details = user_ctx.get("organization", {})
#     # Accessing fake data like:
#     # user_details.get("id") will be "test_user_001" (or from token if provided)
#     # user_details.get("email") will be "testuser@example.com" (or from token)
#     # org_details.get("plan") will be "premium_test_plan"
#     return { ... }
# ...
