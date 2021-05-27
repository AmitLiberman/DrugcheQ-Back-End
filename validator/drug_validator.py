import requests
from DB import DB


def send_req(drug_name):
    url = "https://esb.gov.il/GovServiceList/IDRServer/SearchByName"

    payload = (
            "{\"val\":\"" + drug_name + "\",\"prescription\":false,\"healthServices\":false,\"pageIndex\":1,\"orderBy\":0}").encode(
        'utf-8')
    headers = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
        'Accept': 'application/json, text/plain, */*',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
        'Content-Type': 'application/json',
        'Origin': 'https://data.health.gov.il',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://data.health.gov.il/',
        'Accept-Language': 'he-IL,he;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cookie': 'p_hosting=!i6PwamUFvB3CyvOXpk/8obFbxLspvVCUpZ2JL/XKvQRJPbUiLc50/TpmFA6ZcKJahUHFpRrfCSHILg=='
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()


def db_check(english_name, hebrew_name):
    data_base = DB()
    temp_drug_list = data_base.fetch_row_data(
        "SELECT * FROM drug_name WHERE hebrew_name=%s and english_name=%s", hebrew_name, english_name)
    data_base.close_connection()
    print(temp_drug_list)
    if len(temp_drug_list) > 0:
        return True
    else:
        return False


def insert_data(new_drug_details):
    data_base = DB()
    new_drug_data = (
        new_drug_details['remedy_number'],
        new_drug_details['english_name'],
        new_drug_details['hebrew_name'],
        new_drug_details['ingredients'],
        new_drug_details['details'],
        new_drug_details['dosage_form'],
        new_drug_details['how_taking'],
        new_drug_details['prescription'],
        new_drug_details['health_basket'],)
    postgres_insert_query = """ INSERT INTO drug_name (remedy_number, english_name, hebrew_name,ingredients,details, dosage_form,\
    how_taking,prescription,health_basket) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    data_base.insert_data_row(postgres_insert_query, new_drug_data)
    data_base.close_connection()


def validate(drug_name):
    response = send_req(drug_name)
    print(response)
    if len(response['results']) == 0:
        return
    english_name = response['results'][0]['dragEnName']
    hebrew_name = response['results'][0]['dragHebName']
    drug_exist = db_check(english_name, hebrew_name)
    if drug_exist:
        print("Drug already exist in DB")
        return

    remedy_number = response['results'][0]['dragRegNum'].replace(" ", "-")
    ingredients = ''
    for key, value in response['results'][0]['activeComponents'][0].items():
        ingredients += value + ';'
    ingredients = ingredients[:-1]
    details = response['results'][0]['indications']
    dosage_form = response['results'][0]['dosageForm']
    how_taking = response['results'][0]['usageForm']
    if response['results'][0]['prescription'] == True:
        prescription = "כן"
    else:
        prescription = "לא"
    if response['results'][0]['health'] == True:
        health_basket = "כן"
    else:
        health_basket = "לא"
    new_drug_details = {'english_name': english_name, 'hebrew_name': hebrew_name, 'remedy_number': remedy_number,
                        'ingredients': ingredients, 'details': details, 'dosage_form': dosage_form,
                        'how_taking': how_taking,
                        'prescription': prescription, 'health_basket': health_basket}
    print("Inserting new drug row to DB")
    print(new_drug_details)
    insert_data(new_drug_details)


if __name__ == '__main__':
    validate("אדמלוג")
