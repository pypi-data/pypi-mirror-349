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



from ._version import __version__


"""
###############################################################################
#                                                                             #
#  *** ATTENTION ***                                                          #
#                                                                             #
#  DO NOT REMOVE OR MODIFY THE LINE BELOW:                                    #
#                                                                             #
#  ## -- quantsumore -- ##                                                    #
#                                                                             #
#  This line is a critical marker that indicates the root directory.          #
#  Removing or changing this line will break the script and cause errors.     #
#                                                                             #
#  YOU HAVE BEEN WARNED!                                                      #
#                                                                             #
###############################################################################
"""

## -- quantsumore -- ##




# Disclaimer message defined as a string
disclaimer = """
╔══════════════════════════════════════════════════════════════════════════════════════════════════════╗
║                                      Legal Disclaimer:                                               ║
╠══════════════════════════════════════════════════════════════════════════════════════════════════════╣
║ quantsumore is an independent Python library that provides users with the ability to fetch market    ║
║ data for various financial instruments. The creators and maintainers of quantsumore do not own any   ║
║ of the data retrieved through this library. Furthermore, quantsumore is not affiliated with any      ║
║ financial institutions or data providers. The data sourced by quantsumore is owned and distributed   ║
║ by respective data providers, with whom quantsumore has no affiliation or endorsement. Users of      ║
║ quantsumore should verify the data independently and rely on their judgment and professional advice  ║
║ for investment decisions. The developers of quantsumore assume no responsibility for inaccuracies,   ║
║ errors, or omissions in the data provided.                                                           ║
╚══════════════════════════════════════════════════════════════════════════════════════════════════════╝
"""


# Equity notice due to Yahoo Finance bot protection
equity_notice = """
╔═════════════════════════════════════════════════════════════════════════════════════════════════════╗
║                    Notice: Partial Disruption in Yahoo-Based Equity Endpoints:                      ║
╠═════════════════════════════════════════════════════════════════════════════════════════════════════╣
║ Yahoo Finance has implemented aggressive bot protections:                                           ║
║ • Many endpoints now return fake 404s to non-browser clients.                                       ║
║ • Profile and stats pages use JavaScript rendering and anti-bot tokens.                             ║
║ • User-agent spoofing alone is no longer sufficient for scraping.                                   ║
║                                                                                                     ║
║ As a result, the following equity methods are currently unavailable:                                ║
║ • CompanyBio, CompanyExecutives, CompanyDetails, Stats, sLatest, Lastn, sHistorical                 ║
║                                                                                                     ║
║ Other modules (crypto, CPI, treasury, forex) remain unaffected.                                     ║
╚═════════════════════════════════════════════════════════════════════════════════════════════════════╝
"""

# Print the disclaimer and equity notice when the module is imported
print(disclaimer)
print(equity_notice)
