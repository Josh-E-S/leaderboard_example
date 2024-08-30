# zapier_integration.py

import requests
import pandas as pd

def get_leaderboard_data_from_zapier(webhook_url):
    """
    Fetch leaderboard data from Zapier using a webhook URL.
    
    :param webhook_url: The Zapier webhook URL to fetch data from
    :return: A pandas DataFrame containing the leaderboard data
    """
    try:
        response = requests.get(webhook_url)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        
        # Assuming the data is a list of dictionaries, each representing a row
        df = pd.DataFrame(data)
        
        # Ensure all expected columns are present
        expected_columns = ['Rank', 'Runner Name', 'DogCallName', 'LifeTimeMiles', 'Breed']
        for column in expected_columns:
            if column not in df.columns:
                df[column] = None  # Add missing columns with None values
        
        # Convert 'Rank' and 'LifeTimeMiles' to appropriate types
        df['Rank'] = pd.to_numeric(df['Rank'], errors='coerce')
        df['LifeTimeMiles'] = pd.to_numeric(df['LifeTimeMiles'], errors='coerce')
        
        return df
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from Zapier: {e}")
        return None

# Example usage:
# webhook_url = "https://hooks.zapier.com/hooks/catch/your_unique_webhook_url"
# df = get_leaderboard_data_from_zapier(webhook_url)