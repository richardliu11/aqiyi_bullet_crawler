# -*- coding: utf-8 -*-
# Title :aqiyi_bullet_crawler
# Author : richard
# Date : 2022/4/24 周日还要上班我操

import requests
import json
import zlib
import pandas as pd
from xml.dom.minidom import parse
import xml.dom.minidom



def get_tv_id(aid):
    # tv_id列表
    tv_id_list = []

    for page in range(1, 3):
        url = 'https://pcw-api.iqiyi.com/albums/album/avlistinfo?aid=' \
              + aid + '&page='\
              + str(page) + '&size=30'

        # 请求网页内容
        res = requests.get(url).text

        res_json = json.loads(res)

        # 视频列表
        move_list = res_json['data']['epsodelist']
        for j in move_list:
            tv_id_list.append(j['tvId'])
            #print(tv_id_list)

    return tv_id_list



def get_bullet(tv_id):
    danmus = []#弹幕存放空列表
    for page in range(1,8):# 剧集时长除以300向上取整:str(page)
        # https://cmts.iqiyi.com/bullet/tv_id[-4:-2]/tv_id[-2:]/tv_id_300_x.z
        # https://cmts.iqiyi.com/bullet/视频编号的倒数4、3位/视频编号的倒数2、1位/视频编号_300_序号.z
        # 弹幕文件每5分钟（300秒）向服务器请求一次，故每集弹幕文件数量等于视频时间(秒)除以300之后向上取整，实际编程时这里可以简单处理
        print(page)
        url = 'https://cmts.iqiyi.com/bullet/'\
              + tv_id[-4:-2] + '/'\
              + tv_id[-2:] + '/'\
              + tv_id + '_300_'\
              + str(page) \
              + '.z'
        print(url)

        # 请求弹幕压缩文件
        res = requests.get(url).content
        res_byte = bytearray(res)
        #print(res_byte)
        try:
            xml1 = zlib.decompress(res_byte).decode('utf-8')
            # 保存路径
            path = 'D:/项目/Enjoy影视剧数据监测及舆情分析框架/爱奇艺相关数据采集/data1/' + tv_id + '_300_' + str(page) + '.xml'
            with open(path, 'w', encoding='utf-8') as f:
                f.write(xml1)
            DOMTree = xml.dom.minidom.parse(path)
            collection = DOMTree.documentElement
            entrys = collection.getElementsByTagName('entry')
            for entry in entrys:
                danmu = entry.getElementsByTagName('content')[0].childNodes[0].data
                danmus.append(danmu)
            df = pd.DataFrame({'弹幕': danmus})
            path2 = 'D:/项目/Enjoy影视剧数据监测及舆情分析框架/爱奇艺相关数据采集/data2/' + tv_id + '_300_' + str(page) + '.csv'
            df.to_csv(path2,encoding='utf-8-sig', index=False)
            # return df
        except:
            return






if __name__ == '__main__':
    # 剧集id
    my_aid = '7881780807418901'
    # tv_id列表
    my_tv_id_list = get_tv_id(my_aid)
    print(my_tv_id_list)
    # print(my_tv_id_list)
    for i in my_tv_id_list:
        get_bullet(str(i))