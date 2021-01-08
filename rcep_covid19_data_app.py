import eikon as ek
import configparser as cp
import json
import datetime

# Pandas
import pandas as pd
from pandasgui import show

cfg = cp.ConfigParser()
cfg.read('credential.cfg')

ek.set_app_key(cfg['workspace']['app_key'])

print("#----------- Requesting Today Data -------------#")

fields = ['DSPLY_NMLL', #Display Name
          'COUNTRY',    #Country code
          'CF_DATE', #Announcement Date
          'ECON_ACT', #Actual value
          'ECON_PRIOR'
]

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

rics_thailand = ['THCCOV=ECI','THNCOV=ECI','THRCOV=ECI','THACOV=ECI','THDCOV=ECI']

df_thailand, err = ek.get_data(rics_thailand, fields)

events_rename={'THCCOV=ECI': 'Total Cases','THNCOV=ECI': 'New Cases', 'THRCOV=ECI': 'Recover Cases', 'THACOV=ECI': 'Active Cases', 'THDCOV=ECI': 'Death Cases'}

df_thailand.replace(events_rename, inplace = True)

#gui = show(df_thailand)

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



# Today Data

fields = ['COUNTRY',    #Country code
          'CF_DATE', #Announcement Date
          'ECON_ACT', #Actual value
          'ECON_PRIOR' #Previous value
]

rics_rcep_total_cases = ['BNCCOV=ECI','KHCCOV=ECI','IDCCOV=ECI','LACCOV=ECI','MYCCOV=ECI','MMCCOV=ECI','PHCCOV=ECI','SGCCOV=ECI','THCCOV=ECI','VNCCOV=ECI','CNCCOV=ECI','JPCCOV=ECI','KRCCOV=ECI','AUCCOV=ECI','NZCCOV=ECI']

df_rcep_total_cases, err = ek.get_data(rics_rcep_total_cases, fields)

df_rcep_total_cases['Description'] = get_events_descriptions(rics_rcep_total_cases)

#df_rcep_total_cases.replace(get_events_names(rics_rcep_total_cases,rcep_country_code,covid19_rics_pattern), inplace = True)

#print(df_rcep_total_cases)


rics_rcep_new_cases = ['BNNCOV=ECI','KHNCOV=ECI','IDNCOV=ECI','LANCOV=ECI','MYNCOV=ECI','MMNCOV=ECI','PHNCOV=ECI','SGNCOV=ECI','THNCOV=ECI','VNNCOV=ECI','CNNCOV=ECI','JPNCOV=ECI','KRNCOV=ECI','AUNCOV=ECI','NZNCOV=ECI']

df_rcep_new_cases, err = ek.get_data(rics_rcep_new_cases, fields)

df_rcep_new_cases['Description'] = get_events_descriptions(rics_rcep_new_cases)
#print(df_rcep_new_cases)


rics_rcep_death_cases = ['BNDCOV=ECI','KHDCOV=ECI','IDDCOV=ECI','LADCOV=ECI','MYDCOV=ECI','MMDCOV=ECI','PHDCOV=ECI','SGDCOV=ECI','THDCOV=ECI','VNDCOV=ECI','CNDCOV=ECI','JPDCOV=ECI','KRDCOV=ECI','AUDCOV=ECI','NZDCOV=ECI']

df_rcep_death_cases, err = ek.get_data(rics_rcep_death_cases, fields)

df_rcep_death_cases['Description'] = get_events_descriptions(rics_rcep_death_cases)

#rint(df_rcep_death_cases)


# Historical Data

print("#----------- Requesting Historical Data -------------#")

df_thailand_historical = ek.get_timeseries(rics_thailand, start_date='2020-01-01', end_date='2021-01-06', interval='daily')

columns_rename={'THCCOV=ECI': 'Total Cases','THNCOV=ECI': 'New Cases', 'THRCOV=ECI': 'Recover Cases', 'THACOV=ECI': 'Active Cases', 'THDCOV=ECI': 'Death Cases'}

df_thailand_historical.rename(columns=columns_rename, inplace = True)
#print(df_thailand_historical)

df_rcep_historical_new_cases = ek.get_timeseries(rics_rcep_new_cases, start_date='2020-01-01', end_date='2021-01-06', interval='daily')

df_rcep_historical_new_cases.rename(columns=get_events_columns(rics_rcep_new_cases), inplace = True)

#print(df_rcep_historical_total_cases.head(5))


df_rcep_historical_death_cases = ek.get_timeseries(rics_rcep_death_cases, start_date='2020-01-01', end_date='2021-01-06', interval='daily')
df_rcep_historical_death_cases.rename(columns=get_events_columns(rics_rcep_death_cases), inplace = True)

# Fill missing value as 0

df_rcep_historical_new_cases.fillna(0 ,inplace = True )

df_rcep_historical_death_cases.fillna(0 ,inplace = True )

print("#----------- Displaying Data in PandasGUI -------------#")

dataset = {
    'Thailand Today Cases': df_thailand,
    'RCEP Today Total Cases': df_rcep_total_cases, 
    'RCEP Today New Cases': df_rcep_new_cases, 
    'RCEP Today Death Cases': df_rcep_death_cases, 
    'Thailand Historical Cases': df_thailand_historical,
    'RCEP Historical New Cases': df_rcep_historical_new_cases,
    'RCEP Historical Death Cases': df_rcep_historical_death_cases,
}
show(**dataset)
