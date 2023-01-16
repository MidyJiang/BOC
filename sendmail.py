import time,random
import requests,os,datetime,pytz
import pandas as pd
import smtplib 
import matplotlib
import matplotlib.pyplot as plt
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

url=r'https://www.boc.cn/sourcedb/whpj/'
################################################################

from smtplib import SMTP_SSL
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage

df=pd.DataFrame({"time":time.ctime(),"zone":"GMT","currency":"GBP英镑"},index=['test'])
df.to_csv('df.csv',encoding=os.environ["ENCODE"])


def sendmail(receive_mail,title=None):
    sendtime=str(datetime.datetime.now(pytz.timezone('Asia/Chongqing'))).replace(":",".")[:16]
    send_usr = '782568799@qq.com'  # 发件人
    send_pwd ='pdnfrwfijoewbeff'#'BUQRRQFPUANBCWMY' # 授权码，邮箱设置
    receive = receive_mail#'782568799@qq.com'  # 接收者

    content = '发送于{}<p><a href="{}">GBPCNY-中国银行现价动态,from github</a></p>\n\ncookie={},freq={},encode={},url={}.'.format(
        str(datetime.datetime.now(pytz.timezone('Asia/Chongqing'))).replace(":",".")[:16],url,os.environ["COOKIE1"],
        os.environ["FREQ"],os.environ["ENCODE"],os.environ["URL"])
    #content 内容设置
    html_img = f'<p>{content}<br><img src="cid:image1"></br></p>' # html格式添加图片
    email_server = 'smtp.qq.com'


    msg = MIMEMultipart() # 构建主体
    msg['Subject'] = Header(title,'utf8')  # 邮件主题
    msg['From'] = send_usr  # 发件人
    msg['To'] = Header('midynow','utf8') # 收件人--这里是昵称
    
#     msg.attach(MIMEText(content,'html','utf-8'))  # 构建邮件正文,不能多次构造
    attchment = MIMEApplication(open(r'df.csv','rb').read()) # 文件
    attchment.add_header('Content-Disposition','attachment',filename=r'df.csv')
    msg.attach(attchment)  # 添加附件到邮件
#     attchment2 = MIMEApplication(open(r'/kaggle/working/{}.csv'.format(sendtime),'rb').read()) # 文件
#     attchment2.add_header('Content-Disposition','attachment',filename=r'/kaggle/working/{}.csv'.format(sendtime))
#     msg.attach(attchment2)  # 添加附件到邮件
    
#     f = open(r'/kaggle/working/{}.png'.format(sendtime), 'rb')  #打开图片
#     msgimage = MIMEImage(f.read())
#     f.close()
#     msgimage.add_header('Content-ID', '<image1>')  # 设置图片
#     msg.attach(msgimage)
#     msg.attach(MIMEText(html_img,'html','utf-8'))  # 添加到邮件正文
    
    try:
       
        smtp = SMTP_SSL(email_server)  #指定邮箱服务器
        smtp.ehlo(email_server)   # 部分邮箱需要
        smtp.login(send_usr,send_pwd)  # 登录邮箱
        smtp.sendmail(send_usr,receive,msg.as_string())  # 分别是发件人、收件人、格式
        smtp.quit()  # 结束服务
        print(receive_mail,'邮件发送成功,mailflag已经改成False!'.encode('utf-8'),str(datetime.datetime.now(pytz.timezone('Asia/Chongqing'))).replace(":",".")[:16])
        global mailflag
        mailflag=False
    except Exception as E:
        print('发送失败'.encode('utf-8'),E)
        return 'sent'
    
sendmail("782568799@qq.com",title='GithubTry'+time.ctime())
