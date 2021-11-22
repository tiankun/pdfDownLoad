#coding=utf8
import datetime
import hashlib
import time
import sys
import json
import pika
import requests

#import cx_Oracle

from selenium import webdriver

chrome_options = webdriver.ChromeOptions()
# 使用headless无界面浏览器模式
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

# oracle
# cx_Oracle.init_oracle_client(lib_dir=r"C:\\oracle\\instantclient_19_9")
# connection = cx_Oracle.connect("tk", "tk", "localhost:1521/orcl")
# cursor = connection.cursor()

# RabbitMQ
username = 'ynws_ynws_test'
password = 'ynws_test'
url = '112.74.100.252'
port = 5672
queue = 'ynws_google_list_test'
exchange = 'ynws_google_news'
routing_key = 'list_news'

# 建立连接
userx = pika.PlainCredentials(username, password)
conn = pika.BlockingConnection(pika.ConnectionParameters(url, port, 'ynws_vhost_collect', credentials=userx))

# 开辟管道
channelx = conn.channel()


# 声明队列，参数为队列名
channelx.queue_bind(exchange=exchange,
                   queue=queue)
#channelx.queue_declare(queue, durable=True)
#channelx.queue_declare(queue="dongchannel11")


class Alipay:
    def __init__(self, kw):
        self.kw = kw
        self.driver = webdriver.Chrome(executable_path="D:\\tools\\chromedriver.exe")
        self.driver.set_window_size(1024,768)
        self.page_url="https://www.google.com/search?q=" + self.kw + "&newwindow=1&tbm=nws&sxsrf=ALeKk02C0TOW7gYl5lPcugA3YD2r-uuIbA:1614928852468&source=lnt&tbs=qdr:m&sa=X&ved=0ahUKEwiiztrkzpjvAhUjMn0KHR8wA4IQpwUIJw&biw=1409&bih=880&dpr=1"

    def getData(self):
        driver = self.driver
        driver.implicitly_wait(30)  # 隐性等待，最长等30秒
        driver.get(
            "https://www.google.com/search?q=" + self.kw + "&newwindow=1&tbm=nws&sxsrf=ALeKk02C0TOW7gYl5lPcugA3YD2r-uuIbA:1614928852468&source=lnt&tbs=qdr:m&sa=X&ved=0ahUKEwiiztrkzpjvAhUjMn0KHR8wA4IQpwUIJw&biw=1409&bih=880&dpr=1")
        self.login()

    def login(self):
        time.sleep(2)
        if (self.driver.find_elements_by_xpath('//*[@id="recaptcha"]')):
            self.open_google(self,self.page_url)
        try:
            self.driver.find_elements_by_xpath("//div[@id='rso']/div")
        except:
            try:
                self.driver.find_element_by_xpath("//span[text()='下一页']")
                nextPage = self.driver.find_element_by_xpath("//span[text()='下一页']")
                nextPage.click()
                self.login()
            except:
                print()
        divs = self.driver.find_elements_by_xpath("//div[@id='rso']/div")
        dd = self.driver.find_elements_by_xpath("//div[@class='dbsr']//a")

        for index, v in enumerate(divs):
            ff = v.text.split("\n")
            url = dd[index].get_attribute("href")
            urlmd5 = hashlib.md5(url.encode(encoding='UTF-8')).hexdigest()
            # writeDb(ff[0], ff[1], ff[2], ff[3], url, self.kw, urlmd5)
            body = {
                "source": ff[0],
                "title": ff[1],
                "discript": ff[2],
                "timeStr": ff[3],
                "creaTime": time.time(),
                "kw": self.kw,
                "url": url,
                "md5": urlmd5
            }
            # 发送数据，发送一条，如果要发送多条则复制此段
            channelx.basic_publish(exchange=exchange, routing_key=routing_key, body=json.dumps(body))
            print("--------发送数据完成-----------")
        try:
            nextPage = self.driver.find_element_by_xpath("//span[text()='下一页']")
            if (nextPage):
                nextPage.click()
                self.login()
        except:
            print('')
            # 关闭连接
            print("no")
            conn.close()

    def open_google(self,page_url):
        API_KEY = "42f642c70d242742567bd427ef832fa0"
        data_sitekey = self.driver.find_element_by_xpath('//*[@id="recaptcha"]').get_attribute("data-sitekey")
        data_s = self.driver.find_element_by_xpath('//*[@id="recaptcha"]').get_attribute("data-s")
        u1 = f"https://2captcha.com/in.php?key={API_KEY}&method=userrecaptcha&data-s={data_s}&googlekey={data_sitekey}&pageurl={page_url}&json=1"
        print(u1)
        print(data_sitekey)
        print(data_s)
        r1 = requests.get(u1)
        print(r1.json())
        rid = r1.json().get("request")
        u2 = f"https://2captcha.com/res.php?key={API_KEY}&action=get&id={rid}&json=1"
        time.sleep(10)
        while True:
            print(u2)
            r2 = requests.get(u2)
            print(r2.json())
            if r2.json().get("status") == 1:
                form_tokon = r2.json().get("request")
                break
            time.sleep(3)
        wirte_tokon_js = f'document.getElementById("g-recaptcha-response").innerHTML="{form_tokon}";'
        submit_js = 'document.getElementById("captcha-form").submit();'
        self.driver.execute_script(wirte_tokon_js)
        time.sleep(1)
        self.driver.execute_script(submit_js)


# def writeDb(newsource, title, discript, TIMESTR, newurl, kw, urlmd5):
#     sql = "insert into T_NEWS(newsource,title,discript,TIMESTR,CREATETIME,kw,newurl,urlmd5) values(:2,:3,:4,:5,:6,:7,:8,:9)"
#     data = (newsource, title, discript, TIMESTR, datetime.datetime.now(), kw, newurl, urlmd5)
#     cursor.execute(sql, data)
#     connection.commit()

if __name__ == '__main__':
    #alipay = Alipay(sys.argv[1])
    alipay = Alipay("jeep")
    alipay.getData()
