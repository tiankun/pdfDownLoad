# coding=utf8
import time
import sys

from selenium import webdriver

chrome_options = webdriver.ChromeOptions()
# 使用headless无界面浏览器模式
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')


class AA:
    def __init__(self):
        #self.driver = webdriver.Chrome(executable_path="D:\\tools\\chromedriver.exe", options=chrome_options)
        self.driver = webdriver.Chrome(executable_path="D:\\tools\\chromedriver.exe")

    def cc(self):
        driver = self.driver
        driver.implicitly_wait(30)  # 隐性等待，最长等30秒
        driver.maximize_window()
        driver.get("https://km.meituan.com/s/%E5%AF%86%E5%AE%A4%E9%80%83%E8%84%B1/")
        self.getData();

    def getData(self):
        driver = self.driver
        aa = driver.find_element_by_xpath("//input[@placeholder='手机号']").send_keys(18787176584)
        time.sleep(2)
        driver.find_element_by_xpath("//input[@placeholder='密码']").send_keys('tk19891113')
        time.sleep(2)
        driver.find_element_by_xpath("//input[@type='checkbox']/following-sibling::i[1]").click()
        time.sleep(2)
        driver.find_element_by_xpath("//input[@type='submit']").click()
        time.sleep(2)
        print(aa.text)



if __name__ == '__main__':
    alipay = AA()
    alipay.cc()
