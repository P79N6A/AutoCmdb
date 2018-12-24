#!/usr/bin/env python
# encoding: utf-8
'''
@author: jerry
@contact: wangqiyuan@blhcn.com
@file: aliHandle.py
@time: 2018/11/6 18:40
@desc:
'''
import json
import os
import django
import oss2
import multiprocessing
from aliyunsdkcore import client
from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest,DescribeRegionsRequest
from aliyunsdkdomain.request.v20180129 import QueryDomainListRequest,QueryDomainByInstanceIdRequest
from aliyunsdkalidns.request.v20150109 import DescribeDomainRecordsRequest,SetDomainRecordStatusRequest,\
    DescribeDomainRecordInfoRequest,UpdateDomainRecordRequest
from aliyunsdkslb.request.v20140515 import DescribeLoadBalancersRequest,DescribeLoadBalancerAttributeRequest,\
    DescribeLoadBalancerTCPListenerAttributeRequest,DescribeLoadBalancerUDPListenerAttributeRequest, \
    DescribeLoadBalancerHTTPListenerAttributeRequest,DescribeLoadBalancerHTTPSListenerAttributeRequest, \
    DescribeVServerGroupsRequest,DescribeVServerGroupAttributeRequest

from aliyunsdkrds.request.v20140815 import DescribeDBInstancesRequest,DescribeDBInstanceAttributeRequest,\
    ModifyDBInstanceDescriptionRequest,DescribeAccountsRequest,ModifyAccountDescriptionRequest,\
    DescribeDBInstanceIPArrayListRequest,DescribeDBInstanceNetInfoRequest
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AutoCmdb.settings")
django.setup()
from aliyun import models



