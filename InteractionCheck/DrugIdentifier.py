from DB import DB
from langdetect import detect
import json
import requests


class DrugIdentifier:
    ''''
    In this class we'll identify all the drug details from the user drug name input.
    The class retrieves the drug names and ingredients for the DB, and get the serial numbers from the API
    Detail about the API you can find here: https://rxnav.nlm.nih.gov/InteractionAPIs.html#
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
        self.remedy_number = ''
        self.taking_form = ''
        self.dosage_form = ''
        self.prescription = ''
        self.health_basket = ''
        self.details = ''

        found_drug_names = self.find_names()  # updates drug_hebrew_name,drug_english_name
        if found_drug_names:
            self.find_ingredients()  # updates ingredients
            self.find_other_data()
            self.find_serial_number()  # u pdates serial_number, ingredients_serials (if is needed)

        print('User Insert: ', self.drug_user_name)
        print('Hebrew drug name: ', self.drug_hebrew_name)
        print('English drug name: ', self.drug_english_name)
        print('Drug serial number: ', self.serial_number)
        print('Drug ingredients: ', self.ingredients)
        print('Drug ingredients serials: ', self.ingredients_serials)

    # find Hebrew and English Names from DB
    def find_names(self):
        data_base = DB()

        # if the drug name inserted contains only spaces
        if self.drug_user_name.isspace():
            return False

        # if the drug name written in Hebrew
        if detect(self.drug_user_name) == 'he':
            drug_names = data_base.fetch_all_data(
                "SELECT english_name,hebrew_name FROM drug_name WHERE hebrew_name LIKE %s ",
                '%' + self.drug_user_name + '%')
        else:  # written in english
            drug_names = data_base.fetch_all_data(
                "SELECT english_name,hebrew_name FROM drug_name WHERE english_name LIKE %s ",
                '%' + self.drug_user_name.upper() + '%')
        data_base.close_connection()
        # if data base returns the drug names
        if len(drug_names) != 0:
            self.drug_hebrew_name = drug_names[0][1].split()[0]
            self.drug_english_name = drug_names[0][0].split()[0]
            return True
        return False

    # find the ingredients of the drug from DB. Will help us later for searching interaction.
    def find_ingredients(self):
        data_base = DB()
        temp_drug_list = data_base.fetch_all_data(
            "SELECT ingredients FROM drug_name WHERE english_name LIKE %s ", '%' + self.drug_english_name.upper() + '%')
        if ';' in temp_drug_list[0][0]:
            ingredients_list = temp_drug_list[0][0].split(';')
        else:
            ingredients_list = temp_drug_list[0][0].split(',')

        for ingredient in ingredients_list:
            self.ingredients.append(ingredient.split()[0])
        data_base.close_connection()

    # find the ingredients of the drug from DB. Will help us later for searching interaction.
    def find_other_data(self):
        data_base = DB()
        temp_form = data_base.fetch_all_data(
            "SELECT remedy_number, how_taking, dosage_form, prescription, health_basket, details FROM drug_name WHERE english_name LIKE %s ",
            '%' + self.drug_english_name.upper() + '%')
        self.remedy_number = temp_form[0][0]
        self.taking_form = temp_form[0][1]
        self.dosage_form = temp_form[0][2]
        self.prescription = temp_form[0][3]
        self.health_basket = temp_form[0][4]
        self.details = temp_form[0][5].replace('_x000D_', '\n')

        data_base.close_connection()

    # find the drug serial number (rxcui) from the API
    def find_serial_number(self):
        api_response = requests.get('https://rxnav.nlm.nih.gov/REST/rxcui.json?name=' + self.drug_english_name)
        response_as_dict = json.loads(api_response.text)
        # if we found the serial number of the english drug name
        if 'rxnormId' in response_as_dict['idGroup']:
            self.serial_number = response_as_dict['idGroup']['rxnormId'][0]
        else:  # search serials for the drug ingredients
            for ingr in self.ingredients:
                api_response = requests.get('https://rxnav.nlm.nih.gov/REST/rxcui.json?name=' + ingr)
                response_as_dict = json.loads(api_response.text)
                if 'rxnormId' in response_as_dict['idGroup']:
                    self.ingredients_serials.append(response_as_dict['idGroup']['rxnormId'][0])

    def build_search_answer(self):
        answer = {'drug_hebrew_name': self.drug_hebrew_name, 'drug_english_name': self.drug_english_name,
                  'ingredients': self.ingredients, 'remedy_number': self.remedy_number, 'taking_form': self.taking_form,
                  'dosage_form': self.dosage_form, 'prescription': self.prescription,
                  'health_basket': self.health_basket, 'details': self.details}
        return answer
