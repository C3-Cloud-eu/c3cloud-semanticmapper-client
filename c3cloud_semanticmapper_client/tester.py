import sys
from lib import *
import client
import numpy as np
import os
import importlib
import re
import json
from itertools import groupby

client.__init__()
## client.baseurl = 'https://rubis.limics.upmc.fr/c3-cloud/'
## client.baseurl = 'http://localhost:5000/c3-cloud/'

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




#### counts
def load(req):
    return json.loads(client.sendrequest(req).content)['data']


def describe_counts(o):
    d = {'total': len(o),
         'total_clinical': len([e for e in o if not e['concept'].startswith("C3DP_CDSM_PROFILE|")])}

    ## per sheet
    sheets = ["Conditions",
              "Observations",
              "Immunizations",
              "Medications",
              "Family History",
              "Procedures",
              "C3DP_CDSM_PROFILE"]
    
    recs = {which: len([e for e in o if e['concept'].startswith("{}|".format(which))]) for which in sheets }
    # print( json.dumps([e for e in o if e['concept'].startswith("{}|".format("Immunizations"))], indent=4))

    d.update(recs)
    
    print('\t'.join(map(str, d.values())))


def onlyone_per(o, keyfunction):
    o = sorted(o, key=keyfunction)
    return [list(v)[0] for k, v in groupby(o, keyfunction)]
    

def onlyone_per_concept_and_site(o):
    return onlyone_per(o, lambda e: (e['concept'], e['site']))

mappings = load("mappings")
describe_counts( onlyone_per_concept_and_site(mappings) )

for site in ["CDSM", "RJH", "OSAKI", "SWFT"]:
    describe_counts(onlyone_per_concept_and_site([ e for e in mappings if e['site'] == site ]))


len(set([e['concept'] for e in mappings]))

