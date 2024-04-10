from check_agents import get_proxies
import requests
import json
from fake_headers import Headers

google_url = "https://www.google.com/"
fake_header_generator: Headers = Headers()

proxies_data = get_proxies()
for i, proxy_ip in enumerate(proxies_data):
    proxy_url = proxies_data[proxy_ip]['proxy_url']
    location = proxies_data[proxy_ip]['location']
    proxies = {
        'http': proxy_url,
        'https': proxy_url
    }

    try:
        r = requests.request(method='GET',
                             url=google_url,
                             proxies=proxies,
                             headers=fake_header_generator.generate(),
                             timeout=7)

        print(i + 1, proxy_url, location, r.status_code, r.status_code == 200)
    except Exception as e:
        print(f'\033[31m{i + 1} {str(e)}\033[0m')
        continue
