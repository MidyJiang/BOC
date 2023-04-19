import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os
import time

# 函数: 发送邮件
def send_email(to_email):
    # 配置邮件参数    
    sender_email = '782568799@qq.com'
    sender_password =os.environ["COOKIE1"]# 'your_sender_password'
    subject = 'CSV File'
    text = 'Attached please find the CSV file.'

    # 添加附件
    directory = '/github/workspace'
    filename = 'exchange_rate.csv'
    filepath = os.path.join(directory, filename)
    with open(filepath, 'rb') as f:
        attachment = MIMEApplication(f.read(), _subtype='csv')
        attachment.add_header('Content-Disposition', 'attachment', filename=filename)

    # 创建邮件内容
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = to_email
    message['Subject'] = subject
    message.attach(MIMEText(text))
    message.attach(attachment)

    # 发送邮件
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to_email, message.as_string())
        server.quit()
        print('Email sent')
    except Exception as e:
        print('Error:', e)

# 主程序
while True:
    # 记录时间并写入 CSV 文件中
    current_time = time.strftime('%Y-%m-%d %H:%M:%S')
    with open('/github/workspace/exchange_rate.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([current_time])

    # 每小时发送一次邮件
    if time.localtime().tm_min % 5 == 0  :
        send_email('your_recipient_email@example.com')

    # 等待 15 秒钟继续循环
    time.sleep(5)
