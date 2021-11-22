# coding=utf8
import datetime
import hashlib
import time
import sys
import json
import _thread
import pika
import threading

from selenium.webdriver import ActionChains  # 鼠标右键操作模拟
import pyautogui  # 右键菜单元素选择

from urllib.parse import quote_plus
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pc555 import AA

chrome_options = webdriver.ChromeOptions()
# 使用headless无界面浏览器模式
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
#chrome_options.add_argument("--user-data-dir=" + r"C:/Users/1172/AppData/Local/Google/Chrome/User Data/")
prefs = {
    'profile.default_content_setting_values':
        {
            'notifications': 2
        }
}
chrome_options.add_experimental_option('prefs', prefs)  # 关掉浏览器左上角的通知提示
chrome_options.add_argument("disable-infobars")  # 关闭'chrome正受到自动测试软件的控制'提示

# driver.implicitly_wait(10)
driver = webdriver.Chrome(executable_path="D:\\tools\\chromedriver.exe")
driver.maximize_window()



# RabbitMQ
username = 'ynws_ynws_test'
password = 'ynws_test'
url = '112.74.100.252'
port = 5672
exchange = 'ynws_google_news'

queue1 = 'ynws_google_list_test'
queue2 = 'ynws_google_detail'

routing_key1 = 'list_news'
routing_key2 = 'google_news_detail'

mongo_user = "root"
mongo_password = "p@ssword001x"
mongo_host = "39.129.20.84:27020"

# 建立连接
userx = pika.PlainCredentials(username, password)
conn = pika.BlockingConnection(pika.ConnectionParameters(url, port, 'ynws_vhost_collect', credentials=userx))

# 开辟管道
channel = conn.channel()

# 声明队列，参数为队列名
channel.queue_bind(exchange=exchange,queue=queue1)
channel.queue_bind(exchange=exchange,queue=queue2)

class Heartbeat(threading.Thread):
    def __init__(self, connection):
        super(Heartbeat, self).__init__()
        self.lock = threading.Lock()
        self.connection = connection
        self.quitflag = False
        self.stopflag = True
        self.setDaemon(True)

    def run(self):
        while not self.quitflag:
            time.sleep(10)
            self.lock.acquire()
            if self.stopflag:
                self.lock.release()
                continue
            try:
                self.connection.process_data_events()
            except Exception as ex:
                # logging.warn("Error format: %s"%(str(ex)))
                self.lock.release()
                return
            self.lock.release()

    def startHeartbeat(self):
        self.lock.acquire()
        if self.quitflag == True:
            self.lock.release()
            return
        self.stopflag = False
        self.lock.release()


