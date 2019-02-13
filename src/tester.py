import sys
from loaderScript_pandas import run
from lib import *
import client
import numpy as np
import os
import importlib

sif __name__ == '__main__':
    client.interactive = False
    client.baseurl = 'http://localhost:5000/c3-cloud/'
    
    importlib.reload(client)
    client.__init__()
    configpath = '/home/mika/Documents/random/sante_publique/cismef/c3_cloud_client/data/data_2019_02_07/import.yaml'
    load_config(configpath)
    
    run( '/home/mika/Documents/random/sante_publique/cismef/c3_cloud_client/data/data_2019_02_07/import.yaml' )
    
    for category, count in client.report.items():
        print('{}: {}'.format(category, count))
    
    
    f = os.path.join(os.path.dirname(configpath), './SemMapper-CDSMCodeMappings-with-cdsm-profile-v2-7Feb2019.xlsx')
    sheets = ['C3DP_CDSM_PROFILE', 'Conditions', 'Medications', 'Family History', 'Procedures']
    
    sheetName = sheets[1]
    good_df_columns(df)
