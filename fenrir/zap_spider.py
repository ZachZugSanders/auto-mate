import time
from os import environ

from zapv2 import ZAPv2


def spider_scanner(target: str):
    zap_url = environ.get('ZAP_URL', 'http://127.0.0.1:8080')
    zap = ZAPv2(proxies={'http': zap_url, 'https': zap_url})

    # Exclude URL in the context
    print('Exclude URL from context:')
    zap.urlopen(target)
    scan_id = zap.ajaxSpider.scan(target)
    time.sleep(2)

    while zap.spider.status(scan_id) == 'OK':
        print('Spider progress %: {}'.format(zap.spider.status(scan_id)))
        time.sleep(2)
    print('Spider completed')

    while int(zap.pscan.records_to_scan) > 0:
        print('Records to passive scan : {}'.format(zap.pscan.records_to_scan))
        time.sleep(2)
    print('Passive Scan completed')

    print('Active Scanning target {}'.format(target))
    scan_id = zap.ascan.scan(target)
    while int(zap.ascan.status(scan_id)) < 100:
        print('Scan progress %: {}'.format(zap.ascan.status(scan_id)))
        time.sleep(5)

    alerts = zap.core.alerts()
    print('Active Scan completed')
    for result in alerts:
        assert result['risk'] != 'High'
    return {target: alerts}
