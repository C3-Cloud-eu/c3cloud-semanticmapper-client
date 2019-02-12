import json
import client

def test_albuminuria_cdsm_osaki():
    client.baseurl = 'https://rubis.limics.upmc.fr/c3-cloud/'
    answer = json.loads('''
{
  "group": [
    {
      "element": {
        "code": "albuminuria", 
        "display": "Albuminuria", 
        "target": [
          {
            "code": "albuminuria", 
            "comment": "The definitions of the concepts mean the same thing (including when structural implications of meaning are considered) (i.e. extensionally identical).", 
            "display": "Proteinuria", 
            "equivalence": "Equal"
          }
        ]
      }, 
      "source": "http://www.c3-cloud.eu/fhir/clinical-concept", 
      "sourceVersion": "unknown", 
      "target": "http://www.c3-cloud.eu/fhir/clinical-concept", 
      "targetVersion": "unknown"
    }
  ], 
  "resourceType": "ConceptMap", 
  "title": "mapping of 'C3DP_CDSM_PROFILE|Albuminuria' from CDSM (C3-Cloud) to OSAKI (C3-Cloud)"
}
''')
    req = client.sendrequest('translate',
                             get = {'code':'albuminuria',
                                    'code_system':'http://www.c3-cloud.eu/fhir/clinical-concept',
                                    'fromSite':'CDSM',
                                    'toSite':'OSAKI'})
    print(json.loads(req))

