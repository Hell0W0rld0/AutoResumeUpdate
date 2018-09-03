# -*- coding: utf-8 -*-
# Created by Allen

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
import argparse
import sys
from time import sleep


class AutoJobHunter:
    def __init__(self, username, password):
        # 登陆网站所需要的用户名和密码
        self.username = username
        self.password = password
        # 需要自动刷新简历的网站
        self.zp_url = 'https://www.zhaopin.com'
        self.lp_url = 'https://m.liepin.com/login/?url=https://m.liepin.com/cq/'

    def zhaopin(self):
        try:
            #实例化Options,为启动无GUI界面做准备
            options = Options()
            #添加无GUI模式启动浏览器选项
            options.add_argument('-headless')
            #实例化对象
            driver = Firefox(firefox_options=options)
            #使用webdriver请求url
            driver.get(self.zp_url)
            #定位元素，输入用户名和密码，然后进行提交操作
            driver.find_element_by_name('loginname').send_keys(self.username)
            driver.find_element_by_name('Password').send_keys(self.password)
            driver.find_element_by_tag_name('button').submit()
            sleep(3)
            #定位元素，点击"刷新简历"
            driver.find_element_by_css_selector("a.zp-pfme-funcs-link:nth-child(2) > div:nth-child(3)").click()
            #获取页面变化部分，因为该位置会变化成"刷新成功"
            t = driver.find_element_by_css_selector("a.zp-pfme-funcs-link:nth-child(2) > p:nth-child(2)").text
            if "刷新成功" in t:
                print("智联招聘简历刷新成功！\n")
            driver.close()
        except Exception as e:
            print("出现异常，程序将退出！\n")
            print("具体错误信息如下：\n", e)
            sys.exit(1)

    def liepin(self):
        try:
            options = Options()
            options.add_argument('-headless')
            driver = Firefox(firefox_options=options)
            driver.get(self.lp_url)
            driver.find_element_by_name('user_login').send_keys(self.username)
            driver.find_element_by_css_selector('div.inputzone:nth-child(3) > input:nth-child(2)').send_keys(self.password)
            driver.find_element_by_css_selector('.btn').click()
            sleep(3)
            link = driver.find_element_by_css_selector('div.liepin-channel-list:nth-child(8) > div:nth-child(4) > a:nth-child(1)').get_attribute('href')
            driver.get(link)
            driver.find_element_by_css_selector('a.btn:nth-child(2)').click()
            if driver.get_screenshot_as_file("success.png"):
                print('猎聘网简历刷新成功！\n')
            driver.close()
        except Exception as e:
            print("出现异常，程序将退出！\n")
            print("具体错误如下：\n", e)
            sys.exit(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="自动刷新简历程序")
    parser.add_argument('-u', '--username', help='Please input your username')
    parser.add_argument('-p', '--password', help="Please input your password")
    args = parser.parse_args()
    username = args.username
    password = args.password
    if username and password:
        aj = AutoJobHunter(username, password)
        aj.liepin()
        aj.zhaopin()
    else:
        print(parser.usage)
