import pandas as pd
import numpy as np
import yaml
import json
import sys
import os.path
# from openpyxl import load_workbook
import re
import requests
import unicodedata
import time
import schema

from helpers import schema_mapping
from objects import *
from lib import *
import client

# assumptions about the xlsx structure:
# [Concepts][        site name 1       ][        site name 2       ]...
# [        ][codesys][code][designation][codesys][code][designation]...
# ....rows....
#
# the first column of each "site name X" can be anything and have to be specified
# in the YAML config file
#
# refer to the documentation for more details

# ### xlsx ### #

# coordinate manipulation
# class Coord:
#     def __init__(self, col, row):
#         self.col = col
#         self.row = row

#     def __str__(self):
#         return self.col + str(self.row)

#     def __repr__(self):
#         return self.__str__()

#     def horizontal(self, dir=1):
#         return Coord(chr(ord(self.col) + dir), self.row)

#     def vertical(self, dir=1):
#         return Coord(self.col, self.row + dir)

#     def down(self, n=1):
#         return self.vertical(n)
    
#     def right(self, n=1):
#         return self.horizontal(n)

#     def left(self, n=1):
#         return self.horizontal(-n)

#     def top(coord):  # get the associated site
#         return Coord(coord.col, 1)

#     def concept(coord):  # get the associated concept
#         return Coord("A", coord.row)


# # retrieve a reference to another cell
# # ie if the value of the cell is "=F42", retrieve the value at F42 in the current sheet
# # and if it is "=$'some other sheet'.=F42", retrieve the F42 value in the sheet "some other sheet" in the workbook
# def resolveCell(wb, sheet, coord):
#     if isinstance(coord, Coord):
#         coord = str(coord)
#     # print("<<<<<<<{}>>>>>>>>".format(coord), type(coord))
    
#     v = sheet[coord].value
#     if isinstance(v, str) and v[0] == '=':
#         if '.' in v:
#             sht, coord = v.split('.')
#             sht = wb[re.sub(r"^\$'|'$", "", sht)]
#         else:
#             sht = sheet
#             coord = v
#         coord = coord[1:]
#         return(clean(sht[coord].value))
#     else:
#         # return('' if v is None else v)
#         return(clean(v))

def good_df_columns(df):
    def is_ok(df):
        return all([e in df.iloc[1,:].unique() for e in ['Code','Coding System','Designation']])
    ok_sites = [ e for e in df.iloc[0,:].unique() if is_ok(df.iloc[:,[c == e for c in df.iloc[0,:]]]) ]
    return ok_sites

# dataframe -> {site: subset_dataframe} -> [mapping]
def build_items(df):
    global tdf
    concepts = list(df.iloc[2:, 0])

    concept = ''
    for i in range(len(concepts)):
        if concepts[i] is np.nan:
            concepts[i] = concept
        else:
            concept = concepts[i]

    def split_df(df, site):
        # only the columns for the site
        df = df.iloc[:, [c == site for c in df.iloc[0,:]]]
        # columns will be the second row
        df.columns = df.iloc[1,:]
        # remove first two rows and add index
        df = df.iloc[2:,:]
        df['concepts'] = concepts
        # tdf = df
        # print(df.columns)
        df = df[['concepts', 'Coding System', 'Code', 'Designation']]
        # clean empty lines
        df = df.loc[df.drop(columns=['concepts'])
                     .apply(lambda r: not any( r.isna() ), axis=1), :]
        # df = filter_df_empty_rows(df)
        return df

    def build_site(s, df):
        return [build_item(site=s,concept=c,df=df) for c in set(df.concepts)]
    return [e for e in flatmap(lambda s: build_site(s, split_df(df, s)), good_df_columns(df)) if e is not None]

# build all the items for a row
def build_item(site, concept, df):
    global tdf
    tdf = df
    if len(df) == 0:
        print('no row')
        return None

    df = df.loc[df.concepts == concept,:]
    # print(df)
    
    assert len(df['Coding System'].unique()) == 1
    codesystem = list(df['Coding System'])[0]
    
    try:
        # lookup the code system uri from the server
        uri = [cs['code_system_uri'] for cs in codesystems if cs['code_system'] == codesystem][0]
    except IndexError:
        printcolor('no such URI for {}'.format(codesystem), color=bcolors.FAIL)
        print(codesystems)
        report['error'] += 1
        return None
    
    def f(code, designation):
        return {'code': code,
                'designation': designation,
                'code_system': codesystem,
                'code_system_uri': uri}
    # take the unique of the codes 
    codes = [f(*t) for t in list(set(zip(df['Code'], df['Designation'])))]
    
    # add the uri to the POST data to send
    # o['code_system_uri'] = uri
    

    
    o = Mapping(site = site,
                codes = codes,
                concept = concept)
    
    # assert schema_mapping.is_valid(o)
    
    return o

# return df.apply(lambda x: {SITE: site,
    #                            CODE_SYSTEM: cs,
    #                            CODE: x.Code,
    #                            DESIGNATION: x.Designation,
    #                            CONCEPT: concept},
    #                 axis = 1)
    

# def remove_invalid_rows(df):
#     def invalid(df)
#     # printinfo('checking {}'.format(i))
#     def is_illegal(s):
#         s = str(s).lower()
#         # print(i, s)
#         illegal = (s is None or s is np.nan
#                    or s in ['', 'no coding', 'no code', 'no designation', 'n/a']
#                    or any([e in s for e in ['tbc by', 'there is no']]))
#         if illegal:
#             printerr('{} is illegal'.format(i))
#             # report['error'] += 1 # cound as an error?
#         return illegal
    
