*** Settings ***
Library           json
Library           requests
Library           Collections
Library           apm

*** test cases ***
节点组性能数据
    ${status}    performance_subtotal    j3o6kg04-2    j3o6kg04-2-j3pa93wd-12
    should contain    ${status}    pass
    ${status}    performance_subtotal_order    j3o6kg04-2    j3o6kg04-2-j3pa93wd-12
    should contain    ${status}    pass

节点组性能数据排序
    ${status}    performance_subtotal_order    system_id=j3o6kg04-2    targetIds=j3o6kg04-2-j3pa93wd-12    orderBy=ip_port
    should contain    ${status}    pass
    ${status}    performance_subtotal_order    system_id=j3o6kg04-2    targetIds=j3o6kg04-2-j3pa93wd-12    orderBy=system/throughput/total
    should contain    ${status}    pass
    ${status}    performance_subtotal_order    system_id=j3o6kg04-2    targetIds=j3o6kg04-2-j3pa93wd-12    orderBy=system/response_time/avg
    should contain    ${status}    pass
    ${status}    performance_subtotal_order    system_id=j3o6kg04-2    targetIds=j3o6kg04-2-j3pa93wd-12    orderBy=system/success/rate
    should contain    ${status}    pass
    ${status}    performance_subtotal_order    system_id=j3o6kg04-2    targetIds=j3o6kg04-2-j3pa93wd-12    orderBy=system/error/count
    should contain    ${status}    pass
    ${status}    performance_subtotal_order    system_id=j3o6kg04-2    targetIds=j3o6kg04-2-j3pa93wd-12    orderBy=ip_port    desc=True
    should contain    ${status}    pass
    ${status}    performance_subtotal_order    system_id=j3o6kg04-2    targetIds=j3o6kg04-2-j3pa93wd-12    orderBy=system/throughput/total    desc=True
    should contain    ${status}    pass
    ${status}    performance_subtotal_order    system_id=j3o6kg04-2    targetIds=j3o6kg04-2-j3pa93wd-12    orderBy=system/response_time/avg    desc=True
    should contain    ${status}    pass
    ${status}    performance_subtotal_order    system_id=j3o6kg04-2    targetIds=j3o6kg04-2-j3pa93wd-12    orderBy=system/success/rate    desc=True
    should contain    ${status}    pass
    ${status}    performance_subtotal_order    system_id=j3o6kg04-2    targetIds=j3o6kg04-2-j3pa93wd-12    orderBy=system/error/count    desc=True
    should contain    ${status}    pass

性能查询
    ${status}    performance    system_ids=j3o6kg04-2
    should contain    ${status}    pass
    ${status}    performance    system_id=j3o6kg04-2    applicationIds=j3o6kg04-2-bcf75564,j3o6kg04-2-c0f1859d,j3o6kg04-2-35e7f5b6
    should contain    ${status}    pass
    ${status}    performance    system_id=j3o6kg04-2    applicationIds=j3o6kg04-2-bcf75564    agentIds=APM:10.1.7.130:8080
    should contain    ${status}    pass

回溯模式性能数据查询
    ${status}    performance    system_ids=j3o6kg04-2    size=hour
    should contain    ${status}    pass
