# _*_ coding:utf8 _*_
import requests
import random
import time

class requests_list(object):
    def __init__(self, ip, token, agent_id):
        self.ip = ip
        self.token = token
        self.agent_id = agent_id

    def request_list(self, system_id, interval_time=60, start_time=0, end_time=0, call=0):
        """
        interval_time 表示分钟，开始时间和结束时间为0时，以间隔时间为准，否则以开始结束时间为准；call不为0时，返回calltree的值。

        """
        if (int(start_time) == 0) & (int(end_time) == 0):
            end_date = int(round(time.time() * 1000) - 2 * 60 * 1000)
            start_date = end_date - int(interval_time) * 1000 * 60
        else:
            start_date = start_time
            end_date = end_time

        url = 'http://{}/front/rest/apm/performances/request_list'.format(self.ip)
        data = {
            "system_id": system_id,
            "agent_id": self.agent_id,
            "start_date": start_date,
            "end_date": end_date,
            "page_size": 20,
            "token": self.token
        }
        response = requests.get(url, params=data)
        content = response.json()

        if not call:
            if not content["result"]:
                return 'no request list , pass'
            else:
                if system_id in response.content:
                    return "pass"
                else:
                    return 'search fail'
        else:
            if not content["result"]:
                return 0
            else:
                return content["result"]


    def calltree(self, request_result, method=0):
        """
        参数是从请求列表那边接收过来的

        """
        if not request_result:
            return 'no request list, pass'

        else:
            if not method:
                for tree in request_result:
                    txId = tree["transactionId"]
                    timestamp = tree["timestamp"]
                    url = 'http://{}/front/rest/apm/calltree'.format(self.ip)
                    data = {
                        "txId": txId,
                        "timestamp": timestamp,
                        "token": self.token
                    }
                    response = requests.get(url=url, params=data)
                    content = response.json()
                    if not content["callTrees"]:
                        return 'fail'
                    else:
                        continue
            else:
                num = random.randint(0, len(request_result) - 1)
                txId = request_result[num]["transactionId"]
                timestamp = request_result[num]["timestamp"]
                url = 'http://{}/front/rest/apm/calltree'.format(self.ip)
                data = {
                    "txId": txId,
                    "timestamp": timestamp,
                    "token": self.token
                }
                response = requests.get(url=url, params=data)
                content = response.json()
                return content["callTrees"], txId, timestamp

        return 'pass'


    def method_description(self, callTrees, transactionId, times):
        
        if not callTrees:
            return 'no request list, pass'

        else:

            for calldata in callTrees:
                sequence = calldata["sequence"]
                url = 'http://{}/front/rest/apm/calltree/methodDescriptor'.format(self.ip)
                data = {
                    "token": self.token,
                    "txId": transactionId,
                    "sequence": sequence,
                    "timestamp": times + calldata["startElapsed"]
                }
                response = requests.get(url=url, params=data)
                content = response.json()
                if not content["methodName"]:
                    return "fail"
                else:
                    continue

        return "pass"


    def request_list_status(self, system_id, apdex_normal=1, apdex_slow=0, apdex_veryslow=0, apdex_error=0, interval_time=60):
        """

        第二至第五个参数表示请求列表中参与搜索的状态，0表示不参与，1表示参与

        """
        apdex_status = []
        if apdex_normal:
            apdex_status.append(0)
        if apdex_slow:
            apdex_status.append(1)
        if apdex_veryslow:
            apdex_status.append(2)
        if apdex_error:
            apdex_status.append(3)
        if not apdex_status:
            return 'no select'

        end_date = int(round(time.time() * 1000) - 2 * 60 * 1000)
        start_date = end_date - int(interval_time) * 1000 * 60
        url = 'http://10.1.51.103/front/rest/apm/performances/request_list'
        data = {
            "system_id": system_id,
            "agent_id": self.agent_id,
            "start_date": start_date,
            "end_date": end_date,
            "page_size": 100,
            "apdex_status": tuple(apdex_status),
            "order_by": "elapsed",
            "desc": "false",
            "token": self.token
        }
        response = requests.get(url, params=data)
        content = response.json()
        if not content["result"]:
            return 'pass'

        for status in content["result"]:
            if status["status"] not in apdex_status:
                return 'fail'
            else:
                continue
        return 'pass'


    def request_list_search(self, system_id, keyword=None, interval_time=60):
        """
        第二个参数表示要搜索的参数，列表格式

        """
        if keyword is None:
            keyword = []
        end_date = int(round(time.time() * 1000) - 2 * 60 * 1000)
        start_date = end_date - int(interval_time) * 1000 * 60
        url = 'http://{}/front/rest/apm/performances/request_list'.format(self.ip)
        data = {
            "system_id": system_id,
            "agent_id": self.agent_id,
            "start_date": start_date,
            "end_date": end_date,
            "page_size": 100,
            "keyword": tuple(keyword),
            "order_by": "elapsed",
            "desc": "true",
            "token": self.token
        }
        response = requests.get(url, params=data)
        content = response.json()
        if not content["result"]:
            return 'pass'

        else:
            for key in keyword:
                if key not in response.content:
                    return 'search fail'
                else:
                    continue
        return "pass"

    def jvm(self, system_id, interval_time=60, start_time=0, end_time=0):
        """
        interval_time 表示分钟，开始时间和结束时间为0时，以间隔时间为准，否则以开始结束时间为准     
        system_id 表示应用系统id   
        agent_id 表示agent的id   

        """

        if (int(start_time) == 0) & (int(end_time) == 0):
            end_date = int(round(time.time() * 1000) - 2 * 60 * 1000)
            start_date = end_date - int(interval_time) * 1000 * 60
        else:
            start_date = start_time
            end_date = end_time

        url = "http://{}/front/rest/apm/jvm".format(self.ip)
        data = {
            "system_id": system_id,
            "agent_id": self.agent_id,
            "start_date": start_date,
            "end_date": end_date,
            "token": self.token
        }
        response = requests.get(url=url, params=data)
        content= response.json()
        for i in  content["AgentStat"]["performanceList"]:
            if not i:
                return "jvm 查询失败"
            else:
                pass
        if content["status"] == "success":
            return "pass"


    def jvm_info(self, system_id):
        """
        system_id 表示应用系统id   
        agent_id 表示agent的id  
        
        """
        url = "http://{}/front/rest/apm/jvm/info".format(self.ip)
        data = {
            "system_id": system_id,
            "agent_id": self.agent_id,
            "token": self.token
        }
        response = requests.get(url=url, params=data)
        content = response.json()
        for i in content["agentBasicInfo"]:
            if not i:
                return "jvm info 查询失败"
            else:
                pass
        if content["status"] == "success":
            return "pass"