#     return (not (i is None or i is np.nan
#                  or i[CONCEPT] is np.nan
#                  or any(i[CODE].isna())
#                  or any(i[DESIGNATION].isna())
#                  or len(i[CODE]) == 0
#                  or i[CONCEPT] is np.nan
#                  or i[CODE] is np.nan
#                  or any([any(map(is_illegal, e)) for e in [i[CONCEPT], i[CODE], i[CODE_SYSTEM]]])))

def normalize_fused_cells(sheet, row):
    sheet = sheet.copy()
    col = ''
    for ci in sheet.columns:
        if sheet.iloc[row,ci] is np.nan:
            sheet.iloc[row,ci] = col
        else:
            col = sheet.iloc[row,ci]
    return sheet

# def filter_df_empty_rows(df):
#     return df.loc[ df.apply(lambda x: not all(x.isna()), axis=1),:]

def clean_df(df):
    df = df.copy()
    # bad data cells
    def dirty(s):
        if s is None or s is np.nan:
            return False
        else:
            s = str(s).lower().strip()
            illegal = (s in ['', 'no coding', 'no code', 'no designation', 'n/a']
                       or any([e in s for e in ['tbc by', 'there is no']]))
            if illegal:
                printerr('{} is illegal'.format(s))
            # report['error'] += 1 # count as an error?
        return illegal
    # cleaning for all cells
    def clean(c):
        if c is np.nan:
            return c
        else:
            return unicodedata.normalize('NFKC', str(c)).strip()
    def f(c):
        c[list(map(dirty, c))] = np.nan
        c = [clean(s) for s in c]
        return c
    return df.apply(f)

    
def importFile(f, sheets):
    global tdf
    printcolor("importing {}".format(f), color=bcolors.OKBLUE)
    # d = {}
    # wb = load_workbook(f)
    for sheetName in sheets:
        # sheet = loadPandaStringOnly(load_workbook(wb[sheetName]).values)
        df = pd.read_excel(f, sheet_name = sheetName, dtype= np.object, header=None)
        tdf = df
        print(sheetName, '============')
        df = clean_df(df)
        df = normalize_fused_cells(df,0)

        def updateconcept(x):
            x.concept = '{}|{}'.format(sheetName, x.concept)
            return x
        l = [updateconcept(x) for x in build_items(df)]
        # print(l[1:10])
        client.process_items(l)
        # for o in l:
        #     print(json.dumps(o))
        #     print('----')


def fetch_data_form_server():
    global codesystems
    global mappings
    client.jsondata = json.loads(client.sendrequest(url="all"))['data']
    client.mappings = client.jsondata['mappings']
    client.codesystems = client.jsondata['code_systems']
    mappings = client.jsondata['mappings']
    codesystems = client.jsondata['code_systems']

def load_config(configpath):
    global codesystems
    global mappings
    with open(configpath) as f:
        y = yaml.load(f)
        fetch_data_form_server()
    return y

# ### terminologies uris ### #
def upload_terminologies(f):
    printok('updating terminologies from: {}'.format(f))
    terminos = pd.read_csv(f)[['code_system','code_system_uri']]
    print(terminos)
    def upload(x):
        printinfo('uploading terminology: {}'.format(x))
        resp = client.sendrequest('code-systems', method='post', data = x)
        print(resp)
    for x in terminos.iterrows():
        x = x[1]
        o = {CODE_SYSTEM: x[CODE_SYSTEM],
             CODE_SYSTEM_URI: x[CODE_SYSTEM_URI]}
        upload(o)
    fetch_data_form_server()

# ### Main ### #

def run(configpath):
    dirname = os.path.dirname(configpath)
    def fullpath(e):
        return os.path.join(dirname, e)
    config = load_config(configpath)
    print(config)
    if 'terminologies' in config.keys():
        upload_terminologies(fullpath(config['terminologies']))
        
    [importFile(fullpath(k), e['sheets'])
     for k, e in config['mappings'].items()]


def main():
    args = sys.argv
    
    global codesystems
    # global report
    global baseurl
    
    # report = Counter(
    #     identical=0,
    #     different=0,
    #     new=0,
    #     error=0
    # )

    client.interactive = '--interactive' in args
    client.dryrun = '--dry-run' in args
    client.FORCE = '--force' in args
    if '--url' in args:
        client.baseurl = args[args.index('--url')+1]
        args.remove('--url')
        args.remove(client.baseurl)
        printinfo('Using "{}" as base url'.format(client.baseurl))
    if client.FORCE:
        args.remove('--force')
    if client.dryrun:
        args.remove('--dry-run')
    if client.interactive:
        args.remove('--interactive')
    if '--NUKE' in args:
        args.remove('--NUKE')
        printwarn('deleting everything.')
        input()
        ans = client.sendrequest('all', method='delete')
        print(ans)
    
    # print(mappings)

    if len(args) < 2:
        raise(Exception("please provide the path to a yaml configuration file"))
    else:
        run(args[1])
    print('done.')
    print('──────────────────────────────')
    for category, count in client.report.items():
        print('{}: {}'.format(category, count))


if __name__ == "__main__":
    client.__init__()
    main()

# def tests_tmp():

# # [str(resolveCell(df, df['Observation & Units'], Coord(l,1))) for l in 'ABCDEFGHIJKLMNOPQRSTUV']

# f = '../data/data_2019_02_07/SemMapper-CDSMCodeMappings-with-cdsm-profile-v2-7Feb2019.xlsx'
# df = load_workbook(f)

# # for sh in config['sheets']:
# for sh in ["C3DP_CDSM_PROFILE", "Observations", "Conditions", "Medications", "Family History", "Procedures", "Observations & Units"]:
#     sheet = pd.DataFrame(df[sh].values)



    