class AliyunEcs:
    def __init__(self, accessKey, accessSecret, region,account):
        self.accessKey = accessKey
        self.accessSecret = accessSecret
        self.region = region
        self.account = account

    def get_sys_info(self):
        clt = client.AcsClient(self.accessKey,self.accessSecret,self.region)
        request = DescribeInstancesRequest.DescribeInstancesRequest()
        # request.set_PageNumber(1)   #设置页数
        request.set_PageSize(50)  # 设置每页返回多少，默认为10条
        request.set_accept_format('json')
        self.result = json.loads(clt.do_action(request)).get('Instances').get('Instance')
        # result = clt.do_action(request)
        return self.result

    def format_data(self):
        result = []
        self.ecs_data = self.get_sys_info()
        for line in self.ecs_data:
            act_obj = models.AliAccount.objects.filter(id=self.account).first()
            data = {
                "InnerIpAddress_IpAddress": line.get("InnerIpAddress").get("IpAddress"),  # list
                "ImageId": line.get("ImageId"),  # str
                "InstanceTypeFamily": line.get("InstanceTypeFamily"),  # str
                "VlanId": line.get("VlanId"),  # str
                "NetworkInterfaces_NetworkInterface_MacAddress": line.get("NetworkInterfaces").get("NetworkInterface")[0].get("MacAddress"),  # str
                "NetworkInterfaces_NetworkInterface_PrimaryIpAddress": line.get("NetworkInterfaces").get("NetworkInterface")[0].get("PrimaryIpAddress"),  # str
                "NetworkInterfaces_NetworkInterface_NetworkInterfaceId": line.get("NetworkInterfaces").get("NetworkInterface")[0].get("NetworkInterfaceId"),  # str
                "InstanceId": line.get('InstanceId'),  # str
                "EipAddress_IpAddress": line.get("EipAddress").get("IpAddress"),  # str
                "EipAddress_AllocationId": line.get("EipAddress").get("AllocationId"),  # str
                "EipAddress_InternetChargeType": line.get("EipAddress").get("InternetChargeType"),  # str
                "InternetMaxBandwidthIn": line.get("InternetMaxBandwidthIn"),  # int
                "CreditSpecification": line.get("CreditSpecification"),  # str
                "ZoneId": line.get('ZoneId'),  # str
                "InternetChargeType": line.get("InternetChargeType"),  # str
                "SpotStrategy": line.get("SpotStrategy"),  # str
                "StoppedMode": line.get("StoppedMode"),  # str
                "SerialNumber": line.get("SerialNumber"),  # str
                "IoOptimized": line.get("IoOptimized"),  # bool
                "Memory": line.get("Memory"),  # int
                "Cpu": line.get('Cpu'),  # int
                "VpcAttributes_NatIpAddress": line.get("VpcAttributes").get("NatIpAddress"),  # str
                "VpcAttributes_PrivateIpAddress_IpAddress": line.get("VpcAttributes").get("PrivateIpAddress").get("IpAddress"),  # list
                "VpcAttributes_VSwitchId": line.get("VpcAttributes").get("VSwitchId"),  # str
                "VpcAttributes_VpcId": line.get("VpcAttributes").get("VpcId"),  # str
                "InternetMaxBandwidthOut": line.get("InternetMaxBandwidthOut"),  # int
                "DeviceAvailable": line.get("DeviceAvailable"),  # bool
                "SecurityGroupIds_SecurityGroupId": line.get("SecurityGroupIds").get("SecurityGroupId"),  # list
                "SaleCycle": line.get("SaleCycle"),  # str
                "SpotPriceLimit": line.get("SpotPriceLimit"),  # float
                "AutoReleaseTime": line.get("AutoReleaseTime"),  # str
                "StartTime": line.get("StartTime"),  # str
                "InstanceName": line.get("InstanceName"),  # str
                "Description": line.get("Description"),  # str
                "ResourceGroupId": line.get("ResourceGroupId"),  # str
                "OSType": line.get("OSType"),  # str
                "OSName": line.get("OSName"),  # str
                "InstanceNetworkType": line.get("InstanceNetworkType"),  # str
                "PublicIpAddress_IpAddress": line.get('PublicIpAddress').get('IpAddress'),  # list
                "HostName": line.get('HostName'),  # str
                "InstanceType": line.get('InstanceType'),  # str
                "CreationTime": line.get('CreationTime'),  # str
                "Status": line.get('Status'),  # str
                "ClusterId": line.get("ClusterId"),  # str
                "Recyclable": line.get("Recyclable"),  # bool
                "RegionId": line.get("RegionId"),  # str
                "GPUSpec": line.get("GPUSpec"),  # str
                "DedicatedHostAttribute_DedicatedHostId": line.get("DedicatedHostAttribute").get("DedicatedHostId"),  # str
                "DedicatedHostAttribute_DedicatedHostName": line.get("DedicatedHostAttribute").get("DedicatedHostName"),  # str
                "OperationLocks_LockReason": line.get("OperationLocks").get("LockReason"),  # list
                "GPUAmount": line.get("GPUAmount"),  # int
                "InstanceChargeType": line.get("InstanceChargeType"),  # str
                "ExpiredTime": line.get("ExpiredTime"),  # str
                "DeploymentSetId": line.get("DeploymentSetId"),  # str
                "account":act_obj,
            }
            result.append(data)
        return result

    def insert_db(self):
        result = self.format_data()
        print(result)
        for oneEcs in result:
            InstanceId = oneEcs.get("InstanceId")
            print(InstanceId)
            z = models.AliEcs.objects.filter(InstanceId=InstanceId)
            RegionId = models.Region.objects.get(RegionId=oneEcs.get("RegionId"))

            print(RegionId)
            oneEcs.update({"RegionId":RegionId})
            if not z:

                obj = models.AliEcs(**oneEcs)
                obj.save()
            else:
                z.update(**oneEcs)


