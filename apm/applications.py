# -*- coding:utf-8 -*-
import time
import requests
import random

class applications(object):

    def __init__(self, ip, token):
        self.ip = ip
        self.token = token


    def applications(self, num, params, whole=0):
        """
        num: 表示第几个应用
        params: 想要看什么参数，id或者name，字符型
        whole: 非0时显示所有参数
        return: 返回应用相关信息，字典

        """
        applications_url = 'http://{}/front/rest/apm/applications'.format(self.ip)
        applications_params = {
            "token": self.token
            }
        applications_rawdata = requests.get(
            url=applications_url,
            params=applications_params
            )
        applications_content = applications_rawdata.json()
        if whole == 0:
            return applications_content['applications'][int(num)][params]
        else:
            return applications_content['applications']

    def applications_sys(self, system_id, panelId='system', topo=False):
        """
        system_id: 应用系统id
        topo: 为真时，返回是否为标签节点，默认为假
        panelId: 应用或系统，默认为应用

        """
        url = 'http://{}/front/rest/apm/applications/{}'.format(self.ip, system_id)
        data = {
            "panelId": panelId,
            "token": self.token
        }
        response = requests.get(url=url, params=data)
        content = response.json()
        if topo:
            for ids in content["application"]["topoNodes"]:
                if ids["nodeType"] == 4:
                    return True
            return False
        else:
            if system_id in response.content:
                return "pass"
            else:
                return "fail"

    def applications_no(self, system_id, panelId='system'):
        """
        system_id: 应用系统id
        panelId: 应用或系统，默认为应用
        函数返回真时，表示应用内没有节点

        """
        url = 'http://{}/front/rest/apm/applications/{}'.format(self.ip, system_id)
        data = {
            "panelId": panelId,
            "token": self.token
        }
        response = requests.get(
            url=url,
            params=data
            )
        content = response.json()
        if not content["application"]["topoNodes"]:
            return True
        else:
            return False


    def application_append(self, name):
        """
        输入想要添加的应用的名称

        """
        application_append_url = 'http://{}/front/rest/apm/applications'.format(self.ip)
        application_append_data = {
            "name": name
        }
        application_append_params = {
            "token": self.token
        }
        headers = {
            'content-type': 'application/json'
        }
        requests.post(
            url=application_append_url,
            json=application_append_data,
            params=application_append_params,
            headers=headers
            )
        self.applications(-1, 'name')

        if self.applications(-1, 'name') == name:
            if name == '':
                self.application_delete('')
                return 'name can not be empty!!'
            else:
                return 'pass'

        else:
            return 'append fail'


    def application_name_id(self, name):
        """
        输入应用的名称，返回应用id，字符型

        """
        apps = self.applications(1, 1, 1)
        for l in apps:
            if name == l['name']:
                return l['id']


    def application_delete(self, name):
        """
        name: 输入需要删除的应用的名字就好，字符型

        """
        delete_id = self.application_name_id(name)
        application_delete_url = 'http://{}/front/rest/apm/applications/{}'.format(self.ip, str(delete_id))
        application_delete_params = {
            "token": self.token
        }
        requests.delete(application_delete_url, params=application_delete_params)

        if name in self.applications(1, 1, 1):
            return "delete fail"
        else:
            return 'pass'


    def applications_inoverview(self, true_false):
        """
        boolen: True表示已显示的所用交易系统；False表示所有交易系统

        """
        applications_inoverview_url = 'http://{}/front/rest/apm/applications/'.format(self.ip)
        end_date = int(round(time.time() * 1000) - 2 * 60 * 1000)
        start_date = end_date - 1000 * 3600 * 24
        applications_inoverview_data = {
            'inOverview': true_false,
            'start_date': start_date,
            'end_date': end_date,
            'token': self.token
        }
        applications_inoverview_rawdata = requests.get(
            url=applications_inoverview_url, params=applications_inoverview_data)
        if '接口测试专用' in applications_inoverview_rawdata.content:
            return 'pass'
        else:
            return 'search fail !!'

    def list_string(self, tostring):
        """
        将列表拼接成字符串

        """
        strings = u''
        for i in tostring:
            strings = strings + i
        return strings

    def abnormal_input(self, num, space=False, language='chinese', specialword=True, front=False):
        """
        num: 表示最多可以输入多少个字符；
        space: 是否可以输入空；
        language: 表示语言，可选'chinese' 'english'，默认为'chinese'；
        specialword: 是否可以输入特殊字符；
        return: 返回一个列表，包含提供的异常值；

        """
        abnormal_list = []
        chinese = u'灮灱灲灳灴灷灸灹灺灻灼炀炁炂炃炄炅炆炇炈炋炌炍炏炐炑炓炔炕炖炗炘炙炚炛炜炝炞炟炠炡炢炣炤炥炦炧炨炩炪炫炯'
        special = '~!@#$%^&*()_+=-<>:";[]{}? \|/`\'~!@#$%^&*()_+=-<>:";[]{}? \|/`\''
        english = 'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzxxyy'
        mix = self.list_string(random.sample(chinese, int(num) / 3)) + self.list_string(
            random.sample(special, int(num) / 3)) + self.list_string(random.sample(english, int(num) / 3))
        if space:
            abnormal_list.append('')

        if language == 'chinese':
            append = self.list_string(random.sample(chinese, int(num)))
            abnormal_list.append(append)

        if language == 'english':
            append = self.list_string(random.sample(english, int(num)))
            abnormal_list.append(append)

        if specialword:
            append = self.list_string(random.sample(special, int(num)))
            abnormal_list.append(append)
            abnormal_list.append('null')
            abnormal_list.append('NaN')

        if front:
            for one in special[0:30]:
                abnormal_list.append(one)

        if int(num) > 3:
            abnormal_list.append(mix)

        return abnormal_list

    def applications_protos(self, system_id, allapps=False):
        """
        system_id: 应用系统id
        allapps: 为真时，检查所有应用系统，默认为假

        """
        if allapps:
            for ids in self.applications(1, 1, 1):
                data = {
                    'system_id': ids["id"],
                    'token': self.token
                }
                url = 'http://{}/front/rest/apm/applications/{}/protos'.format(self.ip, ids["id"])
                response = requests.get(url=url, params=data)
                content = response.json()
                if not content["protos"]:
                    if not self.applications_sys(system_id=ids["id"], topo=True):
                        if not self.applications_no(system_id=ids['id']):
                            return "fail"
                    else:
                        pass
            return "pass"

        else:
            url = 'http://{}/front/rest/apm/applications/{}/protos'.format(self.ip, str(system_id))
            data = {
                'system_id': system_id,
                'token': self.token
            }
            response = requests.get(url=url, params=data)
            content = response.json()
            if not content["protos"]:
                if not self.applications_sys(system_id=system_id, topo=True):
                    if not self.applications_no(system_id=ids['id']):
                        return "fail"
                else:
                    pass
            return "pass"


    def applications_ips(self, system_id, allapps=False):
        """
        system_id: 应用系统id
        allapps: 为真时，检查所有应用系统，默认为假

        """
        if allapps:
            for ids in self.applications(1, 1, 1):
                data = {
                    'system_id': ids["id"],
                    'token': self.token
                }
                url = 'http://{}/front/rest/apm/applications/{}/ips'.format(self.ip, ids["id"])
                response = requests.get(url=url, params=data)
                content = response.json()
                if content["status"] != "success":
                    return "fail"

            return "pass"

        else:
            url = 'http://{}/front/rest/apm/applications/{}/ips'.format(self.ip, str(system_id))
            data = {
                'system_id': system_id,
                'token': self.token
            }
            response = requests.get(url=url, params=data)
            content = response.json()
            if not content["ips"]:
                return "fail"
            else:
                return "pass"


    def applications_baseResource(self, system_id, allapps=False, panelId='system'):
        """
        system_id: 应用系统id
        allapps: 为真时，检查所有应用系统，默认为假
        panelId: 默认为应用系统

        """
        if allapps:
            for ids in self.applications(1, 1, 1):
                data = {
                    'system_id': ids["id"],
                    'token': self.token
                }
                url = 'http://{}/front/rest/apm/applications/{}/baseResource/{}'.format(self.ip, ids["id"], panelId)
                response = requests.get(url=url, params=data)
                content = response.json()
                if content["status"] != "success":
                    return "fail"
            return "pass"

        else:
            url = 'http://{}/front/rest/apm/applications/{}/baseResource/{}'.format(self.ip, str(system_id), panelId)
            data = {
                'system_id': system_id,
                'token': self.token
            }
            response = requests.get(url=url, params=data)
            content = response.json()
            if not content["result"]:
                return "fail"
            else:
                return "pass"