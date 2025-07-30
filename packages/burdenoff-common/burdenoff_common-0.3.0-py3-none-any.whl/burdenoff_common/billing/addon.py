from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict, Any


class PlanDuration(str, Enum):
    MONTHLY = "monthly"
    YEARLY = "yearly"


@dataclass
class AddonQuotaInput:
    quota_id: str
    quantity: int


@dataclass
class CreateAddonInput:
    name: str
    price: float
    duration: PlanDuration
    quotas: List[AddonQuotaInput]
    currency: Optional[str] = None  # Default USD


@dataclass
class UpdateAddonInput:
    id: str
    quotas: List[AddonQuotaInput]
    name: Optional[str] = None
    price: Optional[float] = None
    currency: Optional[str] = None
    duration: Optional[PlanDuration] = None
    is_active: Optional[bool] = None


@dataclass
class SubscriptionFeature:
    id: str
    quota: Optional[dict] = None


@dataclass
class Subscription:
    id: str
    status: str
    created_at: datetime
    updated_at: datetime


@dataclass
class AddonSubscription:
    id: str
    current_subscription: Optional[Subscription]
    current_subscription_id: str
    addon_id: str
    quantity: int
    start_date: datetime
    end_date: datetime
    created_at: datetime
    updated_at: datetime


@dataclass
class AddonData:
    id: str
    name: str
    price: float
    currency: str
    duration: PlanDuration
    is_active: bool
    features: List[SubscriptionFeature]
    addon_subscriptions: List[AddonSubscription]
    created_at: datetime
    updated_at: datetime


class Addon:
    """
    Addon management for the Burdenoff Server.
    Handles add-on creation, updates, and retrieval.
    """
    
    def __init__(self, client):
        """
        Initialize Addon module.
        
        Args:
            client: WorkspaceClient instance
        """
        self.client = client
    
    def get_all_addons(self) -> List[AddonData]:
        """
        Get all add-ons.
        
        Returns:
            List of all add-ons
        """
        query = """
        query GetAllAddOns {
            getAllAddOns {
                id
                name
                price
                currency
                duration
                isActive
                features {
                    id
                    quota {
                        id
                    }
                }
                addonSubscriptions {
                    id
                    currentSubscription {
                        id
                        status
                        createdAt
                        updatedAt
                    }
                    currentSubscriptionId
                    addonId
                    quantity
                    startDate
                    endDate
                    createdAt
                    updatedAt
                }
                createdAt
                updatedAt
            }
        }
        """
        
        result = self.client.execute(query)
        
        return [
            self._parse_addon(addon)
            for addon in result['getAllAddOns']
        ]
    
    def get_selected_addons(self, addon_ids: List[str]) -> List[AddonData]:
        """
        Get details for selected add-ons.
        
        Args:
            addon_ids: List of add-on IDs to retrieve
            
        Returns:
            List of add-on details
        """
        query = """
        query GetSelectedAddons($addonIDs: [String!]!) {
            getSelectedAddons(addonIDs: $addonIDs) {
                id
                name
                price
                currency
                duration
                isActive
                features {
                    id
                    quota {
                        id
                    }
                }
                addonSubscriptions {
                    id
                    currentSubscription {
                        id
                        status
                        createdAt
                        updatedAt
                    }
                    currentSubscriptionId
                    addonId
                    quantity
                    startDate
                    endDate
                    createdAt
                    updatedAt
                }
                createdAt
                updatedAt
            }
        }
        """
        
        variables = {
            "addonIDs": addon_ids
        }
        
        result = self.client.execute(query, variables)
        
        return [
            self._parse_addon(addon)
            for addon in result['getSelectedAddons']
        ]
    
    def create_addon(self, input: CreateAddonInput) -> bool:
        """
        Create a new add-on.
        
        Args:
            input: CreateAddonInput with add-on details
            
        Returns:
            Boolean indicating success
        """
        mutation = """
        mutation CreateAddOns($input: createAddOnsInput!) {
            createAddOns(input: $input)
        }
        """
        
        variables = {
            "input": {
                "name": input.name,
                "price": input.price,
                "currency": input.currency,
                "duration": input.duration.value,
                "quotas": [
                    {
                        "quotaId": quota.quota_id,
                        "quantity": quota.quantity
                    }
                    for quota in input.quotas
                ]
            }
        }
        
        result = self.client.execute(mutation, variables)
        return result['createAddOns']
    
    def update_addon(self, input: UpdateAddonInput) -> bool:
        """
        Update an existing add-on.
        
        Args:
            input: UpdateAddonInput with add-on details
            
        Returns:
            Boolean indicating success
        """
        mutation = """
        mutation UpdateAddOnDetails($input: updateAddOnsInput!) {
            updateAddOnDetails(input: $input)
        }
        """
        
        variables = {
            "input": {
                "id": input.id,
                "name": input.name,
                "price": input.price,
                "currency": input.currency,
                "duration": input.duration.value if input.duration else None,
                "isActive": input.is_active,
                "quotas": [
                    {
                        "quotaId": quota.quota_id,
                        "quantity": quota.quantity
                    }
                    for quota in input.quotas
                ]
            }
        }
        
        result = self.client.execute(mutation, variables)
        return result['updateAddOnDetails']
    
    def toggle_addon(self, addon_id: str, status: bool) -> bool:
        """
        Toggle the active status of an add-on.
        
        Args:
            addon_id: ID of the add-on to toggle
            status: New status (True for active, False for inactive)
            
        Returns:
            Boolean indicating success
        """
        mutation = """
        mutation ToggleAddOn($id: ID!, $status: Boolean!) {
            toggleAddOn(id: $id, status: $status)
        }
        """
        
        variables = {
            "id": addon_id,
            "status": status
        }
        
        result = self.client.execute(mutation, variables)
        return result['toggleAddOn']
    
    def _parse_addon(self, addon_data: dict) -> AddonData:
        """
        Parse add-on data from GraphQL response.
        
        Args:
            addon_data: Dict containing add-on data
            
        Returns:
            AddonData object
        """
        return AddonData(
            id=addon_data['id'],
            name=addon_data['name'],
            price=addon_data['price'],
            currency=addon_data['currency'],
            duration=PlanDuration(addon_data['duration']),
            is_active=addon_data['isActive'],
            features=[
                SubscriptionFeature(
                    id=feature['id'],
                    quota=feature.get('quota')
                )
                for feature in addon_data['features']
            ],
            addon_subscriptions=[
                AddonSubscription(
                    id=sub['id'],
                    current_subscription=Subscription(
                        id=sub['currentSubscription']['id'],
                        status=sub['currentSubscription']['status'],
                        created_at=self._parse_datetime(sub['currentSubscription']['createdAt']),
                        updated_at=self._parse_datetime(sub['currentSubscription']['updatedAt'])
                    ) if sub.get('currentSubscription') else None,
                    current_subscription_id=sub['currentSubscriptionId'],
                    addon_id=sub['addonId'],
                    quantity=sub['quantity'],
                    start_date=self._parse_datetime(sub['startDate']),
                    end_date=self._parse_datetime(sub['endDate']),
                    created_at=self._parse_datetime(sub['createdAt']),
                    updated_at=self._parse_datetime(sub['updatedAt'])
                )
                for sub in addon_data['addonSubscriptions']
            ],
            created_at=self._parse_datetime(addon_data['createdAt']),
            updated_at=self._parse_datetime(addon_data['updatedAt'])
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