class AliyunDomain:
    def __init__(self,accessKey,accessSecret):
        self.accessKey = accessKey
        self.accessSecret = accessSecret

    def get_second_domain(self,pageSize,pageStart):
        clt = client.AcsClient(self.accessKey, self.accessSecret)
        request = QueryDomainListRequest.QueryDomainListRequest()
        print(request.get_uri_pattern())
        request.set_PageNum(pageStart)
        request.set_PageSize(pageSize)  # 设置每页返回多少，默认为10条
        request.set_accept_format('json')
        result = json.loads(clt.do_action(request))
        print(result)
        return result

    def get_domain_info(self,instance_id):
        clt = client.AcsClient(self.accessKey, self.accessSecret)
        request = QueryDomainByInstanceIdRequest.QueryDomainByInstanceIdRequest()
        request.set_InstanceId(instance_id)
        #request.set_PageSize(50)  # 设置每页返回多少，默认为10条
        request.set_accept_format('json')
        result = json.loads(clt.do_action(request))
        return result



class AliyunDns:
    def __init__(self,accessKey,accessSecret):
        self.accessKey = accessKey
        self.accessSecret = accessSecret
        self.clt = client.AcsClient(self.accessKey, self.accessSecret)

    def del_dns_record(self, recordId):
        pass

    def set_dns_status(self,recordId,status):
        request = SetDomainRecordStatusRequest.SetDomainRecordStatusRequest()
        request.set_accept_format("json")
        request.set_RecordId(recordId)
        request.set_Status(status)
        result = json.loads(self.clt.do_action(request))
        print(result)
        return result

    def get_dns_status(self,recordId):
        request = DescribeDomainRecordInfoRequest.DescribeDomainRecordInfoRequest()
        request.set_accept_format("json")
        request.set_RecordId(recordId)
        result = json.loads(self.clt.do_action(request))
        print(result)
        return result


    def get_domain_records(self,DomainName,PageNumber=0,PageSize=0,RRKeyWord=0,TypeKeyWord=0,ValueKeyWord=0):
        clt = client.AcsClient(self.accessKey, self.accessSecret)
        request = DescribeDomainRecordsRequest.DescribeDomainRecordsRequest()
        request.set_accept_format("json")
        request.set_DomainName(DomainName)
        if PageNumber:
            request.set_PageNumber(PageNumber)
        if PageSize:
            request.set_PageSize(PageSize)
        if RRKeyWord:
            request.set_RRKeyWord(RRKeyWord)
        if TypeKeyWord:
            request.set_TypeKeyWord(TypeKeyWord)
        if ValueKeyWord:
            request.set_ValueKeyWord(ValueKeyWord)
        print(request)

        result = json.loads(clt.do_action(request))
        print(result)
        return result

    def set_domain_records(self,RecordId,RR,Type,Value,TTL,Priority,Line):
        request = UpdateDomainRecordRequest.UpdateDomainRecordRequest()
        request.set_accept_format("json")
        request.set_RecordId(RecordId)
        request.set_RR(RR)
        request.set_Type(Type)
        request.set_Value(Value)
        request.set_TTL(TTL)
        if Priority:
            request.set_Priority(Priority)
        request.set_Line(Line)
        result = json.loads(self.clt.do_action(request))
        print(result)
        return result

