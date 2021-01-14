import requests
import json

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
        drugs_serial_number.append(response_as_dict['idGroup']['rxnormId'][0])
    return drugs_serial_number


# parse the response JSON file from the API and build dictionary with relevant data
def build_interaction_dict(response_as_dict):
    full_interaction_type = response_as_dict['fullInteractionTypeGroup'][0]['fullInteractionType']
    interaction_dict = {}
    for i in range(len(full_interaction_type)):
        interaction_dict[i] = {}
        interaction_dict[i]['drug1'] = full_interaction_type[i]['minConcept'][0]['name']
        interaction_dict[i]['drug2'] = full_interaction_type[i]['minConcept'][1]['name']
        interaction_dict[i]['description'] = full_interaction_type[i]['interactionPair'][0]['description']
        severity_interaction_type = response_as_dict['fullInteractionTypeGroup'][1]['fullInteractionType']
        for j in range(len(severity_interaction_type)):

            if interaction_dict[i]['drug1'] in severity_interaction_type[j]['comment'] and interaction_dict[i]['drug2'] \
                    in severity_interaction_type[j]['comment']:
                interaction_dict[i]['severity'] = severity_interaction_type[j]['interactionPair'][0]['severity']
    return interaction_dict


# find the interaction between given drugs
def find_interaction(drug_list):
    drugs_serial_number = find_serials(drug_list)

    serials = "+".join(drugs_serial_number)

    # get request for the interaction api.
    if len(drug_list) == 1:
        res = requests.get('https://rxnav.nlm.nih.gov/REST/interaction/interaction.json?rxcui=' + serials)
    else:
        res = requests.get('https://rxnav.nlm.nih.gov/REST/interaction/list.json?rxcuis=' + serials)

    response_as_dict = json.loads(res.text)

    interaction_dict = build_interaction_dict(response_as_dict)

    return interaction_dict


if __name__ == '__main__':
    list = ['rizatriptan', 'moclobemide', 'Humira']
    find_interaction(list)
