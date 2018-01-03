*** Settings ***
Library           json
Library           requests
Library           Collections
Library           apm

*** Test Cases ***
新增应用告警
    ${status}    alarms_append    system_id=j1ka5bak-7    targetId=j1ka5bak-7-29ad4521    indicator=rpm    serious=50    warning=40
    ...    caution=30    operator=>    times=1
    should contain    ${status}    pass
    ${status}    alarms_append5    system_id=j1ka5bak-7    targetId=j1ka5bak-7-2e6c31e7
    should contain    ${status}    pass

新增基线告警
    ${status}    alarms_append_alg    system_id=j1ka5bak-7    targetId=j1ka5bak-7-cd0e11cf
    should contain    ${status}    pass

查看某应用所有告警信息
    ${status}    alarms_overview    system_id=j1ka5bak-7
    should contain    ${status}    pass

查看应用内某个节点的告警配置
    ${status}    alarms_list    system_id=j1ka5bak-7    targetId=j1ka5bak-7-29ad4521
    should contain    ${status}    pass

修改应用告警
    ${status}    alarms_change_alg    system_id=j1ka5bak-7    targetId=j1ka5bak-7-29ad4521
    should contain    ${status}    pass
    ${status}    alarms_change    system_id=j1ka5bak-7    targetId=j1ka5bak-7-29ad4521    indicator=rpm    serious=30    warning=40
    ...    caution=50    operator=<    times=1
    should contain    ${status}    pass
    ${status}    alarms_change    system_id=j1ka5bak-7    targetId=j1ka5bak-7-29ad4521    indicator=rtt    serious=3    warning=4
    ...    caution=5    operator=<    times=2
    should contain    ${status}    pass
    ${status}    alarms_change    system_id=j1ka5bak-7    targetId=j1ka5bak-7-29ad4521    indicator=rtt    serious=6    warning=5
    ...    caution=4    operator=>    times=3
    should contain    ${status}    pass
    ${status}    alarms_change    system_id=j1ka5bak-7    targetId=j1ka5bak-7-29ad4521    indicator=error    serious=4    warning=3
    ...    caution=2    operator=>    times=5
    should contain    ${status}    pass

删除应用告警
    ${status}    alarms_delete    system_id=j1ka5bak-7    targetId=j1ka5bak-7-2e6c31e7    thresholdType=threshold
    should contain    ${status}    pass
    ${status}    alarms_delete    system_id=j1ka5bak-7    targetId=j1ka5bak-7-29ad4521    thresholdType=threshold
    should contain    ${status}    pass
    ${status}    alarms_delete    system_id=j1ka5bak-7    targetId=j1ka5bak-7-cd0e11cf    thresholdType=algorithm
    should contain    ${status}    pass
