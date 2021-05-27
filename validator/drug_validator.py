import requests


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


def validate(drug_name):
    response = send_req(drug_name)
    print(response)
    relevant_cols = ['remedy_number', 'english_name', 'hebrew_name', 'ingredients', 'details', 'dosage_form',
                     'how_taking',
                     'prescription', 'health_basket']
    remedy_number = response['results'][0]['dragRegNum']
    english_name = response['results'][0]['dragEnName']
    hebrew_name = response['results'][0]['dragHebName']
    ingredients = ''
    for key, value in  response['results'][0]['activeComponents'][0].items():
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



# drug_exist()


if __name__ == '__main__':
    validate("Humira")
