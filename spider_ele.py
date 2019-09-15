import time
import requests
from bs4 import BeautifulSoup
import logging; logging.basicConfig(level=logging.DEBUG)
import re
import time
url = "https://www.ele.me/restapi/shopping/v3/restaurants?latitude={latitude}&longitude={longitude}&offset={offset}&limit=24&extras[]=activities&extras[]=tags&terminal=web"
h5_url  = "https://h5.ele.me/restapi/shopping/v3/restaurants?latitude={latitude}&longitude={longitude}&offset={offset}}&limit=8&extras[]=activities&extras[]=tags&extra_filters=home&terminal=h5"

session = requests.session()
header = {
            # ":authority": "www.ele.me",
            # ":method": "GET",
            # ":path": "/restapi/shopping/v3/restaurants?latitude=24.455828&longitude=118.085435&offset=96&limit=24&extras[]=activities&extras[]=tags&terminal=web",
            # ":scheme": "https",
            "accept": "application/json, text/plain, */*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7",
            "cookie": "ubt_ssid=x0s9zhdbr01gpazgo7iumwmvj636assf_2019-06-01; _utrace=d22e180b5c5438c99f7f28bb7db3c631_2019-06-01; perf_ssid=kdd2x2pbxgq38gfisny1603lv28dcj86_2019-06-01; cna=Izm6FJWoRQgCASPcw8nIpoyY; OUTFOX_SEARCH_USER_ID_NCOO=1827448673.549656; track_id=1559335327|f6c378928d6f9d7f7e7836ed4a22ef8cdcb2b2b7a03ec88ed8|b0e92a3bdb6980fa302510d49e72ac98; tzyy=c4206b64841cb5e5a6db8a2cd3a39237; _bl_uid=IRjvmws4cnsl81f4O6mqaeRn6yX6; ut_ubt_ssid=k9yvvnw66xjaed9vg1q8g45wieoe7f0k_2019-07-29; USERID=20566431; UTUSER=20566431; SID=ju6tL4m4oH45AzjaOK9jrdQyHGboJHdChrlw; ZDS=1.0|1565765155|LzA4f7RnDMORYPnKQd2S+SKqyHhqtLiM7pwzmfi+I+0540QrSk1Dz7elNFhCJfvU; ___rl__test__cookies=1566201008212; l=cBavDyruqbArB0MoBOCwNuI8LL7tHIRfluPRwCx9i_5Iz181YBQOkkwI1eJ6cjWFMX8B4elWAJ2Tze3g8PMB5RNYl_ic_q5..; isg=BD8_ytdcXhutLFubUBy0wZeLzhUJjJI0LoNdhtEMre414F5i2fSqF2CyIvC71ms-; pizza73686f7070696e67=soFDFDje30y95-txtpbwC2tlj216KD3w4UsGbsX8fF0lo_l-LI0m1c_Dob8O5TdC",
            "referer": "https://www.ele.me/place/wtw3rhjf989v?latitude=31.179632&longitude=121.604643",
            "referer":"https://h5.ele.me/msite/",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
            # "x-shard": "loc=121.604643,31.179632"
}
def get_storeId(latitude,longitude,offset):
    string = session.get(url.format(latitude=latitude,longitude=longitude,offset=offset*8), headers=header).text
    print(string)
    patten = re.findall(r"E[1-9][0-9]{10,}", string)
    print(patten)
    for i in set(patten):
        with open("/Users/xulun/storeid.text","a") as f:
            f.write(str(i)+"\n")


if __name__ == '__main__':
    for i in range(1,50):
        get_storeId('24.482942','118.159086',i)
        time.sleep(10)



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
