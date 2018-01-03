*** Settings ***
Library           json
Library           requests
Library           Collections
Library           apm

*** Test Cases ***
添加应用
    ${status}    application_append    interface_test
    should be equal as strings    ${status}    pass

删除应用
    ${status}    application_delete    interface_test
    should be equal as strings    ${status}    pass

交易总览中的业务系统
    ${status}    applications_inoverview    True
    should be equal as strings    ${status}    pass
    ${status}    applications_inoverview    False
    should be equal as strings    ${status}    pass

添加删除应用_异常输入
    @{applications_input_delete_abnormal}    abnormal_input    50
    : FOR    ${abnormal_input}    IN    @{applications_input_delete_abnormal}
    \    ${status}    application_append    ${abnormal_input}
    \    should be equal as strings    ${status}    pass
    \    ${status}    application_delete    ${abnormal_input}
    \    should be equal as strings    ${status}    pass

查询应用内所有协议
    ${status}    applications_protos    system_id=j3o6kg04-2
    should contain    ${status}    pass
    ${status}    applications_protos    system_id=j3o6kg04-2    allapps=True
    should contain    ${status}    pass

查询应用内所有ip
    ${status}    applications_ips    system_id=j3o6kg04-2
    should contain    ${status}    pass
    ${status}    applications_ips    system_id=j3o6kg04-2    allapps=True
    should contain    ${status}    pass

查看应用系统下所有节点和id
    ${status}    applications_baseResource    system_id=j3o6kg04-2
    should contain    ${status}    pass
    ${status}    applications_baseResource    system_id=j3o6kg04-2    allapps=True
    should contain    ${status}    pass
