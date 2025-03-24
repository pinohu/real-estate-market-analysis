import pytest
import requests
import urllib.parse
from config.free_sources import FreeSourcesConfig
import os

def test_real_census_api_call():
    """Test real Census API call"""
    config = FreeSourcesConfig.get_config()
    api_key = config['census_api_key']
    
    # Test Census API with a simple query for Seattle's population
    url = f"https://api.census.gov/data/2020/dec/pl?get=P1_001N&for=place:63000&in=state:53&key={api_key}"
    response = requests.get(url)
    
    assert response.status_code == 200
    data = response.json()
    print("\nCensus API Response:")
    print(f"Seattle Population: {data[1][0]}")
    return data

def test_real_walk_score_api_call():
    """Test real Walk Score API call"""
    config = FreeSourcesConfig.get_config()
    api_key = config['walk_score_api_key']
    
    # Test Walk Score API with Seattle address
    address = "700 1st Ave Seattle WA 98104"
    lat = "47.6032"
    lon = "-122.3303"
    
    params = {
        'format': 'json',
        'address': address,
        'lat': lat,
        'lon': lon,
        'wsapikey': api_key
    }
    
    url = f"https://api.walkscore.com/score?{urllib.parse.urlencode(params)}"
    response = requests.get(url)
    
    assert response.status_code == 200
    data = response.json()
    print("\nWalk Score API Response:")
    print(f"Walk Score: {data.get('walkscore', 'N/A')}")
    print(f"Description: {data.get('description', 'N/A')}")
    return data

