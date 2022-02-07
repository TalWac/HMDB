import xml.etree.ElementTree as et
import time
import json
import pandas as pd
# pathtoxmlfile = r'D:/BCDD/Documents/Tal/Projects/HMDB/DataSets/Parser_HMDB.py Input/saliva_metabolites/saliva_metabolites.xml'
pathtoxmlfile = r'D:/BCDD/Documents/Tal/Projects/HMDB/DataSets/Parser_HMDB.py Input/hmdb_metabolites/hmdb_metabolites.xml'



def parser_hmdb_logp(pathtoxmlfile, pathtojsonfile):
    '''
    The function receive an XML file from HMDB and parse it while selecting only few nodes.
    :param pathtoxmlfile: Is a path to a XML input file in local library from the HMDB.
    :param pathtojsonfile: Is a path to a JSON output file in local library .
    :return: A list of dictionaries. Each dictionary represents a metabolite with 12 keys
    '''

    data = et.parse(pathtoxmlfile)

    root = data.getroot()
    # name space
    ns = {"h": "http://www.hmdb.ca"}

    # extract the first 3 metabolites
    metabolites = root.findall('./h:metabolite', ns) # [0:3]



    newlist = []
    start_time = time.time()
    for child in metabolites:
        innerlistsyn = []
        innerlistpath=[]
        innerlistpredlogp = []
        innerlistexplogp = []
        innerlistdis=[]
        dicts = {}
        for subchild in child:
            # if the node tag is "accession" the create a key with called "accession" with the value in that node
            if subchild.tag == '{http://www.hmdb.ca}accession':
                dicts["accession"] = subchild.text
            if subchild.tag == '{http://www.hmdb.ca}name':
                dicts["name"] = subchild.text
                # innerlist.append(subchild.text)
            # if subchild.tag == '{http://www.hmdb.ca}description':
            #     dicts["description"] = subchild.text

            # # if the node tag is "synonyms" the create a key with called "synonyms" with a list of values in that node
            # if subchild.tag == '{http://www.hmdb.ca}synonyms':
            #     for synonym in subchild:
            #         innerlistsyn.append(synonym.text)
            #         # print(innerlist)
            #     dicts["synonyms"] = innerlistsyn

            if subchild.tag == '{http://www.hmdb.ca}chemical_formula':
                dicts["chemical_formula"] = subchild.text

            # similr to the "synonyms" create a list of values to the key "pathway_name"
            if subchild.tag == '{http://www.hmdb.ca}hmdb':
                for property in subchild:
                    if property.tag == '{http://www.hmdb.ca}property':
                        for kind in property:
                            if kind.tag == '{http://www.hmdb.ca}kind' and kind.text == 'logp':
                                # print(kind.text)
                                for value in property:
                                    if value.tag ==  '{http://www.hmdb.ca}value':
                                        print(value.text)
                                        innerlistpredlogp.append(value.text)
                                # print(innerlist)
                dicts["pred_logp"]= innerlistpredlogp


            # similr to the "synonyms" create a list of values to the key "pathway_name"
            if subchild.tag == '{http://www.hmdb.ca}experimental_properties':
                for property in subchild:
                    if property.tag == '{http://www.hmdb.ca}property':
                        for kind in property:
                            if kind.tag == '{http://www.hmdb.ca}kind' and kind.text == 'logp':
                                # if kind.text == 'logp':
                                #print(kind.text)
                                for value in property:
                                    if value.tag ==  '{http://www.hmdb.ca}value':
                                        print(value.text)
                                        innerlistexplogp.append(value.text)
                                # print(innerlist)
                dicts["exp_logp"]= innerlistexplogp



    ###
            # if subchild.tag == '{http://www.hmdb.ca}diseases':
            #     for disease in subchild:
            #         if disease.tag == '{http://www.hmdb.ca}disease':
            #             for childisease in disease:  # childisease = is  references
            #                 if childisease.tag == '{http://www.hmdb.ca}name':
            #                     diseasekey = childisease.text
            #                     innerlistpubmed_id = []
            #                     innerlistrefe_text = []
            #                     innerdictpubmed_id = {}
            #                     innerdictrefe_text = {}
            #                     # innerlistdisname.append(diseasekey.text)
            #                     # print(diseasekey)
            #                 if childisease.tag == '{http://www.hmdb.ca}references':
            #                     for reference in childisease:
            #                         if reference.tag == '{http://www.hmdb.ca}reference':
            #                             # print(reference.tag)
            #                             for childref in reference:
            #                                 # print (pubmed_id.tag)
            #                                 if childref.tag == '{http://www.hmdb.ca}pubmed_id':
            #                                     # print(pubmed_id.text)
            #                                     innerlistpubmed_id.append(childref.text)
            #                                 if childref.tag == '{http://www.hmdb.ca}reference_text':
            #                                     # print(pubmed_id.text)
            #                                     innerlistrefe_text.append(childref.text)
            #                                     innerdictrefe_text["refe_text"] = innerlistrefe_text
            #                                     innerdictpubmed_id["pubmed_id"] = innerlistpubmed_id
            #                     dicts[diseasekey] = {}
            #                     dicts[diseasekey]["pubmed_id"] = innerlistpubmed_id
            #                     dicts[diseasekey]["refe_text"] = innerlistrefe_text


    ###
            # # similr to the "synonyms" create a list of values to the key "pathway_name"
            # if subchild.tag == '{http://www.hmdb.ca}biological_properties':
            #     for pathways in subchild:
            #         if pathways.tag == '{http://www.hmdb.ca}pathways':
            #             for pathway in pathways:
            #                 if pathway.tag == '{http://www.hmdb.ca}pathway':
            #                     for name in pathway:
            #                         if name.tag == '{http://www.hmdb.ca}name':
            #                             innerlistpath.append(name.text)
            #                     # print(innerlist)
            #     dicts["pathway_name"]= innerlistpath
        newlist.append(dicts)


    print("--- %s seconds ---" % (time.time() - start_time))

    JSON_metabolites = newlist
    # create a  JSON file in with the parse data from the HMDB
    with open(pathtojsonfile, 'w') as fout:
        json.dump(JSON_metabolites, fout, indent=4)

    newlist_df = pd.DataFrame(newlist)
    return newlist_df
    # newlist_df = pd.DataFrame(newlist)
