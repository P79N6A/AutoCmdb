from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin


# urlpatterns = [
#
# ]
from aliyun.views import ecs,account,domain,dns,rds,slb,ram,vpc,oss

urlpatterns = [
    url(r'^$', ecs.aliViews.as_view(),name="aliyun"),
    url(r'^account$',account.aliAccount.as_view(),name="ali_account"),
    url(r'^account/add',account.aliAccountAdd.as_view(),name="add_ali_account"),
    url(r'^account/del',account.aliAccountDel.as_view(),name="del_ali_account"),
    url(r'^account/edit',account.aliAccountEdit.as_view(),name="edit_ali_account"),

    # url(r'^api/account/region',ecs.aliAccountRegion.as_view(),name="get_act_region"),
    url(r'^ecs$', ecs.ecsViews.as_view(),name="get_ecs_view"),
    url(r'domain$', domain.domainViews.as_view(),name="get_domain_view"),

    url(r'get_domainInfo$',domain.domainInfo.as_view(),name="get_domain_info"),
    url(r"^dns/records/details",dns.detailDnsRecord.as_view(),name="detail_dns_record"),


    url(r'^ali/ecs',ecs.aliAccountRegionS.as_view(),name="get_ali_ar_all"),
    url(r'^api/ecs/update',ecs.updateEcsView.as_view(), name="ecs_list_update"),
    url(r'^api/ecs/del',ecs.deleteEcs.as_view(),name="delete_ecs"),
    url(r'^api/ecs/Info',ecs.getEcsInfo.as_view(),name="api_ecs_info"),

    url(r"^ecs_info.html",ecs.getEcsInfoView.as_view(),name="ecs_info"),

    url(r"^api/account/get$", ecs.getAccount.as_view(),name="account_getProv"),
    url(r"^api/account/region/get$", ecs.getActRegion.as_view(),name="account_getCity"),
    url(r'^api/ecs/get',ecs.getEcsView.as_view(),name="ecs_list"),


    url(r"^api/domain/get",domain.aliSecondDomains.as_view(),name="get_seconde_domain"),
    url(r"^api/dns/records/get",dns.DnsRecords.as_view(),name="get_dns_records"),
    url(r"^api/dns/records/setstatus",dns.dnsRecordSetStatus.as_view(),name="stop_dns_record"),

    url(r'^dns/records', dns.DnsRecordsViews.as_view(), name="dns_records"),
    url(r'^dns/records/get', dns.DnsRecordsTest.as_view(), name="dns_records_get"),


    url(r'^rds$',rds.RdsView.as_view(),name="ali_rds_index"),
    url(r'^api/rds/get',rds.getRdsView.as_view(),name="rds_list"),
    url(r'^rds/info',rds.getRdsInfo.as_view(),name="rds_info"),

    url(r'^slb$',slb.SlbView.as_view(),name="ali_slb_index"),
    url(r'^api/slb/get', slb.getSlbView.as_view(), name="slb_list"),
    url(r'^slb/info',slb.getSlbInfo.as_view(),name="slb_info"),
    url(r'^slb/slb_server_group',slb.getSlbServerGroup.as_view(),name="slb_server_group"),
    url(r'^slb/slb-server-group/server',slb.getSlbServerGroupS.as_view(),name="slb_server_group_s"),
    url(r'^redis/clear', rds.clearDomainCache.as_view(), name="clear_domain_cache"),


    url(r'^ram$',ram.RAMView.as_view(),name="ali_ram_index"),
    url(r'^ram/info',ram.getRamInfo.as_view(),name="ram_info"),
    url(r'^ram/accessKey/set-status',ram.setAccessStatus.as_view(),name="set_access_status"),
    url(r'^ram/accessKey/del',ram.delAccessKey.as_view(),name="del_accesskey"),
    url(r'^ram/accessKey/add',ram.addAccessKey.as_view(),name="add_accesskey"),

    url("^vpc$",vpc.VPCView.as_view(),name="ali_vpc_index"),
    url("^vpc/route",vpc.VpcRouteView.as_view(),name="ali_vpc_route"),
    url("^vpc/switch",vpc.VpcSwitchView.as_view(),name="ali_vpc_switch"),
    url("^vpc/eip",vpc.VpcEipView.as_view(),name="ali_vpc_eip"),


    url("^oss$",oss.OssView.as_view(), name="ali_oss_index"),
    url(r'^oss/info',oss.getOssInfo.as_view(),name="oss_info"),

]