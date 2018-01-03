# _*_ coding:utf8 _*_
import requests
import random
import time
import json

class alarm(object):
    def __init__(self, ip, token):
        self.ip = ip
        self.token = token

    def alarms_list(self, system_id, targetId, panelId="system", whole=False):
        """
        system_id: 应用系统id
        targetId: 目标节点id
        panelId: 应用或交易
        hole: 默认为假，为真时返回告警列表

        """
        url = 'http://{}/front/rest/apm/alarms/{}/{}/{}/thresholds'.format(self.ip, system_id, targetId[-8:], panelId)
        data = {
            "token": self.token
        }
        response = requests.get(url=url, params=data)
        content = response.json()
        if whole:
            return content["result"]
        else:
            if content["status"] == "success":
                return "pass"
            else:
                return "fail"


    def alarms_overview(self, system_id, panelId='system', whole=False):
        """
        system_id: 应用系统id
        panelId: 应用或交易
        hole: 默认为假，为真时返回整个应用的告警列表

        """
        url = 'http://{}/front/rest/apm/alarms/{}/thresholds/{}'.format(self.ip, system_id, panelId)
        data = {
            "token": self.token
        }
        response = requests.get(url=url, params=data)
        content = response.json()
        if whole:
            return content["result"]
        else:
            if content["status"] == "success":
                return "pass"
            else:
                return "fail"


    def alarms_append(self, system_id, targetId, indicator, serious, warning, caution, operator, times, thresholdType='threshold',
                    panelId='system'):
        """
        system_id: 应用系统id
        targetId: 应用系统内节点的id
        indicator: 告警项，error表示错误数，rpm表示吞吐量，rtt表示响应时间
        serious: 严重
        warning: 警告
        caution: 提醒
        operator: > < 表示大于 小于
        times: 时间长度，字符型，单位为分钟
        thresholdType: threshold为阈值告警
        panelId: 应用或者交易

        """
        url = 'http://{}/front/rest/apm/alarms/{}/{}/thresholds'.format(self.ip, system_id, panelId)
        headers = {
            'content-type': 'application/json'
        }
        params = {
            "token": self.token
        }
        data = {
            "targetId": targetId[-8:],
            "thresholdType": thresholdType,
            "thresholdParam": [
                {
                    "indicator": indicator,
                    "operator": operator,
                    "times": times,
                    "level": {
                        "50": serious,
                        "20": warning,
                        "10": caution
                    }
                }
            ]
        }
        response = requests.post(
            url=url,
            json=data,
            headers=headers,
            params=params
            )
        alarms = self.alarms_list(
            system_id=system_id,
            targetId=targetId[-8:],
            whole=True
            )
        if response.json()["status"] == "success":
            if (serious in json.dumps(alarms))and(operator in json.dumps(alarms)):
                return "pass"
            else:
                return "fail"
        else:
            return "fail"


    def alarms_append5(self, system_id, targetId, panelId='system'):
        """
        system_id: 应用系统id
        targetId: 目标节点id
        panelId: 应用或交易

        """
        url = 'http://{}/front/rest/apm/alarms/{}/{}/thresholds'.format(self.ip, system_id, panelId)
        headers = {
            'content-type': 'application/json'
        }
        params = {
            "token": self.token
        }
        data = {
            "targetId": targetId[-8:],
            "thresholdType": 'threshold',
            "thresholdParam": [
                {
                    "indicator": 'rpm',
                    "operator": '>',
                    "times": '1',
                    "level": {
                        "50": '60',
                        "20": '50',
                        "10": '40'
                    }
                },
                {
                    "indicator": 'rpm',
                    "operator": '<',
                    "times": '3',
                    "level": {
                        "50": '10',
                        "20": '20',
                        "10": '30'
                    }
                },
                {
                    "indicator": 'error',
                    "operator": '>',
                    "times": '5',
                    "level": {
                        "50": '6',
                        "20": '5',
                        "10": '4'
                    }
                },
                {
                    "indicator": 'rtt',
                    "operator": '>',
                    "times": '2',
                    "level": {
                        "50": '6',
                        "20": '5',
                        "10": '4'
                    }
                },
                {
                    "indicator": 'rtt',
                    "operator": '<',
                    "times": '3',
                    "level": {
                        "50": '1',
                        "20": '2',
                        "10": '3'
                    }
                }
            ]
        }
        response = requests.post(
            url=url,
            json=data,
            headers=headers,
            params=params
            )
        alarms = self.alarms_list(
            system_id=system_id,
            targetId=targetId[-8:],
            whole=True
            )
        if response.json()["status"] == "success":
            if len(alarms["thresholdParam"]) == 5:
                return "pass"
            else:
                return "fail"
        else:
            return "fail"


    def alarms_append_alg(self, system_id, targetId, panelId='system'):
        """
        基线告警专用
        system_id: 应用系统id
        targetId: 目标节点id
        panelId: 应用或交易

        """
        url = 'http://{}/front/rest/apm/alarms/{}/{}/thresholds'.format(self.ip, system_id, panelId)
        headers = {
            'content-type': 'application/json'
        }
        params = {
            "token": self.token
        }
        data = {
            "panelId": panelId,
            "status": "on",
            "targetId": targetId[-8:],
            "thresholdParam": [],
            "thresholdType": "algorithm"
        }
        response = requests.post(
            url=url, json=data, params=params, headers=headers)
        alarms = self.alarms_list(
            system_id=system_id,
            targetId=targetId[-8:],
            whole=True
            )
        if response.json()["status"] == "success":
            if "algorithm" in json.dumps(alarms):
                return "pass"
            else:
                return "alg append fail"
        else:
            return "alg append fail"


    def alarms_change(self, system_id, targetId, indicator, serious, warning, caution, operator, times, panelId='system'):
        """
        system_id: 应用系统id
        targetId: 应用系统内节点的id
        indicator: 告警项，error表示错误数，rpm表示吞吐量，rtt表示响应时间
        serious: 严重
        warning: 警告
        caution: 提醒
        operator: > < 表示大于 小于
        times: 时间长度，字符型，单位为分钟
        panelId: 应用或者交易

        """
        url = 'http://{}/front/rest/apm/alarms/{}/thresholds/{}'.format(self.ip, system_id, panelId)
        headers = {
            'content-type': 'application/json'
        }
        params = {
            "token": self.token
        }
        data = {
            "targetId": targetId[-8:],
            "thresholdType": 'threshold',
            "thresholdParam": [
                {
                    "indicator": indicator,
                    "operator": operator,
                    "times": times,
                    "level": {
                        "50": serious,
                        "20": warning,
                        "10": caution
                    }
                }
            ]
        }
        response = requests.put(url=url, json=data, params=params, headers=headers)
        alarms = self.alarms_list(
            system_id=system_id,
            targetId=targetId[-8:],
            whole=True
            )
        if response.json()["status"] == "success":
            if (serious in json.dumps(alarms))and(operator in json.dumps(alarms)):
                return "pass"
            else:
                return "fail"
        else:
            return "fail"


    def alarms_change_alg(self, system_id, targetId, panelId='system'):
        """
        基线告警专用
        system_id: 应用系统id
        targetId: 目标节点id
        panelId: 应用或交易

        """
        url = 'http://{}/front/rest/apm/alarms/{}/thresholds/{}'.format(self.ip, system_id, panelId) 
        headers = {
            'content-type': 'application/json'
        }
        params = {
            "token": self.token
        }
        data = {
            "panelId": panelId,
            "status": "on",
            "targetId": targetId[-8:],
            "thresholdParam": [],
            "thresholdType": "algorithm"
        }
        response = requests.put(url=url, json=data, params=params, headers=headers)
        alarms = self.alarms_list(
            system_id=system_id,
            targetId=targetId[-8:],
            whole=True
            )
        if response.json()["status"] == "success":
            if "algorithm" in json.dumps(alarms):
                return "pass"
            else:
                return "alg append fail"
        else:
            return "alg append fail"


    def alarms_delete(self, system_id, targetId, thresholdType, panelId='system'):
        """
        system_id: 应用系统id
        targetId: 目标节点id
        panelId: 应用或交易
        thresholdType: 基线告警或阈值告警

        """
        url = 'http://{}/front/rest/apm/alarms/{}/thresholds/{}/{}/{}'.format(self.ip, system_id, targetId[-8:], panelId, thresholdType)
        params = {
            "token": self.token
        }
        response = requests.delete(
            url=url,
            params=params
            )
        alarms = self.alarms_overview(
            system_id=system_id,
            whole=True
            )
        if response.json()["status"] == "success":
            if targetId[-8:] in json.dumps(alarms):
                return "fail"
            else:
                return "pass"
        else:
            return "fail"
