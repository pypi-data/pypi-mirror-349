from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List, Optional


class BillingFrequency(str, Enum):
    DAILY = 'daily'
    WEEKLY = 'weekly'
    MONTHLY = 'monthly'
    QUARTERLY = 'quarterly'
    YEARLY = 'yearly'


@dataclass
class PaymentMethod:
    id: str
    # Add other payment method fields as needed


@dataclass
class Transaction:
    id: str
    # Add other transaction fields as needed


@dataclass
class Invoice:
    id: str
    # Add other invoice fields as needed


@dataclass
class Subscription:
    id: str
    # Add other subscription fields as needed


@dataclass
class Workspace:
    id: str
    name: str


@dataclass
class BillingAccount:
    id: str
    account_name: str
    billing_address: str
    city: str
    state: str
    country: str
    postal_code: str
    contact_email: str
    contact_phone_number: Optional[str]
    workspace_id: str
    billing_frequency: BillingFrequency
    next_billing_date: datetime
    billing_start_date: datetime
    created_at: datetime
    updated_at: Optional[datetime]
    workspace: Optional[Workspace] = None
    subscriptions: Optional[List[Subscription]] = None
    payment_methods: Optional[List[PaymentMethod]] = None
    transactions: Optional[List[Transaction]] = None
    invoices: Optional[List[Invoice]] = None


@dataclass
class CreateBillingAccountInput:
    account_name: str
    billing_address: str
    city: str
    state: str
    country: str
    postal_code: str
    contact_email: str
    billing_frequency: BillingFrequency
    contact_phone_number: Optional[str] = None


@dataclass
class UpdateBillingAccountInput:
    id: str
    account_name: Optional[str] = None
    billing_address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone_number: Optional[str] = None
    billing_frequency: Optional[BillingFrequency] = None


class BillingError(Exception):
    def __init__(self, message: str, code: str = None):
        super().__init__(message)
        self.message = message
        self.code = code


