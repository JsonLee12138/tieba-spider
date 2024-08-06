import requests
def proxy_valid(ip, port, test_url = 'www.baidu.com',use_ssl = True):
    protocol = 'https' if use_ssl else 'http'
    test_url = f'{protocol}://{test_url}'
    proxy = {
        'http': f'http://{ip}:{port}'
    }
    if use_ssl:
        proxy['https'] = f'http://{ip}:{port}'
    try:
        res = requests.get(test_url, proxies=proxy, timeout=5)
        if res.ok:
            return True, proxy
        return False, None
    except requests.RequestException as e:
        return False, None