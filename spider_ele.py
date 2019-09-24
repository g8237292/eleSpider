import fcntl
import time
import json
import requests
import logging
logging.basicConfig(level=logging.DEBUG)

url = "https://www.ele.me/restapi/shopping/v3/restaurants?latitude={latitude}&longitude={longitude}&offset={offset}&limit=24&extras[]=activities&extras[]=tags&terminal=web"
h5_url = "https://h5.ele.me/restapi/shopping/v3/restaurants?latitude={latitude}&longitude={longitude}&offset={offset}&limit=8&extras[]=activities&extras[]=tags&extra_filters=home&rank_id=17667b7daf1544c18496ec88c89112e8&terminal=h5"

cookies = "ubt_ssid=slvhb3netga92dm40vbqetzjatsj3btm_2019-06-13; _utrace=1a812ba45e39e60de4b18ec481349d77_2019-06-13; cna=DR8+FfPPpmMCAXAwAvv+hDr9; ut_ubt_ssid=4v15iukdx6x6o5hvrwv51oh5xetbqssm_2019-09-02; perf_ssid=w2xbf0ztkmrqjddr5t5ezutfdcder3yk_2019-09-02; track_id=1567436167|cfa43b34c3f91ec3fff85b8b84e21529c02c51e567cc2ef1ef|fd881eeed9a33e70083ee0c6062fc8eb; _bl_uid=Ihk6z0Um25OjwC1a51ndzg0ypbp0; tzyy=c4206b64841cb5e5a6db8a2cd3a39237; l=cBPFjt_eqmXBwiiJBOfZdurza779yIOfCsPzaNbMiICPOA1WyqxFBZCZe78XCnGVLsg683Jwszq0B-TL1PaFQFw_Mr1Sm1uV.; USERID=1000013954925; UTUSER=1000013954925; SID=qMwkSnw4KkItVPcrAOsW225AxqNHLCrxy9dQ; ZDS=1.0|1569365790|WKR7hsb7kSafU40mX4VCfECI/qIPcKJDo9c9Yz/QgjdE5fuh+isuCizPao3N0eWT/Z9arIaK4AYnOCpLusXwfg==; pizza-rc-ca=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE1NjkzNjU4NTMsInNhbHQxIjoiMmI5ZTg4OWMyMGQ3ZmNmMzhkMTlhOTM0MzViNDJjMDgiLCJzYWx0MiI6IjVjZjA3NWRmMTczNmRmZDBkZTgwNzY0NWIwYWI5ZTU5In0.qsqIsa51YaVL2TDcTwzSp4GdJcsU2kiC5ZR9LF16Zi4; pizza-rc-ca-result=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhbGciOiJIUzI1NiIsImV4cCI6MTU2OTM2NzU5NCwic2FsdDEiOiIyYjllODg5YzIwZDdmY2YzOGQxOWE5MzQzNWI0MmMwOCIsInNhbHQyIjoiNWNmMDc1ZGYxNzM2ZGZkMGRlODA3NjQ1YjBhYjllNTkifQ.u8LPlM_BZW7EsObxnCWsjJWqoVq1CeXmhBZKY2TQaRA; pizza73686f7070696e67=soFDFDje30y95-txtpbwC51nGhFXLFhwOc-FG2B7Hh954ezpCIv60PT_zvUzy-L1; isg=BLOzRxiW6tBukaYEyzzFMsAUQrHd6EeqSNU_L2VQFlI5ZNgG7bnZ-Kj6GvIvRJ-i"

header = {
    # ":authority": "www.ele.me",
    # ":method": "GET",
    # ":path": "/restapi/shopping/v3/restaurants?latitude=24.455828&longitude=118.085435&offset=96&limit=24&extras[]=activities&extras[]=tags&terminal=web",
    # ":scheme": "https",
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7",
    "cookie": cookies,
    "referer": "https://h5.ele.me/msite/",
    "user-agent": "Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Mobile Safari/537.36",
    # "x-shard": "loc=121.604643,31.179632"
}
shop_header = {
    # ":authority": "www.ele.me",
    # ":method": "GET",
    # ":path": "/restapi/shopping/v3/restaurants?latitude=24.455828&longitude=118.085435&offset=96&limit=24&extras[]=activities&extras[]=tags&terminal=web",
    # ":scheme": "https",
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7",
    # "cookie":cookie,
    "origin": "https://h5.ele.me",
    "referer": "https://h5.ele.me/shop/",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
    # "x-shard": "shopid=E17685299309075531961;loc=118.086011,24.464966"
}


# def get_storeId(latitude, longitude, offset):
#     string = session.get(h5_url.format(latitude=latitude, longitude=longitude, offset=offset * 8), headers=header).text
#     patten = re.findall(r"E[1-9][0-9]{10,}", string)
#     print(patten)
#     for i in set(patten):
#         with open("/Users/xulun/storeid.text", "a") as f:
#             f.write(str(i) + "\n")

def get_restaurant_info(session, latitude, longitude, offset):
    r = session.get(h5_url.format(latitude=latitude, longitude=longitude, offset=offset * 8), headers=header)
    wb_data = r.json()
    print(wb_data)
    msg = wb_data.get('message')
    has_next = wb_data.get('has_next')
    if msg:
        print(msg)
        return False
    if not has_next:
        print('完成')
        return False
    time.sleep(3)
    return parsing_info(wb_data, session)


