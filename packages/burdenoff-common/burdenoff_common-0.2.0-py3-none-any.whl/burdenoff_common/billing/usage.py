from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional


@dataclass
class Usage:
    """A usage record for a quota."""
    id: str
    amount: float
    description: str
    last_updated: datetime
    timestamp: datetime
    tags: Optional[Dict] = None


@dataclass
class QuotaAssignment:
    """A quota assignment for a subscription."""
    id: str
    name: str
    limits: Dict
    reusable: bool
    subscription_id: str
    created_at: datetime
    endtime: datetime
    usages: List[Usage]


@dataclass
class PaginatedUsages:
    """Paginated list of usage records."""
    usages: List[Usage]
    total_count: int
    page: int
    page_size: int
    total_pages: int


@dataclass
class QuotaAssignmentSummary:
    """Summary of a quota assignment with usage information."""
    current_usage_sum: int
    usage_count: int
    usages: List[Usage]
    created_at: datetime
    endtime: datetime
    id: str
    name: str
    limits: Dict


@dataclass
class SubscriptionWithQuotas:
    """A subscription with its associated quotas."""
    id: str
    created_at: datetime
    status: str
    quotas: List[QuotaAssignmentSummary]


@dataclass
class SubscriptionQuotaUsageWithFilter:
    """Paginated and filtered subscription quota usage."""
    page_size: int
    total_count: int
    total_pages: int
    page: int
    usages: List[Usage]


@dataclass
class QuotaCheckResult:
    """Result of checking if a quota is exhausted."""
    limit_left: int
    no_limit: bool


@dataclass
class QuotaUsageAndLimit:
    """Current usage and limit information for a quota."""
    limit: int
    limit_left: int
    no_limit: bool


class UsageError(Exception):
    """Custom error class for usage-related errors."""
    def __init__(self, message: str, code: str = None):
        super().__init__(message)
        self.message = message
        self.code = code


