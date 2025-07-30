import requests
import random

def getproxy(proxylist: list):
    url = "http://ipinfo.io/json"
    
    random.shuffle(proxylist)

    for proxy in proxylist:
        try:
            proxies = {"http": proxy, "https": proxy}
            response = requests.get(url, proxies=proxies, timeout=5)
            if response.status_code == 200:
                return proxy
        except requests.RequestException:
            continue

    print("Valid proxy not found. Contact the package owner: levovarma@gmail.com.")
    return None
