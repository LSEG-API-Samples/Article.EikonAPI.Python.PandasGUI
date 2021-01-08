import eikon as ek
import configparser as cp
import json
import datetime

# Pandas
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

def get_events_descriptions(list_rics):
    list_result = []
    for ric in list_rics:
        country_code = ric[:2]
        event = ric[2:]
        list_result.append('{country} {event}'.format(country = rcep_country_code[country_code], event = covid19_rics_pattern[event]))
    return list_result

def get_events_columns(list_rics):
    dict_result = {}
    for ric in list_rics:
        country_code = ric[:2]
        event = ric[2:]
        dict_result[ric] = '{country} {event}'.format(country = rcep_country_code[country_code], event = covid19_rics_pattern[event])

    return dict_result


if __name__ == "__main__":
    print('#----------- Initialize Session -------------#')
    cfg = cp.ConfigParser()
    cfg.read('credential.cfg')
    ek.set_app_key(cfg['workspace']['app_key'])

    # Get Today Data

    print("#----------- Requesting Today Data -------------#")

    fields = ['DSPLY_NMLL', #Display Name
            'COUNTRY',    #Country code
            'CF_DATE', #Announcement Date
            'ECON_ACT', #Actual value
            'ECON_PRIOR' #Previous value
    ]

    rics_thailand = ['THCCOV=ECI','THNCOV=ECI','THRCOV=ECI','THACOV=ECI','THDCOV=ECI']

    df_thailand, err = ek.get_data(rics_thailand, fields)
    
    # Rename Instrument to be readable value
    #events_rename={'THCCOV=ECI': 'Total Cases','THNCOV=ECI': 'New Cases', 'THRCOV=ECI': 'Recover Cases', 'THACOV=ECI': 'Active Cases', 'THDCOV=ECI': 'Death Cases'}
    #df_thailand.replace(events_rename, inplace = True)

    # Today Data for RCEP Countries

    fields = ['COUNTRY',    #Country code
            'CF_DATE', #Announcement Date
            'ECON_ACT', #Actual value
            'ECON_PRIOR' #Previous value
    ]

    # RCEP Contries Covid-19 new cases
    rics_rcep_new_cases = ['BNNCOV=ECI','KHNCOV=ECI','IDNCOV=ECI','LANCOV=ECI','MYNCOV=ECI','MMNCOV=ECI','PHNCOV=ECI','SGNCOV=ECI','THNCOV=ECI','VNNCOV=ECI','CNNCOV=ECI','JPNCOV=ECI','KRNCOV=ECI','AUNCOV=ECI','NZNCOV=ECI']

    df_rcep_new_cases, err = ek.get_data(rics_rcep_new_cases, fields)
    # Add 'Description' column (example value: 'Thailand New Cases', etc.)
    df_rcep_new_cases['Description'] = get_events_descriptions(rics_rcep_new_cases)
    
    # RCEP Contries Covid-19 death cases
    rics_rcep_death_cases = ['BNDCOV=ECI','KHDCOV=ECI','IDDCOV=ECI','LADCOV=ECI','MYDCOV=ECI','MMDCOV=ECI','PHDCOV=ECI','SGDCOV=ECI','THDCOV=ECI','VNDCOV=ECI','CNDCOV=ECI','JPDCOV=ECI','KRDCOV=ECI','AUDCOV=ECI','NZDCOV=ECI']

    df_rcep_death_cases, err = ek.get_data(rics_rcep_death_cases, fields)
    # Add 'Description' column (example value: 'Thailand Death Cases', etc.)
    df_rcep_death_cases['Description'] = get_events_descriptions(rics_rcep_death_cases)

    # Historical Data

    print("#----------- Requesting Historical Data -------------#")

    df_thailand_historical = ek.get_timeseries(rics_thailand, start_date='2020-01-01', end_date='2021-01-06', interval='daily')
    # Change RIC columns names to be readable values (example value: 'Thailand New Cases', etc.)
    df_thailand_historical.rename(columns=get_events_columns(rics_thailand), inplace = True)

    df_rcep_historical_new_cases = ek.get_timeseries(rics_rcep_new_cases, start_date='2020-01-01', end_date='2021-01-06', interval='daily')
    # Change RIC columns names to be readable values (example value: 'Thailand New Cases', etc.)
    df_rcep_historical_new_cases.rename(columns=get_events_columns(rics_rcep_new_cases), inplace = True)


    df_rcep_historical_death_cases = ek.get_timeseries(rics_rcep_death_cases, start_date='2020-01-01', end_date='2021-01-06', interval='daily')
    # Change RIC columns names to be readable values (example value: 'Thailand New Cases', etc.)
    df_rcep_historical_death_cases.rename(columns=get_events_columns(rics_rcep_death_cases), inplace = True)

    # Fill missing value as 0
    df_rcep_historical_new_cases.fillna(0 ,inplace = True )
    df_rcep_historical_death_cases.fillna(0 ,inplace = True )

    print("#----------- Displaying Data in PandasGUI -------------#")

    # Create Data Dictionary to sends all DataFrame objects to PandasGUI
    dataset = {
        'Thailand Today Cases': df_thailand,
        'RCEP Today Total Cases': df_rcep_total_cases, 
        'RCEP Today New Cases': df_rcep_new_cases, 
        'RCEP Today Death Cases': df_rcep_death_cases, 
        'Thailand Historical Cases': df_thailand_historical,
        'RCEP Historical New Cases': df_rcep_historical_new_cases,
        'RCEP Historical Death Cases': df_rcep_historical_death_cases,
    }
    # Display all DataFrame objects in PandasGUI
    show(**dataset)
