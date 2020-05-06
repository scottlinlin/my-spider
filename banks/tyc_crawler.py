# -*- coding: utf-8 -*-
# author: Jiahong Zhou
# create time: 2020-01-24

import re
import requests
import time
from bs4 import BeautifulSoup
import json
import threading
import os
import logging
import urllib
import xlrd
import xlwt
import random


target_headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    'Cache-Control': 'max-age=0',
    'Connection': 'close',
    # 'Cookie': "aliyungf_tc=AQAAANOg6SHR5w0AR4byKtfGhDIlUPVZ; csrfToken=HJcy4CslKltG8OP_lVmIsT5j; TYCID=b0a8b5003ddb11eab6ceff1efdcc5c3a; undefined=b0a8b5003ddb11eab6ceff1efdcc5c3a; ssuid=6383112650; bannerFlag=undefined; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1579782440; _ga=GA1.2.748090208.1579782440; _gid=GA1.2.612510165.1579782440; token=4f15bbf324064781b33be81ffcf72c5b; _utm=7164389fe14e4964aa3b02dee9816dd7; tyc-user-phone=%255B%252215122119332%2522%255D; RTYCID=bc39c3adadc14336a163bc037172b464; CT_TYCID=65e86830ed044dab8547b29c4203ca59; tyc-user-info=%257B%2522claimEditPoint%2522%253A%25220%2522%252C%2522myAnswerCount%2522%253A%25220%2522%252C%2522myQuestionCount%2522%253A%25220%2522%252C%2522signUp%2522%253A%25220%2522%252C%2522explainPoint%2522%253A%25220%2522%252C%2522privateMessagePointWeb%2522%253A%25220%2522%252C%2522nickname%2522%253A%2522%25E5%2585%258B%25E9%2587%258C%25E6%2596%25AF%25C2%25B7%25E5%259F%2583%25E6%2596%2587%25E6%2596%25AF%2522%252C%2522integrity%2522%253A%25220%2525%2522%252C%2522privateMessagePoint%2522%253A%25220%2522%252C%2522state%2522%253A%25220%2522%252C%2522announcementPoint%2522%253A%25220%2522%252C%2522isClaim%2522%253A%25220%2522%252C%2522bidSubscribe%2522%253A%2522-1%2522%252C%2522vipManager%2522%253A%25220%2522%252C%2522discussCommendCount%2522%253A%25221%2522%252C%2522monitorUnreadCount%2522%253A%2522200%2522%252C%2522onum%2522%253A%25220%2522%252C%2522claimPoint%2522%253A%25220%2522%252C%2522token%2522%253A%2522eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxNTEyMjExOTMzMiIsImlhdCI6MTU3OTg0Nzk3MSwiZXhwIjoxNjExMzgzOTcxfQ.e7eU7QMcU65BcMV9H4TdteyY_LXcRVOVVMmh4R6LblckT7cMOswLGKzkV6yX5Hc3x8s-JI3KD3nV3B7MTLGBRA%2522%252C%2522pleaseAnswerCount%2522%253A%25220%2522%252C%2522redPoint%2522%253A%25220%2522%252C%2522bizCardUnread%2522%253A%25220%2522%252C%2522vnum%2522%253A%25220%2522%252C%2522mobile%2522%253A%252215122119332%2522%257D; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxNTEyMjExOTMzMiIsImlhdCI6MTU3OTg0Nzk3MSwiZXhwIjoxNjExMzgzOTcxfQ.e7eU7QMcU65BcMV9H4TdteyY_LXcRVOVVMmh4R6LblckT7cMOswLGKzkV6yX5Hc3x8s-JI3KD3nV3B7MTLGBRA; cloud_token=120ce0a8696246a4a9a14b224b29dcfe; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1579849497; _gat_gtag_UA_123487620_1=1",
    'Cookie': 'bad_id658cce70-d9dc-11e9-96c6-833900356dc6=0fed08d1-8bb7-11ea-8b2e-f3d050bb9ff2; nice_id658cce70-d9dc-11e9-96c6-833900356dc6=0fed08d2-8bb7-11ea-8b2e-f3d050bb9ff2; aliyungf_tc=AQAAAK8MiGxm2wgAh4GitNy2fXsABGrG; csrfToken=EQuJwm42J9yulk3Xp-BBibAK; jsid=SEM-BAIDU-PZ2005-SY-000001; TYCID=18e0cb108bb811ea8ac6b515b39257b1; undefined=18e0cb108bb811ea8ac6b515b39257b1; ssuid=8439714296; bannerFlag=false; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1588343343; _ga=GA1.2.2142242078.1588343343; _gid=GA1.2.218692447.1588343343; RTYCID=8f6f09ff4cbf4e3ea42f8a1af0588501; CT_TYCID=28db6d2d23734d79a4beee31913ad336; tyc-user-info=%257B%2522claimEditPoint%2522%253A%25220%2522%252C%2522vipToMonth%2522%253A%2522false%2522%252C%2522explainPoint%2522%253A%25220%2522%252C%2522integrity%2522%253A%252210%2525%2522%252C%2522state%2522%253A%25220%2522%252C%2522announcementPoint%2522%253A%25220%2522%252C%2522bidSubscribe%2522%253A%2522-1%2522%252C%2522vipManager%2522%253A%25220%2522%252C%2522onum%2522%253A%25220%2522%252C%2522monitorUnreadCount%2522%253A%25220%2522%252C%2522discussCommendCount%2522%253A%25220%2522%252C%2522token%2522%253A%2522eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxODkzMDgzMzI3NyIsImlhdCI6MTU4ODQ4MzM0NSwiZXhwIjoxNjIwMDE5MzQ1fQ.YhnwhKkw1fdJK6kA1hCY-iFRJHBZh5Fijmh_AckAoLID5BMSH0napiMT2jHgv4Xiwjq3BqVNWEram7pVHmMxCg%2522%252C%2522claimPoint%2522%253A%25220%2522%252C%2522redPoint%2522%253A%25220%2522%252C%2522myAnswerCount%2522%253A%25220%2522%252C%2522myQuestionCount%2522%253A%25220%2522%252C%2522signUp%2522%253A%25220%2522%252C%2522nickname%2522%253A%2522%25E4%25B8%25B0%25E8%2587%25A3%25E7%25A7%2580%25E5%2590%2589%2522%252C%2522privateMessagePointWeb%2522%253A%25220%2522%252C%2522privateMessagePoint%2522%253A%25220%2522%252C%2522isClaim%2522%253A%25220%2522%252C%2522pleaseAnswerCount%2522%253A%25220%2522%252C%2522vnum%2522%253A%25220%2522%252C%2522bizCardUnread%2522%253A%25220%2522%252C%2522mobile%2522%253A%252218930833277%2522%257D; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxODkzMDgzMzI3NyIsImlhdCI6MTU4ODQ4MzM0NSwiZXhwIjoxNjIwMDE5MzQ1fQ.YhnwhKkw1fdJK6kA1hCY-iFRJHBZh5Fijmh_AckAoLID5BMSH0napiMT2jHgv4Xiwjq3BqVNWEram7pVHmMxCg; tyc-user-phone=%255B%252218930833277%2522%255D; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1588483348; token=ed9231bb8fb447e8a2fafd4cbf29e40f; _utm=acbef99b5c184a2dabe1579dc3787eda; cloud_token=f9baa9e67a204c5d8afd43c4f93f98db; cloud_utm=49f2ba6a44244073a9a71d2dd73f2a00',
    'DNT': '1',
    'Host': 'www.tianyancha.com',
    'Upgrade-Insecure-Requests': '1'
}

