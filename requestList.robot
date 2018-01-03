*** Settings ***
Library           json
Library           requests
Library           Collections
Library           apm

*** Test Cases ***
请求列表
    sleep    180s
    ${status}    request_list    j3o6kg04-0
    should contain    ${status}    pass

calltree
    ${request_result}    request_list    j3o6kg04-0    60    0    0    1
    ${status}    calltree    ${request_result}
    should contain    ${status}    pass

方法详情
    ${request_lists}    request_list    j3o6kg04-0    60    0    0    1
    ${calltrees_rawdata}    calltree    ${request_lists}    1
    ${calltrees}    convert to list    ${calltrees_rawdata}
    ${tree}    get from list    ${calltrees}    0
    ${transactionid}    get from list    ${calltrees}    1
    ${timestamp}    get from list    ${calltrees}    2
    ${status}    method_description    ${tree}    ${transactionid}    ${timestamp}
    should contain    ${status}    pass

时间区间
    ${headers}    create dictionary    content-type=application/json
    ${url}    set variable    http://10.1.51.103/front/rest/apm/authentication/login?token=
    ${data0}    create dictionary    account=admin    password=admin
    ${data}    json.dumps    ${data0}
    ${response}    requests.post    url=${url}    data=${data}    headers=${headers}
    ${content}    loads    ${response.content}
    ${meta}    Get From Dictionary    ${content}    meta
    ${token}    Get From Dictionary    ${meta}    token
    ${apdex_url}    set variable    http://10.1.51.103/front/rest/apm/applications/j3o6kg04-0
    ${apdex_params}    create dictionary    token=${token}    panelId=system
    ${apdex_rawdata}    requests.get    url=${apdex_url}    params=${apdex_params}
    ${apdex_content}    loads    ${apdex_rawdata.content}
    ${apdex_app}    get from dictionary    ${apdex_content}    application
    ${apdex_t}    get from dictionary    ${apdex_app}    apdex_t
    ${timespace_url}    set variable    http://10.1.51.103/front/rest/apm/applications/apdexstatus/j3o6kg04-0
    ${timespace_data}    create dictionary    token=${token}
    ${timespace_rawdata}    requests.get    url=${timespace_url}    params=${timespace_data}
    ${timespace_app}    loads    ${timespace_rawdata.content}
    ${timespace}    get from dictionary    ${timespace_app}    applications
    ${normal}    set variable    0 - ${apdex_t}s
    ${slow}    set variable    ${apdex_t}s - ${apdex_t*4}s
    ${veryslow}    set variable    > ${apdex_t*4}s
    ${timespace_normal}    get from dictionary    ${timespace}    0
    ${timespace_slow}    get from dictionary    ${timespace}    1
    ${timespace_veryslow}    get from dictionary    ${timespace}    2
    should be equal as strings    ${normal}    ${timespace_normal}
    should be equal as strings    ${slow}    ${timespace_slow}
    should be equal as strings    ${veryslow}    ${timespace_veryslow}

状态筛选
    ${status}    request_list_status    j3o6kg04-0    1    1    1    1
    should be equal as strings    ${status}    pass
    ${status}    request_list_status    j3o6kg04-0    1    0    0    0
    should be equal as strings    ${status}    pass
    ${status}    request_list_status    j3o6kg04-0    0    1    0    0
    should be equal as strings    ${status}    pass
    ${status}    request_list_status    j3o6kg04-0    0    0    1    0
    should be equal as strings    ${status}    pass
    ${status}    request_list_status    j3o6kg04-0    0    0    0    1
    should be equal as strings    ${status}    pass
    ${status}    request_list_status    j3o6kg04-0    1    1    0    0
    should be equal as strings    ${status}    pass
    ${status}    request_list_status    j3o6kg04-0    1    0    1    1
    should be equal as strings    ${status}    pass

搜索请求
    @{keyword}    create list    select
    ${status}    request_list_search    j3o6kg04-0    ${keyword}
    should be equal as strings    ${status}    pass
    @{keyword}    create list    select    from
    ${status}    request_list_search    j3o6kg04-0    ${keyword}
    should be equal as strings    ${status}    pass
    @{keyword}    create list    中文    0
    ${status}    request_list_search    j3o6kg04-0    ${keyword}
    should be equal as strings    ${status}    pass
    @{keyword}    abnormal_input    3
    ${status}    request_list_search    j3o6kg04-0    ${keyword}
    should be equal as strings    ${status}    pass

jvm
    ${status}    jvm    system_id=j3o6kg04-0
    should contain    ${status}    pass

jvm_info
    ${status}    jvm_info    system_id=j3o6kg04-0
    should contain    ${status}    pass
