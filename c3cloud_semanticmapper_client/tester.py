import sys
from loaderScript_pandas import run
from lib import *
import client
import numpy as np
import os
import importlib
import re

client.__init__()
## client.baseurl = 'https://rubis.limics.upmc.fr/c3-cloud/'
client.baseurl = 'http://localhost:5000/c3-cloud/'

## client.delete_concept("C3DP_CDSM_PROFILE|RASA")

e = json.loads(client.sendrequest("all").content)

def filterfrailty(e):
    return any([re.match(r'.*frai?li?t.*', ee) for ee in e.values()])

def simplify(e):
    return {k: e[k] for k in ['code', 'code_system', 'site', 'designation']}

l = list(filter(lambda e: filterfrailty(simplify(e)), e['data']['mappings']))

print('\n'.join(map(str, l)))

if __name__ == '__main__':
    client.interactive = False
    ## client.baseurl = 'http://localhost:5000/c3-cloud/'
    
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
