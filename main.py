# script.py
import argparse
import json
import re

import requests
from bs4 import BeautifulSoup
import os
from proxy_manager import proxy_valid, ProxyManager

proxyList = [
    ['209.121.164.50', 31147],
    ['135.148.171.194', 18080],
    ['47.74.40.128', 7788],
    ['103.237.144.232', 1311],
    ['114.129.2.82', 8081],
    ['8.223.31.16', 1080],
    ['128.199.136.56', 3128],
    ['67.43.227.227', 11023],
    ['45.136.197.202', 8080],
    ['67.43.227.228', 23737],
    ['195.159.124.57', 85],
    ['166.1.22.160', 8080],
    ['67.43.227.226', 30373],
    ['13.56.18.97', 3128],
    ['47.88.31.196', 8080],
    ['35.185.196.38', 3128],
    ['67.43.227.230', 4961],
    ['152.42.224.138', 3128],
    ['72.10.160.173', 29439],
    ['181.188.27.162', 8080],
    ['47.251.70.179', 80],
    ['13.83.94.137', 3128],
    ['223.135.156.183', 8080],
    ['72.10.160.93', 13931],
    ['188.166.197.129', 3128],
    ['67.43.228.250', 26991],
    ['172.183.241.1', 8090],
    ['160.86.242.23', 8080],
    ['47.236.236.2', 8899],
    ['200.174.198.86', 8888],
    ['72.10.160.170', 2657],
    ['72.10.160.172', 9739],
    ['72.10.164.178', 1417],
    ['164.52.206.180', 80],
    ['189.240.60.171', 9090],
    ['67.43.236.18', 1853],
    ['72.10.160.174', 13093],
    ['222.122.110.26', 80],
    ['72.10.160.92', 5635],
    ['67.43.228.252', 10579],
    ['154.0.132.35', 3128],
    ['64.23.232.139', 3128],
    ['72.10.160.94', 18345],
    ['67.43.236.21', 8307],
    ['8.219.97.248', 80],
    ['67.43.228.253', 12915],
    ['47.90.205.231', 33333],
    ['189.240.60.166', 9090],
    ['47.251.43.115', 33333],
    ['167.99.228.84', 3128],
    ['171.231.28.200', 49236],
    ['148.72.165.7', 30135],
    ['148.72.140.24', 30127],
    ['67.43.236.19', 17293],
    ['5.189.184.6', 80],
    ['20.27.86.185', 8080],
    ['154.236.177.100', 1977],
    ['94.101.185.188', 13699],
    ['66.206.15.148', 8136],
    ['174.138.184.82', 33229],
    ['217.77.102.14', 3128],
    ['119.96.113.193', 30000],
    ['67.43.227.229', 16401],
    ['41.111.167.61', 80],
    ['124.156.237.232', 1080],
    ['74.103.66.15', 80],
    ['20.219.176.57', 3129],
    ['20.204.212.45', 3129],
    ['20.44.189.184', 3129],
    ['171.238.239.96', 5004],
    ['150.136.153.231', 80],
    ['5.196.111.29', 20634],
    ['50.28.7.7', 80],
    ['20.44.188.17', 3129],
    ['20.204.214.79', 3129],
    ['64.206.77.122', 3128],
    ['149.248.6.181', 40002],
    ['37.195.222.7', 52815],
    ['68.183.149.126', 11008],
    ['219.151.19.1', 3128],
    ['3.95.154.78', 3128],
    ['113.219.247.226', 30000],
    ['51.8.224.206', 9000],
    ['119.96.118.113', 30000],
    ['158.101.93.164', 8080],
    ['43.132.124.11', 3128],
    ['69.197.167.74', 6661],
    ['144.48.222.240', 80],
    ['47.88.85.102', 3389],
    ['20.204.214.23', 3129],
    ['188.121.128.250', 9080],
    ['162.253.155.94', 3128],
    ['144.217.131.61', 3148],
    ['46.250.239.99', 8000],
    ['41.173.239.161', 3128],
    ['18.228.173.246', 3128],
    ['66.31.131.217', 8080],
    ['103.228.36.164', 10000]
]
usedProxy = []
proxy = ProxyManager(proxyList)
def main():
    # 创建ArgumentParser对象
    parser = argparse.ArgumentParser(description="Script to demonstrate argument parsing")

    # 添加一个参数：-q/--query
    parser.add_argument('-q', '--query', type=str, help='Query string')

    # 解析命令行参数
    args = parser.parse_args()

    # 获取-q参数的值
    query = args.query
    if query is not None:
        searchFromTieba(query)
    else:
        query = input("请输入您要查询的贴吧：")
        searchFromTieba(query)