def parsing_info(infos, session):
    # print(infos_str)
    restaurant_dict = {}
    info = True
    # infos = json.loads(infos_str)
    for info in infos:
        if not infos.get(info):
            return
    items = infos.get('items')
    for item in items:
        restaurant_info = item.get('restaurant')
        activity = restaurant_info.get('activities')
        description = [activity[0].get('description') if activity else ""]
        month_sale = json.loads(restaurant_info.get('business_info')).get("recent_order_num_display")
        cate = [i.get('name') for i in restaurant_info.get('flavors')]
        name = restaurant_info.get('name')
        scheme = restaurant_info.get('scheme')
        is_new = ''.join('新店' if restaurant_info.get('is_new') else "\t")
        is_premium = ''.join('品牌' if restaurant_info.get('is_premium') else "\t")
        shop_id = scheme.split('=')[-1]
        if "newretail" in scheme:
            time.sleep(1)
            print('newretail')
            continue
        info = get_phone_address(shop_id, session)
        restaurant_dict['activity_description'] = description
        restaurant_dict['month_sale'] = month_sale
        restaurant_dict['cate'] = '\t'.join(cate)
        restaurant_dict['name'] = name
        restaurant_dict['scheme'] = scheme
        restaurant_dict['is_new'] = is_new
        restaurant_dict['is_premium'] = is_premium
        restaurant_dict['shop_id'] = shop_id
        if not info:
            print(scheme)
            return False
        restaurant_dict['phone'] = info['phone']
        restaurant_dict['address'] = info['address']
        write_info_txt(restaurant_dict)
    return info


def write_info_txt(info):
    with open("shop_info.csv", "a") as f:
        f.write('{name},{is_new},{is_premium},{cate},{month_sale},{activity},{url},{phone},{address}\n'.format(
            name=info.get('name'),
            url=info.get('scheme'),
            cate=info.get('cate'),
            month_sale=info.get('month_sale'),
            activity=info.get('activity_description'),
            is_new=info.get('is_new'),
            is_premium=info.get('is_premium'),
            phone=info.get('phone'),
            address=info.get('address')
        ))

# def read_json(filename, key):
#     with open(filename) as f:
#         a = f.read()
#         print(a)
# read_json("latitude_longitude.json", '软二')

def get_phone_address(shop_id, s):
    address, phone = " ", " "
    data = {
        "add_on_type": 0,
        "additional_actions": [],
        "business_type": 0,
        "come_from": "mobile",
        "entities": [[]],
        "restaurant_id": shop_id,
        "entities_with_ingredient": [[]],
        "packages": [[]],
    }
    url = "https://h5.ele.me/restapi/booking/v1/cart_client"
    time.sleep(3)
    r = s.post(url, data=data, headers=shop_header)
    wb_data = r.json()
    msg = wb_data.get('message')
    if msg:
        print(msg)
        return False
    print(wb_data)
    info_json = wb_data.get('cart')
    if info_json:
        restaurant = info_json.get('restaurant')
        address = restaurant.get('address')
        phone = restaurant.get('phone').replace(' ', ';')
    return {'phone': phone, 'address': address}

if __name__ == '__main__':
    s = requests.session()
    for i in range(59, 90):
        if not get_restaurant_info(
                            s,
                            '24.468965',
                            '118.097526',
                            i,
                            ):
            break


# token = test['validate_token']
# test = "'header_style': 0, 'price_color': 'ff5339', 'hongbao_style': 0, 'default_color': '2395ff'}, 'is_stock_empty': 0, 'id': 'E7126806919857495747'"
# print(test)
# print(re.findall(r"(\d{19})", test))


# url_2 = 'https://h5.ele.me/restapi/eus/login/login_by_mobile'
# code = input('请输入手机验证码：')
# data_2 = {'mobile':tel,
#          'scf':'ms',
#          'validate_code':code,
#          'validate_token':token}
# session.post(url_2,headers=header,data=data_2)

# address_url = 'https://www.ele.me/restapi/v2/pois?'
# place = input('请输入你的收货地址：')
# params = {'extras[]':'count','geohash':'ws105rz9smwm','keyword':place,'limit':'20','type':'nearby'}
# address_res = requests.get(address_url,params=params)
# address_json = address_res.json()
# print('以下，是与'+place+'相关的位置信息：\n')
# n=0
# for address in address_json:
#     print(str(n)+'. '+address['name']+'：'+address['short_address']+'\n')
#     n = n+1
# address_num = int(input('请输入您选择位置的序号：'))
# final_address = address_json[address_num]

# restaurants_url = 'https://www.ele.me/restapi/shopping/restaurants?'

# params = {'extras[]':'activities',
#          'geohash':final_address['geohash'],
#          'latitude':final_address['latitude'],
#          'limit':'24',
#          'longitude':final_address['longitude'],
#          'offset':'0',
#          'terminal':'web'
#  }

# restaurants_res = session.get(restaurants_url,params=params)

# restaurants = restaurants_res.json()
# with open("shopData.text", 'w') as f:
#     f.write("{}".format(restaurants))
# for restaurant in restaurants:
#     print(restaurant['name'])