def get_web_detail(json_body):
    driver.get(json_body["url"])
    try:
        element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        # 第一种
        # 第二种
        # text = driver.execute_script("(function(window){function getHtml(){let datas=window.document.getElementsByTagName('p');if(datas&&datas.length>0){let parents=[];for(let i=0;i<datas.length;i++){let data=datas[i];let parent=data.parentElement;let found=false;parents.some((item)=>{let{p}=item;if(p===parent){found=true;item.count++;return true}});if(!found){parents.push({p:parent,count:1})}}parents.sort((v1,v2)=>{return v2.count-v1.count});if(parents.length>0){let datas=parents[0].p.getElementsByTagName('p');if(datas&&datas.length>0){let content='';for(let i=0;i<datas.length;i++){let v=datas[i];let txt=v.innerText;content=`${content}\n${txt}`}console.log(content);return content}}}}window.google={getHtml}})(window);return google.getHtml();")
        # text = driver.execute_script("(function(window){function getHtml(){let datas=window.document.getElementsByTagName('p');if(datas&&datas.length>0){let parents=[];for(let i=0;i<datas.length;i++){let data=datas[i];let parent=data.parentElement;let found=false;parents.some((item)=>{let{p}=item;if(p===parent){found=true;item.count++;return true}});if(!found){parents.push({p:parent,count:1})}}parents.sort((v1,v2)=>{return v2.count-v1.count});if(parents.length>0){let datas=parents[0].p.getElementsByTagName('p');if(datas&&datas.length>0){let content='';for(let i=0;i<datas.length;i++){let v=datas[i];let txt=v.innerText;content=`${content}\n${txt}`}console.log(content);return content}}}}window.google={getHtml}})(window);return google.getHtml();")
        # 第三种
        # htmlText = driver.execute_script("function getHtml(){let datas=window.document.getElementsByTagName('p');if(datas&&datas.length>0){let parents=[];for(let i=0;i<datas.length;i++){let data=datas[i];let parent=data.parentElement;let found=false;parents.some((item)=>{let{p}=item;if(p===parent){found=true;item.count++;return true}});if(!found){parents.push({p:parent,count:1})}}parents.sort((v1,v2)=>{return v2.count-v1.count});if(parents.length>0){let datas=parents[0].p.getElementsByTagName('p');if(datas&&datas.length>0){let content='';for(let i=0;i<datas.length;i++){let v=datas[i];let txt=v.innerText;content=`${content}\n${txt}`}console.log(content);return content}}}}; return getHtml();")
        # htmlText = driver.execute_script("return document.body.clientHeight")

        # 直接取body
        text = driver.execute_script("return document.body.innerText")
        html = driver.execute_script("return document.body.innerHTML")

        json_body['text'] = text
        #google_translate_chrome(driver)
        #mongo_update_one(myquery, newvalues)
        #channel.basic_publish(exchange=exchange, routing_key=routing_key2, body=json.dumps(json_body))
        # driver.quit()
    finally:
        return


def callback(ch, method, properties, body):  # 四个参数为标准格式


    # 管道内存对象  内容相关信息  后面
    json_body = json.loads(body.decode())
    get_web_detail(json_body)
    ch.basic_ack(delivery_tag=method.delivery_tag)  # 告诉生成者，消息处理完成
    # 创建两个线程
    # try:
    #     get_web_detail(json_body)
    #     ch.basic_ack(delivery_tag=method.delivery_tag)  # 告诉生成者，消息处理完成
    #     # _thread.start_new_thread(get_web_detail, (json_body,))
    # except:
    #     print("Error: 无法启动线程")
    #     print(body.decode())
    # finally:
    #     print()


def mq_consume_start():
    channel.basic_qos(prefetch_count=1, global_qos=True)
    channel.basic_consume(  # 消费消息
        queue1,  # 你要从那个队列里收消息
        callback,  # 如果收到消息，就调用callback函数来处理消息
        # no_ack=True  # 写的话，如果接收消息，机器宕机消息就丢了 True，无论调用callback成功与否，消息都被消费掉
        # 一般不写。宕机则生产者检测到发给其他消费者
    )

    print(' [*] Waiting for messages. To exit press CTRL+C')
    # heartbeat = Hear
    # tbeat(conn)
    # heartbeat.start()  # 开启心跳线程
    # heartbeat.startHeartbeat()
    channel.start_consuming()  # 开始消费消息

def google_translate_chrome(driver):
    rightClick = ActionChains(driver)  # 实例化ActionChains类
    rightClick.move_by_offset(0, 500).context_click().perform()  # context_click(body)在body上执行右键操作，perform()是一个执行动作
    pyautogui.typewrite(['up', 'up', 'up'])  # 选中右键菜单中第2个选项
    time.sleep(0.5)

    pyautogui.typewrite(['enter'])  # 最后一个按键： mac电脑用的return，Windows应用enter
    time.sleep(2)
    newHeight = 0
    while True:
        scHeight = driver.execute_script("return document.body.scrollHeight")
        newHeight = newHeight + 1000
        driver.execute_script("window.scrollTo(0, " + str(newHeight) + ");")
        time.sleep(1)
        if newHeight >= scHeight:
            break
        rightClick.move_by_offset(0, -500).context_click().perform()
    return driver


if __name__ == '__main__':
    mq_consume_start()
