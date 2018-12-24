#!/usr/bin/env python
# encoding: utf-8
'''
@author: jerry
@contact: wangqiyuan@blhcn.com
@file: aliVpc.py
@time: 2018/11/27 10:27
@desc:
'''
import json
import os
import wrapt
from aliyunsdkcore import client
from aliyunsdkvpc.request.v20160428 import DescribeVpcsRequest,DescribeVpcAttributeRequest,DescribeVRoutersRequest, \
    DescribeRouteTableListRequest,DescribeRouteTablesRequest,DescribeVSwitchesRequest,DescribeVSwitchAttributesRequest,\
    DescribeCommonBandwidthPackagesRequest,DescribeEipAddressesRequest
from aliyun.service import othHandler


class aliVpc:
    def __init__(self, accessKey, accessSecret, RegionId):
        self.accessKey = accessKey
        self.accessSecret = accessSecret
        self.RegionId = RegionId
        self.clt = client.AcsClient(self.accessKey, self.accessSecret,self.RegionId)

    @othHandler.ali_wrap
    def vpc_list(self,VpcId='',IsDefault=True,PageNumber=1,PageSize=10):
        """
        vpc列表
        :param VpcId:
        :param IsDefault:
        :param PageNumber:
        :param PageSize:
        :return:
        """
        request = DescribeVpcsRequest.DescribeVpcsRequest()
        if VpcId:
            request.set_VpcId(VpcId)
        request.set_IsDefault(IsDefault)
        request.set_PageNumber(PageNumber)
        request.set_PageSize(PageSize)
        return request

    @othHandler.ali_wrap
    def get_vpc(self,VpcId,IsDefault=True):
        """
        查询指定VPC的配置信息
        :param VpcId:      要查询的VPC ID。
        :param IsDefault:  是否是默认VPC，取值
                            false：不是默认VPC
                            true：是默认VPC
        :return:
        """
        request = DescribeVpcAttributeRequest.DescribeVpcAttributeRequest()
        request.set_VpcId(VpcId)
        request.set_IsDefault(IsDefault)
        return request

    @othHandler.ali_wrap
    def get_v_routers(self,VRouterId='',PageNumber=1,PageSize=10):
        """
        查询指定地域的路由器列表。
        :param VRouterId:   路由器的ID。
        :param PageNumber:  列表的页码，默认值为1。
        :param PageSize:    分页查询时每页的行数，最大值为50，默认值为10。
        :return:
        """
        request = DescribeVRoutersRequest.DescribeVRoutersRequest()
        if VRouterId:
            request.set_VRouterId(VRouterId)
        request.set_PageNumber(PageNumber)
        request.set_PageSize(PageSize)
        return request

    @othHandler.ali_wrap
    def get_route_list(self,RouterType="VRouter",RouterId='',VpcId='',RouteTableId='',RouteTableName='',PageNumber=1,PageSize=10):
        """
        查询路由表。
        :param RouterType:路由表所属的路由器类型。取值：
                                                            VRouter（默认值）：VPC路由器
                                                            VBR：边界路由器
        :param RouterId:路由表所属路由器的ID。
        :param VpcId:   路由表所属的VPC路由器的ID。指定该参数后，参数RouterType的值自动设置为VRouter。
        :param RouteTableId:路由表的ID。
        :param RouteTableName:路由表的名称。
        :param PageNumber:列表的页码，默认值为1。
        :param PageSize:分页查询时每页的行数，最大值为50，默认值为10。
        :return:
        """
        request = DescribeRouteTableListRequest.DescribeRouteTableListRequest()
        request.set_RouterType(RouterType)
        if RouterId:
            request.set_RouterId(RouterId)
        if VpcId != "0":
            request.set_VpcId(VpcId)
        if RouteTableId:
            request.set_RouteTableId(RouteTableId)
        if RouteTableName:
            request.set_RouteTableName(RouteTableName)
        request.set_PageNumber(PageNumber)
        request.set_PageSize(PageSize)
        return request

    @othHandler.ali_wrap
    def get_route_tables(self,RouterType="VRouter",RouterId='',VRouterId='',RouteTableId="",PageNumber=1,PageSize=10):
        """
        查询路由表的路由条目。
        :param RouterType:
        :param RouterId:
        :param VRouterId:
        :param RouteTableId:
        :param PageNumber:
        :param PageSize:
        :return:
        """
        request = DescribeRouteTablesRequest.DescribeRouteTablesRequest()
        request.set_RouterType(RouterType)
        if RouterId:
            request.set_RouterId(RouterId)
        if RouterId:
            request.set_RouterId(RouterId)
        if VRouterId:
            request.set_VRouterId(VRouterId)
            request.set_RouterType("VRouter")
        if RouteTableId:
            request.set_RouteTableId(RouteTableId)
        request.set_PageNumber(PageNumber)
        request.set_PageSize(PageSize)
        return request

    @othHandler.ali_wrap
    def get_switch_list(self,VpcId='',ZoneId='',VSwitchId='',IsDefault=True,PageNumber=1,PageSize=10,*args,**kwargs):
        request = DescribeVSwitchesRequest.DescribeVSwitchesRequest()
        dic = ["VpcId",
               "ZoneId",
               "VSwitchId",
               "IsDefault",
               "PageNumber",
               "PageSize"
               ]
        for k in dic:
            if exec(k):
                if hasattr(request,"set_{}"):
                    getattr(request,"set_{}".format(k),)(exec(k))
        request.set_IsDefault(IsDefault)
        return request

    @othHandler.ali_wrap
    def get_switch(self,VSwitchId):
        request = DescribeVSwitchAttributesRequest.DescribeVSwitchAttributesRequest()
        request.set_VSwitchId(VSwitchId)
        return request

    @othHandler.ali_wrap
    def get_common_bandwidth_packages(self,BandwidthPackageId="",PageNumber=1,PageSize=10):
        """
        获取共享带宽
        :param BandwidthPackageId:
        :param PageNumber:
        :param PageSize:
        :return:
        """
        request = DescribeCommonBandwidthPackagesRequest.DescribeCommonBandwidthPackagesRequest()
        param = {"BandwidthPackageId":BandwidthPackageId,
               "PageNumber":PageNumber,
               "PageSize":PageSize
                 }
        return request,param

    @othHandler.ali_wrap
    def get_eip_addresses(self,Status="",AllocationId="",AssociatedInstanceType="",AssociatedInstanceId="",PageNumber=1,PageSize=10):
        request = DescribeEipAddressesRequest.DescribeEipAddressesRequest()
        param = {"Status": Status,
                 "AllocationId": AllocationId,
                 "AssociatedInstanceType": AssociatedInstanceType,
                 "AssociatedInstanceId": AssociatedInstanceId,
                 "PageNumber": PageNumber,
                 "PageSize": PageSize
                 }
        return request, param



if __name__ == '__main__':
    pass
    # vpc = aliVpc("LTAIeeuxK8V5grmN","qD8Z4LWicExfwZ72EdcPmLa2ieKg0N","cn-beijing")
    #     # z = vpc.get_eip_addresses()
    #     # print(z)