class AliyunRDS:
    def __init__(self,accessKey,accessSecret,regionId):
        self.accessKey = accessKey
        self.accessSecret = accessSecret
        self.clt = client.AcsClient(self.accessKey, self.accessSecret,regionId)


    def get_regions(self):
        """
        可用区查询:
        """
        request = DescribeRegionsRequest.DescribeRegionsRequest()
        request.set_accept_format("json")
        result = json.loads(self.clt.do_action(request))
        print(result)
        return result

    def get_rds(self,pageStart=0,pageSize=0):
        """
        获取rds列表
        :param pageStart:
        :param pageSize:
        :return:
        """
        request = DescribeDBInstancesRequest.DescribeDBInstancesRequest()
        if pageStart:
            request.set_PageNumber(pageStart)
        if pageSize:
            request.set_PageSize(pageSize)  # 设置每页返回多少，默认为10条
        request.set_accept_format("json")
        result = json.loads(self.clt.do_action(request))
        print(result)
        return result


    def get_rds_instace(self,DBInstanceId):
        """
        获取rds实例内同
        :param DBInstanceId:
        :return:
        """
        request = DescribeDBInstanceAttributeRequest.DescribeDBInstanceAttributeRequest()
        request.set_DBInstanceId(DBInstanceId)
        request.set_accept_format("json")
        result = json.loads(self.clt.do_action(request))
        print(result)
        return result

    def get_rds_netinfo(self,DBInstanceId):
        """
        查看指定实例的所有连接信息。
        :param DBInstanceId:
        :return:
        """
        request = DescribeDBInstanceNetInfoRequest.DescribeDBInstanceNetInfoRequest()
        request.set_DBInstanceId(DBInstanceId)
        request.set_accept_format("json")
        result = json.loads(self.clt.do_action(request))
        print(result)
        return result



    def modify_rds_instance_Description(self,DBInstanceId,DBInstanceDescription):
        """
        修改实例的备注名
        :return:
        """
        request = ModifyDBInstanceDescriptionRequest.ModifyDBInstanceDescriptionRequest()
        request.set_DBInstanceId(DBInstanceId)
        request.set_DBInstanceDescription(DBInstanceDescription)
        request.set_accept_format("json")
        result = json.loads(self.clt.do_action(request))
        print(result)
        return result

    def create_account(self,DBInstanceId,AccountName,AccountPassword):
        pass

    def get_accounts(self,DBInstanceId):
        """
        获取账号
        :param DBInstanceId:
        :return:
        """
        request = DescribeAccountsRequest.DescribeAccountsRequest()
        request.set_DBInstanceId(DBInstanceId)
        request.set_accept_format("json")
        result = json.loads(self.clt.do_action(request))
        print(result)
        return result

    def modify_account_description(self,DBInstanceId,AccountName,AccountDescription):
        """
        修改数据库名的备注名
        :return:
        """
        request = ModifyAccountDescriptionRequest.ModifyAccountDescriptionRequest()
        request.set_DBInstanceId(DBInstanceId)
        request.set_AccountName(AccountName)
        request.set_AccountDescription(AccountDescription)
        request.set_accept_format("json")
        result = json.loads(self.clt.do_action(request))
        print(result)
        return result

    def get_rds_IP_ArrayList(self,DBInstanceId):
        """
        获取白名单
        :param DBInstanceId:
        :return:
        """
        request = DescribeDBInstanceIPArrayListRequest.DescribeDBInstanceIPArrayListRequest()
        request.set_DBInstanceId(DBInstanceId)
        request.set_accept_format("json")
        result = json.loads(self.clt.do_action(request))
        print(result)
        return result

    def get_sql_logfiles(self):
        """
        获取sql审计文件列表
        :return:
        """




