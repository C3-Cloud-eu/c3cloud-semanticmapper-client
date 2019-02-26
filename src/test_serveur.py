import json
import client
import objects
import pandas as pd
import jsondiff

client.__init__()
client.baseurl = 'https://rubis.limics.upmc.fr/c3-cloud/'
# client.baseurl = 'http://localhost:5000/c3-cloud/'

def comparedicts(a, b):
    d = jsondiff.diff(a, b)
    if len(d):
        print(a)
        print('========')
        print(b)
        print('================')
        print(d)
    assert len(d) == 0

def loadjsonfile(f):
    with open(f) as f:
        js = json.load(f)
    return js

def test_albuminuria_cdsm_osaki():
    answer = loadjsonfile('testdata/albuminuria_cdsm_osaki.json')
    req = client.translate(code = 'albuminuria',
                           code_system = 'http://www.c3-cloud.eu/fhir/clinical-concept',
                           fromSite = 'CDSM',
                           toSite = 'OSAKI')
    reqjs = json.loads(req)
    ansjs = loadjsonfile('testdata/albuminuria_cdsm_osaki_result.json')
    comparedicts(reqjs, ansjs)

def test_upload():
    m = {"codes": [
                {"code": "code1",
                "code_system": {"code_system": "cs1", "uri": "uri1"},
                "designation": "des1"}],
        "concept": "test",
        "site": "EFG"}
    m = objects.Mapping(**m)
    
    client.upload_mapping(m)
    ans = client.sendrequest('mappings', get = {'site':'EFG', 'concept':'test'})
    assert json.loads(ans)['data'] == [{'code': 'code1', 'code_system': 'cs1', 'code_system_uri': 'uri1', 'concept': 'test', 'designation': 'des1', 'site': 'EFG'}]

    

def test_get_terminology():
    css = pd.read_csv('../data/data_2019_02_07/terminologies.csv')[['code_system','code_system_uri']]
    def check(r):
        print(f'checking terminology {r}')
        cs = client.get_code_system(r['code_system'])
        if not cs.uri == r['code_system_uri']:
            print(cs.uri)
            print(r['code_system_uri'])
            print('no')
            raise
            
    css.apply(check, axis = 1)

    

def test_multi_code_translate_structural_renal_tract_disease():
    req = client.translate(code = '118642009',
                           code_system = client.get_code_system('SNOMED CT').uri,
                           fromSite = 'CDSM',
                           toSite = 'OSAKI')
    
    req = json.loads(req)
    ref = loadjsonfile('./testdata/structural_renal_tract_disease_cdsm_osaki_result.json')
    comparedicts(ref, req)
