from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict, Any


class PlanDuration(str, Enum):
    MONTHLY = "monthly"
    YEARLY = "yearly"


class SubscriptionStatus(str, Enum):
    ACTIVE = "active"
    CANCELED = "canceled"
    EXPIRED = "expired"


@dataclass
class SubscriptionFeature:
    id: str


@dataclass
class SubscriptionEntitlement:
    id: str


@dataclass
class QuotaAssignment:
    id: str


@dataclass
class Subscription:
    id: str
    billing_account_id: str
    plan_id: str
    status: SubscriptionStatus
    start_date: datetime
    end_date: datetime
    credits_awarded: float
    recurrence: bool
    duration: PlanDuration
    quotas: List[QuotaAssignment]
    created_at: datetime
    updated_at: datetime


@dataclass
class PlanData:
    id: str
    name: str
    price: float
    currency: str
    duration: PlanDuration
    is_active: bool
    features: List[SubscriptionFeature]
    subscriptions: List[Subscription]
    item_entitlements: List[SubscriptionEntitlement]
    created_at: datetime
    updated_at: datetime


@dataclass
class PlanQuotaInput:
    quota_id: str
    quantity: int


@dataclass
class CreatePlanInput:
    name: str
    price: float
    duration: PlanDuration
    quotas: List[PlanQuotaInput]
    currency: Optional[str] = None  # Default USD


@dataclass
class UpdatePlanInput:
    id: str
    quotas: List[PlanQuotaInput]
    name: Optional[str] = None
    price: Optional[float] = None
    currency: Optional[str] = None
    duration: Optional[PlanDuration] = None
    is_active: Optional[bool] = None


class Plan:
    """
    Plan management for the Burdenoff Server.
    Handles plan creation, updates, and retrieval.
    """
    
    def __init__(self, client):
        """
        Initialize Plan module.
        
        Args:
            client: WorkspaceClient instance
        """
        self.client = client
    
    def get_all_plans(self) -> List[PlanData]:
        """
        Get all plans.
        
        Returns:
            List of all plans
        """
        query = """
        query GetAllPlans {
            getAllPlans {
                id
                name
                price
                currency
                duration
                isActive
                features {
                    id
                }
                subscriptions {
                    id
                    billingAccountId
                    planId
                    status
                    startDate
                    endDate
                    creditsAwarded
                    recurrence
                    duration
                    quotas {
                        id
                    }
                    createdAt
                    updatedAt
                }
                itemEntitlements {
                    id
                }
                createdAt
                updatedAt
            }
        }
        """
        
        result = self.client.execute(query)
        
        return [
            self._parse_plan(plan)
            for plan in result['getAllPlans']
        ]
    
    def get_plan(self, plan_id: str) -> PlanData:
        """
        Get details for a specific plan.
        
        Args:
            plan_id: ID of the plan to retrieve
            
        Returns:
            Plan details
        """
        query = """
        query GetPlan($id: ID!) {
            getPlan(id: $id) {
                id
                name
                price
                currency
                duration
                isActive
                features {
                    id
                }
                subscriptions {
                    id
                    billingAccountId
                    planId
                    status
                    startDate
                    endDate
                    creditsAwarded
                    recurrence
                    duration
                    quotas {
                        id
                    }
                    createdAt
                    updatedAt
                }
                itemEntitlements {
                    id
                }
                createdAt
                updatedAt
            }
        }
        """
        
        variables = {
            "id": plan_id
        }
        
        result = self.client.execute(query, variables)
        
        return self._parse_plan(result['getPlan'])
    
    def create_plan(self, input: CreatePlanInput) -> bool:
        """
        Create a new plan.
        
        Args:
            input: CreatePlanInput with plan details
            
        Returns:
            Boolean indicating success
        """
        mutation = """
        mutation CreatePlan($input: createPlanInput!) {
            createPlan(input: $input)
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
        return result['createPlan']
    
    def update_plan(self, input: UpdatePlanInput) -> bool:
        """
        Update an existing plan.
        
        Args:
            input: UpdatePlanInput with plan details
            
        Returns:
            Boolean indicating success
        """
        mutation = """
        mutation UpdatePlan($input: updatePlanInput!) {
            updatePlan(input: $input)
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
        return result['updatePlan']
    
    def toggle_plan(self, plan_id: str, status: bool) -> bool:
        """
        Toggle the active status of a plan.
        
        Args:
            plan_id: ID of the plan to toggle
            status: New status (True for active, False for inactive)
            
        Returns:
            Boolean indicating success
        """
        mutation = """
        mutation TogglePlan($planID: ID!, $status: Boolean!) {
            togglePlan(planID: $planID, status: $status)
        }
        """
        
        variables = {
            "planID": plan_id,
            "status": status
        }
        
        result = self.client.execute(mutation, variables)
        return result['togglePlan']
    
    def _parse_plan(self, plan_data: dict) -> PlanData:
        """
        Parse plan data from GraphQL response.
        
        Args:
            plan_data: Dict containing plan data
            
        Returns:
            PlanData object
        """
        return PlanData(
            id=plan_data['id'],
            name=plan_data['name'],
            price=plan_data['price'],
            currency=plan_data['currency'],
            duration=PlanDuration(plan_data['duration']),
            is_active=plan_data['isActive'],
            features=[SubscriptionFeature(id=f['id']) for f in plan_data['features']],
            subscriptions=[
                Subscription(
                    id=sub['id'],
                    billing_account_id=sub['billingAccountId'],
                    plan_id=sub['planId'],
                    status=SubscriptionStatus(sub['status']),
                    start_date=self._parse_datetime(sub['startDate']),
                    end_date=self._parse_datetime(sub['endDate']),
                    credits_awarded=sub['creditsAwarded'],
                    recurrence=sub['recurrence'],
                    duration=PlanDuration(sub['duration']),
                    quotas=[QuotaAssignment(id=q['id']) for q in sub['quotas']],
                    created_at=self._parse_datetime(sub['createdAt']),
                    updated_at=self._parse_datetime(sub['updatedAt'])
                )
                for sub in plan_data['subscriptions']
            ],
            item_entitlements=[SubscriptionEntitlement(id=e['id']) for e in plan_data['itemEntitlements']],
            created_at=self._parse_datetime(plan_data['createdAt']),
            updated_at=self._parse_datetime(plan_data['updatedAt'])
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