user_agents = [
    r'Mozilla/5.0 (Linux; U; Android 4.4.2; zh-cn; PE-TL20 Build/HuaweiPE-TL20) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 MQQBrowser/5.3 Mobile Safari/537.36',
    r'Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/600.1.3 (KHTML, like Gecko) Version/8.0 Mobile/12A4345d Safari/600.1.4',
    r'Mozilla/5.0 (iPhone; CPU iPhone OS 7_0 like Mac OS X; en-us) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11A465 Safari/9537.53'
]

def read_comp_names_from_xlsx(path=None, sheet_name=None):
    """
    read company names from disk
    :param path: the path of company names(.xlsx)
    :return: the company name is a list of str
    """
    if not path:
        path = "./company_list.xlsx"
    if not sheet_name:
        sheet_name = "Sheet2"
    workbook = xlrd.open_workbook(path)
    # print(workbook.sheet_names())
    work_sheet = workbook.sheet_by_name(sheet_name)
    # print(work_sheet.row(0))
    names = []
    for row in list(work_sheet.get_rows())[1:]:
        names.append(row[0].value)
    return names


def get_html(url, params=None, post_data=None, proxies=False):
    """
    get the html by url and params
    :param url: is target url
    :param params: is a dict of params and they have been encoded
    :param post_data: the data(dict) for post, this param will be None when Get method
    :return: a text of html
    """
    # print("%s %s" % (url, params))
    headers = target_headers
    headers['User-Agent'] = random.choice(user_agents)
    proxies = None
    if params is not None:
        url += "?"
        for key in params.keys():
            url += "%s=%s&" % (str(key), str(params[key]))
        url = url[0:-1]
    if post_data is not None:
        html = requests.post(url, data=post_data, proxies=proxies)
    else:
        # print "url: [%s]" % url
        # print "proxies: %s" % proxies
        # logging.info("target url: [%s], proxies: [%s]" % (url, proxies))
        html = requests.get(url, proxies=proxies, headers=headers)
        # html = requests.get(url)
    # print "url: [%s]\nhtml.text: [%s]" % (url, html.text.encode("utf-8"))
    return html.text


