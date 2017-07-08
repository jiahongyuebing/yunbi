import requests
import re
from bs4 import BeautifulSoup
import json
import time

def get_html(url):
    
    #模仿GET包的形式
    agent="Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36"
    headers={
        "Host":"yunbi.com",
        "Referer":"https://yunbi.com/?warning=false",
        "Cookie":cookie,
        "User-Agent":agent
        }

    #构造用于网络请求的session
    session=requests.Session()
    #转化为有价值的数据的字典
    response=session.get(url=url,headers=headers).json()
    return response

#将静态html上的内容取下
def get_value(html):
    #将html文件解析
    soup=BeautifulSoup(html,"html.parser")
    print (soup)
    #写出正则表达式
    '''p=r'<span class="ui header highchart market">*?</span>'
    text=re.findall(p,html)
    for each in text:
        print(each)'''

def get_data(html):
    data={}
    data['btccny']=html['btccny']['ticker']['sell']
    data['ethcny']=html['ethcny']['ticker']['sell']
    data['zeccny']=html['zeccny']['ticker']['sell']
    data['qtumcny']=html['qtumcny']['ticker']['sell']
    data['gxscny']=html['gxscny']['ticker']['sell']
    data['eoscny']=html['eoscny']['ticker']['sell']
    data['anscny']=html['anscny']['ticker']['sell']
    data['sccny']=html['sccny']['ticker']['sell']
    data['dgdcny']=html['dgdcny']['ticker']['sell']
    data['1stcny']=html['1stcny']['ticker']['sell']
    data['btscny']=html['btscny']['ticker']['sell']
    data['gntcny']=html['gntcny']['ticker']['sell']
    data['repcny']=html['repcny']['ticker']['sell']
    data['etccny']=html['etccny']['ticker']['sell']
    return data


#存储数据
def store_data(sell,bi_type):
    import pymysql
    import datetime
    config = {
          'host':'127.0.0.1',
          'port':3306,
          'user':'root',
          'password':none,
          'db':'database',
          'charset':'utf8mb4',
          'cursorclass':pymysql.cursors.DictCursor,
          }
    conn=pymysql.connect(**config)
    try:
        cur=conn.cursor()
        sql="INSERT INTO "+bi_type+"(date_time,sell) VALUES(%s,%s)"
        cur.execute(sql,(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),sell))
        #print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        conn.commit()
    finally:
        cur.close()
        conn.close()
        
    
    

if __name__=='__main__':
    url="https://yunbi.com/api/v2/tickers.json"
    html=get_html(url)
    time_limit_max=1800//半小时
    time_limit=0
    while time_limit<=time_limit_max:
        data=get_data(html)
        bi=['btccny','ethcny','zeccny','qtumcny','gxscny','eoscny','anscny','sccny','dgdcny','1stcny','btscny','gntcny','repcny','etccny']
        for bi_type in bi:
            store_data(data[bi_type],bi_type)
            print(data[bi_type])
        time.sleep(5)
        time_limit=time_limit+5
    #print(data)
    #get_value(html)
