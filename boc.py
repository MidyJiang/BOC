import time,random
import requests,os,datetime,pytz
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs

url=r'https://www.boc.cn/sourcedb/whpj/'
################################################################
import smtplib 
from smtplib import SMTP_SSL
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage




freq=3#30分钟发一次邮件汇报
limit=105000780#最大300条数据，停止，发送邮件汇报
mailflag=True
receive_list=['782568799@qq.com']




plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号 #有中文出现的情况，需要u'内容'



######################################################
# myfont= matplotlib.font_manager.FontProperties("/kaggle/input/simplechinesefont/STKAITI.TTF")
########################################################


def sendmail(receive_mail,title=None):
    send_usr = '782568799@qq.com'  # 发件人
    send_pwd ='pdnfrwfijoewbeff'#'BUQRRQFPUANBCWMY' # 授权码，邮箱设置
    receive = receive_mail#'782568799@qq.com'  # 接收者
    content = '发送于{}<p><a href="{}">GBPCNY-中国银行现价动态,from github</a></p>'.format(
        str(datetime.datetime.now(pytz.timezone('Asia/Chongqing'))).replace(":",".")[:16],url)
    #content 内容设置
    html_img = f'<p>{content}<br><img src="cid:image1"></br></p>' # html格式添加图片
    email_server = 'smtp.qq.com'


    msg = MIMEMultipart() # 构建主体
    msg['Subject'] = Header(title,'utf8')  # 邮件主题
    msg['From'] = send_usr  # 发件人
    msg['To'] = Header('midynow','utf8') # 收件人--这里是昵称
    
    # msg.attach(MIMEText(content,'html','utf-8'))  # 构建邮件正文,不能多次构造
    attchment = MIMEApplication(open(r'/kaggle/working/{}.png'.format(sendtime),'rb').read()) # 文件
    attchment.add_header('Content-Disposition','attachment',filename=r'/kaggle/working/{}.png'.format(sendtime))
    msg.attach(attchment)  # 添加附件到邮件
    attchment2 = MIMEApplication(open(r'/kaggle/working/{}.csv'.format(sendtime),'rb').read()) # 文件
    attchment2.add_header('Content-Disposition','attachment',filename=r'/kaggle/working/{}.csv'.format(sendtime))
    msg.attach(attchment2)  # 添加附件到邮件
    
    f = open(r'/kaggle/working/{}.png'.format(sendtime), 'rb')  #打开图片
    msgimage = MIMEImage(f.read())
    f.close()
    msgimage.add_header('Content-ID', '<image1>')  # 设置图片
    msg.attach(msgimage)
    msg.attach(MIMEText(html_img,'html','utf-8'))  # 添加到邮件正文
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
    
    
    
count=0
timelist=[]

