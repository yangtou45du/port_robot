# -*- coding:utf-8 -*-
import requests
import time


class performance(object):

    def __init__(self, ip, token):
        self.ip = ip
        self.token = token

    def performance_subtotal(self, system_id, targetIds, top=10, interval_time=60, pageIndex=0, startDate=0, endDate=0,
                             panelId='system'):
        """
        system_id: 应用系统Id
        targetIds: 节点组id
        top: 一页显示多少个
        interval_time: 间隔时间
        pageIndex: 页码
        startDate: 开始时间
        endDate: 结束时间，与开始时间均为0时，只计间隔时间，非0时才计算开始与结束时间
        panelId: 应用/交易

        """
        if (int(startDate) == 0) & (int(endDate) == 0):
            end_date = int(round(time.time() * 1000) - 2 * 60 * 1000)
            start_date = end_date - int(interval_time) * 1000 * 60
        else:
            start_date = startDate
            end_date = endDate
        url = 'http://{}/front/rest/apm/performances/subtotal'.format(self.ip)
        data = {
            'system_id': system_id,
            'type': 'service',
            'targetIds': targetIds,
            'panelId': panelId,
            'startDate': start_date,
            'endDate': end_date,
            'top': top,
            'pageIndex': pageIndex,
            'token': self.token
        }
        response = requests.get(url=url, params=data)
        content = response.json()
        if not content["result"]:
            return content["status"]
        else:
            if "APM" in response.content:
                return "pass"
            else:
                return "fail"

    def order_name(self, data, orderby, desc=True):
        """
        data: 列表，每个值都是字典
        orderby: 排序字段
        desc: True为降序，False为升序
        return: 返回排序是否正确

        """
        if desc:
            if (type(data[0][orderby]) == int) or (type(data[0][orderby]) == float):
                a = []
                for i in data:
                    a.append(i[orderby])
                b = sorted(a, reverse=True)
                if a == b:
                    return "pass"
                else:
                    return "order fail!"
            else:
                a = []
                for i in data:
                    a.append(i[orderby])

                for num in range(0, len(a) / 2):
                    if a[num] < a[len(a) / 2 + num]:
                        return "fail"

                return "pass"

        else:
            if (type(data[0][orderby]) == int) or (type(data[0][orderby]) == float):
                a = []
                for i in data:
                    a.append(i[orderby])
                b = sorted(a)
                if a == b:
                    return "pass"
                else:
                    return "order fail!"
            else:
                a = []
                for i in data:
                    a.append(i[orderby])

                for num in range(0, len(a) / 2):
                    if a[num] < a[len(a) / 2 + num]:
                        return "fail"

                return "pass"

    def performance_subtotal_order(self, system_id, targetIds, orderBy='ip_port', desc=True, interval_time=1440):
        """
        :type interval_time: int
        :param system_id: 应用系统
        :param targetIds: 节点组id
        :param orderBy: 排序字段
        :param desc: True为降序，False为升序
        :param interval_time: 间隔是时间
        :return: 返回排序是否正确

        """
        end_date = int(round(time.time() * 1000) - 2 * 60 * 1000)
        start_date = end_date - int(interval_time) * 1000 * 60
        url = 'http://{}/front/rest/apm/performances/subtotal'.format(self.ip)
        data = {
            'system_id': system_id,
            'type': 'service',
            'targetIds': targetIds,
            'panelId': 'system',
            'startDate': start_date,
            'endDate': end_date,
            'token': self.token,
            'orderBy': orderBy,
            'desc': desc
        }
        response = requests.get(url=url, params=data)
        content = response.json()
        status = self.order_name(content["result"], orderBy, desc)
        return status

    def performance(self, system_ids=None, system_id=None, applicationIds=None, agentIds=None, size=None, interval_time=60,
                    startDate=0, endDate=0, panelId='system'):
        """
        system_ids: 表示多个应用系统的id,也可为一个应用系统，字符型，逗号分割
        system_id: 表示单个应用系统，与agent或者applicationid连用
        applicationIds: 应用系统内的节点id，可为一个或者多个，字符型，逗号分割
        agentIds: agent或者apm的都有，表示名字，与应用系统id连用
        size: 粒度，现在只支持hour，回溯模式时用到，只显示应用系统的值
        interval_time: 间隔时间，默认是60分钟
        startDate: 开始时间，默认没有
        endDate: 结束时间，默认没有
        panelId: 应用系统或者交易系统，默认为应用系统

        """
        url = 'http://{}/front/rest/apm/performances'.format(self.ip)
        if (int(startDate) == 0) & (int(endDate) == 0):
            end_date = int(round(time.time() * 1000) - 2 * 60 * 1000)
            start_date = end_date - int(interval_time) * 1000 * 60
        else:
            start_date = startDate
            end_date = endDate

        if system_ids:
            if size:
                start_date = end_date - 1000 * 60 * 60 * 24 * 30
                data = {
                    'system_ids': system_ids,
                    'startDate': start_date,
                    'endDate': end_date,
                    'panelId': panelId,
                    'size': size,
                    'token': self.token
                }
                response = requests.get(url=url, params=data)
                if system_ids in response.content:
                    return "pass"
                else:
                    return "fail"
            else:
                data = {
                    'system_ids': system_ids,
                    'startDate': start_date,
                    'endDate': end_date,
                    'token': self.token
                }
                response = requests.get(url=url, params=data)
                content = response.json()
                sys_id = system_ids.split(',')
                for sys in sys_id:
                    if not content[sys]:
                        return "fail"
                return "pass"

        if system_id:
            if agentIds:
                data = {
                    'system_id': system_id,
                    'startDate': start_date,
                    'endDate': end_date,
                    'applicationIds': applicationIds,
                    'agentIds': agentIds,
                    'token': self.token
                }
                response = requests.get(url=url, params=data)
                if applicationIds in response.content:
                    return "pass"
                else:
                    return "fail"
            else:
                data = {
                    'system_id': system_id,
                    'startDate': start_date,
                    'endDate': end_date,
                    'applicationIds': applicationIds,
                    'panelId': panelId,
                    'token': self.token
                }
                response = requests.get(url=url, params=data)
                content = response.json()
                sys_id = applicationIds.split(',')
                for sys in sys_id:
                    if not content[sys]:
                        return "fail"
                return "pass"
        if size:
            start_date = end_date - 1000 * 60 * 60 * 24 * 30
            data = {
                'system_ids': system_ids,
                'startDate': start_date,
                'endDate': end_date,
                'panelId': panelId,
                'size': size,
                'token': self.token
            }
            response = requests.get(url=url, params=data)
            if system_ids in response.content:
                return "pass"
            else:
                return "fail"

    # def open_perf(self, system_name=u'接口测试专用（镜像数据），勿动！', system_id=None,
    #               service_id=None, ip=None, port=0, last=1, field=None):
    #     url = 'http://{}/front/rest/v1/apm/performances'.format(self.ip)
    #     data = {
    #         'system_name': system_name,
    #         'ip': ip,
    #         'port': port,
    #         'token': self.token,
    #         'system_id': system_id,
    #         'service_id': service_id,
    #         'field': field,
    #         'last': last
    #     }
    #     response = requests.get(url=url, params=data)
    #     content = response.json()
    #     if content['status'] == 'success' :
    #         if 



