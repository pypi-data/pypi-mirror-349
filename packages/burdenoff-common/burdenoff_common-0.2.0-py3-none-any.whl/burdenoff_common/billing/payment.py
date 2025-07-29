from typing import List, Dict, Optional, Any
from datetime import datetime
from enum import Enum
from dataclasses import dataclass


class PaymentMethodType(str, Enum):
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    PAYMENT_GATEWAY = "payment_gateway"
    NET_BANKING = "net_banking"
    UPI = "upi"
    WALLET = "wallet"
    OTHER = "other"


class TransactionStatus(str, Enum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"


class TransactionType(str, Enum):
    PAYMENT = "payment"
    REFUND = "refund"
    ADJUSTMENT = "adjustment"


class InvoiceStatus(str, Enum):
    DRAFT = "draft"
    PAID = "paid"


@dataclass
class Transaction:
    id: str
    billing_account_id: str
    payment_method_id: Optional[str]
    amount: float
    currency: str
    description: Optional[str]
    status: TransactionStatus
    type: TransactionType
    discount_id: Optional[str]
    created_at: datetime
    updated_at: datetime


@dataclass
class Invoice:
    id: str
    billing_account_id: str
    total_amount: float
    currency: str
    period_start: datetime
    period_end: datetime
    status: InvoiceStatus
    tax_amount: float
    tax_details: Optional[Dict[str, Any]]
    created_at: datetime
    updated_at: datetime


@dataclass
class PollingStatus:
    status: str


@dataclass
class PDF:
    pdf: str


@dataclass
class AddOnInputPayment:
    id: str
    quantity: Optional[int]


@dataclass
class CreateRazorpayOrderInput:
    billing_account_id: str
    plan_id: Optional[str]
    store_item_id: Optional[str]
    add_on_ids: Optional[List[AddOnInputPayment]]
    recurrence: Optional[bool]


@dataclass
class CreateStripeOrderInput:
    billing_account_id: str
    plan_id: Optional[str]
    store_item_id: Optional[str]
    add_on_ids: Optional[List[AddOnInputPayment]]
    recurrence: Optional[bool]


@dataclass
class CreateRazorpayOrderResponse:
    amount: str
    currency: str
    order_id: str
    key: str
    transaction_id: str


@dataclass
class CreateStripeOrderResponse:
    client_secret: str
    transaction_id: str
    key: str
    amount: str


class Payment:
    """
    Payment operations for the Burdenoff Server.
    Handles transactions, invoices, and payment processing.
    """
    
    def __init__(self, client):
        """
        Initialize Payment module.
        
        Args:
            client: WorkspaceClient instance
        """
        self.client = client
    
    def get_billing_account_transactions(self, billing_account_id: str, days: int) -> List[Transaction]:
        """
        Get transactions for a billing account within a specific time period.
        
        Args:
            billing_account_id: ID of the billing account
            days: Number of days to look back
            
        Returns:
            List of transactions
        """
        query = """
        query GetBillingAccountTransactions($billingAccountID: ID!, $days: Int!) {
            getBillingAccountTransactions(billingAccountID: $billingAccountID, days: $days) {
                id
                billingAccountId
                paymentMethodId
                amount
                currency
                description
                status
                type
                discountId
                createdAt
                updatedAt
            }
        }
        """
        
        variables = {
            "billingAccountID": billing_account_id,
            "days": days
        }
        
        result = self.client.execute(query, variables)
        
        return [
            Transaction(
                id=tx['id'],
                billing_account_id=tx['billingAccountId'],
                payment_method_id=tx.get('paymentMethodId'),
                amount=tx['amount'],
                currency=tx['currency'],
                description=tx.get('description'),
                status=TransactionStatus(tx['status']),
                type=TransactionType(tx['type']),
                discount_id=tx.get('discountId'),
                created_at=self._parse_datetime(tx['createdAt']),
                updated_at=self._parse_datetime(tx['updatedAt'])
            )
            for tx in result['getBillingAccountTransactions']
        ]
    
    def get_transaction_details(self, transaction_id: str) -> Transaction:
        """
        Get details for a specific transaction.
        
        Args:
            transaction_id: ID of the transaction
            
        Returns:
            Transaction details
        """
        query = """
        query GetTransactionDetails($transactionID: ID!) {
            getTransactionDetails(transactionID: $transactionID) {
                id
                billingAccountId
                paymentMethodId
                amount
                currency
                description
                status
                type
                discountId
                createdAt
                updatedAt
            }
        }
        """
        
        variables = {
            "transactionID": transaction_id
        }
        
        result = self.client.execute(query, variables)
        tx = result['getTransactionDetails']
        
        return Transaction(
            id=tx['id'],
            billing_account_id=tx['billingAccountId'],
            payment_method_id=tx.get('paymentMethodId'),
            amount=tx['amount'],
            currency=tx['currency'],
            description=tx.get('description'),
            status=TransactionStatus(tx['status']),
            type=TransactionType(tx['type']),
            discount_id=tx.get('discountId'),
            created_at=self._parse_datetime(tx['createdAt']),
            updated_at=self._parse_datetime(tx['updatedAt'])
        )
    
    def get_invoice(self, invoice_id: str) -> Invoice:
        """
        Get details for a specific invoice.
        
        Args:
            invoice_id: ID of the invoice
            
        Returns:
            Invoice details
        """
        query = """
        query GetInvoice($invoiceID: ID!) {
            getInvoice(invoiceID: $invoiceID) {
                id
                billingAccountId
                totalAmount
                currency
                periodStart
                periodEnd
                status
                taxAmount
                taxDetails
                createdAt
                updatedAt
            }
        }
        """
        
        variables = {
            "invoiceID": invoice_id
        }
        
        result = self.client.execute(query, variables)
        inv = result['getInvoice']
        
        return Invoice(
            id=inv['id'],
            billing_account_id=inv['billingAccountId'],
            total_amount=inv['totalAmount'],
            currency=inv['currency'],
            period_start=self._parse_datetime(inv['periodStart']),
            period_end=self._parse_datetime(inv['periodEnd']),
            status=InvoiceStatus(inv['status']),
            tax_amount=inv['taxAmount'],
            tax_details=inv.get('taxDetails'),
            created_at=self._parse_datetime(inv['createdAt']),
            updated_at=self._parse_datetime(inv['updatedAt'])
        )
    
    def get_polling_status(self, transaction_id: str) -> PollingStatus:
        """
        Get current status of a transaction.
        
        Args:
            transaction_id: ID of the transaction
            
        Returns:
            Status information
        """
        query = """
        query GetPollingStatus($transactionID: String!) {
            pollingStatus(transactionID: $transactionID) {
                status
            }
        }
        """
        
        variables = {
            "transactionID": transaction_id
        }
        
        result = self.client.execute(query, variables)
        return PollingStatus(status=result['pollingStatus']['status'])
    
    def get_invoice_pdf(self, invoice_id: str) -> PDF:
        """
        Get PDF content for an invoice.
        
        Args:
            invoice_id: ID of the invoice
            
        Returns:
            PDF content
        """
        query = """
        query GetInvoicePdf($invoiceID: ID!) {
            getInvoicePdf(invoiceID: $invoiceID) {
                pdf
            }
        }
        """
        
        variables = {
            "invoiceID": invoice_id
        }
        
        result = self.client.execute(query, variables)
        return PDF(pdf=result['getInvoicePdf']['pdf'])
    
    def generate_invoice_for_billing_account(
        self,
        billing_account_id: str,
        start_date: datetime,
        end_date: datetime
    ) -> Invoice:
        """
        Generate an invoice for a billing account in a specific period.
        
        Args:
            billing_account_id: ID of the billing account
            start_date: Start date for the invoice period
            end_date: End date for the invoice period
            
        Returns:
            Generated invoice
        """
        mutation = """
        mutation GenerateInvoiceForBillingAccount(
            $billingAccountID: ID!,
            $startDate: DateTime!,
            $endDate: DateTime!
        ) {
            generateInvoiceForBillingAccount(
                billingAccountID: $billingAccountID,
                startDate: $startDate,
                endDate: $endDate
            ) {
                id
                billingAccountId
                totalAmount
                currency
                periodStart
                periodEnd
                status
                taxAmount
                taxDetails
                createdAt
                updatedAt
            }
        }
        """
        
        variables = {
            "billingAccountID": billing_account_id,
            "startDate": start_date.isoformat(),
            "endDate": end_date.isoformat()
        }
        
        result = self.client.execute(mutation, variables)
        inv = result['generateInvoiceForBillingAccount']
        
        return Invoice(
            id=inv['id'],
            billing_account_id=inv['billingAccountId'],
            total_amount=inv['totalAmount'],
            currency=inv['currency'],
            period_start=self._parse_datetime(inv['periodStart']),
            period_end=self._parse_datetime(inv['periodEnd']),
            status=InvoiceStatus(inv['status']),
            tax_amount=inv['taxAmount'],
            tax_details=inv.get('taxDetails'),
            created_at=self._parse_datetime(inv['createdAt']),
            updated_at=self._parse_datetime(inv['updatedAt'])
        )
    
    def generate_invoice_for_transaction(self, transaction_id: str) -> Invoice:
        """
        Generate an invoice for a specific transaction.
        
        Args:
            transaction_id: ID of the transaction
            
        Returns:
            Generated invoice
        """
        mutation = """
        mutation GenerateInvoiceForTransaction($transactionID: ID!) {
            generateInvoiceForTransaction(transactionID: $transactionID) {
                id
                billingAccountId
                totalAmount
                currency
                periodStart
                periodEnd
                status
                taxAmount
                taxDetails
                createdAt
                updatedAt
            }
        }
        """
        
        variables = {
            "transactionID": transaction_id
        }
        
        result = self.client.execute(mutation, variables)
        inv = result['generateInvoiceForTransaction']
        
        return Invoice(
            id=inv['id'],
            billing_account_id=inv['billingAccountId'],
            total_amount=inv['totalAmount'],
            currency=inv['currency'],
            period_start=self._parse_datetime(inv['periodStart']),
            period_end=self._parse_datetime(inv['periodEnd']),
            status=InvoiceStatus(inv['status']),
            tax_amount=inv['taxAmount'],
            tax_details=inv.get('taxDetails'),
            created_at=self._parse_datetime(inv['createdAt']),
            updated_at=self._parse_datetime(inv['updatedAt'])
        )
    
    def create_razorpay_order(self, input: CreateRazorpayOrderInput) -> CreateRazorpayOrderResponse:
        """
        Create a new order using Razorpay.
        
        Args:
            input: Order creation parameters
            
        Returns:
            Order details
        """
        mutation = """
        mutation CreateRazorpayOrder($input: createRazorpayOrderInput!) {
            createRazorpayOrder(input: $input) {
                amount
                currency
                orderID
                key
                transactionID
            }
        }
        """
        
        variables = {
            "input": {
                "billingAccountId": input.billing_account_id,
                "planId": input.plan_id,
                "storeItemId": input.store_item_id,
                "addOnInput": [{"id": addon.id, "quantity": addon.quantity} for addon in input.add_on_ids] if input.add_on_ids else None,
                "recurrence": input.recurrence
            }
        }
        
        result = self.client.execute(mutation, variables)
        order = result['createRazorpayOrder']
        
        return CreateRazorpayOrderResponse(
            amount=order['amount'],
            currency=order['currency'],
            order_id=order['orderID'],
            key=order['key'],
            transaction_id=order['transactionID']
        )
    
    def create_stripe_order(self, input: CreateStripeOrderInput) -> CreateStripeOrderResponse:
        """
        Create a new order using Stripe.
        
        Args:
            input: Order creation parameters
            
        Returns:
            Order details
        """
        mutation = """
        mutation CreateStripeOrder($input: createStripeOrderInput!) {
            createStripeOrder(input: $input) {
                clientSecret
                key
                transactionID
            }
        }
        """
        
        variables = {
            "input": {
                "billingAccountId": input.billing_account_id,
                "planId": input.plan_id,
                "storeItemId": input.store_item_id,
                "addOnInput": [{"id": addon.id, "quantity": addon.quantity} for addon in input.add_on_ids] if input.add_on_ids else None,
                "recurrence": input.recurrence
            }
        }
        
        result = self.client.execute(mutation, variables)
        order = result['createStripeOrder']
        
        return CreateStripeOrderResponse(
            client_secret=order['clientSecret'],
            key=order['key'],
            transaction_id=order['transactionID'],
            amount=order.get('amount', "0")  # Default to "0" if amount is not provided
        )
    
    def _parse_datetime(self, dt_str: str) -> datetime:
        """Parse datetime string from the API"""
        try:
            # Try the dateutil parser first
            from dateutil.parser import parse
            return parse(dt_str)
        except (ImportError, ValueError):
            # Fallback to basic datetime parsing
            try:
                return datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
            except ValueError:
                # Last resort fallback
                return datetime.utcnow() 