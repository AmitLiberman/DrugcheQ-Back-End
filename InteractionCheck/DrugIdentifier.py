from DB import DB
from langdetect import detect


class DrugIdentifier:
    ''''
    In this class we'll identify all the drug details from the user drug name input.
    '''

    # get the name that the user inserted
    def __init__(self, name):
        self.drug_name = name
        # Initialize hebrew and english name to none. They will Initialize in find_names method.
        self.drug_hebrew_name = ''
        self.drug_english_name = ''
        self.ingredients = []
        self.find_names()
        self.find_ingredients()
        print(self.drug_name,self.drug_hebrew_name,self.drug_english_name,self.ingredients)

    # find Hebrew and English Names from DB
    def find_names(self):
        data_base = DB()
        # if the drug name written in Hebrew
        if detect(self.drug_name) == 'he':
            self.drug_hebrew_name = data_base.fetch_all_data(
                "SELECT english_name,hebrew_name FROM drug_name WHERE hebrew_name LIKE %s ",
                '%' + self.drug_name + '%')
            self.drug_english_name = self.drug_name
        else:  # written in english
            self.drug_english_name = data_base.fetch_all_data(
                "SELECT english_name,hebrew_name FROM drug_name WHERE english_name LIKE %s ",
                '%' + self.drug_name.upper() + '%')
            self.drug_hebrew_name = self.drug_name
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
