import json
from typing import Dict, Any, Optional, Union, List
import requests

from .types import (
    Environment,
    PlantTreeParams,
    CleanOceanParams,
    CaptureCarbonParams,
    DonateMoneyParams,
    GetRecordsParams,
    GetCustomerRecordsParams,
    GetCustomersParams,
    PlantTreeResponse,
    CleanOceanResponse,
    CaptureCarbonResponse,
    DonateMoneyResponse,
    GetRecordsResponse,
    GetCustomerRecordsResponse,
    GetCustomersResponse,
    ImpactResponse,
    WhoAmIResponse,
    Customer,
    CustomerInfo,
    CustomerDetails,
    BaseRecord,
    TreePlantedRecord,
    WasteRemovedRecord,
    CarbonCapturedRecord,
    MoneyDonatedRecord,
    BaseRecordWithCustomer,
    TreePlantedRecordWithCustomer,
    WasteRemovedRecordWithCustomer,
    CarbonCapturedRecordWithCustomer,
    MoneyDonatedRecordWithCustomer,
    ImpactRecord,
    CustomerImpactRecord
)
from .exceptions import OneClickImpactError


class OneClickImpact:
    """
    Client for interacting with the 1ClickImpact API
    """

    def __init__(self, api_key: str, environment: Environment = Environment.PRODUCTION):
        """
        Initialize the 1ClickImpact SDK
        
        Args:
            api_key: Your 1ClickImpact API key (get a free key from https://www.1clickimpact.com/pricing)
            environment: Optional: Specify whether to use production or sandbox environment
        """
        if not api_key:
            raise ValueError("API key is required to initialize the 1ClickImpact SDK")
        
        self.api_key = api_key
        
        # Set the base URL based on the environment
        self.base_url = (
            "https://sandbox.1clickimpact.com" 
            if environment == Environment.SANDBOX 
            else "https://api.1clickimpact.com"
        )

    def plant_tree(self, params: PlantTreeParams) -> PlantTreeResponse:
        """
        Plant trees through 1ClickImpact
        
        Args:
            params: Configuration for planting trees
                amount: Number of trees to plant (1-10,000,000)
                category: Optional: Category for the tree planting
                customer_email: Optional: Customer's email
                customer_name: Optional: Customer's name (only used if email is provided)
                
        Returns:
            PlantTreeResponse: Response containing details about the planted trees
        """
        body = {"amount": params.amount}
        
        if params.category:
            body["category"] = params.category
        if params.customer_email:
            body["customer_email"] = params.customer_email
            if params.customer_name:
                body["customer_name"] = params.customer_name
                
        response = self._make_request("/v1/plant_tree", body)
        
        # Transform API response to match the PlantTreeResponse interface
        return PlantTreeResponse(
            user_id=response["user_id"],
            tree_planted=response["tree_planted"],
            category=response.get("category"),
            customer=self._transform_customer(response.get("customer")),
            time_utc=response["time_utc"],
        )

    def clean_ocean(self, params: CleanOceanParams) -> CleanOceanResponse:
        """
        Clean ocean plastic through 1ClickImpact
        
        Args:
            params: Configuration for cleaning ocean plastic
                amount: Amount of waste to clean in pounds (lbs) (1-10,000,000)
                customer_email: Optional: Customer's email
                customer_name: Optional: Customer's name (only used if email is provided)
                
        Returns:
            CleanOceanResponse: Response containing details about the waste removed
        """
        body = {"amount": params.amount}
        
        if params.customer_email:
            body["customer_email"] = params.customer_email
            if params.customer_name:
                body["customer_name"] = params.customer_name
                
        response = self._make_request("/v1/clean_ocean", body)
        
        # Transform API response to match the CleanOceanResponse interface
        return CleanOceanResponse(
            user_id=response["user_id"],
            waste_removed=response["waste_removed"],
            customer=self._transform_customer(response.get("customer")),
            time_utc=response["time_utc"],
        )

    def capture_carbon(self, params: CaptureCarbonParams) -> CaptureCarbonResponse:
        """
        Capture carbon through 1ClickImpact
        
        Args:
            params: Configuration for capturing carbon
                amount: Amount of carbon to capture in pounds (lbs) (1-10,000,000)
                customer_email: Optional: Customer's email
                customer_name: Optional: Customer's name (only used if email is provided)
                
        Returns:
            CaptureCarbonResponse: Response containing details about the carbon captured
        """
        body = {"amount": params.amount}
        
        if params.customer_email:
            body["customer_email"] = params.customer_email
            if params.customer_name:
                body["customer_name"] = params.customer_name
                
        response = self._make_request("/v1/capture_carbon", body)
        
        # Transform API response to match the CaptureCarbonResponse interface
        return CaptureCarbonResponse(
            user_id=response["user_id"],
            carbon_captured=response["carbon_captured"],
            customer=self._transform_customer(response.get("customer")),
            time_utc=response["time_utc"],
        )

    def donate_money(self, params: DonateMoneyParams) -> DonateMoneyResponse:
        """
        Donate money through 1ClickImpact
        
        Args:
            params: Configuration for donating money
                amount: Amount in smallest USD units (cents). For example, $1 = 100, $0.10 = 10 (1-1,000,000,000)
                customer_email: Optional: Customer's email
                customer_name: Optional: Customer's name (only used if email is provided)
                
        Returns:
            DonateMoneyResponse: Response containing details about the money donated
        """
        body = {"amount": params.amount}
        
        if params.customer_email:
            body["customer_email"] = params.customer_email
            if params.customer_name:
                body["customer_name"] = params.customer_name
                
        response = self._make_request("/v1/donate_money", body)
        
        # Transform API response to match the DonateMoneyResponse interface
        return DonateMoneyResponse(
            user_id=response["user_id"],
            money_donated=response["money_donated"],
            customer=self._transform_customer(response.get("customer")),
            time_utc=response["time_utc"],
        )

    def get_impact(self) -> ImpactResponse:
        """
        Get impact statistics
        
        Returns:
            ImpactResponse: Impact statistics for your organization
        """
        response = self._make_request("/v1/impact", None, "GET")
        
        return ImpactResponse(
            user_id=response["user_id"],
            tree_planted=response.get("tree_planted", 0),
            waste_removed=response.get("waste_removed", 0),
            carbon_captured=response.get("carbon_captured", 0),
            money_donated=response.get("money_donated", 0),
        )

    def who_am_i(self) -> WhoAmIResponse:
        """
        Verify API key and get account information
        
        Returns:
            WhoAmIResponse: Account information for the provided API key
        """
        response = self._make_request("/v1/whoami", None, "GET")
        
        return WhoAmIResponse(
            user_id=response["user_id"],
            email=response["email"],
        )

    def get_records(self, params: Optional[GetRecordsParams] = None) -> GetRecordsResponse:
        """
        Get impact records
        
        Args:
            params: Optional parameters to filter records
                filter_by: Optional: Filter records by type. The value could be either 
                          "tree_planted", "waste_removed", "carbon_captured", or "money_donated".
                start_date: Optional: Filter records created on or after this date (format: YYYY-MM-DD)
                end_date: Optional: Filter records created on or before this date (format: YYYY-MM-DD)
                cursor: Optional: Pagination cursor from previous response for fetching next page
                limit: Optional: Maximum number of records to return (1-1000, default: 10)
                
        Returns:
            GetRecordsResponse: Records based on the provided filters
        """
        if params is None:
            params = GetRecordsParams()
            
        query_params = {}
        if params.filter_by:
            query_params["filter_by"] = params.filter_by
        if params.start_date:
            query_params["start_date"] = params.start_date
        if params.end_date:
            query_params["end_date"] = params.end_date
        if params.cursor:
            query_params["cursor"] = params.cursor
        if params.limit is not None:
            query_params["limit"] = params.limit
            
        endpoint = "/v1/records"
        response = self._make_request(endpoint, None, "GET", query_params)
        
        # Transform the API response format to match our SDK interface
        user_records = []
        for record in response["user_records"]:
            base_record = {
                "user_id": record["user_id"],
                "time_utc": record["time_utc"],
            }
            
            if "tree_planted" in record:
                user_records.append(TreePlantedRecord(
                    **base_record,
                    tree_planted=record["tree_planted"],
                    category=record.get("category")
                ))
            elif "waste_removed" in record:
                user_records.append(WasteRemovedRecord(
                    **base_record,
                    waste_removed=record["waste_removed"]
                ))
            elif "carbon_captured" in record:
                user_records.append(CarbonCapturedRecord(
                    **base_record,
                    carbon_captured=record["carbon_captured"]
                ))
            elif "money_donated" in record:
                user_records.append(MoneyDonatedRecord(
                    **base_record,
                    money_donated=record["money_donated"]
                ))
                
        return GetRecordsResponse(
            user_records=user_records,
            cursor=response.get("cursor"),
        )

    def get_customer_records(self, params: Optional[GetCustomerRecordsParams] = None) -> GetCustomerRecordsResponse:
        """
        Get customer records
        
        Args:
            params: Optional parameters to filter customer records
                customer_email: Optional: Filter records by customer email
                filter_by: Optional: Filter records by type. The value could be either 
                          "tree_planted", "waste_removed", "carbon_captured", or "money_donated".
                start_date: Optional: Filter records created on or after this date (format: YYYY-MM-DD)
                end_date: Optional: Filter records created on or before this date (format: YYYY-MM-DD)
                cursor: Optional: Pagination cursor from previous response for fetching next page
                limit: Optional: Maximum number of records to return (1-1000, default: 10)
                
        Returns:
            GetCustomerRecordsResponse: Customer records based on the provided filters
        """
        if params is None:
            params = GetCustomerRecordsParams()
            
        query_params = {}
        if params.customer_email:
            query_params["customer_email"] = params.customer_email
        if params.filter_by:
            query_params["filter_by"] = params.filter_by
        if params.start_date:
            query_params["start_date"] = params.start_date
        if params.end_date:
            query_params["end_date"] = params.end_date
        if params.cursor:
            query_params["cursor"] = params.cursor
        if params.limit is not None:
            query_params["limit"] = params.limit
            
        endpoint = "/v1/customer_records"
        response = self._make_request(endpoint, None, "GET", query_params)
        
        # Transform the API response format to match our SDK interface
        customer_records = []
        for record in response["customer_records"]:
            base_record = {
                "user_id": record["user_id"],
                "time_utc": record["time_utc"],
                "customer": self._transform_customer(record["customer"]),
            }
            
            if "tree_planted" in record:
                customer_records.append(TreePlantedRecordWithCustomer(
                    **base_record,
                    tree_planted=record["tree_planted"],
                    category=record.get("category")
                ))
            elif "waste_removed" in record:
                customer_records.append(WasteRemovedRecordWithCustomer(
                    **base_record,
                    waste_removed=record["waste_removed"]
                ))
            elif "carbon_captured" in record:
                customer_records.append(CarbonCapturedRecordWithCustomer(
                    **base_record,
                    carbon_captured=record["carbon_captured"]
                ))
            elif "money_donated" in record:
                customer_records.append(MoneyDonatedRecordWithCustomer(
                    **base_record,
                    money_donated=record["money_donated"]
                ))
                
        return GetCustomerRecordsResponse(
            customer_records=customer_records,
            cursor=response.get("cursor"),
        )

    def get_customers(self, params: Optional[GetCustomersParams] = None) -> GetCustomersResponse:
        """
        Get customers
        
        Args:
            params: Optional parameters to filter customers
                customer_email: Optional: Filter customers by email
                limit: Optional: Maximum number of customers to return (1-1000, default: 10)
                cursor: Optional: Pagination cursor from previous response for fetching next page
                
        Returns:
            GetCustomersResponse: Customers based on the provided filters
        """
        if params is None:
            params = GetCustomersParams()
            
        query_params = {}
        if params.customer_email:
            query_params["customer_email"] = params.customer_email
        if params.limit is not None:
            query_params["limit"] = params.limit
        if params.cursor:
            query_params["cursor"] = params.cursor
            
        endpoint = "/v1/customers"
        response = self._make_request(endpoint, None, "GET", query_params)
        
        # Transform the API response to match our SDK interface
        customers = []
        for customer in response["customers"]:
            customers.append(CustomerDetails(
                customer_id=customer["customer_id"],
                customer_email=customer["customer_email"],
                customer_name=customer.get("customer_name"),
                onboarded_on=customer["onboarded_on"],
            ))
                
        return GetCustomersResponse(
            customers=customers,
            cursor=response.get("cursor"),
        )

    def _make_request(
        self, 
        endpoint: str, 
        body: Optional[Dict[str, Any]] = None, 
        method: str = "POST",
        query_params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Makes a request to the 1ClickImpact API
        
        Args:
            endpoint: API endpoint
            body: Request body
            method: HTTP method (default: POST)
            query_params: Query parameters to include in the URL
            
        Returns:
            API response
            
        Raises:
            OneClickImpactError: If the API returns an error
        """
        try:
            headers = {
                "Content-Type": "application/json",
                "x-api-key": self.api_key,
            }
            
            url = f"{self.base_url}{endpoint}"
            
            if query_params:
                # Add query parameters to URL
                query_string = "&".join(f"{k}={v}" for k, v in query_params.items())
                url = f"{url}?{query_string}"
            
            if method == "GET":
                response = requests.get(url, headers=headers)
            elif method == "POST":
                response = requests.post(url, headers=headers, json=body if body else {})
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response_data = response.json()
            
            if not response.ok:
                if "type" in response_data and "message" in response_data:
                    raise OneClickImpactError(
                        message=response_data["message"],
                        error_type=response_data["type"]
                    )
                raise OneClickImpactError(f"Request failed with status {response.status_code}")
            
            return response_data
        
        except requests.RequestException as e:
            raise OneClickImpactError(f"1ClickImpact API Error: {str(e)}")
        except Exception as e:
            raise OneClickImpactError(f"1ClickImpact SDK Error: {str(e)}")

    def _transform_customer(self, customer_data: Optional[Dict[str, Any]]) -> Optional[Customer]:
        """
        Helper function to transform customer data from API format to SDK format
        
        Args:
            customer_data: Customer data from the API
            
        Returns:
            Transformed Customer object or None if customer_data is None
        """
        if not customer_data:
            return None
            
        return Customer(
            customer_id=customer_data["customer_id"],
            customer_info=CustomerInfo(
                customer_email=customer_data.get("customer_email"),
                customer_name=customer_data.get("customer_name"),
            )
        )
