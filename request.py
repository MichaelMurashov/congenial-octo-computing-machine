import requests
import logging

logger = logging.getLogger(__name__)

status_codes = { 'found'       : 204,
                 'not_found'   : 406,
                 'bad_request' : 400 }


def check_exist(data, payload, auth, headers, proxies=None):
    response = requests.get(
        'https://proverkacheka.nalog.ru:9999/v1/ofds/*/inns/*/fss/' + data.fss + '/operations/1/tickets/' + data.tickets,
        params=payload,
        auth=auth,
        headers=headers,
        proxies=proxies
    )

    logger.info(f'{response.status_code}')
    if response.status_code == status_codes['found']:
        return True
    else:
        return False


def request(data):
    payload = { 'fiscalSign': data.facial_sign,
                'date': data.time,
                'sum':data.sum }

    headers = { 'Authorization': 'Basic Kzc5NTA2MjY4MjQ0OjUxMDUwNg==',
                'Device-Id': 'EEF53799158A89CE',
                'Device-OS': 'Adnroid 7.1.1',
                'Version': '2',
                'ClientVersion': '1.4.4.1',
                'Host': 'proverkacheka.nalog.ru:9999',
                'Connection': 'Keep-Alive',
                'Accept-Encoding': 'gzip',
                'User-Agent': 'okhttp/3.0.1' }
    
    auth = ('+79506268244', '420605')
    
    proxi = { 'https': open('data/proxy.txt').read() }
    
    if check_exist(data, payload, auth, headers, proxi):      
        response = requests.get(
            'https://proverkacheka.nalog.ru:9999/v1/inns/*/kkts/*/fss/' + data.fss + '/operations/1/tickets/' + data.tickets,
            params=payload, auth=auth, headers=headers, proxies=proxi
        )
    else:
        return ""

    return response.text
