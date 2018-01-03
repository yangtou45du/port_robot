*** Settings ***
Library           requests
Library           apm

*** Test Cases ***
perf
    ${content}    open_perf    system_name=接口测试专用（agent），勿动！    system_id=j1ka5bak-6    service_id=j1ka5bak-6-3405c16a    ip=10.1.51.103    port=80
    ...    field=system/throughput/total    last=6
    log    ${content}
