from pyquery import PyQuery
import time
import random
import sys


print(sys.version)
def dic(city, firstRow=None, totalRows=None):
    # region 1 = taipei city
    # region 3 = new taipei city
    data = {
        'is_new_list': 1,
        'type': 1,
        'kind': 0,
        'searchtype': 1,
        'region': city
    }
    if firstRow:
        data['firstRow'] = firstRow
    if totalRows:
        data['totalRows']  = totalRows
    return data

def collection_link(web):
    linklist = []
    for link in web('h3 a'):
        print(link.text,'http:'+link.get('href'))
        link = 'http:'+link.get('href')
        linklist.append(link)
    return linklist

linklist = []
for region in [1,3]:
    url = 'https://rent.591.com.tw/?kind=0&region=%s' % region
    cookies = {'urlJumpIp': str(region)}
    web = PyQuery(url,cookies=cookies)
    total2 = web('div.pull-left.hasData i').text().replace(',', '')
    total2 = int(total2)
    total = 90
    print("There're %s records" % total2)
    linklist.extend(collection_link(web))
    print(len(linklist))
    print('---------------------------------------------------------')
    time.sleep(5)
    for data in range(60,total,30):
        web = PyQuery(url, dic(city=region,firstRow=data, totalRows=total2), cookies=cookies)
        linklist.extend(collection_link(web))
        print('---------------------------------------------------------')
        print(len(linklist))
        time.sleep(random.randint(6,15))
