import json
from c3_cloud_client import client
from c3_cloud_client import objects
import pandas as pd
import jsondiff

client.__init__()
# client.baseurl = 'https://rubis.limics.upmc.fr/c3-cloud/'
client.baseurl = 'http://localhost:5000/c3-cloud/'


def sortjson(e):
    def order_for_list(e):
        if type(e) == list:
            return ''.join(order_for_list(ee) for ee in e)
        elif type(e) == dict:
            return ''.join(
                ''.join([k, order_for_list( e[k] ) ]) for k in sorted(e.keys())
                )
        else:
            return str(e)
    
    if type(e) == dict:
        ans = { k: sortjson(e[k]) for k in sorted(e.keys())  }
    elif type(e) == list:
        ans = [ sortjson(v) for v in e ]
        if len(e) > 0 and type(e[0]) == dict:
            ans = sorted(ans, key = order_for_list)
        else:
            ans = sorted(ans)
    else:
        ans = e
    return ans


def comparedicts(a, b):
    a = sortjson(a)
    b = sortjson(b)
    
    d = jsondiff.diff(a, b)
    if len(d):
        print(json.dumps(a,
                         indent=2))
        print('========')
        print(json.dumps(b,
                         indent=2))
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
    reqjs = json.loads(req.text)
    ansjs = loadjsonfile('testdata/albuminuria_cdsm_osaki_result.json')
    comparedicts(reqjs, ansjs)

def test_upload():
    c, cs, uri, des, con, si = "code1", "cs1", "uri1", "des1", "test", "EFG"
    m = objects.Mapping(**{
        "codes": [
                {"code": c,
                "code_system": {"code_system": cs, "uri": uri},
                "designation": des}],
        "concept": con, "site": si})
    
    client.upload_mapping(m)
    ans = client.sendrequest('mappings', get = {'site':'EFG', 'concept':con}).text
    print("test upload ans:", ans)
    assert json.loads(ans)['data'] == [{'code': c, 'code_system': cs, 'code_system_uri': uri, 'concept': con, 'designation': des, 'site': si}]

    
def test_unauthorized_request():
    key = client.APIKEY
    client.APIKEY = "wrongapikey"
    ans = client.upload_concept("test")
    print("test upload concept:", ans)
    client.APIKEY = key
    assert ans.status_code == 401

    
def test_delete_concept():
    concept = "test"
    print(client.delete_concept(concept))
    ans = client.sendrequest('concepts', get = {'concept':concept})
    print(ans)
    assert json.loads(ans.text)['count'] == 0


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

def translatorchecker(c,cs,f,t,shouldbe):
    req = client.translate(code = c,
                           code_system = cs,
                           fromSite = f,
                           toSite = t)
    
    req = json.loads(req.text)
    ref = shouldbe
    comparedicts(ref, req)


def translatorcheckerr(c,cs,f,t,shouldbe):
    translatorchecker(c,
                      client.get_code_system(cs).uri,
                      f,
                      t,
                      loadjsonfile(shouldbe))    
    

def test_multi_code_gangrene():
    translatorcheckerr('372070002',
                       'SNOMED CT',
                       'CDSM',
                       'RJH',
                       './testdata/gangrene_cdsm_rjh_mapping_result.json')


## print(translate("BRO", get_code_system('HL7-ROLE').uri, 'CDSM', 'OSAKI'))
def test_hl7_role():
    translatorcheckerr('BRO',
                       'HL7-ROLE',
                       'CDSM',
                       'OSAKI',
                       './testdata/hl7_bro_cdsm_osaki_result.json')


def test_hl7_role():
     translatorcheckerr("influenza_vaccines",
                        'C3-Cloud',
                        'OSAKI',
                        'RJH',
                        './testdata/c3dp_influenza_osaki_rjh_result.json')


def test_update_existing_mapping():
    d = loadjsonfile("./testdata/mapping_update_hfca_lipid__data.json")
    dd = loadjsonfile("./testdata/mapping_update_hfca_lipid__data.json")
    dd['codes'][0]['designation'] = "TEST"

    mmodif = objects.Mapping(**dd)
    morig = objects.Mapping(**d)

    client.upload_mapping(mmodif)
    ans = client.upload_mapping(morig)

    m = client.get_mapping(site=d['site'], concept=d['concept'])
    print("original: ", morig)
    print("modified: ", mmodif)
    print("observed: ", m)
    
    assert m == morig
    

def test_multiterminology_mapping():
    translatorcheckerr("42343007",
                       "SNOMED CT",
                       "CDSM",
                       "SWFT",
                       './testdata/mapping_multitermino_a.json'
                       )
    
    translatorcheckerr("G580",
                   "Read",
                   "SWFT",
                   "CDSM",
                   './testdata/mapping_multitermino_b.json'
                   )

    translatorcheckerr("I500",
                   "ICD-10-UK",
                   "SWFT",
                   "CDSM",
                   './testdata/mapping_multitermino_c.json'
                   )

    

    
    
# def test_update_existing_mapping_bis():
#     d  = loadjsonfile("./testdata/mapping_update_hfca_lipid__data.json")
#     dd = loadjsonfile("./testdata/mapping_update_hfca_lipid__data.json")
#     dd['concept'] = "something else"

#     morig  = objects.Mapping(**d)
#     mmodif = objects.Mapping(**dd)

#     client.upload_mapping(mmodif)
#     sendrequest("mappings", method="post",
#                 data= {'old': json.loads(mmodif.tojson()),
#                        'new': json.loads(morig.tojson())})

#     m = client.get_mapping(site=d['site'], concept=d['concept'])
#     print("original: ", morig)
#     print("modified: ", mmodif)
#     print("observed: ", m)
    
#     assert m == morig
    
    
