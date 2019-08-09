import re
from pyquery import PyQuery


def housetype(housetype):
    detailInfo = {}
    housetype = housetype.replace('\xa0', '')
    housetype = housetype.replace('\n', '')
    housetype = housetype.replace(' ', '\n')

    htype = re.findall('型態:(.*)\n', housetype)
    state = re.findall('現況:(.*)\n', housetype)
    floor = re.findall('樓層:(.*)\n', housetype)

    if htype:
        detailInfo.update({'house_type': htype[0]})
    if state:
        detailInfo.update({'state': state[0]})
    if floor:
        detailInfo.update({'floor': floor[0]})

    return detailInfo

def gender_limit(house_info):
    house_info = house_info.replace('\xa0', '')
    house_info = house_info.replace('\n', '')
    house_info = house_info.replace(' ', '\n')

    sex_limit = re.findall('性別要求：(.*)\n', house_info)
    if sex_limit:
        return sex_limit[0]
    else:
        return '--'


def identity_f(data):
    data = data.remove('i').remove('div.auatarSon')
    data = data.text().replace('（', '').replace('）', '')
    data = data.replace('(', '').replace(')', '')
    return data


def get_info(url):
    rent_detail = {}
    data = PyQuery(url)
    if data('#container dl dd'):
        return None
    else:
        title = data('div.houseInfo.clearfix h1 span').text().replace('\n', '')
        house_info_data = data('div.detailInfo.clearfix ul.attr li').text()
        address = data("#propNav span").text().replace('\n' , '')
        owner = data('div.infoOne.clearfix div.avatarRight div i').text()
        identity_data = data("div.infoOne.clearfix div.avatarRight div").remove('i').remove('div.auatarSon')
        identity = identity_f(identity_data)

        text = data.html()
        mobile = PyQuery(text).find('div span.dialPhoneNum')[0].get('data-value')
        gender_data = data('div.leftBox ul.clearfix.labelList.labelList-1 li').text().replace('\n', '')
        price = data('div.price.clearfix i').text().replace('\n', '')
        description = data('div.leftBox div.houseIntro').text().replace('\n', '').replace('\xa0', '')

        rent_detail.update({
            'title': title,
            'url': url,
            'address': address,
            'owner': owner,
            'identity': identity,
            'mobile': mobile,
            'house_info': housetype(house_info_data),
            'price': price,
            'gender': gender_limit(gender_data),
            'description': description
        })
        return rent_detail