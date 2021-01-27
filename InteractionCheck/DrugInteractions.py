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
        self.drug_objects = drug_objects
        self.drug_serials = self.configure_serials()
        self.interaction_api_response = self.check_interaction()

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
        else:
            res = requests.get('https://rxnav.nlm.nih.gov/REST/interaction/list.json?rxcuis=' + self.drug_serials)

        return json.loads(res.text)

    # def build_interaction_results(self):