while True:
    count+=1
    try:
        time.sleep(4)
        r = urlopen(url)
        c = r.read()
        bs_obj = bs(c,"html")
        t = bs_obj.find_all("table")[1]
        all_tr = t.find_all("tr")
        all_tr.pop(0) 
        for r in all_tr:
            all_td = r.find_all("td")
            if all_td[0].text in ("英镑"):
                price=float(all_td[3].text)
                try:
                    if len(df)>0:pass;
                except Exception as NE:
                    print(NE,'新建df.'.encode('utf-8'))    
                    df=pd.DataFrame(dict(zip([i.text for i in t.find_all('th')],[i.text for i in all_td])),index=['test'])
                if all_td[-2].text not in df['发布日期'].values:
                    df=pd.concat([df,pd.DataFrame(dict(zip([i.text for i in t.find_all('th')],[i.text for i in all_td])),index=['test'])])
                    
                print( all_td[-2].text.encode('utf-8') ,'len=',len(df),end='\t')               

        print(str(datetime.datetime.now(pytz.timezone('Asia/Chongqing'))).replace(":",".")[14:16],end='分.'.encode('utf-8'))
        
    except TypeError as E:
        print(134,E)
        pass;
    df=df.drop_duplicates(['发布日期'])

    if int(str(datetime.datetime.now(pytz.timezone('Asia/Chongqing'))).replace(":",".")[:16][14:16])%freq==1 and not mailflag:mailflag=True
    if int(str(datetime.datetime.now(pytz.timezone('Asia/Chongqing'))).replace(":",".")[:16][14:16])%freq==0 and mailflag:
        plt.close()
        print("\n\nfreq达到，程序继续，发送邮件记录。".encode('utf-8'))
        df=df.drop_duplicates(['发布日期'])
        df['发布日期']=pd.to_datetime(df['发布日期'])
        df1=df.sort_values(by=['发布日期'],ascending=[True])#按值，降序排列
        
        df1=df.set_index(['发布日期'])
        df1.index=pd.to_datetime(df1.index)
        pd.to_numeric(df1['现汇卖出价']).plot()
        plt.scatter(df1[df1['现汇卖出价']==df1['现汇卖出价'].min()]['现汇卖出价'].index[0],
                    pd.to_numeric(df1[df1['现汇卖出价']==df1['现汇卖出价'].min()]['现汇卖出价'].values[0]),
                   color='r',marker='p')
        print(df1[df1['现汇卖出价']==df1['现汇卖出价'].min()]['现汇卖出价'].index[0],pd.to_numeric(df1[df1['现汇卖出价']==df1['现汇卖出价'].min()]['现汇卖出价'].values[0]))
        plt.xticks(rotation=30)
        plt.text(df1[df1['现汇卖出价']==df1['现汇卖出价'].min()]['现汇卖出价'].index[0],
                    pd.to_numeric(df1[df1['现汇卖出价']==df1['现汇卖出价'].min()]['现汇卖出价'].values[0])*.99985, 
                 '{}最低点{}'.format(pd.to_numeric(df1[df1['现汇卖出价']==df1['现汇卖出价'].min()]['现汇卖出价'].values[0]),df1[df1['现汇卖出价']==df1['现汇卖出价'].min()]['现汇卖出价'].index[0]), 
                 color='r',ha='center')
        plt.grid()
        plt.title('Trend_GBP')#,fontproperties=myfont)
        sendtime=str(datetime.datetime.now(pytz.timezone('Asia/Chongqing'))).replace(":",".")[:16]
        plt.savefig(r'{}.png'.format(sendtime))    
        df.to_csv(r'{}.csv'.format(sendtime))
        try:
            for receive_mail in receive_list:
                sendmail(receive_mail,"《Github中行{}min_{}》".format(freq,price)+str(datetime.datetime.now(pytz.timezone('Asia/Chongqing'))).replace(":",".")[:16])
        except Exception as E:
            print(E)
        continue;  
        
    elif len(df)>limit:
        print("\n\nlimit超限，程序停止。发送邮件。".encode('utf-8'))
        df=df.drop_duplicates(['发布日期'])
        df['发布日期']=pd.to_datetime(df['发布日期'])
        df1=df.sort_values(by=['发布日期'],ascending=[True])#按值，降序排列
        
        df1=df.set_index(['发布日期'])
        df1.index=pd.to_datetime(df1.index)
        pd.to_numeric(df1['现汇卖出价']).plot()
        plt.scatter(df1[df1['现汇卖出价']==df1['现汇卖出价'].min()]['现汇卖出价'].index[0],
                    pd.to_numeric(df1[df1['现汇卖出价']==df1['现汇卖出价'].min()]['现汇卖出价'].values[0]),
                   color='r',marker='p')
        print(df1[df1['现汇卖出价']==df1['现汇卖出价'].min()]['现汇卖出价'].index[0],pd.to_numeric(df1[df1['现汇卖出价']==df1['现汇卖出价'].min()]['现汇卖出价'].values[0]))
        plt.xticks(rotation=30)
        plt.text(df1[df1['现汇卖出价']==df1['现汇卖出价'].min()]['现汇卖出价'].index[0],
                    pd.to_numeric(df1[df1['现汇卖出价']==df1['现汇卖出价'].min()]['现汇卖出价'].values[0])*.99985, 
                 '{}u最低点{}'.format(pd.to_numeric(df1[df1['现汇卖出价']==df1['现汇卖出价'].min()]['现汇卖出价'].values[0]),df1[df1['现汇卖出价']==df1['现汇卖出价'].min()]['现汇卖出价'].index[0]),
                color='r',ha='center')
        plt.grid()
        plt.title('Trend_GBP')#,fontproperties=myfont)
        sendtime=str(datetime.datetime.now(pytz.timezone('Asia/Chongqing'))).replace(":",".")[:16]
        plt.savefig(r'{}.png'.format(sendtime))    
        df.to_csv(r'{}.csv'.format(sendtime))
        try:
            for receive_mail in receive_list:
                sendmail(receive_mail,"《Github中行{}min_{}》".format(freq,price)+str(datetime.datetime.now(pytz.timezone('Asia/Chongqing'))).replace(":",".")[:16])
        except:pass;
        
        break;
    else:continue;
