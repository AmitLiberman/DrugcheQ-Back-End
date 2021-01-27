from DB import DB
from langdetect import detect
import json
import requests


class DrugIdentifier:
    ''''
    In this class we'll identify all the drug details from the user drug name input.
    '''

    # get the name that the user inserted and initialize the relevant properties
    def __init__(self, name):
        self.drug_user_name = name
        # Initialize hebrew and english name to none. They will Initialize in find_names method.
        self.drug_hebrew_name = ''
        self.drug_english_name = ''
        self.ingredients = []
        self.ingredients_serials = []  # empty if there is no need for ingredients_serials
        self.serial_number = 0

        self.find_names()
        self.find_ingredients()
        print(self.drug_user_name, self.drug_hebrew_name, self.drug_english_name, self.ingredients)

    # find Hebrew and English Names from DB
    def find_names(self):
        data_base = DB()
        # if the drug name written in Hebrew
        if detect(self.drug_user_name) == 'he':
            self.drug_hebrew_name = data_base.fetch_all_data(
                "SELECT english_name,hebrew_name FROM drug_name WHERE hebrew_name LIKE %s ",
                '%' + self.drug_user_name + '%')
            self.drug_english_name = self.drug_user_name
        else:  # written in english
            self.drug_english_name = data_base.fetch_all_data(
                "SELECT english_name,hebrew_name FROM drug_name WHERE english_name LIKE %s ",
                '%' + self.drug_user_name.upper() + '%')
            self.drug_hebrew_name = self.drug_user_name
        data_base.close_connection()

    # find the ingredients of the drug from DB. Will help us later for searching interaction.
    def find_ingredients(self):
        data_base = DB()
        temp_drug_list = data_base.fetch_all_data(
            "SELECT ingredients FROM drug_name WHERE english_name LIKE %s ", '%' + self.drug_english_name.upper() + '%')
        ingredients_list = temp_drug_list[0][0].split(';')
        for ingredient in ingredients_list:
            self.ingredients.append(ingredient.split()[0])
        data_base.close_connection()

    # find the drug serial number (rxcui) from the API
    def find_serial_number(self):
        api_response = requests.get('https://rxnav.nlm.nih.gov/REST/rxcui.json?name=' + self.drug_english_name)
        response_as_dict = json.loads(api_response.text)
        # if we found the serial number of the english drug name
        if 'rxnormId' in response_as_dict['idGroup']:
            self.serial_number = response_as_dict['idGroup']['rxnormId'][0]
        else: # search serials for the drug ingredients
            for ingr in self.ingredients:
                api_response = requests.get('https://rxnav.nlm.nih.gov/REST/rxcui.json?name=' +ingr)
                response_as_dict = json.loads(api_response.text)
                if 'rxnormId' in response_as_dict['idGroup']:
                    self.ingredients_serials.append(response_as_dict['idGroup']['rxnormId'][0])

