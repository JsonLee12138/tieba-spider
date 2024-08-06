import re

from .valid import proxy_valid
class ProxyManager():
    used_proxy_index = 0
    proxy_list = []
    proxy_count = 0
    def __init__(self, proxy_list = []):
        self.proxy_list = proxy_list;
        self.proxy_count = len(proxy_list);
    def use_proxy(self):
        index = self.used_proxy_index % self.proxy_count
        proxy_item = self.proxy_list[index]
        self.used_proxy_index += 1
        ip = ""
        port = 0
        if isinstance(proxy_item, list):
            ip = proxy_item[0]
            port = proxy_item[1]
        elif isinstance(proxy_item, dict):
            ip = proxy_item["ip"]
            port = proxy_item["port"]
        elif isinstance(proxy_item, str):
            t = re.sub(r'^\s*(https?://)?\s*|\s*$', '',proxy_item)
            _arr = t.split(":")
            ip = _arr[0]
            port = int(_arr[1])
        else:
            raise ValueError("The proxy element must be a list or dict!")
        ok, proxy = proxy_valid(ip, port)
        if not ok:
            self.use_proxy()
        return proxy
