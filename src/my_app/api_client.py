import requests
import os
from dotenv import load_dotenv
from config.logger import get_logger
from typing import List, Dict, Any

logger = get_logger(__name__)

# load env variables
load_dotenv()

# store the api key
tfl_app_key = os.getenv('TFL_API_KEY')
tfl_app_id = os.getenv("TFL_APP_ID")


accidents_url =  "https://api.tfl.gov.uk/AccidentStats/2015"
params = {
    "app_id": tfl_app_id,
    "app_key": tfl_app_key
}

response = requests.get(accidents_url, params)
print(response.json())

data = response.get("value", [])

def get_tfl_api_data(
        api_url: str,
        year: int | List[int],
        app_id:str,
        app_key:str,
) -> List[Dict[str, Any]]:
    """
    Function to retrieve data from the sepcified Transport for London api url

    Args:
        api_url: str: The api url to retrieve data from
        year: int | List[int]: Single year or list of years to get data for
        app_id:str : Id for the API
        app_key:str: API key

    Returns:
        List[Dict[str, Any]]: List containing a dictionary of data
    """
    pass