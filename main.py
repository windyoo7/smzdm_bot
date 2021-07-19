"""
什么值得买自动签到脚本
使用github actions 定时执行
@author : stark
"""
import requests,os
from sys import argv

import config
from utils.serverchan_push import push_to_wechat

class SMZDM_Bot(object):
    def __init__(self):
        self.session = requests.Session()
        # 添加 headers
        self.session.headers = config.DEFAULT_HEADERS

    def __json_check(self, msg):
        """
        对请求 盖乐世社区 返回的数据进行进行检查
        1.判断是否 json 形式
        """
        try:
            result = msg.json()
            print(result)
            return True
        except Exception as e:
            print(f'Error : {e}')            
            return False

    def load_cookie_str(self, cookies):
        """
        起一个什么值得买的，带cookie的session
        cookie 为浏览器复制来的字符串
        :param cookie: 登录过的社区网站 cookie
        """
       
        self.session.headers['Cookie'] = '__ckguid=vBN5s4eHyPGKkHfFUOBIkn2; sajssdk_2015_cross_new_user=1; Hm_lvt_9b7ac3d38f30fe89ff0b8a0546904e58=1626669647; device_id=20060128631626669646718268668817647916a742ab9f6b2b059f6275; zdm_qd={}; _ga=GA1.2.693162245.1626669649; _gid=GA1.2.695482922.1626669649; DISABLE_APP_TIP=1; FROM_BD=1; smidV2=202107191243035107afcad997f1490c4e47153c30e304009cd5006521dc540; sess=AT-wDXGhjzbvfmwHR/fP0mw+VU2LttK6uuLyuWfieu94OkSypAkTVGmgZq1jjmjzq5w/bTqpEdg+a1fWxy2tZaqZmBIue6h+KsDxmOovynlACp5gRmvC7/CDpfC; user=user:5150557481|5150557481; smzdm_id=5150557481; sensorsdata2015jssdkcross={"distinct_id":"17abd1104a7351-09e2ed51e3599b-6373264-2073600-17abd1104a8c96","first_id":"","props":{"$latest_traffic_source_type":"直接流量","$latest_search_keyword":"未取到值_直接打开","$latest_referrer":"","$latest_landing_page":"https://m.smzdm.com/"},"$device_id":"17abd1104a7351-09e2ed51e3599b-6373264-2073600-17abd1104a8c96"}; Hm_lpvt_9b7ac3d38f30fe89ff0b8a0546904e58=1626677357' 
        self.session.headers['Cookie'] = self.session.headers['Cookie'].encode("utf-8").decode("latin1")

    def checkin(self):
        """
        签到函数
        """
        url = 'https://zhiyou.smzdm.com/user/checkin/jsonp_checkin'
        msg = self.session.get(url)
        if self.__json_check(msg):
            return msg.json()
        return msg.content




if __name__ == '__main__':
    sb = SMZDM_Bot()
    # sb.load_cookie_str(config.TEST_COOKIE)
    cookies = os.environ["COOKIES"]
    sb.load_cookie_str(cookies)
    res = sb.checkin()
    print(res)
    SERVERCHAN_SECRETKEY = os.environ["SERVERCHAN_SECRETKEY"]
    print('sc_key: ', SERVERCHAN_SECRETKEY)
    if isinstance(SERVERCHAN_SECRETKEY,str) and len(SERVERCHAN_SECRETKEY)>0:
        print('检测到 SCKEY， 准备推送')
        push_to_wechat(text = '什么值得买每日签到',
                        desp = str(res),
                        secretKey = SERVERCHAN_SECRETKEY)
    print('代码完毕')
