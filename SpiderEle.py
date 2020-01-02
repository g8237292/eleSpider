import fcntl
import os
import sys
import time
import json
from optparse import OptionParser

import requests
import logging
import datetime

logging.basicConfig(
    datefmt='%a, %d %b %Y %H:%M:%S',
    level=logging.DEBUG)

class SpiderEle(object):

    def __init__(self, address, rank_id):
        self.address = address
        data = self.get_json(self.address)
        self.latitude = data.get('latitude')
        self.longitude = data.get('longitude')
        self.rank_id = rank_id

        self.cookies_filename = "eleapi_cookies.txt"
        self.cookies = self.read_cookies(self.cookies_filename)

        self.month =datetime.datetime.now().strftime('%m')
        self.info_dir = './infomation{}/' .format(self.month)

        self.shop_header = {
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

        self.header = {
            "accept": "application/json, text/plain, */*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9",
            "cookie": self.cookies,
            # "cookie": 'ubt_ssid=slvhb3netga92dm40vbqetzjatsj3btm_2019-06-13; _utrace=1a812ba45e39e60de4b18ec481349d77_2019-06-13; cna=DR8+FfPPpmMCAXAwAvv+hDr9; ut_ubt_ssid=4v15iukdx6x6o5hvrwv51oh5xetbqssm_2019-09-02; perf_ssid=w2xbf0ztkmrqjddr5t5ezutfdcder3yk_2019-09-02; track_id=1567436167|cfa43b34c3f91ec3fff85b8b84e21529c02c51e567cc2ef1ef|fd881eeed9a33e70083ee0c6062fc8eb; _bl_uid=Ihk6z0Um25OjwC1a51ndzg0ypbp0; tzyy=c4206b64841cb5e5a6db8a2cd3a39237; l=cBPFjt_eqmXBwiiJBOfZdurza779yIOfCsPzaNbMiICPOA1WyqxFBZCZe78XCnGVLsg683Jwszq0B-TL1PaFQFw_Mr1Sm1uV.; USERID=1000013954925; UTUSER=1000013954925; SID=qMwkSnw4KkItVPcrAOsW225AxqNHLCrxy9dQ; ZDS=1.0|1569365790|WKR7hsb7kSafU40mX4VCfECI/qIPcKJDo9c9Yz/QgjdE5fuh+isuCizPao3N0eWT/Z9arIaK4AYnOCpLusXwfg==; pizza73686f7070696e67=_HHDoSEnvf3wQXmxynSG3kbPgsuDqXj817InDqMxE0Ett7b5dENPwh-IShZb2EIq; isg=BNPTCwKZinCg20ak65wlkiC0YlH9iGdKaLUfj4XwL_IsBPOmDVj3mjFaOjLPpL9C',
            "referer": "https://h5.ele.me/msite/",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Mobile Safari/537.36",
            "x-shard": "loc={longitude},{latitude}, loc={longitude},{latitude}".format(longitude=self.longitude,
                                                                                       latitude=self.latitude)
        }

        self.session = requests.session()

    def get_json(self, address):
        with open("latitude_longitude.json") as j:
            datas = json.load(j)
            data = datas.get(address)
            return data

    def read_cookies(self, filename):
        with open(filename, 'rb') as f:
            return f.read()

    def get_restaurant_info(self, offset):
        # h5_url = "https://h5.ele.me/restapi/shopping/v3/restaurants?latitude={latitude}&longitude={longitude}&offset={offset}&limit=8&extras[]=activities&extras[]=tags&extra_filters=home&rank_id={rank_id}&terminal=h5".format(
        #     latitude=self.latitude, longitude=self.longitude, rank_id=self.rank_id, offset=offset * 8
        # )
        h5_url = 'https://h5.ele.me/restapi/shopping/v3/restaurants?latitude={latitude}&longitude={longitude}&offset={offset}&limit=8&extras[]=activities&extras[]=tags&extra_filters=home&order_by=5&rank_id={rank_id}&terminal=h5'.format(
            latitude=self.latitude, longitude=self.longitude, offset=offset*8, rank_id=self.rank_id)
        r = self.session.get(h5_url, headers=self.header)
        wb_data = r.json()
        print(wb_data)
        msg = wb_data.get('message')
        has_next = wb_data.get('has_next')
        if msg:
            logging.error(msg)
            return False
        if not has_next:
            logging.info("Done")
            return False
        time.sleep(3)
        return self.parsing_info(wb_data)


    def parsing_info(self, infos):
        # print(infos_str)
        restaurant_dict = {}
        info = True
        # infos = json.loads(infos_str)
        for info in infos:
            if not infos.get(info):
                return
        items = infos.get('items')
        for item in items:
            logging.info("item = " + json.dumps(item, indent=2))
            if not item:
                logging.error('item = None')
                continue
            restaurant_info = item.get('restaurant')
            logging.info("restaurant_info = "+json.dumps(restaurant_info, indent=2))
            activity = restaurant_info.get('activities')
            description = [activity[0].get('description') if activity else ""]
            month_sale = json.loads(restaurant_info.get('business_info')).get("recent_order_num_display")
            flavors = restaurant_info.get('flavors')
            cate = []
            if flavors:
                cate = [i.get("name") for i in flavors]
            name = restaurant_info.get('name')
            scheme = restaurant_info.get('scheme')
            is_new = ''.join('新店' if restaurant_info.get('is_new') else "\t")
            is_premium = ''.join('品牌' if restaurant_info.get('is_premium') else "\t")
            shop_id = scheme.split('=')[-1]
            if "newretail" in scheme:
                time.sleep(1)
                print('newretail')
                continue
            info = self.get_phone_address(shop_id)
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
            self.write_info_txt(restaurant_dict)
        return info


    def write_info_txt(self, info):
        if not os.path.exists(self.info_dir):
            os.mkdir(self.info_dir)
        with open(self.info_dir+self.address + '.csv', "a+") as f:
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

    def get_phone_address(self, shop_id):
        address, phone = " ", " "
        """
        {"sub_channel":"","business_type":0,"geohash":"wsk53m9uwbdd","user_id":20566431,"add_on_type":0,"restaurant_id":"E8461406814555919765","come_from":"mobile","additional_actions":[71],"entities":[[]],"entities_with_ingredient":[[]],"operating_sku_ids":[],"tying_sku_entities":[[]],"packages":[[]]}
        """
        data = {
            "sub_channel": "",
            "business_type": 0,
            # "geohash": "wsk53m9uwbdd",
            "geohash": "",
            # "user_id": 20566431,
            "user_id": "",
            "add_on_type": 0,
            "restaurant_id": shop_id,
            "come_from": "mobile",
            "additional_actions": [71],
            "entities": [[]],
            "entities_with_ingredient": [[]],
            "operating_sku_ids": [],
            "tying_sku_entities": [[]],
            "packages": [[]]
        }
        # data = {
        #     "add_on_type": 0,
        #     "additional_actions": [],
        #     "business_type": 0,
        #     "come_from": "mobile",
        #     "entities": [[]],
        #     "restaurant_id": shop_id,
        #     "entities_with_ingredient": [[]],
        #     "packages": [[]],
        # }
        url = "https://h5.ele.me/restapi/booking/v1/cart_client"
        time.sleep(3)
        r = self.session.post(url, data=data, headers=self.shop_header)
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
    parser = OptionParser()
    parser.add_option('-a', '--address', dest='address', help='address')
    parser.add_option('-r', '--rank_id', dest='rank_id', help='rank_id', default="")
    parser.add_option('-p', '--page', dest='page', help='page start', type=int, default=1)
    options, args = parser.parse_args(sys.argv[1:])
    address = options.address
    page = options.page
    rank_id = options.rank_id

    spider = SpiderEle(address, rank_id=rank_id)
    while True:
        if not spider.get_restaurant_info(page):
            logging.error("place:{}\n page:{}".format(address, page))
            break
        page += 1