def test_real_hud_api_call():
    """Test real HUD API call"""
    config = FreeSourcesConfig.get_config()
    api_key = config['hud_api_key']
    
    # Test HUD API for King County (Seattle) Fair Market Rents
    url = "https://www.huduser.gov/hudapi/public/fmr/statedata/WA"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json"
    }
    response = requests.get(url, headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    print("\nHUD API Response:")
    print(f"Fair Market Rents Data for Washington State:")
    if 'data' in data:
        for county in data['data']:
            if 'countyName' in county and county['countyName'].startswith('King'):
                print(f"County: {county['countyName']}")
                print(f"Small Area FMR: {county.get('smallAreaFmr', 'Not available')}")
                print(f"Metro Area: {county.get('metroArea', 'Not available')}")
    return data

def test_real_epa_api_call():
    """Test EPA API call for environmental data"""
    # Test EPA Envirofacts API for facility information
    url = "https://data.epa.gov/efservice/PUB_DIM_FACILITY/STATE_CODE/WA/JSON"
    response = requests.get(url)
    
    assert response.status_code == 200
    data = response.json()
    print("\nEPA Environmental Data Response:")
    if data:
        print(f"Number of EPA-regulated facilities in Washington: {len(data)}")
        if len(data) > 0:
            facility = data[0]
            print(f"Sample Facility:")
            print(f"Name: {facility.get('FACILITY_NAME', 'N/A')}")
            print(f"City: {facility.get('CITY_NAME', 'N/A')}")
            print(f"County: {facility.get('COUNTY_NAME', 'N/A')}")
    return data

def test_real_usgs_api_call():
    """Test USGS API call for earthquake data"""
    # Test USGS Earthquake API for recent earthquakes near Seattle
    url = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&latitude=47.6032&longitude=-122.3303&maxradiuskm=100&minmagnitude=2.0&orderby=time"
    response = requests.get(url)
    
    assert response.status_code == 200
    data = response.json()
    print("\nUSGS Earthquake Response:")
    if data.get('features'):
        latest = data['features'][0]['properties']
        print(f"Latest Earthquake:")
        print(f"Magnitude: {latest.get('mag', 'N/A')}")
        print(f"Location: {latest.get('place', 'N/A')}")
        print(f"Time: {latest.get('time', 'N/A')}")
    return data

def test_real_noaa_api_call():
    """Test NOAA API call for weather data"""
    config = FreeSourcesConfig.get_config()
    api_key = config.get('noaa_api_key', 'XvZNvgZLyxqoBeIwKRnfLbXoKRnWyxNE')
    
    # Test NOAA API for weather forecast
    url = "https://api.weather.gov/points/47.6032,-122.3303"
    headers = {
        "Accept": "application/json",
        "User-Agent": "RealEstateStrategist/1.0"
    }
    response = requests.get(url, headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    print("\nNOAA Weather Response:")
    if 'properties' in data:
        props = data['properties']
        print(f"Grid ID: {props.get('gridId', 'N/A')}")
        print(f"Forecast Office: {props.get('forecastOffice', 'N/A')}")
        
        # Get detailed forecast
        if 'forecast' in props:
            forecast_url = props['forecast']
            forecast_response = requests.get(forecast_url, headers=headers)
            if forecast_response.status_code == 200:
                forecast_data = forecast_response.json()
                if 'properties' in forecast_data and 'periods' in forecast_data['properties']:
                    current = forecast_data['properties']['periods'][0]
                    print(f"Current Forecast: {current.get('shortForecast', 'N/A')}")
                    print(f"Temperature: {current.get('temperature', 'N/A')}°{current.get('temperatureUnit', 'F')}")
    return data

def test_real_fema_api_call():
    """Test FEMA API call through data.gov for disaster declarations"""
    config = FreeSourcesConfig.get_config()
    api_key = config['data_gov_api_key']
    
    # Test FEMA API for disaster declarations in Washington state
    url = f"https://api.data.gov/fema/v2/femaWebDisasterDeclarations?state=WA&$limit=5&api_key={api_key}"
    response = requests.get(url)
    
    assert response.status_code == 200
    data = response.json()
    print("\nFEMA Disaster Declarations Response:")
    if data.get('DisasterDeclarations'):
        for declaration in data['DisasterDeclarations'][:3]:
            print(f"Disaster: {declaration.get('disasterName', 'N/A')}")
            print(f"Type: {declaration.get('incidentType', 'N/A')}")
            print(f"State: {declaration.get('state', 'N/A')}")
            print(f"Declaration Date: {declaration.get('declarationDate', 'N/A')}")
    return data

def test_real_education_api_call():
    """Test Education API call through data.gov for college data"""
    config = FreeSourcesConfig.get_config()
    api_key = config['data_gov_api_key']
    
    # Test College Scorecard API for schools in Washington
    url = f"https://api.data.gov/ed/collegescorecard/v1/schools?school.state=WA&fields=school.name,school.city,latest.admissions.admission_rate.overall&api_key={api_key}"
    response = requests.get(url)
    
    assert response.status_code == 200
    data = response.json()
    print("\nCollege Scorecard API Response:")
    if data.get('results'):
        for school in data['results'][:3]:
            print(f"School: {school.get('school.name', 'N/A')}")
            print(f"City: {school.get('school.city', 'N/A')}")
            print(f"Admission Rate: {school.get('latest.admissions.admission_rate.overall', 'N/A')}")
    return data

def test_real_crime_api_call():
    """Test FBI Crime Data API call through data.gov"""
    config = FreeSourcesConfig.get_config()
    api_key = config['data_gov_api_key']
    
    # Test FBI Crime Data API for Washington state
    url = f"https://api.data.gov/fbi/v1/crime-data-explorer/state/WA/violent-crime?api_key={api_key}"
    response = requests.get(url)
    
    assert response.status_code == 200
    data = response.json()
    print("\nFBI Crime Data API Response:")
    if data.get('results'):
        for result in data['results'][:3]:
            print(f"Year: {result.get('year', 'N/A')}")
            print(f"Violent Crime Rate: {result.get('violent_crime_rate', 'N/A')}")
            print(f"Property Crime Rate: {result.get('property_crime_rate', 'N/A')}")
    return data

def test_real_eia_api_call():
    """Test EIA Energy Data API call through data.gov"""
    config = FreeSourcesConfig.get_config()
    api_key = config['data_gov_api_key']
    
    # Test EIA API for residential electricity rates in Washington
    url = f"https://api.data.gov/eia/v2/electricity/retail-sales?state=WA&sector=RES&api_key={api_key}"
    response = requests.get(url)
    
    assert response.status_code == 200
    data = response.json()
    print("\nEIA Energy Data API Response:")
    if data.get('response', {}).get('data'):
        for rate in data['response']['data'][:3]:
            print(f"Period: {rate.get('period', 'N/A')}")
            print(f"Average Price (cents/kWh): {rate.get('price', 'N/A')}")
            print(f"Sales (MWh): {rate.get('sales', 'N/A')}")
    return data

def test_real_bls_api_call():
    """Test BLS API call for employment data"""
    config = FreeSourcesConfig.get_config()
    api_key = config['bls_api_key']
    
    # Test BLS API for employment data in Seattle area
    headers = {'Content-type': 'application/json'}
    data = {
        "seriesid": ["LAUMT534264000000003"],  # Seattle MSA unemployment rate
        "startyear": "2023",
        "endyear": "2023",
        "registrationkey": api_key
    }
    url = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
    response = requests.post(url, json=data, headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    print("\nBLS Employment Data Response:")
    if data.get('Results', {}).get('series'):
        series = data['Results']['series'][0]
        for observation in series.get('data', [])[:3]:
            print(f"Period: {observation.get('period', 'N/A')}")
            print(f"Value: {observation.get('value', 'N/A')}%")
            print(f"Year: {observation.get('year', 'N/A')}")
    return data

def test_real_gsa_api_call():
    """Test GSA API call for federal buildings data"""
    config = FreeSourcesConfig.get_config()
    api_key = config['data_gov_api_key']
    
    # Test GSA API for federal buildings in Washington state
    url = f"https://api.data.gov/gsa/federal_buildings/v1/properties?state=WA&api_key={api_key}"
    response = requests.get(url)
    
    assert response.status_code == 200
    data = response.json()
    print("\nGSA Federal Buildings Response:")
    if data.get('properties'):
        for property in data['properties'][:3]:
            print(f"Building Name: {property.get('building_name', 'N/A')}")
            print(f"Address: {property.get('address', 'N/A')}")
            print(f"City: {property.get('city', 'N/A')}")
    return data

def test_real_dot_api_call():
    """Test DOT API call for transit data"""
    config = FreeSourcesConfig.get_config()
    api_key = config['data_gov_api_key']
    
    # Test DOT API for transit agencies in Washington
    url = f"https://api.data.gov/dot/ntd/agencies?state=WA&api_key={api_key}"
    response = requests.get(url)
    
    assert response.status_code == 200
    data = response.json()
    print("\nDOT Transit Data Response:")
    if data.get('agencies'):
        for agency in data['agencies'][:3]:
            print(f"Agency Name: {agency.get('agency_name', 'N/A')}")
            print(f"City: {agency.get('city', 'N/A')}")
            print(f"Service Area: {agency.get('service_area', 'N/A')}")
    return data

def test_real_irs_api_call():
    """Test IRS API call for tax statistics"""
    config = FreeSourcesConfig.get_config()
    api_key = config['data_gov_api_key']
    
    # Test IRS API for tax statistics in Washington
    url = f"https://api.data.gov/irs/v1/tax-statistics?state=WA&year=2022&api_key={api_key}"
    response = requests.get(url)
    
    assert response.status_code == 200
    data = response.json()
    print("\nIRS Tax Statistics Response:")
    if data.get('tax_stats'):
        for stat in data['tax_stats'][:3]:
            print(f"ZIP Code: {stat.get('zip_code', 'N/A')}")
            print(f"Average Income: {stat.get('avg_income', 'N/A')}")
            print(f"Returns Filed: {stat.get('returns_filed', 'N/A')}")
    return data

def test_real_usps_api_call():
    """Test USPS API call for address validation"""
    pytest.skip("USPS API access not available")

def test_all_real_api_calls():
    """Test all real API calls"""
    print("\nTesting all API connections...")
    
    census_data = test_real_census_api_call()
    walk_score_data = test_real_walk_score_api_call()
    hud_data = test_real_hud_api_call()
    epa_data = test_real_epa_api_call()
    usgs_data = test_real_usgs_api_call()
    noaa_data = test_real_noaa_api_call()
    fema_data = test_real_fema_api_call()
    education_data = test_real_education_api_call()
    crime_data = test_real_crime_api_call()
    eia_data = test_real_eia_api_call()
    bls_data = test_real_bls_api_call()
    gsa_data = test_real_gsa_api_call()
    dot_data = test_real_dot_api_call()
    irs_data = test_real_irs_api_call()
    # Skipping USPS test as access is not available
    
    print("\nAll API tests completed successfully!")
    return {
        'census': census_data,
        'walk_score': walk_score_data,
        'hud': hud_data,
        'epa': epa_data,
        'usgs': usgs_data,
        'noaa': noaa_data,
        'fema': fema_data,
        'education': education_data,
        'crime': crime_data,
        'eia': eia_data,
        'bls': bls_data,
        'gsa': gsa_data,
        'dot': dot_data,
        'irs': irs_data
    } 