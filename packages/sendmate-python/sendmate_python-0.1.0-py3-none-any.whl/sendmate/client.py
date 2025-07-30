import os
from typing import Optional, Dict, Any
import requests
from dotenv import load_dotenv
from .types import PaymentType, Currency, TransactionStatus

class SendMate:
    def __init__(self, api_key: Optional[str] = None, environment: str = "production"):
        """
        Initialize the SendMate client
        
        Args:
            api_key: Your SendMate API key. If not provided, will look for SENDMATE_API_KEY in environment
            environment: The environment to use ('production' or 'sandbox')
        """
        load_dotenv()
        self.api_key = api_key or os.getenv("SENDMATE_API_KEY")
        if not self.api_key:
            raise ValueError("API key must be provided either directly or through SENDMATE_API_KEY environment variable")
        
        self.base_url = "https://api.sendmate.finance/v1" if environment == "production" else "https://api-sandbox.sendmate.finance/v1"
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

    def _make_request(self, method: str, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Make an HTTP request to the SendMate API
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint
            data: Request payload
            
        Returns:
            API response as dictionary
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = self.session.request(method, url, json=data)
        response.raise_for_status()
        return response.json()

    def create_checkout(self, amount: float, currency: Currency, description: str, return_url: str, cancel_url: str, **kwargs) -> Dict[str, Any]:
        """
        Create a new checkout session
        
        Args:
            amount: Transaction amount
            currency: Currency code
            payment_type: Type of payment
            customer_email: Customer's email
            customer_name: Customer's name
            **kwargs: Additional parameters
            
        Returns:
            Checkout session details
        """
        data = {
            "amount": amount,
            "currency": currency,
            "description": description,
            "return_url": return_url,
            "cancel_url": cancel_url,
            **kwargs
        }
        return self._make_request("POST", "/payments/checkout", data)

    def get_transaction_status(self, transaction_id: str) -> TransactionStatus:
        """
        Get the status of a transaction
        
        Args:
            transaction_id: The transaction ID to check
            
        Returns:
            Transaction status
        """
        response = self._make_request("GET", f"/payments/transactions/{transaction_id}")
        return TransactionStatus(response["status"]) 
    
    
    
    