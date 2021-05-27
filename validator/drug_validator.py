import requests

if __name__ == '__main__':
    url = "https://esb.gov.il/GovServiceList/IDRServer/SearchByName"

    payload = "{\"val\":\"ACAMOL\",\"prescription\":false,\"healthServices\":false,\"pageIndex\":1,\"orderBy\":0}".encode(
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

    print(response.text)
