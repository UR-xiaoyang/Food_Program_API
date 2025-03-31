import smtplib
from email.mime.text import MIMEText

from 数据库.日志.log表 import 记录日志
from 用户.邮箱.smtp配置 import smtp配置

def SMTP(收件人, 邮件内容, 邮件主题, IP):
    try:
        # 创建连接
        smtp = smtplib.SMTP_SSL(smtp配置.SMTP服务器, smtp配置.SMTP端口)

        # 登录
        smtp.login(smtp配置.SMTP用户, smtp配置.SMTP_token)

        # 构造邮件内容并指定编码
        msg = MIMEText(邮件内容, 'plain', 'utf-8')
        msg['From'] = smtp配置.SMTP用户
        msg['To'] = 收件人
        msg['Subject'] = 邮件主题  # 可以自定义邮件主题
        smtp.send_message(msg)
        if smtp and smtp.sock:  # 使用sock属性检查连接状态
            smtp.quit()
            记录日志(f"向{收件人}发送邮件成功", IP, f"游客")
        else:
            记录日志(f"向{收件人}发送邮件失败", IP, f"游客")
            print("SMTP连接已关闭或未成功建立，无需再次关闭")
    except smtplib.SMTPException as e:
        print(f"SMTP服务器异常: {e}")
    except Exception as e:
        print(f"其他异常: {e}")