class Billing:
    """
    Billing account management for the Burdenoff Server.
    Handles billing account creation, updates, and retrieval.
    """
    
    def __init__(self, client):
        """
        Initialize Billing module.
        
        Args:
            client: WorkspaceClient instance
        """
        self.client = client
    
    def get_workspace_billing_accounts(self) -> List[BillingAccount]:
        """
        Get all billing accounts for the current workspace.
        
        Returns:
            List of billing accounts for the workspace
            
        Raises:
            BillingError: If there's an error fetching the billing accounts
        """
        query = """
        query GetWorkspaceBillingAccounts {
            getWorkspaceBillingAccounts {
                id
                accountName
                billingAddress
                city
                state
                country
                postalCode
                contactEmail
                contactPhoneNumber
                workspaceId
                billingFrequency
                nextBillingDate
                billingStartDate
                createdAt
                updatedAt
            }
        }
        """
        
        try:
            result = self.client.execute(query)
            
            return [
                self._parse_billing_account(account)
                for account in result['getWorkspaceBillingAccounts']
            ]
        except Exception as e:
            raise BillingError(str(e), getattr(e, 'code', None))
    
    def get_billing_account_details(self, account_id: str) -> BillingAccount:
        """
        Get detailed information about a specific billing account.
        
        Args:
            account_id: ID of the billing account
            
        Returns:
            Detailed billing account information
            
        Raises:
            BillingError: If there's an error fetching the billing account details
        """
        query = """
        query GetBillingAccountDetails($id: ID!) {
            getBillingAccountDetails(id: $id) {
                id
                accountName
                billingAddress
                city
                state
                country
                postalCode
                contactEmail
                contactPhoneNumber
                workspaceId
                billingFrequency
                nextBillingDate
                billingStartDate
                createdAt
                updatedAt
                workspace {
                    id
                    name
                }
                subscriptions {
                    id
                }
                paymentMethods {
                    id
                }
                transactions {
                    id
                }
                invoices {
                    id
                }
            }
        }
        """
        
        variables = {
            "id": account_id
        }
        
        try:
            result = self.client.execute(query, variables)
            account = result['getBillingAccountDetails']
            
            return self._parse_detailed_billing_account(account)
        except Exception as e:
            raise BillingError(str(e), getattr(e, 'code', None))
    
    def get_filtered_billing_accounts(self) -> List[BillingAccount]:
        """
        Get filtered billing accounts (those without active subscriptions).
        
        Returns:
            List of filtered billing accounts
            
        Raises:
            BillingError: If there's an error fetching the filtered billing accounts
        """
        query = """
        query GetFilteredBillingAccount {
            getFilteredBillingAccount {
                id
                accountName
                billingAddress
                city
                state
                country
                postalCode
                contactEmail
                contactPhoneNumber
                workspaceId
                billingFrequency
                nextBillingDate
                billingStartDate
                createdAt
                updatedAt
            }
        }
        """
        
        try:
            result = self.client.execute(query)
            
            return [
                self._parse_billing_account(account)
                for account in result['getFilteredBillingAccount']
            ]
        except Exception as e:
            raise BillingError(str(e), getattr(e, 'code', None))
    
    def create_billing_account(self, input_data: CreateBillingAccountInput) -> bool:
        """
        Create a new billing account.
        
        Args:
            input_data: Input data for creating a billing account
            
        Returns:
            Boolean indicating success
            
        Raises:
            BillingError: If there's an error creating the billing account
        """
        mutation = """
        mutation CreateBillingAccount($input: CreateBillingAccountInput!) {
            createBillingAccount(input: $input)
        }
        """
        
        variables = {
            "input": {
                "accountName": input_data.account_name,
                "billingAddress": input_data.billing_address,
                "city": input_data.city,
                "state": input_data.state,
                "country": input_data.country,
                "postalCode": input_data.postal_code,
                "contactEmail": input_data.contact_email,
                "contactPhoneNumber": input_data.contact_phone_number,
                "billingFrequency": input_data.billing_frequency.value
            }
        }
        
        try:
            result = self.client.execute(mutation, variables)
            return result['createBillingAccount']
        except Exception as e:
            raise BillingError(str(e), getattr(e, 'code', None))
    
    def update_billing_account(self, input_data: UpdateBillingAccountInput) -> bool:
        """
        Update an existing billing account.
        
        Args:
            input_data: Input data for updating a billing account
            
        Returns:
            Boolean indicating success
            
        Raises:
            BillingError: If there's an error updating the billing account
        """
        mutation = """
        mutation UpdateBillingAccount($input: UpdateBillingAccountInput!) {
            updateBillingAccount(input: $input)
        }
        """
        
        update_data = {
            "id": input_data.id
        }
        
        if input_data.account_name is not None:
            update_data["accountName"] = input_data.account_name
        if input_data.billing_address is not None:
            update_data["billingAddress"] = input_data.billing_address
        if input_data.city is not None:
            update_data["city"] = input_data.city
        if input_data.state is not None:
            update_data["state"] = input_data.state
        if input_data.country is not None:
            update_data["country"] = input_data.country
        if input_data.postal_code is not None:
            update_data["postalCode"] = input_data.postal_code
        if input_data.contact_email is not None:
            update_data["contactEmail"] = input_data.contact_email
        if input_data.contact_phone_number is not None:
            update_data["contactPhoneNumber"] = input_data.contact_phone_number
        if input_data.billing_frequency is not None:
            update_data["billingFrequency"] = input_data.billing_frequency.value
        
        variables = {
            "input": update_data
        }
        
        try:
            result = self.client.execute(mutation, variables)
            return result['updateBillingAccount']
        except Exception as e:
            raise BillingError(str(e), getattr(e, 'code', None))
    
    def _parse_billing_account(self, account: dict) -> BillingAccount:
        """
        Parse basic billing account data from GraphQL response.
        
        Args:
            account: Dict containing account data
            
        Returns:
            BillingAccount object
        """
        return BillingAccount(
            id=account['id'],
            account_name=account['accountName'],
            billing_address=account['billingAddress'],
            city=account['city'],
            state=account['state'],
            country=account['country'],
            postal_code=account['postalCode'],
            contact_email=account['contactEmail'],
            contact_phone_number=account['contactPhoneNumber'],
            workspace_id=account['workspaceId'],
            billing_frequency=BillingFrequency(account['billingFrequency']),
            next_billing_date=self._parse_datetime(account['nextBillingDate']),
            billing_start_date=self._parse_datetime(account['billingStartDate']),
            created_at=self._parse_datetime(account['createdAt']),
            updated_at=self._parse_datetime(account['updatedAt']) if account.get('updatedAt') else None
        )
    
    def _parse_detailed_billing_account(self, account: dict) -> BillingAccount:
        """
        Parse detailed billing account data from GraphQL response.
        
        Args:
            account: Dict containing detailed account data
            
        Returns:
            BillingAccount object with related entities
        """
        billing_account = self._parse_billing_account(account)
        
        # Add additional related data
        if account.get('workspace'):
            billing_account.workspace = Workspace(
                id=account['workspace']['id'],
                name=account['workspace']['name']
            )
        
        if account.get('subscriptions'):
            billing_account.subscriptions = [
                Subscription(id=sub['id'])
                for sub in account['subscriptions']
            ]
        
        if account.get('paymentMethods'):
            billing_account.payment_methods = [
                PaymentMethod(id=pm['id'])
                for pm in account['paymentMethods']
            ]
        
        if account.get('transactions'):
            billing_account.transactions = [
                Transaction(id=tx['id'])
                for tx in account['transactions']
            ]
        
        if account.get('invoices'):
            billing_account.invoices = [
                Invoice(id=inv['id'])
                for inv in account['invoices']
            ]
        
        return billing_account
    
    def _parse_datetime(self, dt_str: str) -> datetime:
        """
        Parse datetime string from API response.
        
        Args:
            dt_str: Datetime string
            
        Returns:
            datetime object
        """
        return datetime.fromisoformat(dt_str.replace('Z', '+00:00')) 