import smtplib
from email.mime.text import MIMEText

from 数据库.日志.log表 import 记录日志
from 用户.邮箱.smtp配置 import smtp配置

def SMTP(收件人, 邮件内容, 邮件主题, IP):
    smtp = None # 初始化 smtp 为 None
    try:
        port = int(smtp配置.SMTP端口)
        # 根据端口号选择连接方式
        if port == 465:
            # 使用 SSL 加密连接
            smtp = smtplib.SMTP_SSL(smtp配置.SMTP服务器, port)
        else:
            # 假设其他端口使用 STARTTLS
            smtp = smtplib.SMTP(smtp配置.SMTP服务器, port)
            smtp.ehlo() # 可选，建议添加
            smtp.starttls()
            smtp.ehlo() # 可选，建议在 starttls 后再次添加

        # 登录
        smtp.login(smtp配置.SMTP用户, smtp配置.SMTP_token)

        # 构造邮件内容并指定编码
        msg = MIMEText(邮件内容, 'plain', 'utf-8')
        msg['From'] = smtp配置.SMTP用户
        msg['To'] = 收件人
        msg['Subject'] = 邮件主题  # 可以自定义邮件主题
        smtp.send_message(msg)
        记录日志(f"向{收件人}发送邮件成功", IP, f"游客")

    except smtplib.SMTPException as e:
        print(f"SMTP服务器异常: {e}")
        记录日志(f"向{收件人}发送邮件失败 (SMTP Error: {e})", IP, f"游客")
    except Exception as e:
        print(f"其他异常: {e}")
        记录日志(f"向{收件人}发送邮件失败 (General Error: {e})", IP, f"游客")
    finally:
        # 确保无论成功或失败都尝试关闭连接
        if smtp:
            try:
                smtp.quit()
            except Exception as quit_e:
                print(f"关闭SMTP连接时发生异常: {quit_e}")
