from lxml import etree
import requests
import re
import parse
import redis
import logging
import sys
logging.basicConfig(level=logging.INFO,format="%(asctime)s %(message)s")  # 设置日志级别 不设置默认为WARING以上

def get_redis_client():
    r = redis.Redis(host='localhost', port=6379, db=0)
    return r

def parser_province(province, redis_client):
    pattern = re.compile(".*(\\d+)\D+(\\d+).*")
    province_xpath = '//div[@class="hanml"]/div[@class="conMidtab"]'


    url = "http://www.weather.com.cn/textFC/{region}.shtml".format(region=province)
    rsp = requests.get(url)
    rsp.encoding = 'utf-8' # 防止中文乱码
    if rsp.status_code == 200:
        rsp_node = etree.HTML(rsp.text)
    province_days_nodes = rsp_node.xpath(province_xpath)
    for province_day_node in province_days_nodes:
        conMidtab5 = province_day_node.xpath('./div[@class="conMidtab5"]')[0]
        conty_days_nodes = province_day_node.xpath('./div[@class="conMidtab3"]')
        date_str = conMidtab5.xpath("./table/tr[1]/td[3]/text()")[0]
        print(date_str)
        month = int(pattern.search(date_str).group(1))
        day = int(pattern.search(date_str).group(2))
        date_str0 = "2020/{month:02d}/{day:02d}".format(month=month, day=day)
        for conty_days_node in conty_days_nodes:
            conty = conty_days_node.xpath("./table/tr/td[1]/text()")[0]
            wether = conty_days_node.xpath("./table/tr/td[3]/text()")[0]
            if wether == "-":
                continue
            key = "{conty}-{date}".format(conty=conty, date=date_str0)
            redis_client.set(key, wether)
            logging.info("k={} v={}".format(key, wether))

if __name__ == "__main__":
    region = sys.argv[1]
    if len(region) == 1:
        region = "shanghai"
    redis_client = get_redis_client()
    parser_province(region, redis_client)