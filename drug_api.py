import requests
import json
from DB import DB
from langdetect import detect

'''
In the current script I'm using an API for checking interaction between
given drugs.
Detail about the API you can find here: https://rxnav.nlm.nih.gov/InteractionAPIs.html#
'''


# Find the serial number for each drug
def find_serials(drug_list):
    drugs_serial_number = []
    for drug in drug_list:
        x = requests.get('https://rxnav.nlm.nih.gov/REST/rxcui.json?name=' + drug)
        response_as_dict = json.loads(x.text)
        try:
            drugs_serial_number.append(response_as_dict['idGroup'])
        except:  # can't find specific drug
            pass
    return drugs_serial_number


# Insert drug names (user insert and generic) to response dictionary
def insert_drug_name(full_interaction_type, drugs_serial_number, interaction_dict, english_hebrew_names, i, drug_num):
    rxcui = full_interaction_type[i]['minConcept'][drug_num - 1]['rxcui']
    print(drugs_serial_number)
    for drug in drugs_serial_number:
        if drug['rxnormId'][0] == rxcui:
            if drug['name'].lower() != full_interaction_type[i]['minConcept'][drug_num - 1]['name'].lower():
                interaction_dict[i]['drug' + str(drug_num) + '_name'] = drug['name']
            else:
                interaction_dict[i]['drug' + str(drug_num) + '_name'] = \
                    full_interaction_type[i]['minConcept'][drug_num - 1]['name']

            interaction_dict[i]['drug' + str(drug_num) + '_hebrew_name'] = english_hebrew_names[drug['name'].upper()]

    interaction_dict[i]['drug' + str(drug_num) + '_generic_name'] = \
        full_interaction_type[i]['interactionPair'][0]['interactionConcept'][drug_num - 1]['sourceConceptItem']['name']


# Insert severity if exists to response dictionary
def insert_severity(response_as_dict, interaction_dict, i):
    severity_interaction_type = response_as_dict['fullInteractionTypeGroup'][1]['fullInteractionType']
    for j in range(len(severity_interaction_type)):
        if interaction_dict[i]['drug1_name'] in severity_interaction_type[j]['comment'] and interaction_dict[i][
            'drug2_name'] \
                in severity_interaction_type[j]['comment'] or interaction_dict[i]['drug1_generic_name'] in \
                severity_interaction_type[j]['comment'] and interaction_dict[i][
            'drug2_generic_name'] \
                in severity_interaction_type[j]['comment']:
            interaction_dict[i]['severity'] = severity_interaction_type[j]['interactionPair'][0]['severity']


# parse the response JSON file from the API and build dictionary with relevant data
def build_interaction_dict(response_as_dict, drugs_serial_number, english_hebrew_names):
    interaction_dict = {}

    print(response_as_dict)

    # try to find interaction between drug. if it fails - that's means there is bo interaction
    try:
        full_interaction_type = response_as_dict['fullInteractionTypeGroup'][0]['fullInteractionType']
    except:
        print('There is no interaction between the drugs')
        interaction_dict[0] = {}
        interaction_dict[0]['comment'] = 'safe'
        return interaction_dict

    # go over all the interactions and build the interaction_dict
    for i in range(len(full_interaction_type)):
        interaction_dict[i] = {}

        insert_drug_name(full_interaction_type, drugs_serial_number, interaction_dict, english_hebrew_names, i,
                         1)  # drug1
        insert_drug_name(full_interaction_type, drugs_serial_number, interaction_dict, english_hebrew_names, i,
                         2)  # drug2

        interaction_dict[i]['description'] = full_interaction_type[i]['interactionPair'][0]['description']
        interaction_dict[i]['comment'] = full_interaction_type[i]['comment']

        if len(response_as_dict['fullInteractionTypeGroup']) > 1:
            insert_severity(response_as_dict, interaction_dict, i)

    return interaction_dict


# find Hebrew/English names for given drugs
def check_names_from_db(drug_list):
    data_base = DB()
    drug_names = []
    for drug in drug_list:
        # if the drug name written in hebrew
        if detect(drug) == 'he':
            drug_names.append(data_base.fetch_all_data(
                "SELECT english_name,hebrew_name FROM drug_name WHERE hebrew_name LIKE %s ", '%' + drug.upper() + '%'))
        else:  # written in english
            drug_names.append(data_base.fetch_all_data(
                "SELECT english_name,hebrew_name FROM drug_name WHERE english_name LIKE %s ", '%' + drug.upper() + '%'))

    data_base.close_connection()
    return drug_names


# find the interaction between given drugs
def find_interaction(drug_list):
    drug_names = check_names_from_db(drug_list)
    english_hebrew_names = {}
    # make dictionary when key=eng_name and value=heb_name
    for drug in drug_names:
        english_hebrew_names[drug[0][0].split()[0]] = drug[0][1].split()[0]

    drugs_serial_number = find_serials(list(english_hebrew_names.keys()))
    interaction_dict = {}

    drug_exist = []
    serial_numbers = []
    for i, drug in enumerate(drugs_serial_number):
        try:
            serial_numbers.append(drug['rxnormId'][0])
            drug_exist.append(drug)
        except:
            interaction_dict[i] = {}
            interaction_dict[i]['error'] = drug['name']

    if len(serial_numbers) <= 1:
        print(interaction_dict)
        return interaction_dict

    serials = "+".join(serial_numbers)

    # get request for the interaction api.
    if len(drug_list) == 1:
        res = requests.get('https://rxnav.nlm.nih.gov/REST/interaction/interaction.json?rxcui=' + serials)

    else:
        res = requests.get('https://rxnav.nlm.nih.gov/REST/interaction/list.json?rxcuis=' + serials)

    response_as_dict = json.loads(res.text)
    interaction_dict = build_interaction_dict(response_as_dict, drug_exist, english_hebrew_names)
    print(interaction_dict)
    return interaction_dict


if __name__ == '__main__':
    # list = ['rizatriptan', 'moclobemide', 'Humira', 'paracetamol', 'coumadin', 'Morphine', 'Acepromazine']
    list1 = ['coumadin', 'paracetamol',"יומירה"]

    find_interaction(list1)
