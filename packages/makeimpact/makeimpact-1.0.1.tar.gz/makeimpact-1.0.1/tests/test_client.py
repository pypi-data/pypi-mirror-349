import os
import pytest
import warnings

# Add dotenv for loading environment variables from .env file
try:
    from dotenv import load_dotenv
    # Load environment variables from .env file if it exists
    load_dotenv()
except ImportError:
    warnings.warn("python-dotenv not installed. Cannot load .env file. Install with: pip install python-dotenv")

from makeimpact import (
    OneClickImpact, Environment, PlantTreeParams, CleanOceanParams,
    CaptureCarbonParams, DonateMoneyParams, GetRecordsParams, GetCustomerRecordsParams,
    GetCustomersParams,
    TreePlantedRecord, WasteRemovedRecord, CarbonCapturedRecord, MoneyDonatedRecord,
    TreePlantedRecordWithCustomer, WasteRemovedRecordWithCustomer, 
    CarbonCapturedRecordWithCustomer, MoneyDonatedRecordWithCustomer
)
from makeimpact.exceptions import OneClickImpactError

# Get API key from environment variable (now loaded from .env if it exists)
API_KEY = os.environ.get("TEST_API_KEY")

# Skip all tests if no API key is provided
if not API_KEY:
    warnings.warn(
        "⚠️ No TEST_API_KEY environment variable found. Skipping live API tests.\n"
        "To run these tests, either:\n"
        "1. Create a .env file in the project root with: TEST_API_KEY=your_sandbox_api_key_here\n"
        "2. Set the environment variable: export TEST_API_KEY=your_sandbox_api_key_here"
    )


@pytest.fixture
def sdk():
    """Initialize SDK fixture"""
    if not API_KEY:
        pytest.skip("No TEST_API_KEY environment variable found")
    return OneClickImpact(API_KEY, Environment.SANDBOX)


