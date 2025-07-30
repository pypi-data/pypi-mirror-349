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


#────────── Third-party library imports (from PyPI or other package sources) ─────────────────────────────────
import pandas as pd

# ────────── Project-specific imports (directly from this project's source code) ─────────────────────────────
from ..prep import cpi_asset
from .parse import cpi
from ..._http.response_utils import Request



# ━━━━━━━━━━━━━━ Core Module Implementation ━━━━━━━━━━━━━━━━━━━━━━━━━━
# This segment delineates the functional backbone of the module.
# It comprises the abstractions and behaviors essential for runtime
# execution—if applicable—encapsulated in class and function constructs.
# In minimal implementations, this may simply define constants, metadata,
# or serve as an interface placeholder.
class APIClient:
    def __init__(self, asset):
        self.asset = asset
        self.CPI_U = self._CPI_U(self) # Auto create CPI_U instance that knows about its parent APIClient instance
       
    def _all_urban(self, series_id='CPIAUCNS'):
        """
        Fetches and processes Consumer Price Index (CPI) data for all urban consumers.

        Args:
            series_id (str): The series ID for CPI data to query. Defaults to 'CPIAUCNS', which represents the all-items Consumer Price Index for all urban consumers in the United States.

        Returns:
            pandas.DataFrame or None: Returns a DataFrame containing the processed CPI data.
        """    	
        make_method = getattr(self.asset, 'make')
        url = make_method(series_id=series_id)
        html_content = Request(url, headers_to_update=None, response_format='html', target_response_key='response', return_url=True, onlyParse=False, no_content=False)
        if html_content:
            obj1 = cpi.CUUR0000AA0.Date(html_content)
            end_date = obj1.date()
            obj2 = cpi.CUUR0000AA0.Data(end_date=end_date)
            data = obj2.all_items_index()
            return data
        return None

    class _CPI_U:
        """
        A private helper class within the APIClient class that facilitates the fetching of CPI data
        and the creation of InflationAdjustment instances.

        This class serves as an interface for accessing Consumer Price Index (CPI) adjustments through
        its property InflationAdjustment. It utilizes the _all_urban method from the parent APIClient instance
        to fetch CPI data, and initializes the _InflationAdjustment class with this data.

        Attributes:
            engine (APIClient): A reference to the parent APIClient instance that provides access to the
                             necessary methods and data for fetching CPI data.

        Properties:
            InflationAdjustment: Provides a property interface that initializes and returns an instance
                                 of the _InflationAdjustment class, using CPI data fetched by invoking
                                 the _all_urban method of the parent APIClient. This ensures that CPI data
                                 is always fresh and relevant whenever the InflationAdjustment is accessed.

        Usage:
            This class is not intended to be used directly by external users but is accessed via the
            CPI_U property of an APIClient instance. It abstracts the details of CPI data fetching and
            inflation adjustment calculations away from the consumer.
        """
        def __init__(self, engine):
            self.engine = engine

        @property
        def InflationAdjustment(self):
            # Property ensures that we can access InflationAdjustment,
            data = self.engine._all_urban()
            return _InflationAdjustment(data)
           
    def __dir__(self):
        return ['CPI_U'] 



