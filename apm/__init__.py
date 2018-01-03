# _*_ coding:utf8 _*_
from apm.applications import applications
from apm.performance import performance
from apm.request_list import requests_list
from apm.alarm import alarm
import requests

def get_token(ip='10.1.51.103'):
    """
    获取token值

    """
    headers = {
        'content-type': 'application/json'
    }
    url = 'http://{}/front/rest/apm/authentication/login?token='.format(ip)
    data = {
        'account': 'admin',
        'password': 'admin'
        }
    response = requests.post(url, json=data, headers=headers)
    content = response.json()
    return content['meta']['token']

class apm(applications, performance, requests_list, alarm):
    def __init__(self, ip='10.1.51.103', agent_id="JAVA:127.0.0.1_test"):
        self.ip = ip
        self.token = get_token(self.ip)
        self.agent_id = agent_id
    
    def change(self, ip, token, agent_id):
        self.ip = ip
        self.token = token
        self.agent_id = agent_id
