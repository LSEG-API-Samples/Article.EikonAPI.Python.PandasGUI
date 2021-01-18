# |-----------------------------------------------------------------------------
# |            This source code is provided under the Apache 2.0 license      --
# |  and is provided AS IS with no warranty or guarantee of fit for purpose.  --
# |                See the project's LICENSE.md for details.                  --
# |           Copyright Refinitiv 2021. All rights reserved.                  --
# |-----------------------------------------------------------------------------

#Import Eikon and Main Modules
import eikon as ek
import configparser as cp

# Pandas and PandasGUI
import pandas as pd
from pandasgui import show

rcep_country_code = {
    'BN': 'Brunei',
    'KH': 'Cambodia',
    'ID': 'Indonesia',
    'LA': 'Laos',
    'MY': 'Malaysia',
    'MM': 'Myanmar',
    'PH': 'Philippines',
    'SG': 'Singapore',
    'TH': 'Thailand',
    'VN': 'Vietnam',
    'CN': 'China',
    'JP': 'Japan',
    'KR': 'South Korea',
    'AU': 'Australia',
    'NZ': 'New Zealand'
}

covid19_rics_pattern = {
    'CCOV=ECI': 'Total Cases',
    'NCOV=ECI': 'New Cases',
    'RCOV=ECI': 'Recover Cases',
    'ACOV=ECI': 'Active Cases',
    'DCOV=ECI': 'Death Cases'
}

"""
RCEP: Regional Comprehensive Economic Partnership
    - Memberships:
        - Brunei
        - Cambodia
        - Indonesia
        - Laos
        - Malaysia
        - Myanmar
        - Philippines
        - Singapore
        - Thailand
        - Vietnam
        - China
        - Japan
        - South Korea
        - Australia
        - New Zealand
"""
# Thailand all static
rics_thailand = ['THCCOV=ECI','THNCOV=ECI','THRCOV=ECI','THACOV=ECI','THDCOV=ECI']
# RCEP Countries  Covid-19 total cases
rics_rcep_total_cases = ['BNCCOV=ECI','KHCCOV=ECI','IDCCOV=ECI','LACCOV=ECI','MYCCOV=ECI','MMCCOV=ECI','PHCCOV=ECI','SGCCOV=ECI','THCCOV=ECI','VNCCOV=ECI','CNCCOV=ECI','JPCCOV=ECI','KRCCOV=ECI','AUCCOV=ECI','NZCCOV=ECI']
# RCEP Countries  Covid-19 new cases
rics_rcep_new_cases = ['BNNCOV=ECI','KHNCOV=ECI','IDNCOV=ECI','LANCOV=ECI','MYNCOV=ECI','MMNCOV=ECI','PHNCOV=ECI','SGNCOV=ECI','THNCOV=ECI','VNNCOV=ECI','CNNCOV=ECI','JPNCOV=ECI','KRNCOV=ECI','AUNCOV=ECI','NZNCOV=ECI']
# RCEP Countries  Covid-19 death cases
rics_rcep_death_cases = ['BNDCOV=ECI','KHDCOV=ECI','IDDCOV=ECI','LADCOV=ECI','MYDCOV=ECI','MMDCOV=ECI','PHDCOV=ECI','SGDCOV=ECI','THDCOV=ECI','VNDCOV=ECI','CNDCOV=ECI','JPDCOV=ECI','KRDCOV=ECI','AUDCOV=ECI','NZDCOV=ECI']

# Get a List of readable Country Name and Event for adding new DataFrame column
def get_events_descriptions(list_rics):
    list_result = []
    for ric in list_rics:
        country_code = ric[:2]
        event = ric[2:]
        list_result.append('{country} {event}'.format(country = rcep_country_code[country_code], event = covid19_rics_pattern[event]))
    return list_result

# Get a Dictionary of readable Country Name and Event for replacing DataFrame column names
def get_events_columns(list_rics):
    dict_result = {}
    for ric in list_rics:
        country_code = ric[:2]
        event = ric[2:]
        dict_result[ric] = '{country} {event}'.format(country = rcep_country_code[country_code], event = covid19_rics_pattern[event])

    return dict_result

