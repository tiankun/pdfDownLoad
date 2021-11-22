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
        #self.driver = webdriver.Chrome(executable_path="D:\\tools\\chromedriver.exe",options=chrome_options)
        self.driver = webdriver.PhantomJS(executable_path=r'D:\phantomjs-2.1.1-windows\bin\phantomjs.exe',chrome_options=chrome_options)
    def cc(self):
        driver = self.driver
        driver.implicitly_wait(30)  # 隐性等待，最长等30秒
        driver.maximize_window()
        driver.get("https://www.cnblogs.com/Jack-cx/p/9405737.html")
        driver.save_screenshot("e:/app1.png")
        # for i in range(10000):
        #     alipay.getData()
        #     print(i)

    def getData(self):
        driver = self.driver
        driver.find_element_by_xpath("//textarea[@role='combobox']").click()
        driver.find_element_by_xpath("//textarea[@role='combobox']").clear()
        driver.find_element_by_xpath("//textarea[@role='combobox']").send_keys("how are you")
        aa = driver.find_element_by_xpath("//div[@class='eyKpYb']//div").text
        print(aa)
if __name__ == '__main__':
    alipay = AA()
    alipay.cc()
