import requests
import logging

logger = logging.getLogger(__name__)


def request(data):
    response = requests.get(
        'https://proverkacheka.nalog.ru:9999/v1/inns/*/kkts/*/fss/' + data.fss + '/tickets/' + data.tickets +
        '?fiscalSign=' + data.facial_sign + '&sendToEmail=no',
        auth=('+79506268244', '510506'),
        headers={
            'Authorization': 'Basic Kzc5NTA2MjY4MjQ0OjUxMDUwNg==',
            'Device-Id': 'EEF53799158A89CE',
            'Device-OS': 'Adnroid 7.1.1',
            'Version': '2',
            'ClientVersion': '1.4.4.1',
            'Host': 'proverkacheka.nalog.ru:9999',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            'User-Agent': 'okhttp/3.0.1'
        }
    )

    logger.info('%s' % response.status_code)
    return response.text