class TestOneClickImpact:
    """Test cases for the OneClickImpact SDK"""

    class TestInitialization:
        """Tests for SDK initialization"""

        def test_empty_api_key(self):
            """Should throw error when API key is not provided"""
            with pytest.raises(ValueError) as excinfo:
                OneClickImpact("")
            assert "API key is required" in str(excinfo.value)

        def test_invalid_api_key(self):
            """Should throw error when API key does not exist"""
            invalid_sdk = OneClickImpact("incorrect_api_key", Environment.SANDBOX)
            with pytest.raises(OneClickImpactError) as excinfo:
                invalid_sdk.who_am_i()
            assert "API Key does not exist" in str(excinfo.value)

        def test_valid_api_key(self, sdk):
            """Should initialize with API key"""
            assert isinstance(sdk, OneClickImpact)

    class TestWhoAmI:
        """Tests for whoAmI method"""

        def test_verify_api_key(self, sdk):
            """Should verify API key"""
            response = sdk.who_am_i()
            assert response is not None
            assert hasattr(response, "user_id")
            assert hasattr(response, "email")

    class TestGetImpact:
        """Tests for getImpact method"""

        def test_get_impact_statistics(self, sdk):
            """Should get impact statistics"""
            response = sdk.get_impact()
            assert response is not None
            assert hasattr(response, "user_id")
            assert hasattr(response, "tree_planted")
            assert hasattr(response, "waste_removed")
            assert hasattr(response, "carbon_captured")
            assert hasattr(response, "money_donated")

    class TestPlantTrees:
        """Tests for plantTree method"""

        def test_plant_trees(self, sdk):
            """Should plant trees"""
            response = sdk.plant_tree(PlantTreeParams(amount=1))
            assert response is not None
            assert response.user_id
            assert response.tree_planted == 1
            assert response.time_utc
            assert response.customer is None
            assert response.category is None

        def test_plant_trees_with_category(self, sdk):
            """Should plant trees with category"""
            response = sdk.plant_tree(PlantTreeParams(amount=1, category="food"))
            assert response is not None
            assert response.user_id
            assert response.tree_planted == 1
            assert response.time_utc
            assert response.customer is None
            assert response.category == "food"

        def test_plant_trees_with_customer_info(self, sdk):
            """Should plant trees with customer info"""
            response = sdk.plant_tree(PlantTreeParams(
                amount=1,
                customer_email="test@example.com",
                customer_name="Test User"
            ))
            assert response is not None
            assert response.user_id
            assert response.tree_planted == 1
            assert response.time_utc
            assert response.customer is not None
            assert response.customer.customer_id
            assert response.customer.customer_info is not None
            assert response.customer.customer_info.customer_email == "test@example.com"
            assert response.customer.customer_info.customer_name == "Test User"
            assert response.category is None

    class TestCleanOcean:
        """Tests for cleanOcean method"""

        def test_clean_ocean_waste(self, sdk):
            """Should clean ocean waste"""
            response = sdk.clean_ocean(CleanOceanParams(amount=1))
            assert response is not None
            assert response.user_id
            assert response.waste_removed == 1
            assert response.time_utc
            assert response.customer is None

        def test_clean_ocean_waste_with_customer_info(self, sdk):
            """Should clean ocean waste with customer info"""
            response = sdk.clean_ocean(CleanOceanParams(
                amount=1,
                customer_email="test@example.com",
                customer_name="Test User"
            ))
            assert response is not None
            assert response.user_id
            assert response.waste_removed == 1
            assert response.time_utc
            assert response.customer is not None
            assert response.customer.customer_id
            assert response.customer.customer_info is not None
            assert response.customer.customer_info.customer_email == "test@example.com"
            assert response.customer.customer_info.customer_name == "Test User"

    class TestCaptureCarbon:
        """Tests for captureCarbon method"""

        def test_capture_carbon(self, sdk):
            """Should capture carbon"""
            response = sdk.capture_carbon(CaptureCarbonParams(amount=1))
            assert response is not None
            assert response.user_id
            assert response.carbon_captured == 1
            assert response.time_utc
            assert response.customer is None

        def test_capture_carbon_with_customer_info(self, sdk):
            """Should capture carbon with customer info"""
            response = sdk.capture_carbon(CaptureCarbonParams(
                amount=1,
                customer_email="test@example.com",
                customer_name="Test User"
            ))
            assert response is not None
            assert response.user_id
            assert response.carbon_captured == 1
            assert response.time_utc
            assert response.customer is not None
            assert response.customer.customer_id
            assert response.customer.customer_info is not None
            assert response.customer.customer_info.customer_email == "test@example.com"
            assert response.customer.customer_info.customer_name == "Test User"

    class TestDonateMoney:
        """Tests for donateMoney method"""

        def test_donate_money(self, sdk):
            """Should donate money"""
            response = sdk.donate_money(DonateMoneyParams(amount=100))  # $1.00
            assert response is not None
            assert response.user_id
            assert response.money_donated == 100
            assert response.time_utc
            assert response.customer is None

        def test_donate_money_with_customer_info(self, sdk):
            """Should donate money with customer info"""
            response = sdk.donate_money(DonateMoneyParams(
                amount=100,  # $1.00
                customer_email="test@example.com",
                customer_name="Test User"
            ))
            assert response is not None
            assert response.user_id
            assert response.money_donated == 100
            assert response.time_utc
            assert response.customer is not None
            assert response.customer.customer_id
            assert response.customer.customer_info is not None
            assert response.customer.customer_info.customer_email == "test@example.com"
            assert response.customer.customer_info.customer_name == "Test User"

    class TestGetRecords:
        """Tests for getRecords method"""

        def test_get_all_records(self, sdk):
            """Should get all records"""
            response = sdk.get_records()
            assert response is not None
            assert hasattr(response, "user_records")
            assert isinstance(response.user_records, list)

        def test_get_records_with_filters(self, sdk):
            """Should get records with filters"""
            response = sdk.get_records(GetRecordsParams(
                filter_by="tree_planted",
                limit=5
            ))
            assert response is not None
            assert hasattr(response, "user_records")
            assert isinstance(response.user_records, list)
            assert len(response.user_records) <= 5

    class TestGetCustomerRecords:
        """Tests for getCustomerRecords method"""

        def test_get_customer_records(self, sdk):
            """Should get customer records"""
            # First create a record with a customer
            sdk.plant_tree(PlantTreeParams(
                amount=1,
                customer_email="test_customer@example.com",
                customer_name="Test Customer"
            ))

            response = sdk.get_customer_records(GetCustomerRecordsParams(
                customer_email="test_customer@example.com"
            ))
            assert response is not None
            assert hasattr(response, "customer_records")
            assert isinstance(response.customer_records, list)

    class TestGetCustomers:
        """Tests for getCustomers method"""

        def test_get_all_customers(self, sdk):
            """Should get all customers"""
            response = sdk.get_customers()
            assert response is not None
            assert hasattr(response, "customers")
            assert isinstance(response.customers, list)

        def test_get_customer_by_email(self, sdk):
            """Should get customer by email"""
            # Create a customer first
            sdk.plant_tree(PlantTreeParams(
                amount=1,
                customer_email="filtered_customer@example.com",
                customer_name="Filtered Customer"
            ))

            response = sdk.get_customers(GetCustomersParams(
                customer_email="filtered_customer@example.com"
            ))
            assert response is not None
            assert hasattr(response, "customers")
            assert isinstance(response.customers, list)
            
            if response.customers:
                customer = response.customers[0]
                assert customer.customer_email == "filtered_customer@example.com"
                assert customer.customer_name == "Filtered Customer"
                assert customer.customer_id
                assert customer.onboarded_on
