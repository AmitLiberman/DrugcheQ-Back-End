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
        self.find_names()

    # find Hebrew and English Names from data base
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
