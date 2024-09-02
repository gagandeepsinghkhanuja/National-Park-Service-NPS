# Import necessary libraries
import requests  # For making API requests
import pandas as pd  # For data manipulation and analysis
import os  # For file operations
import pprint  # For pretty-printing JSON data (optional for debugging)
import json  # For handling JSON data
import time  # For adding delays between requests
import random  # For generating random delays
from fake_useragent import UserAgent  # For generating random User-Agent strings

# Load API key from a file (to keep it secure)
with open('api_key_file.txt', 'r') as f:
    API_KEY = f.read().strip()

# Define the API endpoint and parameters
url = 'https://developer.nps.gov/api/v1/parks?stateCode='
params = {
    'api_key': API_KEY,
    'fields': 'entranceFees',
    'limit': 100
}

# List of state codes to retrieve data for
stateCode = ['AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA',
             'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME',
             'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM',
             'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
             'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY']

# Initialize a list to hold the collected data
data = []
ua = UserAgent()  # Initialize the UserAgent generator

# Start a session for making requests
with requests.Session() as session:
    # Open a file to store the URLs that were accessed
    with open('NPS_urls.txt', 'a+') as f:
        for state in stateCode:
            headers = {
                'User-Agent': ua.random,  # Use a random User-Agent for each request
                'Accept-Language': 'en-US,en;q=0.9',
                'Referer': 'https://www.google.com',
                'DNT': '1'  # Do Not Track request header
            }
            
            # Make the API request
            response = session.get(url + state, params=params, headers=headers)
            
            # Check if the request was successful
            if response.status_code == 200:
                # Ensure the response text is not empty
                if response.text.strip():  # Check if the response is not just empty or whitespace
                    try:
                        # Load the response data as JSON
                        state_data = response.json()
                        
                        # Append the data to the main list
                        data.extend(state_data.get('data', []))
                        
                        # Write the accessed URL to the file
                        f.writelines(response.url + '\n')
                    except json.JSONDecodeError:
                        print(f"JSONDecodeError for state: {state}")
                else:
                    print(f"No data for state: {state}")
            else:
                print(f"Failed to retrieve data for state: {state}. Status code: {response.status_code}")
            
            # Randomized delay between requests (e.g., 8 to 15 seconds)
            delay = random.uniform(8, 15)
            print(f"Sleeping for {delay:.2f} seconds...")
            time.sleep(delay)
        
        # Close the file
        f.close()

# Save the collected data to a JSON file
with open('nps_data.json', 'w') as json_file:
    json.dump(data, json_file, indent=4)

print("Data extraction completed and saved to nps_data.json")

# Convert the data into a pandas DataFrame for further processing
parks_data = pd.DataFrame(data)
print(parks_data.head())

# Initialize a dictionary to store park data with entry fee details
park_data_dict = {}

# Iterate over the rows in the DataFrame to extract relevant information
for index, park in parks_data.iterrows():
    # Initialize a list to hold fee details for this park
    fee_details = []
    
    # Check if 'entranceFees' is available and is a list
    if 'entranceFees' in park and isinstance(park['entranceFees'], list):
        for fee in park['entranceFees']:
            fee_details.append({
                'fee_usd': f"${fee['cost']}",
                'fee_type': fee['title'],
                'fee_description': fee['description']
            })
    
    # Store the park details with its list of fees
    park_data_dict[park['parkCode']] = {
        'fullName': park.get('fullName', ''),
        'latitude': park.get('latitude', ''),
        'longitude': park.get('longitude', ''),
        'latLong': park.get('latLong', ''),
        'states': park.get('states', ''),
        'designation': park.get('designation', ''),
        'fees': fee_details  # Add the list of fees under a 'fees' key, empty if no fees available
    }

# Print the first few entries in the dictionary to verify the data
pprint.pprint(list(park_data_dict.items())[:5])

# Initialize an empty list to store expanded data for the DataFrame
expanded_data = []

# Iterate over the park_data_dict to expand fees into individual rows
for park_code, park_info in park_data_dict.items():
    # Check if the park has any fees; if not, create a row with fee as $0
    if not park_info['fees']:
        expanded_data.append({
            'Park Code': park_code,
            'State(s)': park_info['states'],
            'Park Name': park_info['fullName'],
            'Designation': park_info['designation'],
            'Latitude': park_info['latitude'],
            'Longitude': park_info['longitude'],
            'Coordinates': park_info['latLong'],
            'Fee (USD)': "$0.00",
            'Fee Type': "No Fee",
            'Fee Description': "This location does not charge an entrance fee."
        })
    else:
        for fee in park_info['fees']:
            expanded_data.append({
                'Park Code': park_code,
                'State(s)': park_info['states'],
                'Park Name': park_info['fullName'],
                'Designation': park_info['designation'],
                'Latitude': park_info['latitude'],
                'Longitude': park_info['longitude'],
                'Coordinates': park_info['latLong'],
                'Fee (USD)': fee['fee_usd'],
                'Fee Type': fee['fee_type'],
                'Fee Description': fee['fee_description']
            })

# Create a DataFrame from the expanded data
df_park_fees = pd.DataFrame(expanded_data)

# Display the first few rows of the DataFrame
print(df_park_fees.head())

# Save the DataFrame to a CSV file with renamed columns
df_park_fees.to_csv('park_fees_data.csv', index=False)
print("Data saved to park_fees_data.csv")