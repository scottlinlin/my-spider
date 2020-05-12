"""
@author: scott.lin
@license: (C) Copyright 2020, CIPS.
@contact: lfm@cips.com.cn
@software: Pycharm
@file: lei-parse.py
@time: 2020/4/9 11:57
@desc:
"""
import zipfile
import requests
import os
import time
import json
from mode import LEI
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
# from fishbase.fish_logger import logger as log

# 文件存储目录
FILE_DIR = r'D:\lei'
DB_URL = "mysql+pymysql://wangbo:cipswangbo1@cdb-d8q2dhvq.bj.tencentcdb.com:10115/mytxsql"


def download(url):
    """
    下载 lei 数据，保存到本地
    :param url: lei 数据地址
    :return: lei 数据
    """
    # 下载保存到本地
    response = requests.get(url)
    if not os.path.exists(FILE_DIR):
        os.makedirs(FILE_DIR)
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    file_name = os.path.join(FILE_DIR, date + ".zip")
    with open(file_name, "wb") as data:
        data.write(response.content)

    # 解压 zip
    dst_dir = os.path.join(FILE_DIR, date)
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
    unzip_file(file_name, dst_dir)

    # 读取解压后 json 文件
    file_names = os.listdir(dst_dir)
    json_data = None
    for file_name in file_names:
        json_file_name = os.path.join(dst_dir, file_name)
        with open(json_file_name, 'r', encoding='UTF-8') as load_f:
            json_data = json.load(load_f)

    return json_data


def unzip_file(zip_src, dst_dir):
    """
    解压 zip
    :param zip_src: zip文件源
    :param dst_dir: 目的文件目录
    :return:
    """
    r = zipfile.is_zipfile(zip_src)
    if r:
        fz = zipfile.ZipFile(zip_src, 'r')
        for file in fz.namelist():
            fz.extract(file, dst_dir)
    else:
        print('This is not zip')


def parse(data):
    """
    解析 lei 数据
    :param data: lei 源数据
    :return: 处理后 lei 目标数据
    """
    dst_data = data.get("records")
    if not dst_data or dst_data == "":
        return ""

    return dst_data


def check_existing(session, lei_entity):
    existing = session.query(LEI).filter_by(LEI.LEI == lei_entity.LEI).first()
    if not existing:
        friendship = Friendship(self.me, self.friend)
    else:
        friendship = existing
    session.close()
    return friendship


def load(data):
    """
    加载 lei 数据到数据库
    :param data: 处理后的 lei 数据
    :return: 是否加载成功
    """

    db_engine = create_engine(DB_URL, pool_pre_ping=True, encoding="UTF-8", convert_unicode=True, echo=False)
    session = sessionmaker(bind=db_engine)()
    try:
        for item in data:
            lei = item.get("LEI")
            if lei:
                lei = lei.get("$")
            entity = item.get("Entity")
            registration = item.get("Registration")
            extension = item.get("Extension")

            lei_entity = session.query(LEI).filter(LEI.LEI == lei).first()
            if not lei_entity:
                lei_entity = LEI(LEI=lei, Entity=entity, Registration=registration, Extension=extension)
                session.add(lei_entity)
                print("existing")
            else:
                session.query(LEI).filter(LEI.LEI == lei).update({"LEI": lei, "Entity": entity, "Registration": registration, "Extension": extension})
                print("not existing")

    except Exception as e:
        # log.error("数据库查询错误：{0}".format(str(e)))
        print("error")
        return False
    finally:
        session.commit()
        session.close()

    return True


if __name__ == '__main__':
    # url = "https://leidata-preview.gleif.org/storage/golden-copy-files/2020/04/10/322326/20200410-0000-gleif-goldencopy-lei2-last-day.json.zip"
    url = "https://leidata-preview.gleif.org/storage/golden-copy-files/2020/04/14/325476/20200414-1600-gleif-goldencopy-lei2-last-day.json.zip"
    source_data = download(url)
    dest_data = parse(source_data)
    is_success = load(dest_data)