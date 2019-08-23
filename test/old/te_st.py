#!/usr/bin/env python

import requests


# baseurl = 'http://localhost:5000/c3-cloud/'
# baseurl = 'http://cispro.chu-rouen.fr/c3-cloud/'
baseurl = 'http://rubis.limics.upmc.fr/c3-cloud/'

def line():
    print('────────────────')


def bigline():
    print("\n███████████████████████████████████████████████████████████████████████████\n")


def testrequest(title, url, method="get", get=None, data=None):
    bigline()
    print("testing {}...".format(title))
    full_url = "{}{}/".format(baseurl, url)
    line()
    print(full_url)
    argz = {k: v for k, v in { 'params': get, 'data': data }.items() if v}
    print(argz)
    r = getattr(requests, method)(url=full_url, **argz)
    # if post is not None:
    #     print("post: ", post)
    #     r = requests.post(url=full_url, data=post)
    # else:
    #     r = requests.get(url=full_url, params=get, data=post)
    # print(r.url)
    line()

    print("elapsed:", r.elapsed)
    print("status code:", r.status_code)
    print(r.text)
    line()


def setcodesystem(name, oid):
    testrequest('setting a code system',
                'code-systems',
                method = "post",
                data={
                    "code_system": name,
                    "code_system_uri": oid
                })
    

if __name__ == '__main__':

    new_code_systems = {
        "SNOMED CT": "http://snomed.info/sct",
        "ATC": "http://www.whocc.no/atc",
        "LOINC": "http://loinc.org",
        "ICD-10-SE": "urn:oid:1.2.752.116.1.1.1.1.3",
        "CIE-10": "urn:oid:2.16.724.4.21.5.29",
        "ICD-10": "http://hl7.org/fhir/sid/icd-10",
        "Read Code": "urn:oid:2.16.840.1.113883.6.29",
        "SWE": "unknown"
        }
    for name, oid in new_code_systems.items():
        setcodesystem(name, oid)

    

    testrequest("list sites", "sites")
    testrequest("list code systems", "code-systems")

    testrequest('setting a code system',
                'code-systems',
                method = "post",
                data={
                    "code_system": "SWE",
                    "code_system_uri": "aaa"
                })

    
    testrequest('mapping of Diastolic blood pressure from OSAKI to CDSM',
                'translate',
                get={
                    "code": "8462-4",
                    "code_system": "uri:oid:2.16.840.1.113883.6.1",
                    "fromSite": "OSAKI",
                    "toSite": "SWFT"
                })

    # http://cispro.chu-rouen.fr/c3-cloud/translate/?code=59927004&code_system=uri:oid:2.16.840.1.113883.6.96&fromSite=CDSM&toSite=RJH
    testrequest('mapping example Mustafa',
                'translate',
                get={
                    "code": "59927004",
                    "code_system": "http://snomed.info/sct",
                    "fromSite": "CDSM",
                    "toSite": "RJH"
                })
    
    testrequest('mapping example Mustafa',
                'translate',
                get={
                    "code": "albuminuria",
                    "code_system": "C3-Cloud",
                    "fromSite": "CDSM",
                    "toSite": "RJH"
                })

    testrequest('getting the codes for the "Chronic ischemic heart disease" concept from RJH',
                'mappings',
                {
                    "site": "RJH",
                    "concept": "Chronic ischemic heart disease"
                })

    tmpconcept = '_tmp concept'
    for action in [('adding', 'post'), ('deleting', 'delete')]:
        testrequest('{} a concept {}'.format(action[0], tmpconcept),
                    'concepts',
                    action[1],
                    data={
                        "concept": tmpconcept
                    })
    
        testrequest('get the concept {}'.format(tmpconcept),
                    'concepts',
                    get={'concept': tmpconcept})

    
testrequest('nuke', 'all', method="delete", get=None, data=None)
