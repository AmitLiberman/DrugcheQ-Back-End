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


#find the interaction between given drugs
def find_interaction(drug_list):
    drugs_serial_number = find_serials(drug_list)

    serials = "+".join(drugs_serial_number)

    # get request for the interaction api.
    # the '&sources=ONCHigh' gives as the interaction with the high severity
    if len(drug_list) == 1:
        res = requests.get('https://rxnav.nlm.nih.gov/REST/interaction/interaction.json?rxcui=' + serials)
        res2 = requests.get('https://rxnav.nlm.nih.gov/REST/interaction/interaction.json?rxcui=' + serials + '&sources=ONCHigh')
    else:
        res = requests.get('https://rxnav.nlm.nih.gov/REST/interaction/list.json?rxcuis=' + serials)
        res2 = requests.get('https://rxnav.nlm.nih.gov/REST/interaction/list.json?rxcuis=' + serials + '&sources=ONCHigh')

    response_as_dict = json.loads(res.text)
    response2_as_dict = json.loads(res2.text)

    print(response_as_dict)
    print(response2_as_dict)


    # length = len(response_as_dict['interactionTypeGroup'][0]['interactionType'][0]['interactionPair'])
    # for i in range(length):
    #     print(response_as_dict['interactionTypeGroup'][0]['interactionType'][0]['interactionPair'][i]['severity'])
    # response_as_dict['interactionTypeGroup'][0]['interactionType'][0]['interactionPair'][0]['interactionConcept']['severity']
    # # professional name of aspirin
    # print(response_as_dict['interactionTypeGroup'][0]['interactionType'][0]['interactionPair'][0]['interactionConcept'][0][
    #           'sourceConceptItem']['name'])
    # # professional name of interaction drug
    # print(response_as_dict['interactionTypeGroup'][0]['interactionType'][0]['interactionPair'][0]['interactionConcept'][1][
    #           'sourceConceptItem']['name'])
    # # description
    # print(response_as_dict['interactionTypeGroup'][0]['interactionType'][0]['interactionPair'][0]['description'])


if __name__ == '__main__':
    list = ['rizatriptan','moclobemide']
    find_interaction(list)
