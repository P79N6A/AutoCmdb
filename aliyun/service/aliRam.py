#!/usr/bin/env python
# encoding: utf-8
'''
@author: jerry
@contact: wangqiyuan@blhcn.com
@file: aliRam.py
@time: 2018/11/26 9:21
@desc:
'''
import json
import os
import wrapt
from aliyunsdkcore import client
from aliyunsdkram.request.v20150501 import ListUsersRequest,GetUserRequest,CreateAccessKeyRequest,CreateUserRequest,\
    CreateLoginProfileRequest,GetLoginProfileRequest,UpdateAccessKeyRequest,DeleteAccessKeyRequest,\
    ListAccessKeysRequest,ChangePasswordRequest
from aliyun.service import othHandler



class aliRam:
    def __init__(self, accessKey, accessSecret):
        self.accessKey = accessKey
        self.accessSecret = accessSecret
        self.clt = client.AcsClient(self.accessKey, self.accessSecret)

    @othHandler.ali_wrap
    def list_users(self):
        request = ListUsersRequest.ListUsersRequest()
        return request

    @othHandler.ali_wrap
    def get_user(self,username):
        request = GetUserRequest.GetUserRequest()
        request.set_UserName(username)
        return request

    @othHandler.ali_wrap
    def creata_user(self,username, DisplayName = '', MobilePhone='', Email='',Comments=''):
        """
        创建用户
        :param username: 必填，str，指定用户名，最多包含64个字符，^[a-zA-Z0-9\.@\-_]+$
        :param DisplayName: 非必填，str，显示名称，最多包含128个字符或汉字，^[a-zA-Z0-9\.@\-\u4e00-\u9fa5]+$
        :param MobilePhone:非必填，str，RAM用户手机号，国际区号-号码；例如：86-18600008888
        :param Email:非必填，str，RAM用户的邮箱
        :param Comments:非必填，str，备注, 最大长度128个字符。
        :return:
        """
        request = CreateUserRequest.CreateUserRequest()
        request.set_UserName(username)
        if DisplayName:
            request.set_DisplayName(DisplayName)
        if MobilePhone:
            request.set_MobilePhone(MobilePhone)
        if Email:
            request.set_Email(Email)
        if Comments:
            request.set_Comments(Comments)
        return request

    def create_loginprofile(self,username,password,PasswordResetRequired,MFABindRequired):
        """
        启用Web控制台登录
        :param username:用户名，str，必须
        :param password:指定密码，密码必须符合密码强度要求。str，必须
        :param PasswordResetRequired:指定用户在登录时是否需要修改密码，Boolean，非必须
        :param MFABindRequired:指定用户在下次登录时是否必须绑定多因素认证器，Boolean，非必须
        :return:
        """
        request = CreateLoginProfileRequest.CreateLoginProfileRequest()
        request.set_UserName(username)
        request.set_Password(password)
        request.set_PasswordResetRequired(PasswordResetRequired)
        request.set_MFABindRequired(MFABindRequired)
        return request

    @othHandler.ali_wrap
    def get_loginprofile(self,username):
        """
        查看一个RAM用户的登录配置
        :param username:
        :return:
        """
        request = GetLoginProfileRequest.GetLoginProfileRequest()
        request.set_UserName(username)
        return request


    @othHandler.ali_wrap
    def create_accesskey(self,username=''):
        """
        创建accesskey
        :param username:必填
        :return:{'AccessKey': {'Status': 'Active', 'AccessKeySecret': 'sk4SBfsLtZ3KRd0b1g1iOqbRwX6wd6', 'AccessKeyId': 'LTAIg4PJdRIBGsTR', 'CreateDate': '2018-11-26T03:07:36Z'}, 'RequestId': 'B66704CC-DD50-42D3-98CA-E18CCC4BE64A'}
        """
        request = CreateAccessKeyRequest.CreateAccessKeyRequest()
        if username:
            request.set_UserName(username)
        return request

    @othHandler.ali_wrap
    def update_accesskey(self,UserAccessKeyId,Status,UserName=''):
        """
        变更RAM子用户AccessKey的状态
        :param UserAccessKeyId:指定要更新的AccessKeyId
        :param Status:AccessKey的状态, Active/Inactive
        :param UserName:指定用户名
        :return:
        """
        request = UpdateAccessKeyRequest.UpdateAccessKeyRequest()
        request.set_UserAccessKeyId(UserAccessKeyId)
        request.set_Status(Status)
        if UserName:
            request.set_UserName(UserName)
        return request

    @othHandler.ali_wrap
    def delete_accesskey(self,UserAccessKeyId,UserName=''):
        """
        删除RAM子用户的AccessKey
        :param UserAccessKeyId:指定要删除的AccessKeyId 必须
        :param UserName:指定用户名 非必须
        :return:
        """
        request = DeleteAccessKeyRequest.DeleteAccessKeyRequest()
        request.set_UserAccessKeyId(UserAccessKeyId)
        if UserName:
            request.set_UserName(UserName)
        return request

    @othHandler.ali_wrap
    def list_accesskeys(self,UserName=''):
        """
        列出指定用户的AccessKeys
        :param UserName:
        :return:
        """
        request = ListAccessKeysRequest.ListAccessKeysRequest()
        if UserName:
            request.set_UserName(UserName)
        return request

    @othHandler.ali_wrap
    def change_password(self,OldPassword,NewPassword):

        request = ChangePasswordRequest.ChangePasswordRequest()
        request.set_OldPassword(OldPassword)
        request.set_NewPassword(NewPassword)
        return request


if __name__ == '__main__':
    pass
    # at = aliRam("LTAIeeuxK8V5grmN","qD8Z4LWicExfwZ72EdcPmLa2ieKg0N")
    # print(at.list_accesskeys("wangqiyuan"))


