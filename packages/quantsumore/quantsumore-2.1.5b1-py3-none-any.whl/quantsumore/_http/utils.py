# -*- coding: utf-8 -*-
#
## ╭────────────────────────────────────────────────────────────────────────────────────────────╮
## │  Library         : doydl's Finance API Client — quantsumore                                 │
## │                                                                                             │
## │                                                                                             │
## │  Description     : `quantsumore` is a comprehensive Python library designed to streamline   │
## │                    the process of accessing and analyzing real-time financial data across   │
## │                    various markets. It provides specialized API clients to fetch data       │
## │                    from multiple financial instruments, including:                          │
## │                      - Cryptocurrencies                                                     │
## │                      - Equities and Stock Markets                                           │
## │                      - Foreign Exchange (Forex)                                             │
## │                      - Treasury Instruments                                                 │
## │                      - Consumer Price Index (CPI) Metrics                                   │
## │                                                                                             │
## │                    The library offers a unified interface for retrieving diverse financial  │
## │                    data, enabling users to perform in-depth financial and technical         │
## │                    analysis. Whether you're developing trading algorithms, conducting       │
## │                    market research, or building financial dashboards, `quantsumore` serves  │
## │                    as a reliable and efficient tool in your data pipeline.                  │
## │                                                                                             │
## │                                                                                             │
## │  Key Features    : - Real-time data retrieval from multiple financial markets               │
## │                    - Support for various financial instruments and metrics                  │
## │                    - Simplified API clients for ease of integration                         │
## │                    - Designed for both personal and non-commercial use                      │
## │                                                                                             │
## │                                                                                             │
## │  Legal Disclaimer: `quantsumore` is an independent Python library and is not affiliated     │
## │                    with any financial institutions or data providers. Likewise, doydl       │
## │                    technologies is not affiliated with, endorsed by, or sponsored by any    │
## │                    government, corporate, or financial institutions. Users should verify    │
## │                    the accuracy of the data obtained and consult professional advice        │
## │                    before making investment decisions.                                      │
## │                                                                                             │
## │                                                                                             │
## │  Copyright       : © 2023–2025 by doydl technologies. All rights reserved.                  │
## │                                                                                             │
## │                                                                                             │
## │  License         : Licensed under the Apache License, Version 2.0 (the "License");          │
## │                    you may not use this file except in compliance with the License.         │
## │                    You may obtain a copy of the License at:                                 │
## │                                                                                             │
## │                        http://www.apache.org/licenses/LICENSE-2.0                           │
## │                                                                                             │
## │                    Unless required by applicable law or agreed to in writing, software      │
## │                    distributed under the License is distributed on an "AS IS" BASIS,        │
## │                    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or          │
## │                    implied. See the License for the specific language governing             │
## │                    permissions and limitations under the License.                           │
## ╰────────────────────────────────────────────────────────────────────────────────────────────╯
#



import re
from urllib.parse import urlparse
import random
from collections import deque

#────────── Third-party library imports (from PyPI or other package sources) ─────────────────────────────────
import requests

# ────────── Project-specific imports (directly from this project's source code) ─────────────────────────────
from .._version import __version__



# ━━━━━━━━━━━━━━ Core Module Implementation ━━━━━━━━━━━━━━━━━━━━━━━━━━
# This segment delineates the functional backbone of the module.
# It comprises the abstractions and behaviors essential for runtime
# execution—if applicable—encapsulated in class and function constructs.
# In minimal implementations, this may simply define constants, metadata,
# or serve as an interface placeholder.
class UserAgentRandomizer:
    """
    A class responsible for randomizing user agents from a predefined list of popular user agents across different platforms and browsers.
    This class includes a mechanism to reduce the likelihood of selecting a user agent that has been chosen frequently in the recent selections.

    Attributes:
        user_agents (dict): A class-level dictionary containing user agents categorized by platform and browser combinations.
        recent_selections (deque): A deque to track the history of the last five selections to dynamically adjust selection probabilities.
        last_modified_time (float): The last modification time of the JSON file.

    Methods:
        get_random_user_agent(): Randomly selects and returns a user agent string from the aggregated list of all available user agents, with adjustments based on recent usage to discourage frequent repeats.
        load_user_agents_from_json(): Loads the user_agents dictionary from the default JSON file.
        check_and_reload_user_agents(): Checks if the JSON file has been modified since the last load and reloads it if necessary.
        get_config_path(): Returns the absolute path to the default configuration JSON file.
    """
    user_agents = {}
    recent_selections = deque(maxlen=5)
    last_modified_time = None

    @classmethod
    def get_random_user_agent(cls):
        """
        Retrieves a random user agent string from the predefined list of user agents across various platforms and browsers.
        Adjusts the selection process based on the history of the last five selections to discourage frequently repeated choices.
        """
        cls.user_agents = requests.get(f"https://raw.githubusercontent.com/cedricmoorejr/quantsumore/v{__version__}/files/user_agents.json").json()

        all_user_agents = []
        for category in cls.user_agents.values():
            for subcategory in category.values():
                all_user_agents.extend(subcategory.values())

        choice = random.choice(all_user_agents)
        while cls.recent_selections.count(choice) >= 3:
            choice = random.choice(all_user_agents)

        cls.recent_selections.append(choice)
        return choice

def find_os_in_user_agent(user_agent):
    """
    Determines the operating system from a user-agent string by matching known OS identifiers.

    This function checks the provided `user_agent` string against a dictionary of OS identifiers (`os_dict`).
    The keys in `os_dict` represent substrings that might appear in a user-agent string, and the corresponding values
    represent the human-readable names of the operating systems. The function returns the name of the first matching
    operating system found in the `user_agent` string.

    Parameters:
    -----------
    user_agent : str
        The user-agent string that needs to be analyzed to determine the operating system.
    """    
    os_dict = {
        "Windows": "Windows",
        "Macintosh": "macOS",
        "Linux": "Linux",
        "CrOS": "Chrome OS"
    }
    for key in os_dict:
        if key in user_agent:
            return os_dict[key]
    return None

def findhost(url):
    """Extract the host from a URL or return the hostname if that's what is provided."""
    parsed_url = urlparse(url)
    if parsed_url.scheme and parsed_url.netloc:
        return parsed_url.netloc
    elif not parsed_url.netloc and not parsed_url.scheme:
        return url
    else:
        parsed_url = urlparse('//'+url)
        return parsed_url.netloc



def __dir__():
    return [
    'UserAgentRandomizer',	
    'findhost',
    'find_os_in_user_agent',
	]	
	
	
__all__ = [
	'UserAgentRandomizer',	
	'findhost',
	'find_os_in_user_agent',
	]	
	
	

