import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_census_api():
    """Test Census API key with a direct request."""
    api_key = os.getenv('CENSUS_API_KEY')
    print(f"\nTesting Census API key: {api_key}")
    
    # Test with 2020 ACS 5-year estimates
    base_url = "https://api.census.gov/data/2020/acs/acs5"
    params = {
        'get': 'B01003_001E',  # Total population
        'for': 'state:*',
        'key': api_key
    }
    
    try:
        print("\nMaking request to Census API...")
        response = requests.get(base_url, params=params)
        print(f"Status code: {response.status_code}")
        print(f"Response headers: {response.headers}")
        
        if response.status_code == 200:
            data = response.json()
            print("\nAPI Response:")
            print(data)
            return True
        else:
            print(f"\nError response: {response.text}")
            return False
            
    except Exception as e:
        print(f"\nError: {str(e)}")
        return False

if __name__ == "__main__":
    test_census_api() 