def searchFromTieba(q):
    base_url = 'https://tieba.baidu.com'
    search_url = f'{base_url}/f?ie=utf-8&kw={q}&fr=search'
    res = requestWithProxy(search_url)
    soup = BeautifulSoup(res.text, 'html.parser')
    lis = soup.findAll('li', {'class': 'j_thread_list'})
    result = []
    for li in lis:
        item = {
            'title': '',
            'link': '',
            'content': [],
        }
        # 在外层<div>标签中查找内层<div>标签
        titleDiv = li.find('a', {'class': 'j_th_tit'})
        if titleDiv is not None:
            item['title'] = titleDiv.text.strip(' \n\t')
            item['link'] = titleDiv.attrs['href']
            try:
                detailsRes = requestWithProxy(f'{base_url}{item['link']}')
                detailsSoup = BeautifulSoup(detailsRes.text, 'html.parser')
                pContentMainDivs = detailsSoup.findAll('div', {'class': 'd_post_content_main'})
                for pContentDiv in pContentMainDivs:
                    subItem = {
                        'content': '',
                        'images': [],
                        'reply': []
                    }
                    dPContentDiv = pContentDiv.find('div', {'class': 'd_post_content'})
                    if dPContentDiv is not None:
                        subItem['content'] = dPContentDiv.text
                        imagesDivs = dPContentDiv.findAll('img')
                        for imageDiv in imagesDivs:
                            subItem['images'].append({
                                'url': imageDiv.attrs['src'],
                                'width': imageDiv.attrs['width'],
                                'height': imageDiv.attrs['height'],
                            })
                    replyMainDiv = pContentDiv.find('div', {'class': 'core_reply_tail'})
                    if replyMainDiv is not None:
                        replyDivs = replyMainDiv.findAll('li', {'class': 'lzl_single_post'})
                        for replyDiv in replyDivs:
                            replyItem = {}
                            replyUserDiv = replyDiv.find('a', {'class': 'j_user_card'})
                            replyItem['user'] = {
                                'username': replyUserDiv.text,
                                'href': replyUserDiv.attrs['href']
                            }
                            replyContentDiv = replyDiv.find('span', {'class': 'lzl_content_main'})
                            replyImageDivs = replyContentDiv.findAll('img')
                            replyImages = [];
                            for replyImageDiv in replyImageDivs:
                                replyImages.append(replyImageDiv.attrs['src'])
                            replyItem['content'] = {
                                'content': replyContentDiv.text.strip(' \n\t'),
                                'images': replyImages
                            }
                            if subItem['reply'] is not None:
                                subItem['reply'] = [replyItem]
                            else:
                                subItem['reply'].append(replyItem)
                    item['content'].append(subItem)
            except Exception as e:
                print(e, f'{base_url}{item['link']}')
        result.append(item)
    print(result)
    os.makedirs(os.path.dirname('./data'), exist_ok=True)
    filePath = os.path.join('./data', '%s.json'%q)
    # 2. 打开一个文件（如果文件不存在会自动创建）
    with open(filePath, 'w', encoding='utf-8') as file:
        # 3. 写入 JSON 数据
        json.dump(result, file, ensure_ascii=False, indent=4)
    print(f"JSON 文件创建并写入成功，路径为: {filePath}")

def requestWithProxy(*args, **kwargs):
    _proxy = proxy.use_proxy()
    print(proxy.used_proxy_index)
    return requests.get(*args, **kwargs, proxies=_proxy)

if __name__ == "__main__":
    main()