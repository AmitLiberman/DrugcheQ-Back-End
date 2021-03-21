import requests
import json
from DB import DB
from InteractionCheck.DrugIdentifier import DrugIdentifier


class DrugInteractions:
    ''''
    In this class we'll configure the interaction between drugs (DrugIdentifier objects)
    and will returns the details about the interaction
    '''

    def __init__(self, drug_objects):
        self.one_drug_interaction = -1
        self.drug_objects = drug_objects
        self.drug_serials = self.configure_serials()
        self.interaction_api_response = self.check_interaction()
        if self.one_drug_interaction == 0:
            self.interaction_results = self.build_interaction_results()
        else:
            self.interaction_results = self.build_full_results()

        print(self.interaction_results)

    def configure_serials(self):
        serials = []
        for drug in self.drug_objects:
            if drug.serial_number != 0:
                serials.append(drug.serial_number)
            else:
                for ingredient_serial in drug.ingredients_serials:
                    serials.append(ingredient_serial)
        return "+".join(serials)

    def check_interaction(self):
        # get request for the interaction api.
        if len(self.drug_objects) == 1:
            res = requests.get('https://rxnav.nlm.nih.gov/REST/interaction/interaction.json?rxcui=' + self.drug_serials)
            self.one_drug_interaction = 1
        else:
            res = requests.get('https://rxnav.nlm.nih.gov/REST/interaction/list.json?rxcuis=' + self.drug_serials)
            self.one_drug_interaction = 0

        return json.loads(res.text)

    def build_interaction_results(self):
        interaction_dict = {}
        # try to find interaction between drug. if it fails - that's means there is no interaction
        try:
            full_interaction_type = self.interaction_api_response['fullInteractionTypeGroup'][0]['fullInteractionType']
        except:
            print('There is no interaction between the drugs')
            interaction_dict[0] = {}
            interaction_dict[0]['comment'] = 'safe'
            return interaction_dict
        # go over all the interactions and build the interaction_dict
        for i in range(len(full_interaction_type)):
            interaction_dict[i] = {}

            self.insert_drug_name(full_interaction_type, interaction_dict, i, 1)  # drug1
            self.insert_drug_name(full_interaction_type, interaction_dict, i, 2)  # drug2

            interaction_dict[i]['description'] = full_interaction_type[i]['interactionPair'][0]['description']
            interaction_dict[i]['comment'] = full_interaction_type[i]['comment']

            # if the severity section exist
            if len(self.interaction_api_response['fullInteractionTypeGroup']) > 1:
                self.insert_severity(interaction_dict, i)
        return interaction_dict

    def build_full_results(self):


        interaction_dict = {}



        try:
            full_interaction_type = self.interaction_api_response['interactionTypeGroup'][0]['interactionType'][0][
                'interactionPair']

        except:
            print('There is no interaction between the drugs full')
            interaction_dict[0] = {}
            interaction_dict[0]['comment'] = 'safe'
            return interaction_dict
        full_interaction_type_severity = ""
        try:
            full_interaction_type_severity = \
                self.interaction_api_response['interactionTypeGroup'][1]['interactionType'][0][
                    'interactionPair']
        except:
            pass
        interatction_drug_names = []
        index = 0
        final_interaction_dict = []
        for i in range(len(full_interaction_type)):
            if full_interaction_type[i]['interactionConcept'][1]['sourceConceptItem']['name'] not in \
                    interatction_drug_names:
                interatction_drug_names.append(
                    full_interaction_type[i]['interactionConcept'][1]['sourceConceptItem']['name'])
                interaction_dict = {"drugName": "", "Description": "", "severity": ""}
                interaction_dict["drugName"] = \
                    full_interaction_type[i]['interactionConcept'][1]['sourceConceptItem']['name']
                interaction_dict["Description"] = full_interaction_type[i]["description"]
                interaction_dict["severity"] = '-'
                for j in range(len(full_interaction_type_severity)):
                    if full_interaction_type_severity != "":
                        if full_interaction_type[i]['interactionConcept'][1]['sourceConceptItem']['name'].lower() == \
                                full_interaction_type_severity[j]['interactionConcept'][1]['sourceConceptItem'][
                                    'name'].lower():
                            interaction_dict["severity"] = 'High'
                            break
                final_interaction_dict.append(interaction_dict)
                index += 1
        res = list(sorted(final_interaction_dict, key=lambda k: k['drugName']))
        final_res = []
        for element in res:
            if element["severity"] == 'High':
                final_res.insert(0, element)
            else:
                final_res.append(element)
        return final_res

    def insert_drug_name(self, full_interaction_type, interaction_dict, i, drug_num):
        rxcui = full_interaction_type[i]['minConcept'][drug_num - 1]['rxcui']
        drug_name = full_interaction_type[i]['minConcept'][drug_num - 1]['name']

        for drug in self.drug_objects:
            if drug.serial_number == 0:  # the drug defined by the it's ingredients
                for ingredient_num in drug.ingredients_serials:
                    if ingredient_num == rxcui:  # if it is the drug we want
                        interaction_dict[i]['drug' + str(drug_num) + '_name'] = drug.drug_english_name
                        interaction_dict[i]['drug' + str(drug_num) + '_hebrew_name'] = drug.drug_hebrew_name
                        interaction_dict[i]['drug' + str(drug_num) + '_generic_name'] = \
                            full_interaction_type[i]['interactionPair'][0]['interactionConcept'][drug_num - 1][
                                'sourceConceptItem']['name']
            else:
                if drug.serial_number == rxcui:
                    if drug.drug_english_name.lower() != drug_name.lower():
                        interaction_dict[i]['drug' + str(drug_num) + '_name'] = drug.drug_english_name
                    else:
                        interaction_dict[i]['drug' + str(drug_num) + '_name'] = \
                            full_interaction_type[i]['minConcept'][drug_num - 1]['name']
                    interaction_dict[i]['drug' + str(drug_num) + '_hebrew_name'] = drug.drug_hebrew_name
                    interaction_dict[i]['drug' + str(drug_num) + '_generic_name'] = \
                        full_interaction_type[i]['interactionPair'][0]['interactionConcept'][drug_num - 1][
                            'sourceConceptItem']['name']

    # Insert severity if exists to response dictionary
    def insert_severity(self, interaction_dict, i):
        severity_interaction_type = self.interaction_api_respons['fullInteractionTypeGroup'][1]['fullInteractionType']
        for j in range(len(severity_interaction_type)):
            if interaction_dict[i]['drug1_name'] in severity_interaction_type[j]['comment'] and interaction_dict[i][
                'drug2_name'] \
                    in severity_interaction_type[j]['comment'] or interaction_dict[i]['drug1_generic_name'] in \
                    severity_interaction_type[j]['comment'] and interaction_dict[i][
                'drug2_generic_name'] \
                    in severity_interaction_type[j]['comment']:
                interaction_dict[i]['severity'] = severity_interaction_type[j]['interactionPair'][0]['severity']
