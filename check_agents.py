import requests
import json
import concurrent.futures

IP_check_website = "https://api.ipify.org?format=json"


def get_proxies():
    proxies_info = dict()
    with open("http_proxies.json", 'r+') as f:
        data = json.load(f)['proxies']
        for i, proxy in enumerate(data):
            anonymity = proxy['anonymity']
            country = proxy['ip_data']['country']
            region = proxy['ip_data']['regionName']
            proxy_ip = proxy['ip']
            protocol = proxy['protocol']
            proxy_port = proxy['port']
            proxy_url = proxy['proxy']

            proxies_info[proxy_ip] = {
                'proxy_url': proxy_url,
                'proxy_port': proxy_port,
                'location': f"{region}, {country}",
                'protocol': protocol,
                'anonymity': anonymity
            }
    return proxies_info


proxies = get_proxies()
valid_ones = dict()
for i, ip in enumerate(proxies.keys()):
    proxy_url = proxies[ip]['proxy_url']
    p = {
        'http': proxy_url,
        'https': proxy_url
    }

    try:
        ip_info_checked = requests.request("GET", IP_check_website, proxies=p, timeout=10).json()
    except Exception as e:
        print(f"-----{str(e)}-----")
        continue

    valid_ones[ip] = proxies[ip]
    print(i, proxy_url, ip_info_checked['ip'] == ip)

with open('filtered_valid_proxies.json', 'w+') as f:
    json.dump(valid_ones, f)
    print("Done")

get_proxies()
