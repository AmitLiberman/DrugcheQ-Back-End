import requests
import json
from DB import DB
from langdetect import detect
from InteractionCheck.DrugIdentifier import DrugIdentifier
from InteractionCheck.DrugInteractions import DrugInteractions
import os

'''
In the current script I'm using an API for checking interaction between
given drugs.
Detail about the API you can find here: https://rxnav.nlm.nih.gov/InteractionAPIs.html#
'''

# if __name__ == '__main__':
#     list1 = ['rizatriptan', 'moclobemide', 'Humira', 'paracetamol', 'coumadin', 'Morphine', 'Acepromazine', 'aspirin',
#              'pentobarbital', 'פמינט']
#     # list1 = ['rizatriptan', 'moclobemide']
#
#     # list1 = ['rizatriptan', 'Humira', 'paracetamol', 'coumadin','Morphine']
#     # list2 = ['humira', "aspirin",'טלפסט','אקמול']
#     # list1 = ["יומירה", 'פמינט']
#     # list1=['Humira']
#
#     data_base = DB()
#     postgres_insert_query = """ INSERT INTO private_user_details (user_id, user_name, email, real_data) VALUES (%s,%s,%s,%s)"""
#     record_to_insert = ( 'plony', 'asdsa@afssa', False)
#     data_base.insert_row(postgres_insert_query, record_to_insert)
#     postgres_insert_query = """ INSERT INTO report_details (drugs, symptoms, real_data) VALUES (%s,%s,%s)"""
#     record_to_insert = (['humira'],['סחרחורת'], False)
#     data_base.insert_row(postgres_insert_query, record_to_insert)
#     data_base.close_connection()