# -------------------- Main ------------------------------------------------- #
if __name__ == "__main__":
    print('#----------- Initialize Session -------------#')
    cfg = cp.ConfigParser()
    cfg.read('credential.cfg')
    ek.set_app_key(cfg['workspace']['app_id'])

    # Get Today Data

    print("#----------- Requesting Today Data -------------#")

    # Today Data for RCEP Countries static

    fields = ['COUNTRY',    #Country code
            'CF_DATE', #Announcement Date
            'ECON_ACT', #Actual value
            'ECON_PRIOR' #Previous value
    ]
    # RCEP Countries  Covid-19 total cases
    df_rcep_total_cases, err = ek.get_data(rics_rcep_total_cases, fields)
    if err is None:
        print('Example RCEP COVID-19 Total Cases Today Data:')
        print(df_rcep_total_cases.head())

    # Add 'Description' column (example value: 'Thailand Total Cases', etc.)
    df_rcep_total_cases['Description'] = get_events_descriptions(rics_rcep_total_cases)
    print('DataFrame after added Description column')
    print(df_rcep_total_cases.head())

    # RCEP Countries  Covid-19 new cases
    
    df_rcep_new_cases, err = ek.get_data(rics_rcep_new_cases, fields)
    # Add 'Description' column (example value: 'Thailand New Cases', etc.)
    df_rcep_new_cases['Description'] = get_events_descriptions(rics_rcep_new_cases)
    
    # RCEP Countries Covid-19 death cases
    

    df_rcep_death_cases, err = ek.get_data(rics_rcep_death_cases, fields)
    # Add 'Description' column (example value: 'Thailand Death Cases', etc.)
    df_rcep_death_cases['Description'] = get_events_descriptions(rics_rcep_death_cases)

    # Historical Data

    print("#----------- Requesting Historical Data -------------#")

    df_rcep_historical_total_cases = ek.get_timeseries(rics_rcep_total_cases, start_date='2020-01-01', end_date='2021-01-12', interval='daily')
    print('Example RCEP COVID-19 Total Cases Today Data:')
    print(df_rcep_historical_total_cases.head())

    # Change RIC column names to be readable values (example value: 'Thailand New Cases', etc.)
    df_rcep_historical_total_cases.rename(columns=get_events_columns(rics_rcep_total_cases), inplace = True)
    print('DataFrame after changed instrument columns names to readable values')
    print(df_rcep_historical_total_cases.head())

    df_rcep_historical_new_cases = ek.get_timeseries(rics_rcep_new_cases, start_date='2020-01-01', end_date='2021-01-12', interval='daily')
    # Change RIC column names to be readable values (example value: 'Thailand New Cases', etc.)
    df_rcep_historical_new_cases.rename(columns=get_events_columns(rics_rcep_new_cases), inplace = True)


    df_rcep_historical_death_cases = ek.get_timeseries(rics_rcep_death_cases, start_date='2020-01-01', end_date='2021-01-12', interval='daily')
    # Change RIC column names to be readable values (example value: 'Thailand New Cases', etc.)
    df_rcep_historical_death_cases.rename(columns=get_events_columns(rics_rcep_death_cases), inplace = True)

    # Fill missing value as 0
    df_rcep_historical_total_cases.fillna(0 ,inplace = True )
    df_rcep_historical_new_cases.fillna(0 ,inplace = True )
    df_rcep_historical_death_cases.fillna(0 ,inplace = True )

    print("#----------- Displaying Data in PandasGUI -------------#")

    # Create Data Dictionary to sends all DataFrame objects to PandasGUI
    dataset = {
        'RCEP Today Total Cases': df_rcep_total_cases, 
        'RCEP Today New Cases': df_rcep_new_cases, 
        'RCEP Today Death Cases': df_rcep_death_cases, 
        'RCEP Historical Total Cases': df_rcep_historical_total_cases,
        'RCEP Historical New Cases': df_rcep_historical_new_cases,
        'RCEP Historical Death Cases': df_rcep_historical_death_cases,
    }
    # Display all DataFrame objects in PandasGUI
    show(**dataset)
