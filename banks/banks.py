"""
@author: scott.lin
@license: (C) Copyright 2020, CIPS.
@contact: lfm@cips.com.cn
@software: Pycharm
@file: banks.py
@time: 2020/4/28 11:23
@desc:
"""
import requests
import demjson
import time
import os
import pandas as pd
from bs4 import BeautifulSoup
from tyc_crawler import get_comp_url, get_comp_enname
import random

ORGAN_URL = "http://xkz.cbirc.gov.cn/ilicence/getOrganInfo.do"
BANK_URL = "http://xkz.cbirc.gov.cn/ilicence/reportLicence.do?useState=3"
BANK_FILE_URL= "http://xkz.cbirc.gov.cn/ilicence/reportLicence.do?useState=3"
BANK_DETAIL_URL ="http://xkz.cbirc.gov.cn/ilicence/showLicenceInfo.do?state=7"
FILE_DIR = r'/Users/linfengming/banks'
FILE_DIR_ETL = r'/Users/linfengming/banks_etl'

def get_organs():
    """
    获取监管机构信息
    :return: 监管机构信息
    """
    response = requests.get(ORGAN_URL)
    organs_json = demjson.decode(response.text)
    organs_json = organs_json.get("root")
    return organs_json


def get_banks_from_organ(organs):
    """
    根据监管机构号获取银行信息,银行信息保存 excel 文件
    :param organ: 监管机构号
    :return: 无
    """
    for organ in organs:
        organ_no = organ.get("organNo")
        if organ_no == -1:
            continue

        # 下载保存到本地
        if not os.path.exists(FILE_DIR):
            os.makedirs(FILE_DIR)
        date = time.strftime('%Y%m%d', time.localtime(time.time()))
        file_name = organ.get("organName") + "_" + date + ".xls"
        file_name = os.path.join(FILE_DIR, file_name)
        url = BANK_FILE_URL + "&fatherOrganNo={}".format(organ_no)
        response = requests.get(url)
        with open(file_name, "wb") as data:
            data.write(response.content)


def etl_to_excel():
    """
    数据处理
    :return: 保存为一个 excel 文件
    """
    try:
        # 读取 excel 文件
        file_names = os.listdir(FILE_DIR)
        file_name_copy = ""
        for file_name in file_names:
            if file_name.find('.xls') < 0:
                continue
            file_name_copy = file_name
            file_name = os.path.join(FILE_DIR, file_name)
            df = pd.read_excel(file_name)
            df = df.fillna(0)

            for ix in df.index:
                # 获取银行详细信息
                pid = int(df.loc[ix, '流水号'])
                if pid > 0:
                    url = BANK_DETAIL_URL + "&id=" + str(pid).zfill(8)
                    bank_detail_dic = get_bank_detail(url)
                    # 休眠 200 毫秒，反爬虫
                    # time.sleep(0.5)
                    df.loc[ix, '机构简称'] = bank_detail_dic.get('short_name')
                    df.loc[ix, '邮政编码'] = bank_detail_dic.get('post_code')
                    df.loc[ix, '变更前流水号'] = bank_detail_dic.get('before_pid')
                    df.loc[ix, '变更前机构编码'] = bank_detail_dic.get('before_id')
                    df.loc[ix, '变更前机构名称'] = bank_detail_dic.get('before_name')
                    df.loc[ix, '变更前机构地址'] = bank_detail_dic.get('before_address')

                # 获取英文名
                # name = df.loc[ix, '机构名称']
                # url = get_comp_url(name)
                # enname = get_comp_enname(url)
                # df.loc[ix, '机构英文名'] = enname

                print(ix)
            if not os.path.exists(FILE_DIR_ETL):
                os.makedirs(FILE_DIR_ETL)
            etl_file_name = os.path.join(FILE_DIR_ETL, file_name_copy)
            df.to_excel(etl_file_name, index=False)
    except Exception as e:
        print(e)


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'close',
    'Cookie': 'isClick=true; JSESSIONID=0000U29ZfPj9egpYVo26odJdFSE:-1',
    'Host': 'xkz.cbirc.gov.cn',
    'Upgrade-Insecure-Requests': '1'
}

user_agents = ["Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0;...) Gecko/20100101 Firefox/61.0",
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
                    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
                    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15"
                    ]


def get_bank_detail(url):
    headers['User-Agent'] = random.choice(user_agents)
    html = requests.get(url, headers=headers)
    if str(html.text) == "Not Found":
        return None
    soup = BeautifulSoup(html.text)
    table = soup.findAll('table', {
        'class': "trw-table-s1",
    })
    trs = []
    if len(table) > 0:
        trs = table[0].findAll('tr')

    # 机构简称
    short_name = ''
    if len(trs) > 3:
        tds = trs[3].findAll('td')
        short_name = tds[1].getText().strip()

    # 邮政编码
    post_code = ''
    if len(trs) > 8:
        tds = trs[8].findAll('td')
        post_code = tds[1].getText().strip()

    # 变更前流水号
    before_pid = ''
    if len(trs) > 15:
        tds = trs[15].findAll('td')
        before_pid = tds[1].getText().strip()

    # 变更前机构编码
    before_id = ''
    if len(trs) > 16:
        tds = trs[16].findAll('td')
        before_id = tds[1].getText().strip()

    # 变更前机构名称
    before_name = ''
    if len(trs) >= 17:
        tds = trs[17].findAll('td')
        before_name = tds[1].getText().strip()

    # 变更前机构地址
    before_address = ''
    if len(trs) >= 18:
        tds = trs[18].findAll('td')
        before_address = tds[1].getText().strip()

    return {'short_name': short_name, 'post_code': post_code, 'before_pid': before_pid,
            'before_id': before_id, 'before_name': before_name, 'before_address': before_address}


if __name__ == '__main__':
    # organs = get_organs()

    # banks = get_banks_from_organ(organs)

    etl_to_excel()