class _InflationAdjustment:
    def __init__(self, data):
        if data is None:
            raise ValueError("Failed to fetch or process CPI data.")
        self.data = data
        self.max_year = self.data['year'].max()
        self.min_year = self.data['year'].min()
        self.month_map = {
            '1': 'January', '01': 'January', 'January': 'January', 'Jan': 'January',
            '2': 'February', '02': 'February', 'February': 'February', 'Feb': 'February',
            '3': 'March', '03': 'March', 'March': 'March', 'Mar': 'March',
            '4': 'April', '04': 'April', 'April': 'April', 'Apr': 'April',
            '5': 'May', '05': 'May', 'May': 'May',
            '6': 'June', '06': 'June', 'June': 'June',
            '7': 'July', '07': 'July', 'July': 'July',
            '8': 'August', '08': 'August', 'August': 'August', 'Aug': 'August',
            '9': 'September', '09': 'September', 'September': 'September', 'Sep': 'September',
            '10': 'October', 'October': 'October', 'Oct': 'October',
            '11': 'November', 'November': 'November', 'Nov': 'November',
            '12': 'December', 'December': 'December', 'Dec': 'December'
        }
        self.current_month = self.data[(self.data['year'] == self.max_year) & (self.data['period'] != 'Average')].sort_values(by='period', key=lambda x: x.apply(self.__normalize_month))['period'].iloc[-1]

    def __normalize_month(self, month_input):
        """Normalize various month inputs to standard month names used in the dataframe."""
        month_input = str(month_input).capitalize()
        return self.month_map.get(month_input, None)

    def __validate_inputs(self, amount=None, year=None, month=None, n_years=None):
        """ Validate and convert amount input, and optionally validate the year and month inputs if provided. """
        if amount is not None:
            try:
                amount = float(amount)
            except ValueError:
                raise ValueError("Amount must be a number.")
        if year is not None:
            try:
                year = int(year)
            except ValueError:
                raise ValueError("Year must be a numeric value.")
            if year > self.max_year or year < self.min_year:
                raise ValueError(f"Year must be between {self.min_year} and {self.max_year}.")
        if month is not None:
            month = self.__normalize_month(month)
            if month is None:
                raise ValueError("Please enter a valid month.")
        if n_years is not None:
            try:
                n_years = int(n_years)
            except ValueError:
                raise ValueError("n_years must be a numeric value.")
            if n_years < 0:
                raise ValueError("n_years must be a non-negative integer.")
        return (amount, year, month, n_years)

    def __get_cpi(self, year, period='Average'):
        """Retrieve the CPI for a given year and period from the dataframe."""
        cpi_value = self.data[(self.data['year'] == year) & (self.data['period'] == period)]['value']
        return cpi_value.iloc[0] if not cpi_value.empty else None

    def select(self, original_amount, original_year, target_year, month_input):
        """
        Calculate the inflation-adjusted value for a specific month, defaulting to yearly averages if necessary.

        Args:
        original_amount (float): The amount of money to adjust for inflation.
        original_year (int): The year from which the amount originates.
        target_year (int): The year to which the amount is adjusted.
        month_input (str): The specific month for the calculation, if available.

        Returns:
        str: A formatted string indicating the equivalent value in the target year's dollars.
        """
        # Validate and convert inputs
        original_amount, original_year, month, _  = self.__validate_inputs(amount=original_amount, year=original_year, month=month_input)
        _, target_year, _, _ = self.__validate_inputs(year=target_year)

        cpi_original = self.__get_cpi(original_year, month)
        cpi_target = self.__get_cpi(target_year, month)

        # If either CPI data point is missing, default both to yearly averages and alert the user
        if cpi_original is None or cpi_target is None:
            print(f"Since we do not have the month value for {month} {target_year if cpi_target is None else original_year}, we will be switching to averages of the years.")
            cpi_original = self.__get_cpi(original_year)
            cpi_target = self.__get_cpi(target_year)

        if cpi_original is None or cpi_target is None:
            raise ValueError("CPI data not available for the provided dates.")

        adjusted_value = (original_amount / cpi_original) * cpi_target
        print(f"${original_amount:.2f} from {original_year} is equivalent to ${adjusted_value:.2f} in {target_year} dollars.")
        return round(adjusted_value, 2)

    def year_by_year(self, original_amount, n_years):
        """
        Calculate the value change of a given dollar amount over the past n years relative to the current CPI.

        Args:
        original_amount (float): The original amount of money to evaluate.
        n_years (int): Number of years back from the current year to include in the calculation.

        Returns:
        dict: A dictionary with years as keys and adjusted values as values.
        """
        # Validate and convert inputs
        original_amount, _, _, n_years = self.__validate_inputs(amount=original_amount, n_years=n_years)
        results = {}
        current_cpi = self.__get_cpi(self.max_year, self.current_month) or self.__get_cpi(self.max_year, 'Average')
        target_years = range(self.max_year - n_years, self.max_year)
        for year in target_years:
            month_cpi = self.__get_cpi(year, self.current_month)
            if not month_cpi:
                month_cpi = self.__get_cpi(year, 'Average')
                print(f"Month-specific CPI for {self.current_month} {year} not available, using yearly average.")
            if month_cpi:
                adjusted_value = (original_amount / month_cpi) * current_cpi
                results[year] = round(adjusted_value, 2)
        return results

    def month_by_month(self, amount):
        """
        Calculate the value of an amount against CPI values for each month of the current year.

        Args:
        amount (float): The amount of money to adjust based on monthly CPI values.

        Returns:
        dict: A dictionary with months as keys and the equivalent value of the amount in each month as values.
        """
        amount = self.__validate_inputs(amount=amount)[0]
        results = {}
        monthly_data = self.data[(self.data['year'] == self.max_year) & (self.data['period'] != 'Average')]
        current_cpi = self.__get_cpi(self.max_year, self.current_month)

        for _, row in monthly_data.iterrows():
            month = row['period']
            cpi_value = row['value']
            if current_cpi:
                adjusted_value = (amount / cpi_value) * current_cpi
                results[month] = round(adjusted_value, 2)
            else:
                results[month] = 'CPI data missing for current month'
        return results

    def __dir__(self):
        return ['select', 'year_by_year', 'month_by_month', 'data']



engine = APIClient(cpi_asset)



def __dir__():
    return ['engine']

__all__ = ['engine']


