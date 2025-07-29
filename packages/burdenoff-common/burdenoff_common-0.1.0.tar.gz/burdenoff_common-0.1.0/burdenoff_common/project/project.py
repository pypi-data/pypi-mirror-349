from typing import Dict, Optional, Any, List, Union


class Project:
    """
    Project management operations for Burdenoff Server.
    Handles creating, updating, and managing projects.
    """
    
    def __init__(self, client):
        """
        Initialize Project module.
        
        Args:
            client: WorkspaceClient instance
        """
        self.client = client
    
    def create(self, name: str) -> Dict[str, Any]:
        """
        Create a new project in the current workspace.
        
        Args:
            name: Project name
            
        Returns:
            Dict containing created project details
        """
        query = """
        mutation CreateProject($input: createProjectInput!) {
            createProject(input: $input) {
                id
                name
                workspaceID
                userID
                key
                createdAt
                archived
            }
        }
        """
        
        variables = {
            "input": {
                "name": name
            }
        }
        
        result = self.client.execute(query, variables)
        return result["createProject"]
    
    def get(self, project_id: str) -> Dict[str, Any]:
        """
        Get project details by ID.
        
        Args:
            project_id: ID of the project to retrieve
            
        Returns:
            Dict containing project details
        """
        query = """
        query GetProject($id: ID!) {
            getProject(id: $id) {
                id
                name
                workspaceID
                userID
                key
                createdAt
                archived
                projectMembers {
                    id
                    userID
                    role
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
            "id": project_id
        }
        
        result = self.client.execute(query, variables)
        return result["getProject"]
    
    def list_by_workspaces(self, workspace_ids: List[str]) -> List[Dict[str, Any]]:
        """
        List projects for specified workspaces.
        
        Args:
            workspace_ids: List of workspace IDs
            
        Returns:
            List of workspace projects with their IDs and project lists
        """
        query = """
        query GetWorkspaceProjects($workspaceIDs: [ID!]) {
            getWorkspaceProjects(workspaceIDs: $workspaceIDs) {
                workspaceID
                projects {
                    id
                    name
                    key
                    createdAt
                    archived
                    workspaceID
                    userID
                }
            }
        }
        """
        
        variables = {
            "workspaceIDs": workspace_ids
        }
        
        result = self.client.execute(query, variables)
        return result["getWorkspaceProjects"]
    
    def update(self, project_id: str, name: str) -> Dict[str, Any]:
        """
        Update project details.
        
        Args:
            project_id: ID of the project to update
            name: New project name
            
        Returns:
            Dict containing updated project details
        """
        query = """
        mutation EditProject($input: editProjectInput!) {
            editProject(input: $input) {
                id
                name
                workspaceID
                key
                createdAt
                archived
            }
        }
        """
        
        variables = {
            "input": {
                "id": project_id,
                "name": name
            }
        }
        
        result = self.client.execute(query, variables)
        return result["editProject"]
    
    def archive(self, project_id: str) -> Dict[str, Any]:
        """
        Archive a project.
        
        Args:
            project_id: ID of the project to archive
            
        Returns:
            Dict containing archived project details
        """
        query = """
        mutation ArchiveProject($id: ID!) {
            archiveProject(id: $id) {
                id
                name
                workspaceID
                archived
            }
        }
        """
        
        variables = {
            "id": project_id
        }
        
        result = self.client.execute(query, variables)
        return result["archiveProject"]
    
    def unarchive(self, project_id: str) -> Dict[str, Any]:
        """
        Unarchive a project.
        
        Args:
            project_id: ID of the project to unarchive
            
        Returns:
            Dict containing unarchived project details
        """
        query = """
        mutation UnarchiveProject($id: ID!) {
            unarchiveProject(id: $id) {
                id
                name
                workspaceID
                archived
            }
        }
        """
        
        variables = {
            "id": project_id
        }
        
        result = self.client.execute(query, variables)
        return result["unarchiveProject"]
    
    def switch_project(self, project_id: str) -> str:
        """
        Switch the active project.
        
        Args:
            project_id: ID of the project to switch to
            
        Returns:
            String confirmation message
        """
        query = """
        mutation SwitchProject($projID: ID!) {
            switchProject(projID: $projID)
        }
        """
        
        variables = {
            "projID": project_id
        }
        
        result = self.client.execute(query, variables)
        return result["switchProject"]
    
    def update_member_role(self, project_id: str, user_id: str, role: str) -> Dict[str, Any]:
        """
        Update the role of a project member.
        
        Args:
            project_id: Project ID
            user_id: User ID
            role: New role to assign
            
        Returns:
            Dict containing updated project member details
        """
        query = """
        mutation UpdateProjectMemberRole($input: UpdateProjectMemberRoleInput!) {
            updateProjectMemberRole(input: $input) {
                id
                projectID
                userID
                role
                user {
                    id
                    name
                    email
                }
            }
        }
        """
        
        variables = {
            "input": {
                "projectID": project_id,
                "userID": user_id,
                "role": role
            }
        }
        
        result = self.client.execute(query, variables)
        return result["updateProjectMemberRole"]
    
    def remove_member(self, project_id: str, user_id: str, member_id: str) -> bool:
        """
        Remove a member from a project.
        
        Args:
            project_id: Project ID
            user_id: User ID to remove
            member_id: Membership ID
            
        Returns:
            Boolean indicating if removal was successful
        """
        query = """
        mutation RemoveProjectMember($input: RemoveProjectMemberInput!) {
            removeProjectMember(input: $input)
        }
        """
        
        variables = {
            "input": {
                "projectID": project_id,
                "userID": user_id,
                "id": member_id
            }
        }
        
        result = self.client.execute(query, variables)
        return result["removeProjectMember"] 