# |-----------------------------------------------------------------------------
# |            This source code is provided under the Apache 2.0 license      --
# |  and is provided AS IS with no warranty or guarantee of fit for purpose.  --
# |                See the project's LICENSE.md for details.                  --
# |           Copyright Refinitiv 2021. All rights reserved.                  --
# |-----------------------------------------------------------------------------

#Import Eikon and Main Modules
import eikon as ek
import configparser as cp

# Pandas
import pandas as pd
from pandasgui import show

print('#----------- Initialize Session -------------#')
cfg = cp.ConfigParser()
cfg.read('credential.cfg')
ek.set_app_key(cfg['workspace']['app_key'])

"""
- USA Covid-19 Total Cases: USCCOV=ECI
- USA Covid-19 New Cases: USNCOV=ECI
- USA Covid-19 Active Cases: USACOV=ECI
- USA Covid-19 Recovered Cases: USRCOV=ECI
- USA Covid-19 Death Cases: USDCOV=ECI
"""
rics_usa_today = ['USCCOV=ECI','USNCOV=ECI','USACOV=ECI','USRCOV=ECI','USDCOV=ECI']

# Get Today Data

print("#----------- Requesting Today Data -------------#")

fields = ['DSPLY_NMLL', #Display Name
            'COUNTRY',    #Country code
            'CF_DATE', #Announcement Date
            'ECON_ACT', #Actual value
            'ECON_PRIOR' #Previous value
]
# Get usa Today Covid-19 static
df_usa_today, err = ek.get_data(rics_usa_today, fields)
if err is None:
    print(df_usa_today)
    print(err)

    # show data in PandasGUI
    show(df_usa_today)