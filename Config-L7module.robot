*** Settings ***
Library           requests
Library           Collections
Library           json

*** Variables ***

*** Test Cases ***
get token
    ${headers}    create dictionary    content-type=application/json
    ${url}    set variable    http://10.1.51.103/front/rest/apm/authentication/login?token=
    ${data0}    create dictionary    account=admin    password=admin
    ${data}    json.dumps    ${data0}
    ${response}    requests.post    url=${url}    data=${data}    headers=${headers}
    ${content}    loads    ${response.content}
    ${meta}    Get From Dictionary    ${content}    meta
    ${token}    Get From Dictionary    ${meta}    token
    ${params}    create dictionary    token=${token}
    set global variable    ${token}
    set global variable    ${params}

L7module 查询
    ${url}    set variable    http://10.1.51.103/front/rest/apm/configs/modulel7
    ${data}    create dictionary    token=${token}
    ${reponse}    requests.Get    ${url}    params=${data}
    ${dict0}    json.loads    ${reponse.content}
    ${status0}    get from dictionary    ${dict0}    status
    should be equal as strings    ${status0}    success
    ${modules}    get from dictionary    ${dict0}    modules
    ${module1}    get from list    ${modules}    -1
    ${l7_proto}    get from dictionary    ${module1}    l7_proto
    should be equal as integers    ${l7_proto}    1
    ${status}    get from dictionary    ${module1}    status
    should be equal as integers    ${status}    0

L7模块启用与禁用
    ${headers}    create dictionary    content-type=application/json
    ${data801}    create dictionary    id=80    status=1
    ${url}    set variable    http://10.1.51.103/front/rest/apm/configs/modulel7/status
    ${data}    dumps    ${data801}
    ${response}    requests.Put    ${url}    data=${data}    headers=${headers}    params=${params}
    ${content}    loads    ${response.content}
    ${status}    get from dictionary    ${content}    status
    should be equal as strings    ${status}    success
    ${data800}    create dictionary    id=80    status=0
    ${data}    dumps    ${data800}
    ${response}    requests.Put    url=${url}    data=${data}    headers=${headers}    params=${params}
    ${content}    loads    ${response.content}
    ${status}    get from dictionary    ${content}    status
    should be equal as strings    ${status}    success

L7模块返回码查询
    ${url}    set variable    http://10.1.51.103/front/rest/apm/configs/modulel7/recodes
    ${data}    create dictionary    l7_proto=1    token=${token}
    ${reponse}    requests.Get    url=${url}    params=${data}
    ${content}    json.loads    ${reponse.content}
    ${status}    get from dictionary    ${content}    status
    should be equal as strings    ${status}    success