class Usage:
    """
    Usage tracking and quota management for the Burdenoff Server.
    Handles tracking resource usage, checking quota limits, and retrieving usage data.
    """
    
    def __init__(self, client):
        """
        Initialize Usage module.
        
        Args:
            client: WorkspaceClient instance
        """
        self.client = client
    
    def add_usage(
        self,
        billing_account_id: str,
        quota_name: str,
        value: int,
        description: str,
        tags: Optional[Dict] = None
    ) -> bool:
        """
        Add usage for a specific quota.
        
        Args:
            billing_account_id (str): The billing account ID
            quota_name (str): Name of the quota
            value (int): Usage value to add
            description (str): Description of the usage
            tags (Optional[Dict]): Optional tags for the usage
            
        Returns:
            bool: True if successful, False if quota is exhausted
            
        Raises:
            UsageError: If there's an error adding the usage
        """
        mutation = """
        mutation AddUsage(
            $billingAccountId: ID!
            $quotaName: String!
            $value: Int!
            $description: String!
            $tags: JSON
        ) {
            addUsage(
                billingAccountId: $billingAccountId
                quotaName: $quotaName
                value: $value
                description: $description
                tags: $tags
            )
        }
        """
        
        variables = {
            "billingAccountId": billing_account_id,
            "quotaName": quota_name,
            "value": value,
            "description": description,
            "tags": tags
        }
        
        try:
            result = self.client.execute(mutation, variables)
            return result["addUsage"]
        except Exception as e:
            # Extract error code if available
            code = getattr(e, "code", None)
            raise UsageError(str(e), code)
    
    def check_quota_exhausted(
        self,
        billing_account_id: str,
        quota_name: str
    ) -> QuotaCheckResult:
        """
        Check if a quota has been exhausted.
        
        Args:
            billing_account_id (str): The billing account ID
            quota_name (str): Name of the quota to check
            
        Returns:
            QuotaCheckResult: Object containing limit left and no limit flag
            
        Raises:
            UsageError: If there's an error checking the quota
        """
        query = """
        query CheckQuotaExhausted($billingAccountId: ID!, $quotaName: String!) {
            checkQuotaExhausted(billingAccountId: $billingAccountId, quotaName: $quotaName) {
                limitLeft
                noLimit
            }
        }
        """
        
        variables = {
            "billingAccountId": billing_account_id,
            "quotaName": quota_name
        }
        
        try:
            result = self.client.execute(query, variables)
            data = result["checkQuotaExhausted"]
            return QuotaCheckResult(
                limit_left=data["limitLeft"],
                no_limit=data["noLimit"]
            )
        except Exception as e:
            code = getattr(e, "code", None)
            raise UsageError(str(e), code)
    
    def get_quota_usage_and_limit(
        self,
        billing_account_id: str,
        quota_name: str
    ) -> QuotaUsageAndLimit:
        """
        Get the current usage and limit for a quota.
        
        Args:
            billing_account_id (str): The billing account ID
            quota_name (str): Name of the quota
            
        Returns:
            QuotaUsageAndLimit: Object containing limit, limit left and no limit flag
            
        Raises:
            UsageError: If there's an error getting the quota usage and limit
        """
        query = """
        query GetQuotaUsageAndLimit($billingAccountId: ID!, $quotaName: String!) {
            getQuotaUsageAndLimit(billingAccountId: $billingAccountId, quotaName: $quotaName) {
                limit
                limitLeft
                noLimit
            }
        }
        """
        
        variables = {
            "billingAccountId": billing_account_id,
            "quotaName": quota_name
        }
        
        try:
            result = self.client.execute(query, variables)
            data = result["getQuotaUsageAndLimit"]
            return QuotaUsageAndLimit(
                limit=data["limit"],
                limit_left=data["limitLeft"],
                no_limit=data["noLimit"]
            )
        except Exception as e:
            code = getattr(e, "code", None)
            raise UsageError(str(e), code)
    
    def get_subscription_usages(
        self,
        billing_account_id: str,
        page: int,
        page_size: int,
        search_query: Optional[str] = None,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
        resource_type: Optional[str] = None,
        entity: Optional[str] = None
    ) -> SubscriptionQuotaUsageWithFilter:
        """
        Get paginated usage records for a subscription.
        
        Args:
            billing_account_id (str): The billing account ID
            page (int): Page number
            page_size (int): Number of items per page
            search_query (Optional[str]): Optional search query
            from_date (Optional[datetime]): Filter usages from this date
            to_date (Optional[datetime]): Filter usages to this date
            resource_type (Optional[str]): Filter by resource type
            entity (Optional[str]): Filter by entity
            
        Returns:
            SubscriptionQuotaUsageWithFilter: Paginated usage records
        """
        query = """
        query GetSubscriptionUsages(
            $billingAccountId: ID!
            $page: Int!
            $pageSize: Int!
            $searchQuery: String
            $fromDate: DateTime
            $toDate: DateTime
            $resourceType: String
            $entity: String
        ) {
            getSubscriptionUsages(
                billingAccountId: $billingAccountId
                page: $page
                pageSize: $pageSize
                searchQuery: $searchQuery
                fromDate: $fromDate
                toDate: $toDate
                resourceType: $resourceType
                entity: $entity
            ) {
                pageSize
                totalCount
                totalPages
                page
                usages {
                    id
                    amount
                    description
                    lastUpdated
                    timestamp
                    tags
                }
            }
        }
        """
        
        variables = {
            "billingAccountId": billing_account_id,
            "page": page,
            "pageSize": page_size,
            "searchQuery": search_query,
            "fromDate": from_date.isoformat() if from_date else None,
            "toDate": to_date.isoformat() if to_date else None,
            "resourceType": resource_type,
            "entity": entity
        }
        
        try:
            result = self.client.execute(query, variables)
            data = result["getSubscriptionUsages"]
            
            # Convert raw data to Usage objects
            usages = [
                Usage(
                    id=u["id"],
                    amount=float(u["amount"]),
                    description=u["description"],
                    last_updated=self._parse_datetime(u["lastUpdated"]),
                    timestamp=self._parse_datetime(u["timestamp"]),
                    tags=u["tags"]
                )
                for u in data["usages"]
            ]
            
            return SubscriptionQuotaUsageWithFilter(
                page_size=data["pageSize"],
                total_count=data["totalCount"],
                total_pages=data["totalPages"],
                page=data["page"],
                usages=usages
            )
        except Exception as e:
            code = getattr(e, "code", None)
            raise UsageError(str(e), code)

    def get_all_quotas_assignment(self, billing_account_id: str) -> List[QuotaAssignment]:
        """
        Get all quota assignments for a billing account.
        
        Args:
            billing_account_id (str): The billing account ID
            
        Returns:
            List[QuotaAssignment]: List of quota assignments
            
        Raises:
            UsageError: If there's an error getting the quota assignments
        """
        query = """
        query GetAllQuotasAssignment($billingAccountId: ID!) {
            getAllQuotasAssignment(billingAccountId: $billingAccountId) {
                id
                name
                limits
                reusable
                subscriptionId
                createdAt
                endtime
                usages {
                    id
                    amount
                    description
                    lastUpdated
                    timestamp
                    tags
                }
            }
        }
        """
        
        variables = {
            "billingAccountId": billing_account_id
        }
        
        try:
            result = self.client.execute(query, variables)
            data = result["getAllQuotasAssignment"]
            
            quotas = []
            for quota_data in data:
                usages = [
                    Usage(
                        id=u["id"],
                        amount=float(u["amount"]),
                        description=u["description"],
                        last_updated=self._parse_datetime(u["lastUpdated"]),
                        timestamp=self._parse_datetime(u["timestamp"]),
                        tags=u["tags"]
                    )
                    for u in quota_data["usages"]
                ]
                
                quota = QuotaAssignment(
                    id=quota_data["id"],
                    name=quota_data["name"],
                    limits=quota_data["limits"],
                    reusable=quota_data["reusable"],
                    subscription_id=quota_data["subscriptionId"],
                    created_at=self._parse_datetime(quota_data["createdAt"]),
                    endtime=self._parse_datetime(quota_data["endtime"]),
                    usages=usages
                )
                quotas.append(quota)
                
            return quotas
        except Exception as e:
            code = getattr(e, "code", None)
            raise UsageError(str(e), code)

    def get_quota_usage_details(
        self,
        quota_assignment_id: str,
        page: int,
        page_size: int,
        search_query: Optional[str] = None,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
        resource_type: Optional[str] = None,
        entity: Optional[str] = None
    ) -> PaginatedUsages:
        """
        Get detailed usage information for a quota assignment.
        
        Args:
            quota_assignment_id (str): ID of the quota assignment
            page (int): Page number
            page_size (int): Number of items per page
            search_query (Optional[str]): Optional search query
            from_date (Optional[datetime]): Filter usages from this date
            to_date (Optional[datetime]): Filter usages to this date
            resource_type (Optional[str]): Filter by resource type
            entity (Optional[str]): Filter by entity
            
        Returns:
            PaginatedUsages: Paginated usage details
            
        Raises:
            UsageError: If there's an error getting the usage details
        """
        query = """
        query GetQuotaUsageDetails(
            $quotaAssignmentId: ID!
            $page: Int!
            $pageSize: Int!
            $searchQuery: String
            $fromDate: DateTime
            $toDate: DateTime
            $resourceType: String
            $entity: String
        ) {
            getQuotaUsageDetails(
                quotaAssignmentId: $quotaAssignmentId
                page: $page
                pageSize: $pageSize
                searchQuery: $searchQuery
                fromDate: $fromDate
                toDate: $toDate
                resourceType: $resourceType
                entity: $entity
            ) {
                usages {
                    id
                    amount
                    description
                    lastUpdated
                    timestamp
                    tags
                }
                totalCount
                page
                pageSize
                totalPages
            }
        }
        """
        
        variables = {
            "quotaAssignmentId": quota_assignment_id,
            "page": page,
            "pageSize": page_size,
            "searchQuery": search_query,
            "fromDate": from_date.isoformat() if from_date else None,
            "toDate": to_date.isoformat() if to_date else None,
            "resourceType": resource_type,
            "entity": entity
        }
        
        try:
            result = self.client.execute(query, variables)
            data = result["getQuotaUsageDetails"]
            
            usages = [
                Usage(
                    id=u["id"],
                    amount=float(u["amount"]),
                    description=u["description"],
                    last_updated=self._parse_datetime(u["lastUpdated"]),
                    timestamp=self._parse_datetime(u["timestamp"]),
                    tags=u["tags"]
                )
                for u in data["usages"]
            ]
            
            return PaginatedUsages(
                usages=usages,
                total_count=data["totalCount"],
                page=data["page"],
                page_size=data["pageSize"],
                total_pages=data["totalPages"]
            )
        except Exception as e:
            code = getattr(e, "code", None)
            raise UsageError(str(e), code)

    def get_subscription_usage_overview(
        self,
        billing_account_id: str,
        page: Optional[int] = None,
        page_size: Optional[int] = None
    ) -> List[SubscriptionWithQuotas]:
        """
        Get usage overview for all subscriptions under a billing account.
        
        Args:
            billing_account_id (str): The billing account ID
            page (Optional[int]): Optional page number
            page_size (Optional[int]): Optional number of items per page
            
        Returns:
            List[SubscriptionWithQuotas]: List of subscriptions with quotas
            
        Raises:
            UsageError: If there's an error getting the subscription usage overview
        """
        query = """
        query GetSubscriptionUsageOverview(
            $billingAccountId: ID!
            $page: Int
            $pageSize: Int
        ) {
            getSubscriptionUsageOverview(
                billingAccountId: $billingAccountId
                page: $page
                pageSize: $pageSize
            ) {
                id
                createdAt
                status
                quotas {
                    id
                    name
                    limits
                    createdAt
                    endtime
                    currentUsageSum
                    usageCount
                    usages {
                        id
                        amount
                        description
                        lastUpdated
                        timestamp
                        tags
                    }
                }
            }
        }
        """
        
        variables = {
            "billingAccountId": billing_account_id,
            "page": page,
            "pageSize": page_size
        }
        
        try:
            result = self.client.execute(query, variables)
            data = result["getSubscriptionUsageOverview"]
            
            subscriptions = []
            for sub_data in data:
                quotas = []
                for quota_data in sub_data["quotas"]:
                    usages = [
                        Usage(
                            id=u["id"],
                            amount=float(u["amount"]),
                            description=u["description"],
                            last_updated=self._parse_datetime(u["lastUpdated"]),
                            timestamp=self._parse_datetime(u["timestamp"]),
                            tags=u["tags"]
                        )
                        for u in quota_data["usages"]
                    ]
                    
                    quota = QuotaAssignmentSummary(
                        id=quota_data["id"],
                        name=quota_data["name"],
                        limits=quota_data["limits"],
                        created_at=self._parse_datetime(quota_data["createdAt"]),
                        endtime=self._parse_datetime(quota_data["endtime"]),
                        current_usage_sum=quota_data["currentUsageSum"],
                        usage_count=quota_data["usageCount"],
                        usages=usages
                    )
                    quotas.append(quota)
                
                subscription = SubscriptionWithQuotas(
                    id=sub_data["id"],
                    created_at=self._parse_datetime(sub_data["createdAt"]),
                    status=sub_data["status"],
                    quotas=quotas
                )
                subscriptions.append(subscription)
                
            return subscriptions
        except Exception as e:
            code = getattr(e, "code", None)
            raise UsageError(str(e), code)
    
    def _parse_datetime(self, dt_str: str) -> datetime:
        """
        Parse a datetime string into a datetime object.
        
        Args:
            dt_str (str): ISO format datetime string
            
        Returns:
            datetime: Parsed datetime object
        """
        return datetime.fromisoformat(dt_str.replace('Z', '+00:00')) 