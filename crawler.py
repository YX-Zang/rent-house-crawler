import time
import random
from pyquery import PyQuery
from get591 import  get_info
from storage import insertElasticsearch, insertMongodb


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
        data['totalRows'] = totalRows
    return data


def collection_link(web):
    linklist = []
    for link in web('h3 a'):
        print(link.text, 'http:'+link.get('href'))
        link = 'http:'+link.get('href')
        linklist.append(link)
    return linklist


def crawler():
    linklist = []
    for region in [1, 3]:
        url = 'https://rent.591.com.tw/?kind=0&region=%s' % region
        cookies = {'urlJumpIp':str(region)}
        web = PyQuery(url, cookies=cookies)
        total = web('div.pull-left.hasData i').text().replace(',', '')
        total = int(total)
        print("There're %s records" % total)
        linklist.extend(collection_link(web))
        time.sleep(5)
        for data in range(60, total, 30):
            web = PyQuery(url,
                          dic(city=region, firstRow=data, totalRows=total),
                          cookies=cookies)
            linklist.extend(collection_link(web))
            time.sleep(random.randint(6, 9))
    return linklist



if __name__ == '__main__':
    linklist = crawler()
    count=0
    for link in linklist:
        count += 1
        print('test %s %s' % (count, link))
        receive_data = get_info(link)
        if receive_data:
            insertElasticsearch(receive_data)
            insertMongodb(receive_data)
            print('Done')
        time.sleep(random.randint(6, 9))    

