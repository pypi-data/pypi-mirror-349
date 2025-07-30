from typing import Dict, Optional, Any, List, Union


class Workspace:
    """
    Workspace management operations for Burdenoff Server.
    Handles creating, updating, and managing workspaces.
    """
    
    def __init__(self, client):
        """
        Initialize Workspace module.
        
        Args:
            client: WorkspaceClient instance
        """
        self.client = client
    
    def create(self, name: str, tenant_id: str, 
               workspace_type: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a new workspace.
        
        Args:
            name: Workspace name
            tenant_id: ID of the tenant to associate with the workspace
            workspace_type: Optional workspace type/role
            
        Returns:
            Dict containing created workspace details
        """
        query = """
        mutation CreateWorkspace($input: CreateWorkspaceInput!) {
            createWorkspace(input: $input) {
                id
                name
                type
                status
                createdAt
                tenantID
                orgID
            }
        }
        """
        
        input_data = {
            "name": name,
            "tenantID": tenant_id
        }
        
        # Add optional fields if provided
        if workspace_type:
            input_data["type"] = workspace_type
            
        variables = {
            "input": input_data
        }
        
        result = self.client.execute(query, variables)
        return result["createWorkspace"]
    
    def get(self, workspace_id: str) -> Dict[str, Any]:
        """
        Get workspace details by ID.
        
        Args:
            workspace_id: ID of the workspace to retrieve
            
        Returns:
            Dict containing workspace details
        """
        query = """
        query GetWorkspace($id: ID!) {
            workspace(id: $id) {
                id
                name
                type
                status
                createdAt
                updatedAt
                tenantID
                orgID
                workspaceMembers {
                    id
                    userID
                    user {
                        id
                        name
                        email
                    }
                }
            }
        }
        """
        
        variables = {
            "id": workspace_id
        }
        
        result = self.client.execute(query, variables)
        return result["workspace"]
    
    def list(self, tenant_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        List available workspaces, optionally filtered by tenant.
        
        Args:
            tenant_id: Optional tenant ID to filter workspaces
            
        Returns:
            List of workspace details
        """
        query = """
        query ListWorkspaces($tenantID: ID) {
            workspaces(tenantID: $tenantID) {
                id
                name
                type
                status
                createdAt
                tenantID
                orgID
            }
        }
        """
        
        variables = {}
        if tenant_id:
            variables["tenantID"] = tenant_id
            
        result = self.client.execute(query, variables)
        return result["workspaces"]
    
    def update(self, workspace_id: str, name: Optional[str] = None, 
               workspace_type: Optional[str] = None, 
               status: Optional[str] = None) -> Dict[str, Any]:
        """
        Update workspace details.
        
        Args:
            workspace_id: ID of the workspace to update
            name: Optional new workspace name
            workspace_type: Optional new workspace type/role
            status: Optional new workspace status
            
        Returns:
            Dict containing updated workspace details
        """
        query = """
        mutation UpdateWorkspace($input: UpdateWorkspaceInput!) {
            updateWorkspace(input: $input) {
                id
                name
                type
                status
                updatedAt
            }
        }
        """
        
        # Start with required ID
        input_data = {
            "id": workspace_id
        }
        
        # Add optional fields if provided
        if name:
            input_data["name"] = name
        if workspace_type:
            input_data["type"] = workspace_type
        if status:
            input_data["status"] = status
            
        variables = {
            "input": input_data
        }
        
        result = self.client.execute(query, variables)
        return result["updateWorkspace"]
    
    def delete(self, workspace_id: str) -> Dict[str, Any]:
        """
        Delete a workspace.
        
        Args:
            workspace_id: ID of the workspace to delete
            
        Returns:
            Dict containing deleted workspace details
        """
        query = """
        mutation DeleteWorkspace($id: ID!) {
            deleteWorkspace(id: $id) {
                id
                name
                status
            }
        }
        """
        
        variables = {
            "id": workspace_id
        }
        
        result = self.client.execute(query, variables)
        return result["deleteWorkspace"]
    
    def archive(self, workspace_id: str) -> Dict[str, Any]:
        """
        Archive a workspace.
        
        Args:
            workspace_id: ID of the workspace to archive
            
        Returns:
            Dict containing archived workspace details
        """
        query = """
        mutation ArchiveWorkspace($id: ID!) {
            archieveWorkspace(id: $id) {
                id
                name
                status
                updatedAt
            }
        }
        """
        
        variables = {
            "id": workspace_id
        }
        
        result = self.client.execute(query, variables)
        return result["archieveWorkspace"]
    
    def reactivate(self, workspace_id: str) -> Dict[str, Any]:
        """
        Reactivate an archived workspace.
        
        Args:
            workspace_id: ID of the workspace to reactivate
            
        Returns:
            Dict containing reactivated workspace details
        """
        query = """
        mutation ReactivateWorkspace($id: ID!) {
            reActivateWorkspace(id: $id) {
                id
                name
                status
                updatedAt
            }
        }
        """
        
        variables = {
            "id": workspace_id
        }
        
        result = self.client.execute(query, variables)
        return result["reActivateWorkspace"]
    
    def invite_user(self, workspace_id: str, email: str, 
                    roles: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Invite a user to a workspace.
        
        Args:
            workspace_id: ID of the workspace
            email: Email of the user to invite
            roles: Optional roles to assign to the user
            
        Returns:
            Dict containing invitation details
        """
        query = """
        mutation InviteUser($input: InviteUserInput!) {
            inviteUser(input: $input) {
                email
            }
        }
        """
        
        input_data = {
            "workspaceID": workspace_id,
            "email": email
        }
        
        # Add optional roles if provided
        if roles:
            input_data["roles"] = roles
            
        variables = {
            "input": input_data
        }
        
        result = self.client.execute(query, variables)
        return result["inviteUser"]
    
    def handle_invitation(self, invite_token: str, action: str, 
                         user_data: Optional[Dict[str, Any]] = None, 
                         user_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Handle a workspace invitation (accept or reject).
        
        Args:
            invite_token: Invitation token
            action: "accept" or "reject"
            user_data: Optional user registration data (for new users)
            user_id: Optional user ID (for existing users)
            
        Returns:
            Dict containing invitation response details
        """
        query = """
        mutation HandleInvitation($input: InvitationActionInput!) {
            handleInvitation(input: $input) {
                status
                workspace {
                    id
                    name
                }
            }
        }
        """
        
        input_data = {
            "inviteToken": invite_token,
            "action": action
        }
        
        # Add user data if provided (for new users)
        if user_data:
            input_data["user"] = user_data
            
        # Add user ID if provided (for existing users)
        if user_id:
            input_data["userID"] = user_id
            
        variables = {
            "input": input_data
        }
        
        result = self.client.execute(query, variables)
        return result["handleInvitation"]
    
    def switch_workspace(self, workspace_id: str) -> str:
        """
        Switch the active workspace.
        
        Args:
            workspace_id: ID of the workspace to switch to
            
        Returns:
            String confirmation message
        """
        query = """
        mutation SwitchWorkspace($workspaceID: ID!) {
            switchWorkspace(workspaceID: $workspaceID)
        }
        """
        
        variables = {
            "workspaceID": workspace_id
        }
        
        result = self.client.execute(query, variables)
        return result["switchWorkspace"]
    
    def get_members(self, workspace_id: str, page: Optional[int] = None, 
                   items_per_page: Optional[int] = None, 
                   search: Optional[str] = None) -> Dict[str, Any]:
        """
        Get members of a workspace with pagination and search.
        
        Args:
            workspace_id: Workspace ID
            page: Optional page number for pagination
            items_per_page: Optional items per page for pagination
            search: Optional search query for filtering members
            
        Returns:
            Dict containing count and list of workspace members
        """
        query = """
        query GetWorkspaceMembers($workspaceID: ID!, $page: Int, $itemsPerPage: Int, $search: String) {
            getWorkspaceMembers(workspaceID: $workspaceID, page: $page, itemsPerPage: $itemsPerPage, search: $search) {
                count
                members {
                    id
                    userID
                    workspaceID
                    user {
                        id
                        name
                        email
                        profilePicture
                    }
                }
            }
        }
        """
        
        variables = {
            "workspaceID": workspace_id
        }
        
        # Add optional pagination and search parameters
        if page is not None:
            variables["page"] = page
        if items_per_page is not None:
            variables["itemsPerPage"] = items_per_page
        if search:
            variables["search"] = search
            
        result = self.client.execute(query, variables)
        return result["getWorkspaceMembers"] 