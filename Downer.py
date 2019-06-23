#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-06-16 21:17
# @Author  : Silence
# @Site    :
# @File    : Downer.py
# @Software: PyCharm

import urllib
import urllib.request
import urllib.parse
import time
import re
import os
import logging

logging.basicConfig(
    level=logging.DEBUG,
    filename='./log.txt',
    filemode='w',
    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
yande_post_url = "https://yande.re/post"


def makeDir(dirName):
    dirNameQ = dirName.replace("/", " ")
    if os.path.exists(dirNameQ):
        print("文件夹已经存在")
    else:
        os.mkdir(dirNameQ)
    os.chdir(dirNameQ)


def ask_tag():
    tags_info = {}
    tags = input("请输入搜索的关键字:")  # 使用字典保存,方便以后格式化
    if len(tags) > 0:
        tags_info["tags"] = tags
    url = yande_post_url
    search_word = urllib.parse.urlencode(tags_info)
    full_url = url + "?" + search_word
    return full_url


def check_tag(full_url):
    url_html = urllib.request.urlopen(full_url).read().decode('utf-8')
    list_tag = possible_tag(url_html)
    if len(list_tag) == 0:
        filename = time.strftime("%Y%m%d", time.localtime())
        if len(full_url) > 27:
            filename = full_url[27:]
        makeDir(filename)
        return (url_html, full_url)
    else:
        count = 1
        total_tag = len(list_tag)
        for tag in list_tag:
            print(count, tag)
            count += 1
            if count > total_tag:
                break
        choose_tag = int(input("请输入你要查找的Tag: "))
        while choose_tag > total_tag:
            choose_tag = int(input("请重新输入正确的Tag: "))
        suggest_url_tag = suggest_tag(list_tag, choose_tag - 1)
        suggest_url_html = urllib.request.urlopen(
            suggest_url_tag).read().decode('utf-8')
        makeDir(suggest_url_tag[27:])
        return (suggest_url_html, suggest_url_tag)


def possible_tag(url_html):
    possible_tag_re = re.compile("Maybe you meant: <.*")
    find_tag_re = re.compile('href="(.+?)"')
    tmp_tag = ''
    list_tag = []
    if 'Nobody' in url_html:
        for tag_html in possible_tag_re.findall(url_html):
            tmp_tag = tag_html
        for tag_link in find_tag_re.findall(tmp_tag):
            list_tag.append(urllib.parse.unquote(tag_link[11:]))
    return list_tag


def image_link(url_html):
    link_list = []
    direct_link_re = re.compile(r'directlink \w{5}img"(.+?.jpg)')
    for link in direct_link_re.findall(url_html):
        link_list.append(link[7:])
    return link_list


def down_image(link_list, filename_list):
    count = 0
    for link in link_list:
        filename = filename_list[count]
        if os.path.exists(filename):
            print("第%d张图片已经存在" % (count + 1))
        else:
            logging.debug('downing:' + link)
            urllib.request.urlretrieve(link, filename)
            print("下载第%d张图片" % (count + 1))
        count += 1
    else:
        print("全部%d张图片下载完成" % count)


def get_filename_list(link_list):
    filename_list = []
    for link in link_list:
        tmp = urllib.request.unquote(link)
        filename_list.append(tmp[70:])
    return filename_list


def next_page(url_page, page_number):
    page_number = page_number + 1
    next_page_url = url_page[:22] + 'page=' + \
        str(page_number) + '&' + url_page[22:]
    return (next_page_url, page_number)


def suggest_tag(tag_list, choose):
    url = yande_post_url
    suggest_tag_url = url + '?tags=' + tag_list[choose]
    return suggest_tag_url