def get_json_data(url, params=None, post_data=None):
    """
    get the json data by url and params(Note: just for the url whose response is a json)
    :param url: is target url
    :param params: is a dict of params has been encoded
    :param post_data: the data(dict) for post, this param will be None when Get method
    :return: a string of json
    """
    json_data = get_html(url, params=params, post_data=post_data)
    # why while statement？
    # because the url have no response sometimes(network or some errors of server)
    # RetryTimes = crawler_config.retry_times
    while json_data is None or json_data == "":
        # RetryTimes -= 1
        # if RetryTimes < 0:
        #     logging.error("Thread: [%s] Retry url: [%s], params: [%s] fail, RetryTimes: [%d]", thread_name, url, params, crawler_config.retry_times)
        #     json_data = None
        #     break
        thread_name = threading.current_thread
        logging.warning("Thread: [%s] Retry url: [%s], params: [%s] post_data: [%s]", thread_name, url, params, post_data)
        print("Warnning: Retry %s" % url)
        time.sleep(2)
        json_data = get_html(url, params=params, post_data=post_data)
    # if json_data is None:
    #     thread_name = threading.current_thread
    #     logging.warning("Thread: [%s] Error url: [%s], params: [%s]", thread_name, url, params)
    json_data = json_data.encode("utf-8")
    return json_data


def find_and_create_dirs(dir_name):
    """
    find dir, create it if it doesn't exist
    :param dir_name: the name of dir
    :return: the name of dir
    """
    if os.path.exists(dir_name) is False:
        os.makedirs(dir_name)
    return dir_name


def write_object_to_file(file_name, target_object):
    """
    write the object to file with json(if the file exists, this function will overwrite it)
    :param file_name: the name of new file
    :param target_object: the target object for writing
    :return: True if success else False
    """
    dirname = os.path.dirname(file_name)
    find_and_create_dirs(dirname)
    with open(file_name, "w") as f:
        json.dump(target_object, f, skipkeys=False, ensure_ascii=False, check_circular=True, allow_nan=True, cls=None, indent=True, separators=None, encoding="utf-8", default=None, sort_keys=False)


def get_comp_url(comp_name):
    """
    get url of company on Tian Yan Cha
    :param comp_name: the name of target company
    :return:
    """
    comp_name = urllib.parse.quote(comp_name)
    url = "https://www.tianyancha.com/search?key=%s" % comp_name
    print(url)
    html = get_html(url)
    # print(html)
    if str(html) == "Not Found":
        return None
    # print html
    soup = BeautifulSoup(html)
    # get the list of divs, the first element is grandpa of tags
    company_divs = soup.findAll('a',  {
        'tyc-event-ch': "CompanySearch.Company",
    })
    if not company_divs:
        return None
    company_div = company_divs[0]
    print(company_div)
    comp_url = company_div.get("href")
    # print(comp_url)
    return comp_url


def get_comp_raddr(comp_url):
    """
    get register address of company
    :param comp_url: the url of target company
    :return: register address
    """
    print("comp_url: %s" % comp_url)
    html = get_html(comp_url)
    # print(html)
    # print("注册地址" in html)
    if str(html) == "Not Found":
        return None
    soup = BeautifulSoup(html)
    # get the list of divs, the first element is grandpa of tags
    table = soup.findAll('table',  {
        'class': "table -striped-col -border-top-none -breakall",
    })
    print(table)
    addrs = re.findall(r"""注册地址</td><td colspan="4">(.+?)<!--<span class="tic tic-fujin c9">""", html)
    print(addrs)
    if addrs:
        return addrs[0]
    else:
        return None

def get_comp_enname(comp_url):
    """
    获取企业英文名称
    :param comp_url: the url of target company
    :return: register address
    """
    print("comp_url: %s" % comp_url)
    html = get_html(comp_url)
    if str(html) == "Not Found":
        return None
    soup = BeautifulSoup(html)
    # get the list of divs, the first element is grandpa of tags
    table = soup.findAll('table',  {
        'class': "table -striped-col -border-top-none -breakall",
    })
    print(table)
    ennames = re.findall(r"""<td width="150px">英文名称</td><td colspan="2">(.+?)</td></tr><tr>""", html)
    print(ennames)
    if ennames:
        return ennames[0]
    else:
        return None

def write_data_to_xls(data, path):
    """
    write the data to xls,
     Note: this method Refer from repo: https://github.com/wangyeyu2016/Python_Crawler_Tianyancha.git
    :param data: a list of tuple(example: [("name", "addr"), (...), ...]
    :param path: the target path
    :return: None
    """
    workbook = xlwt.Workbook()
    sheet1 = workbook.add_sheet('data', cell_overwrite_ok=True)
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = '仿宋'
    #    font.bold = True
    style.font = font
    print('正在存储数据，请勿打开excel')
    name_list = ['公司名字', '注册地址']
    for i in range(0, len(name_list)):
        sheet1.write(0, i, name_list[i], style)
    for i in range(1, len(data)):
        print(data[i-1][0])
        name = data[i][0]
        addr = data[i][1]
        sheet1.write(i, 0, name, style)
        sheet1.write(i, 1, addr, style)
    # workbook.save(r"D:\liuyurou_tianyancha_%s.xlsx" % time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()))
    workbook.save(path)


if __name__ == "__main__":
    names = read_comp_names_from_xlsx()
    # print(names)
    data = []
    for name in names:
        url = get_comp_url(name)
        addr = get_comp_raddr(url)
        print("%s: %s" % (name, addr))
        data.append((name, addr))
    print(data)
    write_data_to_xls(data, "./output_data.xls")