class AliyunSlb:
    def __init__(self,accessKey,accessSecret,regionId):
        self.accessKey = accessKey
        self.accessSecret = accessSecret
        self.clt = client.AcsClient(self.accessKey, self.accessSecret,regionId)

    def get_slbs(self,pageStart=0,pageSize=0):
        request = DescribeLoadBalancersRequest.DescribeLoadBalancersRequest()
        if pageStart:
            request.set_PageNumber(pageStart)
        if pageSize:
            request.set_PageSize(pageSize)  # 设置每页返回多少，默认为10条
        request.set_accept_format("json")
        result = json.loads(self.clt.do_action(request))
        print(result)
        return result

    def get_slb(self,LoadBalancerId):
        request = DescribeLoadBalancerAttributeRequest.DescribeLoadBalancerAttributeRequest()
        request.set_LoadBalancerId(LoadBalancerId)
        request.set_accept_format("json")
        result = json.loads(self.clt.do_action(request))
        print(result)
        return result

    def get_slb_listener(self,action,LoadBalancerId,ListenerPort):
        if action == "tcp":
            request = DescribeLoadBalancerTCPListenerAttributeRequest.DescribeLoadBalancerTCPListenerAttributeRequest()
        elif action == "udp":
            request = DescribeLoadBalancerUDPListenerAttributeRequest.DescribeLoadBalancerUDPListenerAttributeRequest()
        elif action == "http":
            request = DescribeLoadBalancerHTTPListenerAttributeRequest.DescribeLoadBalancerHTTPListenerAttributeRequest()
        else:
            request = DescribeLoadBalancerHTTPSListenerAttributeRequest.DescribeLoadBalancerHTTPSListenerAttributeRequest()
        request.set_LoadBalancerId(LoadBalancerId)
        request.set_ListenerPort(ListenerPort)
        request.set_accept_format("json")
        result = json.loads(self.clt.do_action(request))
        print(result)
        return result

    def get_vservergroups(self,LoadBalancerId,):
        """
        获取slb服务器组
        :param LoadBalancerId:
        :return:
        """
        request = DescribeVServerGroupsRequest.DescribeVServerGroupsRequest()
        request.set_LoadBalancerId(LoadBalancerId)
        request.set_accept_format("json")
        result = json.loads(self.clt.do_action(request))
        print(result)
        return result

    def get_vserver_group_attr(self,VServerGroupId):
        """
        获取slb服务器组详细信息
        :param VServerGroupId:
        :return:
        """
        request = DescribeVServerGroupAttributeRequest.DescribeVServerGroupAttributeRequest()
        request.set_VServerGroupId(VServerGroupId)
        request.set_accept_format("json")
        result = json.loads(self.clt.do_action(request))
        print(result)
        return result

    def get_server_cas(self):
        pass


class AliOss:
    def __init__(self, accessKey, accessSecret):
        self.accessKey = accessKey
        self.accessSecret = accessSecret
        self.auth = oss2.Auth(self.accessKey,self.accessSecret)
        self.url = "http://oss-cn-hangzhou.aliyuncs.com"
        self.service = oss2.Service(self.auth, self.url)

    def get_oss_list(self):
        error_dict = {}
        try:
            self.oss_list_obj = [b for b in oss2.BucketIterator(self.service)]
            self.oss_list = []
            for i in self.oss_list_obj:
                print(i)
                self.oss_list.append(i.__dict__)
            return self.oss_list
        except Exception as e:
            error_dict.update(e.__dict__)
            return error_dict

    def get_bucket_info(self, bucket_name):
        self.bucket_info = oss2.Bucket(self.auth, self.url, bucket_name).get_bucket_info().__dict__
        self.bucket_info["acl_name"] = self.bucket_info.get("acl").__dict__["grant"]
        return self.bucket_info



if __name__ == '__main__':
    pass
    # oss = AliOss("LTAIeeuxK8V5grmN","qD8Z4LWicExfwZ72EdcPmLa2ieKg0N")
    # oss_list = oss.get_oss_list()
    # print(oss_list)
    # p = AliyunEcs("LTAIeeuxK8V5grmN","qD8Z4LWicExfwZ72EdcPmLa2ieKg0N","cn-beijing",21)
    # p.insert_db()
    # p = AliyunDomain("LTAIeeuxK8V5grmN","qD8Z4LWicExfwZ72EdcPmLa2ieKg0N")
    # p.get_second_domain(10,1)
    # dns
    # p = AliyunSlb(accessKey="LTAIeeuxK8V5grmN",accessSecret="qD8Z4LWicExfwZ72EdcPmLa2ieKg0N",regionId="cn-beijing")
    # p.get_vserver_group_attr("rsp-2zeptkex87ktq")
    # p.get_slb_listener("tcp","lb-2ze2juql884qnoy1sr7nt","8888")
    # p.get_slbs(pageSize=3,pageStart=1)
    # # p.get_rds_instace("rm-j6c9i5c2ut88022kt")
    # p.get_slbs()
    # p.get_slb("lb-2ze2juql884qnoy1sr7nt")
    # # p.get_domain_records(DomainName="chengkezb.com")   # 查询域名解析记录
    # p.set_dns_stats("4152143709209600","Enable")
