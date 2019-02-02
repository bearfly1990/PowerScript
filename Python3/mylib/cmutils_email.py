#/usr/bin/python3
"""
author: xiche
create at: 08/15/2018
description:
    Utils for send email
Change log:
Date         Author      Version    Description
08/15/2018    xiche      1.0.1      Setup
"""
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.header import Header
class EmailUtils:
    __sender = "bearfly1990@163.com"
    __recipients = ["xiongchen1990@163.com", "xchen1230@163.com"]
    __subject = 'python email 尝试'
    __content = '<p>This is the test by <b>python</b>, please have a try.</p>' #<p>截图如下：</p><p><img src="cid:image1"></p>
    __mail_permission = 'xxxxxx'#授权码，非邮箱密码
    __mail_host = 'smtp.163.com'
    __mail_port = 25 #SSL 465
    __attachments_path = [r'C:\Users\mayn\Desktop\test.txt']
    __content_images_path = [{'cid':'image1', 'path': r'C:\Users\mayn\Desktop\ymj.jpg'}]

    def __init__(self):
        pass

    def send_email(self):
        msg = MIMEMultipart()

        # msg = MIMEText(self.content, 'plain', 'utf-8')
        msg['Subject'] =  Header(self.subject, 'utf-8')
        msg['From'] = self.sender
        msg['To'] = ','.join(self.recipients)

        content = MIMEText(self.__content,'html','utf-8')
        msg.attach(content)

        for content_image in self.__content_images_path:
            msgImage = MIMEImage(open(content_image['path'], 'rb').read())
            msgImage.add_header('Content-ID', '<{}>'.format(content_image['cid']))
            msg.attach(msgImage)

        for attachments_path in self.__attachments_path:
            attachment = MIMEText(open(attachments_path, 'rb').read(), 'base64', 'utf-8')
            attachment["Content-Type"] = 'application/octet-stream'
            attachment["Content-Disposition"] = 'attachment; filename="{}"'.format(os.path.basename(attachments_path))
            msg.attach(attachment)


        # smtp = smtplib.SMTP(self.__mail_host, port=self.__mail_port)
        try:
            smtp = smtplib.SMTP_SSL()  # 注意：如果遇到发送失败的情况（提示远程主机拒接连接），这里要使用SMTP_SSL方法
            smtp.connect(self.__mail_host)
            smtp.login(self.sender, self.__mail_permission)
            # print(msg.as_string())
            smtp.sendmail(self.sender, self.recipients, msg.as_string())
            print('email send successfully.')
        except smtplib.SMTPException as e:
            print(str(e))
        finally:
            smtp.quit()  # 发送完毕后退出smtp

    '''sender'''
    @property
    def sender(self):
        return self.__sender

    @sender.setter
    def sender(self, sender):
        self.__sender = sender
    '''subject'''
    @property
    def subject(self):
        return self.__subject

    @subject.setter
    def subject(self, subject):
        self.__subject = subject
    '''recipients'''
    @property
    def recipients(self):
        return self.__recipients

    @recipients.setter
    def recipients(self, recipients):
        if(isinstance(recipients, str)):
            self.__recipients = recipients.split(';')
        elif(isinstance(recipients, list)):
            self.__recipients = recipients
    '''sender'''
    @property
    def content(self):
        return self.__content

    @content.setter
    def content(self, content):
        self.__content = content

if __name__ == '__main__':
    emailUtils = EmailUtils()
    emailUtils.send_email()
    # print(os.path.basename(r'C:\Users\mayn\Desktop\ymj.jpg'))