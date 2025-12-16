import requests
import os
from dotenv import load_dotenv
from config.logger import get_logger
from typing import List, Dict, Any
from requests.exceptions import Timeout, RequestException
import random
import json

logger = get_logger(__name__)

# load env variables
load_dotenv()

# store the api key
tfl_app_key = os.getenv('TFL_API_KEY')
tfl_app_id = os.getenv("TFL_APP_ID")
accidents_url =  "https://api.tfl.gov.uk/AccidentStats/"

def get_tfl_api_data(
        api_url: str,
        year: int | List[int],
        app_id:str,
        app_key:str,
        retries: int,
        base_delay: float=0.1,
        jitter_factor: float=0.1,
        max_delay: int=60
) -> List[Dict[str, Any]]:
    """
    Function to retrieve data from the sepcified Transport for London api url

    Args:
        api_url: str: The api url to retrieve data from
        year: int | List[int]: Single year or list of years to get data for
        app_id: str : Id for the API
        app_key: str: API key
        retries: int: How many retries can be called on the API

    Returns:
        List[Dict[str, Any]]: List containing a dictionary of data
    """
    # create params
    params = {
        "app_id": app_id,
        "app_key": app_key
    }

    years = [year] if isinstance(year, int) else year
    all_rows = []

    for y in years:
               api_endpoint_url = f"{api_url}{y}"
               logger.info(f"Requesting data from TFL API, params: year={y}, url={api_endpoint_url}")
               
               for attempt in range(retries+1):
                   try:
                    response = requests.get(api_endpoint_url, params, timeout=30)
                    response.raise_for_status()
                    data = response.json()
                    #rows = data.get("value", [])
                    all_rows.extend(data)
                    logger.info(f"Successfuly retrieved the data from TFL API,  params: year={y}, url={api_endpoint_url}")
                    # exit retry loop
                    break
                   
                   except(Timeout, ConnectionError):
                       # retryable network error
                       logger.warning(f"Network error retrying: attempt{attempt}, error:{e}")
                   
                   except RequestException as e:
                       status = getattr(e.response, "status_code", None)
                       if status and 500 <= status < 600:
                           # retryable server errors
                           logger.warning(f"Server error, retrying: attempt{attempt}, error:{e}")
                       else:
                           logger.error(f"Non-retryable request error, error: {e}")
                           raise

                   except Exception as e:
                       raise RuntimeError(f"Non retryable error: {e}")
                   
                       # exponential backoff
                       if attempt < retries:
                        delay = min(base_delay * (2**attempt), max_delay)
                        jitter = random.uniform(0, base_delay * jitter_factor)
                        total_delay = delay + jitter
                        logger.debug(f"Sleeping before retry, attempt:{attempt}, sleep time{total_delay}")
                        time.sleep(total_delay)

                       else:
                           logger.error(f"Max retries exceeded")

    return all_rows
                       

data =  get_tfl_api_data(
        accidents_url,
        2015,
        tfl_app_id,
        tfl_app_key,
        5)


with open("json.data", mode='w') as file:
    json.dump(data, file)