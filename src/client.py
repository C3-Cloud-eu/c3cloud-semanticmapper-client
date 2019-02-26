import requests
import unicodedata
import pandas as pd
from collections import Counter
import numpy as np
import json
import schema

from objects import *
from lib import *
from helpers import schema_mapping


def __init__():
    global report, FORCE, dryrun, interactive
    FORCE = False
    dryrun = False
    interactive = False
    report = Counter(
        identical=0,
        different=0,
        new=0,
        error=0
    )


# baseurl = sys.argv[0]
#baseurl = 'http://localhost:5000/c3-cloud/'  # tests
# baseurl = 'http://cispro.chu-rouen.fr/c3-cloud/'
# baseurl = "http://18.205.143.209/c3-cloud/"


# send a request to the REST API
# url: the part of the URL coming *after* the baseurl
# method: "get" or "post"
# data: json encoded data to send as the POST request body
# get: GET parameters
def sendrequest(url, method="get", get=None, data=None):
    full_url = "{}{}/".format(baseurl, url)
    args = {k: v for k, v in {'params': get, 'json': data}.items() if v}
    # execute either requests.get or requests.post based on the <method> arg
    print(full_url)
    print(args)
    r = getattr(requests, method)(url=full_url, **args)
    # if interactive:
    #     print(method)
    #     print(full_url)
    #     print(args)
    #     print(r)
    #     print(r.status_code)
    if r.status_code != 200:
        report['error'] += 1
        print("error", r.status_code, r.text)
    return(r.text)


# send a mapping to upload
def upload_mapping(o):
    assert type(o) == Mapping
    print(o.__dict__)
    printcolor('[uploading <{}>@<{}>]'.format(o.concept, o.site),
               color=bcolors.OKBLUE, end='')
    if not dryrun:
        ans = sendrequest("mappings", method="post", data= json.loads(o.tojson()) )
        print(ans)


def translate(code, code_system, fromSite, toSite):
    return sendrequest('translate',
                       get = {'code': code,
                              'code_system': code_system,
                              'fromSite': fromSite,
                              'toSite': toSite})


def get_code_system(code_system):
    js = json.loads(sendrequest('code-systems'))['data']
    cs = [cs for cs in js if cs['code_system'] == code_system]
    if len(cs) == 1:
        cs = cs[0]
        return CodeSystem(code_system = cs['code_system'],
                          uri = cs['code_system_uri'])

# given the dictionary of {concept: [mapping]},
# build the object to send as json data,
# check wether it already exist and decide to upload it or not
def process_items(l):
    global ll
    print('process items')
    ll = l
    assert not any([e is None for e in l])
    
    # # sorted lists for objects comparison
    # def f(e):
    #     return set([e[k] for k in [CODE, DESIGNATION, CODE_SYSTEM]])

    # mappings = [f(e) for e in mappings]
    # print(len(mappings))
    m = pd.DataFrame.from_records(mappings)
    # print(m.shape)
    #return(sorted([[v for k, v in x.items() if k in [CODE, DESIGNATION, CODE_SYSTEM]]
        #              for x in l]))

    # "pretty print"
    def disp(title, l):
           print('\n' +
                 '\n'.join([title+':'] + [str([e, i[e]]) for i in l for e in sorted(i.keys())]) +
                 '\n')

    for e in l:
        # same site, same concept
        codelist = [] if len(m)==0 else  m.loc[ np.array(m.site == e.site)
                         & np.array(m.concept == e.concept), :]
        # print(e.codes)
        if len(codelist):
            if( set(codelist.code) == set([ee.code for ee in e.codes])
               and set(codelist.designation) == set([ee.designation for ee in e.codes])):
                if(verbosity<1):
                    print(f"already in db→ <{e.concept}>@<{e.site}>:", end='')
                    printcolor("[identical]", color=bcolors.OKGREEN, end='')
                report['identical'] += 1
            else:
                print(f"already in db→ <{e.concept}>@<{e.site}>:", end='')
                printcolor("[different]", color=bcolors.WARNING, end='')
                print('\nlocal:')
                print(e)
                print('--------')
                print( set(codelist.code), set(codelist.designation) )
                print('========================')
                print('server:')
                print(codelist)
                #print('--------')
                #print(set(m.code), set(m.designation))
                print('\n')
                report['different'] += 1

                if(FORCE):
                    upload_mapping(e)
                else:
                    printcolor('[use --force to overwrite]', color=bcolors.FAIL, end='')
        else:
            upload_mapping(e)
            # print([e[CODE] for e in items], end='')
            report['new'] += 1
        #print('')
            
                
                #             if f(o['codes']) == f(codelist):
    #             # if compare(o['codes'], codelist):
    #                 printcolor("[identical]", color=bcolors.OKGREEN, end='')
    #                 report['identical'] += 1
    #             else:
    #                 printcolor("[different]", color=bcolors.WARNING, end='')
    #                 disp('local', items)
    #                 disp('server', codelist)
    #                 print('to upload: {}', o)
    #                 report['different'] += 1

    #                 if(FORCE):
    #                     upload_mapping(o)
    #                 else:
    #                     printcolor('[use --force to overwrite]', color=bcolors.FAIL, end='')
    #         else:
    #             upload_mapping(o)
    #             print([e[CODE] for e in items], end='')
    #             report['new'] += 1
    #         print('')

                

            
def nothing():
    pass
    # for concept, sites in d.items():
    #     for site, items in sites.items():
    #         # print("processing ", concept, " -- ", site, " -- ", items)

    #         # time.sleep(0.5)
    #         # items = [{clean(k): clean(v) for k, v in i.items()} for i in items]
    #         o = {
    #             'concept': clean(concept),
    #             'site': clean(site),
    #             'codes': [{clean(i): clean(item[i]) for i in [CODE_SYSTEM, CODE, DESIGNATION]}
    #                       for item in items]}
    #         # disp("test", [o])
    #         # get the mappings that already exist on the server
    #         codelist = [i for i in mappings if i[CONCEPT] == o['concept']
    #                     and i[SITE] == o['site']]
    #         if len(codelist) > 0:
    #             print("already in db→ <{}>@<{}>:".format(concept, site), end='')
    #             # print('<<<<<<<<',f(o['codes']),'||||||||||||||||',f(codelist),'>>>>>>>')

    #             if f(o['codes']) == f(codelist):
    #             # if compare(o['codes'], codelist):
    #                 printcolor("[identical]", color=bcolors.OKGREEN, end='')
    #                 report['identical'] += 1
    #             else:
    #                 printcolor("[different]", color=bcolors.WARNING, end='')
    #                 disp('local', items)
    #                 disp('server', codelist)
    #                 print('to upload: {}', o)
    #                 report['different'] += 1

    #                 if(FORCE):
    #                     upload_mapping(o)
    #                 else:
    #                     printcolor('[use --force to overwrite]', color=bcolors.FAIL, end='')
    #         else:
    #             upload_mapping(o)
    #             print([e[CODE] for e in items], end='')
    #             report['new'] += 1
    #         print('')
    #         if interactive:
    #             print(">>>>", o)
    #             input()
