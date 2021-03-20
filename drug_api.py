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

if __name__ == '__main__':
    list1 = ['rizatriptan', 'moclobemide', 'Humira', 'paracetamol', 'coumadin', 'Morphine', 'Acepromazine','aspirin','pentobarbital','פמינט']
    # list1 = ['rizatriptan', 'moclobemide']

    # list1 = ['rizatriptan', 'Humira', 'paracetamol', 'coumadin','Morphine']
    # list2 = ['humira', "aspirin",'טלפסט','אקמול']
    # list1 = ["יומירה", 'פמינט']
    # list1=['Humira']
    #