#
if __name__ == "__main__":
 
    df_hmdb  =  parser_hmdb_logp('D:/BCDD/Documents/Tal/Projects/HMDB/DataSets/Parser_HMDB.py Input/hmdb_metabolites/hmdb_metabolites.xml',
                'D:/BCDD/Documents/Tal/Projects/HMDB/DataSets/Parser_HMDB.py Output/hmdb_metabolites_logp.json')

# df_hmdb = pd.DataFrame(newlist)
#
#
excelpathin= r'D:\BCDD\Documents\Tal\Projects\Library-Generation\2021-04 COMPLETE HML Library V12_no_title.xlsx'
df_excel = pd.read_excel(excelpathin)
joindata_by_MHDB = pd.merge(left=df_excel, right=df_hmdb, how='left', left_on='identifier', right_on='accession')
joindata_by_MHDB.to_excel(r'D:\BCDD\Documents\Tal\Projects\Library-Generation\MetaSci 1200 lib w Log-P.xlsx', index = False)
#
#
# excelpathin= r'D:\BCDD\Documents\Tal\Projects\Library-Generation\MSMLS plate map_230-01.xlsx'
# df_excel = pd.read_excel(excelpathin)
# # remove all nun rows in the table about ~ 70 moleculs
# df_excel = df_excel[df_excel.SMILES.notnull()]
# trim = df_excel['HMDB/YMDB ID'].str[:11]
# new_df_excel= df_excel.copy()
#
# new_df_excel.loc[:,'HMDB/YMDB ID'] = trim
#
# joindata_by_MHDB = pd.merge(left=new_df_excel, right=df_hmdb, how='left', left_on='HMDB/YMDB ID', right_on='accession')
#
#
# joindata_by_MHDB.to_excel(r'D:\BCDD\Documents\Tal\Projects\Library-Generation\Sigma 600 lib w Log-P.xlsx', index = False)
#
# joindata_by_MHDB[['HMDB/YMDB ID','accession', 'exp_logp','pred_logp'  ]]
#
# pd.set_option('display.max_rows', 5000)
# pd.set_option('display.max_columns', 500)