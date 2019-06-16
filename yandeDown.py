#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-06-16 21:17
# @Author  : Silence
# @Site    :
# @File    : yandeDown.py
# @Software: PyCharm


import downer
import urllib
import urllib.request


def core_downer(html_url):
    link_list = downer.image_link(html_url)
    filename_list = downer.get_filename_list(link_list)
    downer.down_image(link_list, filename_list)
    print('下载完成!')


def multi_page_download():
    total_num_page = int(input("请输入一共要下载的页数: "))
    current_page_num = 1
    full_url = downer.ask_tag()
    current_page_html, current_page_url = downer.check_tag(full_url)
    core_downer(current_page_html)
    while current_page_num < total_num_page:
        next_page_url, next_page_num = downer.next_page(
            current_page_url, current_page_num)
        current_page_num = next_page_num
        core_downer(urllib.request.urlopen(
            next_page_url).read().decode('utf-8'))
    return True


def single_page_download():
    full_url = downer.ask_tag()
    curent_page_html, current_page_url = downer.check_tag(full_url)
    core_downer(curent_page_html)
    curent_page_num = 1
    while True:
        answer = input('是否下载下一页:[Y/N]:')
        if answer == 'Y' or answer == 'y':
            next_page_url, next_page_num = downer.next_page(
                current_page_url, curent_page_num)
            curent_page_html = next_page_num
            core_downer(urllib.request.urlopen(
                next_page_url).read().decode('utf-8'))
        else:
            break

    return True


def main():
    chice = int(input('请输入选项\n 1 ) 连续多页下载 \n 2 ) 单个页面下载\n'))
    if chice == 1:
        multi_page_download()
    else:
        single_page_download()


if __name__ == '__main__':
    main()
