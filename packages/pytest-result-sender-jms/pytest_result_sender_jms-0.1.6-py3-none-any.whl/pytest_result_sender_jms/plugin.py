# conftest.py
from datetime import datetime
from email.header import Header
from email.mime.text import MIMEText
import smtplib

import pytest
import requests

data = {'passed': 0, 'failed': 0}


def pytest_addoption(parser):
    # api配置（如微信机器人，qq群机器人等）
    parser.addini('send_when', type='string', help="何时发送")
    parser.addini('send_api', type="string", help="发送到哪里")

    # 邮箱配置项名称保持与配置文件中一致
    parser.addini('smtp_server', type='string', help='SMTP服务器地址', default='smtp.163.com')
    parser.addini('smtp_port', help='SMTP端口', type="string", default="465")
    parser.addini('email_user', type='string', help='发件人邮箱')
    parser.addini('email_password', type='string', help='邮箱授权码')
    parser.addini('receiver_emails', type='string', help='收件人邮箱')


def pytest_runtest_logreport(report: pytest.TestReport):
    # 统计测试通过的数量
    if report.when == 'call':
        data[report.outcome] += 1


def pytest_collection_finish(session: pytest.Session):
    # 统计测试用例总数
    data['total'] = len(session.items)
    print(f"需要执行的测试用例数量{data['total']}")


def pytest_configure(config: pytest.Config):
    # 测试开始执行
    data['start_test'] = datetime.now()
    print(f"测试开始执行{datetime.now()}")



def pytest_unconfigure(config):
    print(f"测试结束{datetime.now()}")
    data['end_test'] = datetime.now()
    data['time_stamp'] = data['end_test'] - data['start_test']
    if data and data['total'] > 0:  # 添加保护条件
        data['passing_rate'] = f"{data['passed'] / data['total'] * 100:.2f}%"
    else:
        data['passing_rate'] = "0.00%"

    # 根据配置决定是否发送
    if config.getini('send_when') == 'on_fail' and data['failed'] == 0:
        return
    if not config.getini('send_api'):
        return
    send_email(config)
    send_result(config)


def send_email(config: pytest.Config):
    """发送邮件通知（修正了配置项名称）"""
    smtp_server = config.getini("smtp_server")
    smtp_port = int(config.getini("smtp_port"))
    username = config.getini("email_user")  # 使用正确的配置项名称
    password = config.getini("email_password")  # 使用正确的配置项名称
    email_to = config.getini("receiver_emails")

    # 构建邮件内容
    html_content = f"""
    <html>
      <body>
        <h2>自动化测试报告</h2>
        <table border="1" cellpadding="5">
          <tr><th>项目</th><th>结果</th></tr>
          <tr><td>测试时间</td><td>{data['end_test']}</td></tr>
          <tr><td>总用例数</td><td>{data['total']}</td></tr>
          <tr><td>通过数</td><td style="color:green">{data['passed']}</td></tr>
          <tr><td>失败数</td><td style="color:red">{data['failed']}</td></tr>
          <tr><td>执行时长</td><td>{data['time_stamp']}</td></tr>
          <tr><td>通过率</td><td>{data['passing_rate']}</td></tr>
        </table>
      </body>
    </html>
    """

    # 创建邮件对象
    msg = MIMEText(html_content, "html", "utf-8")
    msg["From"] = username  # 使用配置中的email_user
    msg["To"] = email_to
    msg["Subject"] = Header("自动化测试报告", "utf-8")  # 固定主题

    # 使用SSL连接（端口465）
    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(username, password)
            server.sendmail(username, email_to.split(","), msg.as_string())  # 拆分多个收件人
            print("邮件发送成功")
            data['email_done'] = 1
    except Exception as e:
        print(f"邮件发送失败: {str(e)}")


def send_result(config):
    """ "Api发送信息通知"""
    if not config.getini('send_api'):
        return

    content = f"""
    python自动化测试结果

    测试时间：{data['end_test']}
    用例数量：{data['total']}
    执行时长：{data['time_stamp']}
    测试通过：<font color='green'>{data['passed']}</font>
    测试失败：<font color='red'>{data['failed']}</font>
    测试通过率：{data['passing_rate']}
    """

    try:
        requests.post(config.getini('send_api'), json={"msgtype": "markdown", "markdown": {"content": content}})
        print("API结果发送成功")
        data['api_done'] = 1
    except Exception as e:
        print(f"API发送失败: {str(e)}")
