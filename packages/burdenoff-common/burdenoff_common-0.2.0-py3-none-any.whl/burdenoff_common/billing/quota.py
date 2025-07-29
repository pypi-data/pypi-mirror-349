from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum
from dataclasses import dataclass


class QuotaEntityType(str, Enum):
    WORKSPACE = "workspace"
    PROJECT = "project"


@dataclass
class Plan:
    id: str
    name: str


@dataclass
class Addon:
    id: str
    name: str


@dataclass
class SubscriptionFeature:
    id: str
    plan_id: Optional[str]
    plan: Optional[Plan]
    addon_id: Optional[str]
    addon: Optional[Addon]
    quota_id: Optional[str]
    quota: Optional['Quota']


@dataclass
class Quota:
    id: str
    name: str
    limits: Dict[str, Any]  # JSON object defining quota limits
    is_active: bool
    reusable: bool
    subscriptions: List[SubscriptionFeature]
    created_at: datetime
    updated_at: datetime


@dataclass
class CreateQuotaInput:
    name: str
    limits: Dict[str, Any]  # JSON object defining quota limits
    reusable: bool


@dataclass
class UpdateQuotaInput:
    id: str
    is_active: bool
    name: Optional[str] = None
    limits: Optional[Dict[str, Any]] = None
    reusable: Optional[bool] = None


class Quota:
    """
    Quota management for the Burdenoff Server.
    Handles quota creation, updates, and retrieval.
    """
    
    def __init__(self, client):
        """
        Initialize Quota module.
        
        Args:
            client: WorkspaceClient instance
        """
        self.client = client
    
    def get_all_quotas(self) -> List[Quota]:
        """
        Get all quotas.
        
        Returns:
            List of all quotas
        """
        query = """
        query GetAllQuotas {
            getAllQuotas {
                id
                name
                limits
                isActive
                reusable
                subscriptions {
                    id
                    planId
                    plan {
                        id
                        name
                    }
                    addonId
                    addOn {
                        id
                        name
                    }
                    quotaId
                    quota {
                        id
                        name
                    }
                }
                createdAt
                updatedAt
            }
        }
        """
        
        result = self.client.execute(query)
        
        return [
            self._parse_quota(quota)
            for quota in result['getAllQuotas']
        ]
    
    def get_all_quotas_of_sub(self, subscription_id: str) -> List[Quota]:
        """
        Get all quotas of a subscription.
        
        Args:
            subscription_id: ID of the subscription
            
        Returns:
            List of quotas associated with the subscription
        """
        query = """
        query GetAllQuotasOfSub($subscriptionId: ID!) {
            getAllQuotasOfSub(subscriptionId: $subscriptionId) {
                id
                name
                limits
                isActive
                reusable
                subscriptions {
                    id
                    planId
                    plan {
                        id
                        name
                    }
                    addonId
                    addOn {
                        id
                        name
                    }
                    quotaId
                    quota {
                        id
                        name
                    }
                }
                createdAt
                updatedAt
            }
        }
        """
        
        variables = {
            "subscriptionId": subscription_id
        }
        
        result = self.client.execute(query, variables)
        
        return [
            self._parse_quota(quota)
            for quota in result['getAllQuotasOfSub']
        ]
    
    def create_quota(self, input: CreateQuotaInput) -> bool:
        """
        Create a new quota.
        
        Args:
            input: CreateQuotaInput with quota details
            
        Returns:
            Boolean indicating success
        """
        mutation = """
        mutation CreateQuota($input: createQuotaInput!) {
            createQuota(input: $input)
        }
        """
        
        variables = {
            "input": {
                "name": input.name,
                "limits": input.limits,
                "reusable": input.reusable
            }
        }
        
        result = self.client.execute(mutation, variables)
        return result['createQuota']
    
    def update_quota(self, input: UpdateQuotaInput) -> bool:
        """
        Update an existing quota.
        
        Args:
            input: UpdateQuotaInput with quota details
            
        Returns:
            Boolean indicating success
        """
        mutation = """
        mutation UpdateQuota($input: updateQuotaInput!) {
            updateQuota(input: $input)
        }
        """
        
        variables = {
            "input": {
                "id": input.id,
                "name": input.name,
                "limits": input.limits,
                "reusable": input.reusable,
                "isActive": input.is_active
            }
        }
        
        result = self.client.execute(mutation, variables)
        return result['updateQuota']
    
    def _parse_quota(self, quota_data: dict) -> Quota:
        """
        Parse quota data from GraphQL response.
        
        Args:
            quota_data: Dict containing quota data
            
        Returns:
            Quota object
        """
        return Quota(
            id=quota_data['id'],
            name=quota_data['name'],
            limits=quota_data['limits'],
            is_active=quota_data['isActive'],
            reusable=quota_data['reusable'],
            subscriptions=[
                SubscriptionFeature(
                    id=sub['id'],
                    plan_id=sub.get('planId'),
                    plan=Plan(
                        id=sub['plan']['id'],
                        name=sub['plan']['name']
                    ) if sub.get('plan') else None,
                    addon_id=sub.get('addonId'),
                    addon=Addon(
                        id=sub['addOn']['id'],
                        name=sub['addOn']['name']
                    ) if sub.get('addOn') else None,
                    quota_id=sub.get('quotaId'),
                    quota=Quota(
                        id=sub['quota']['id'],
                        name=sub['quota']['name'],
                        limits={},  # Simplified for nested quota
                        is_active=True,  # Default values for nested quota
                        reusable=True,
                        subscriptions=[],
                        created_at=self._parse_datetime(quota_data['createdAt']),
                        updated_at=self._parse_datetime(quota_data['updatedAt'])
                    ) if sub.get('quota') else None
                )
                for sub in quota_data['subscriptions']
            ],
            created_at=self._parse_datetime(quota_data['createdAt']),
            updated_at=self._parse_datetime(quota_data['updatedAt'])
        )
    
    def _parse_datetime(self, dt_str: str) -> datetime:
        """
        Parse datetime string from API response.
        
        Args:
            dt_str: Datetime string
            
        Returns:
            datetime object
        """
        return datetime.fromisoformat(dt_str.replace('Z', '+00:00')) 