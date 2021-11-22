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
        self.driver = webdriver.Chrome(executable_path="D:\\tools\\chromedriver.exe", options=chrome_options)

    def cc(self):
        driver = self.driver
        driver.implicitly_wait(30)  # 隐性等待，最长等30秒
        driver.maximize_window()
        driver.get("http://www.cccf.com.cn/certSearch/search")
        self.getData();

    def getData(self):
        driver = self.driver
        aa = driver.find_element_by_xpath("(//table[@class='pageLR2bg']//table)[6]/tbody[1]/tr[1]/td[1]/div[1]/div[1]")
        bb = driver.find_element_by_xpath("(//table[@class='pageLR2bg']//table)[6]/tbody[1]/tr[1]/td[1]/div[1]/div[2]/a[1]")
        cc = driver.find_element_by_xpath("(//table[@class='pageLR2bg']//table)[6]/tbody[1]/tr[1]/td[1]/div[1]/div[3]/div[2]")
        dd = driver.find_element_by_xpath("(//table[@class='pageLR2bg']//table)[6]/tbody[1]/tr[1]/td[1]/div[1]/div[3]/div[4]")
        ee = driver.find_element_by_xpath("(//table[@class='pageLR2bg']//table)[6]/tbody[1]/tr[1]/td[2]/div[1]/a[1]")
        ff = driver.find_element_by_xpath("(//table[@class='pageLR2bg']//table)[6]/tbody[1]/tr[1]/td[2]/div[1]/span[1]")
        gg = driver.find_element_by_xpath("(//table[@class='pageLR2bg']//table)[6]/tbody[1]/tr[1]/td[3]")
        hh = driver.find_element_by_xpath("(//table[@class='pageLR2bg']//table)[6]/tbody[1]/tr[1]/td[4]")
        ii = driver.find_element_by_xpath("(//table[@class='pageLR2bg']//table)[6]/tbody[1]/tr[1]/td[5]")
        xyy = driver.find_element_by_xpath("(//table[@class='pageLR2bg']//table)[13]/tbody[1]/tr[1]/td[2]/a[1]")#首页
        xyy = driver.find_element_by_xpath("(//table[@class='pageLR2bg']//table)[13]/tbody[1]/tr[1]/td[2]/a[3]")#下一页
        xyy = driver.find_element_by_xpath("(//table[@class='pageLR2bg']//table)[13]/tbody[1]/tr[1]/td[2]/a[2]")#上一页
        xyy = driver.find_element_by_xpath("(//table[@class='pageLR2bg']//table)[13]/tbody[1]/tr[1]/td[2]/a[4]")#末页
        xyy = driver.find_element_by_xpath("(//table[@class='pageLR2bg']//table)[13]/tbody[1]/tr[1]/td[2]/input[1]")#输入页码
        xyy = driver.find_element_by_xpath("(//table[@class='pageLR2bg']//table)[13]/tbody[1]/tr[1]/td[2]/input[2]")#go


        jj = bb.get_attribute('href')
        kk = ee.get_attribute('href')
        print(aa.text)
        print(bb.text)
        print(cc.text)
        print(dd.text)
        print(ee.text)
        print(ff.text)
        print(gg.text)
        print(hh.text)
        print(ii.text)
        print(jj)
        print(kk)


if __name__ == '__main__':
    alipay = AA()
    alipay.cc()
