#!/usr/bin/env python
# encoding: utf-8
'''
@author: jerry
@contact: wangqiyuan@blhcn.com
@file: rbac.py
@time: 2018/12/5 9:27
@desc:
'''
from django.views import View
from django.shortcuts import HttpResponse, render
from django.http import JsonResponse
from rbac.cbv.views import RbacView
from rbac.models import Menu, Permission, Role, Permission2Action2Role, Action,User,User2Role
from repository.models import UserProfile
from rbac.Forms.rbacForm import menuAddForm
from rbac.services import menuSer
from django.core.cache import cache
from rbac.cbv.views import RbacView
from django.db.models import Q


DIC_CODE = {
    "code": 0,
    "msg": "",
}


class rbacView(RbacView,View):

    def get(self, request, *args, **kwargs):
        rbac_menu_permission = request.session.get("rbac_permission_session_key")
        username = request.session.get("user_info").get("username")
        role_caption = User2Role.objects.values("role__caption").filter(user__username=username).first()
        rbac_list = list(Permission2Action2Role.objects.values("permission__menu", "action__code", "permission__url",
                                                               "permission__caption", "permission__menu__caption",
                                                               "permission__menu__parent").filter(
            Q(permission__url__in=rbac_menu_permission.keys()) & Q(role__caption=role_caption["role__caption"])))
        for i in rbac_list:
            i["permission__url"] = i["permission__url"].split("$")[0]
        print(rbac_list)
        return render(request,"rbac/basic/index.html",locals())



##################菜单管理###################


class menuAdd(View):

    def get(self, request, *args, **kwargs):
        level = int(request.GET.get("level")) + 1
        parent_id = request.GET.get("parent_id")
        obj = menuAddForm()
        return render(request, "rbac/menu/add.html", locals())

    def post(self, request, *args, **kwargs):
        level2 = request.POST.get("level")
        print(request.POST)
        obj = menuAddForm(data=request.POST)  ##传入进行验证
        if obj.is_valid():
            # models.News.objects.create(**obj.cleaned_data) ##以前Form的时候添加数据要这样写
            obj.save()  ##modelform现在可以直接save就可以，save的时候可以保存一对多、多对多的数据
        else:
            print(obj.errors)
        return render(request, "rbac/menu/add.html", locals())


class menu(RbacView,View):

    def get(self, request, *args, **kwargs):
        rbac_menu_permission = request.session.get("rbac_permission_session_key")
        username = request.session.get("user_info").get("username")
        role_caption = User2Role.objects.values("role__caption").filter(user__username=username).first()
        rbac_list = list(Permission2Action2Role.objects.values("permission__menu", "action__code", "permission__url",
                                                               "permission__caption", "permission__menu__caption",
                                                               "permission__menu__parent").filter(
            Q(permission__url__in=rbac_menu_permission.keys()) & Q(role__caption=role_caption["role__caption"])))
        for i in rbac_list:
            i["permission__url"] = i["permission__url"].split("$")[0]
        all_menu = list(Menu.objects.values("id", "caption", "parent__caption", "level").all())
        return render(request, "rbac/menu/index.html", locals())


class menuDel(View):

    def post(self, request, *args, **kwargs):
        cate_id = request.POST.get("cate_id")
        menu_obj = Menu.objects.filter(id=cate_id).first()
        menu_obj.delete()
        DIC_CODE["code"] = 1
        DIC_CODE["msg"] = "删除成功"
        return JsonResponse(DIC_CODE)


class menuEdit(View):
    def get(self, request, *args, **kwargs):
        parent_id = request.GET.get("parent_id")
        menu_obj = Menu.objects.filter(id=parent_id).first()
        obj = menuAddForm(instance=menu_obj)
        print(obj)
        return render(request, "rbac/menu/edit.html", locals())

    def post(self, request, *args, **kwargs):
        print(request.POST)
        return JsonResponse(DIC_CODE)


#############################################


##################权限管理###################

class authView(RbacView,View):
    def get(self, request, *args, **kwargs):
        auth_objs = Permission.objects.values("id", "caption", "url", "menu").all()
        rbac_menu_permission = request.session.get("rbac_permission_session_key")
        username = request.session.get("user_info").get("username")
        role_caption = User2Role.objects.values("role__caption").filter(user__username=username).first()
        rbac_list = list(Permission2Action2Role.objects.values("permission__menu", "action__code", "permission__url",
                                                               "permission__caption", "permission__menu__caption",
                                                               "permission__menu__parent").filter(
            Q(permission__url__in=rbac_menu_permission.keys()) & Q(role__caption=role_caption["role__caption"])))
        for i in rbac_list:
            i["permission__url"] = i["permission__url"].split("$")[0]
        return render(request, "rbac/auth/index.html", locals())


class menuSelect(View):
    def get(self, request, *args, **kwargs):
        menu_objs = Menu.objects.values("id", "caption", "level", "parent_id").all()
        menu_select_list = menuSer.menu_select(menu_objs=menu_objs)
        print(menu_select_list)
        return JsonResponse(menu_select_list, safe=False)


class authMenuSave(View):
    def post(self, request, *args, **kwargs):
        mid = request.POST.get("mid")  # 要更改的id
        menu_id = request.POST.get("change_menu_id")  # 更改菜单的id
        caption_name = request.POST.get("caption_name")
        url_name = request.POST.get("url_name")
        authValue = Permission.objects.values("caption", "menu", "url").filter(id=mid).first()
        if caption_name != authValue["caption"] and caption_name:
            Permission.objects.filter(id=mid).update(caption=caption_name)

            print(1)
        if url_name != authValue["url"] and url_name:
            Permission.objects.filter(id=mid).update(url=url_name)
            print(2)
        if menu_id != authValue["menu"]:
            Permission.objects.filter(id=mid).update(menu=menu_id)
            print(3)
        DIC_CODE["code"] = 1
        DIC_CODE["msg"] = "更新成功"
        return JsonResponse(DIC_CODE)


class authDel(View):
    def delete(self, request, *args, **kwargs):
        cate_id = request.POST.get("cate_id")
        menu_obj = Permission.objects.filter(id=cate_id).first()
        menu_obj.delete()
        DIC_CODE["code"] = 1
        DIC_CODE["msg"] = "删除成功"
        return JsonResponse(DIC_CODE)


class authAdd(View):
    def get(self, request, *args, **kwargs):
        return render(request, "rbac/auth/add.html")

    def post(self, request, *args, **kwargs):
        try:
            caption = request.POST.get("caption")
            url = request.POST.get("url")
            menu = request.POST.get("menu")
            print(caption, url, menu)
            if caption and url:
                if menu:
                    Permission.objects.create(caption=caption, url=url, menu=menu)
                else:
                    Permission.objects.create(caption=caption, url=url)
                DIC_CODE["code"] = 1
                DIC_CODE["msg"] = "增加成功"
            else:
                DIC_CODE["code"] = 0
                DIC_CODE["msg"] = "请输入正确的值"
        except Exception as e:
            DIC_CODE["code"] = 0
            DIC_CODE["msg"] = e
        finally:
            print(DIC_CODE)
            return JsonResponse(DIC_CODE)


"""
角色管理
"""
class roleView(RbacView,View):
    def get(self, request, *args, **kwargs):
        role_objs = Role.objects.values("id", "caption", "note").all()
        rbac_menu_permission = request.session.get("rbac_permission_session_key")
        username = request.session.get("user_info").get("username")
        role_caption = User2Role.objects.values("role__caption").filter(user__username=username).first()
        rbac_list = list(Permission2Action2Role.objects.values("permission__menu", "action__code", "permission__url",
                                                               "permission__caption", "permission__menu__caption",
                                                               "permission__menu__parent").filter(
            Q(permission__url__in=rbac_menu_permission.keys()) & Q(role__caption=role_caption["role__caption"])))
        for i in rbac_list:
            i["permission__url"] = i["permission__url"].split("$")[0]
        return render(request, "rbac/role/index.html", locals())


class roleAdd(View):
    def get(self, request, *args, **kwargs):
        return render(request, "rbac/role/add.html", )

    def post(self, request, *args, **kwargs):
        caption = request.POST.get("caption")
        note = request.POST.get("note")
        if caption:
            Role.objects.create(caption=caption, note=note)
            DIC_CODE["code"] = 1
            DIC_CODE["msg"] = "添加成功"
        else:
            DIC_CODE["code"] = 0
            DIC_CODE["msg"] = "角色名称不能为空"
        return JsonResponse(DIC_CODE)


class roleDel(View):
    def post(self, request, *args, **kwargs):
        try:
            rid = request.POST.get("rid")
            print(rid)
            role_obj = Role.objects.filter(id=rid).first()
            role_obj.delete()
            DIC_CODE["code"] = 1
            DIC_CODE["msg"] = "删除成功"
        except Exception as e:
            DIC_CODE["code"] = 0
            DIC_CODE["msg"] = "{}".format(e)
            print(e)
        return JsonResponse(DIC_CODE)


class roleEdit(View):
    def get(self, request, *args, **kwargs):
        rid = request.GET.get("rid")
        role_obj = Role.objects.values("id", "caption", "note").filter(id=rid).first()
        print(rid)
        return render(request, "rbac/role/edit.html", locals())

    def post(self, request, *args, **kwargs):
        rid = request.POST.get("rid")
        caption = request.POST.get("caption")
        note = request.POST.get("note")
        print(111, caption, 111, note)
        role_obj = Role.objects.values("id", "caption", "note").filter(id=rid).first()
        if caption != role_obj["caption"] and caption:
            Role.objects.filter(id=rid).update(caption=caption)
        if note != role_obj["note"]:
            Role.objects.filter(id=rid).update(note=note)
        DIC_CODE["code"] = 1
        DIC_CODE["msg"] = "更新成功"
        return JsonResponse(DIC_CODE)


"""
角色授权功能
"""

class roleAuthView(RbacView,View):
    def get(self, request, *args, **kwargs):
        role_auth_objs = Permission.objects.all()
        actions = Action.objects.all()
        roles = Role.objects.all()
        role_objs = Role.objects.values("id", "caption", "note").all()
        rbac_menu_permission = request.session.get("rbac_permission_session_key")
        username = request.session.get("user_info").get("username")
        role_caption = User2Role.objects.values("role__caption").filter(user__username=username).first()
        rbac_list = list(Permission2Action2Role.objects.values("permission__menu", "action__code", "permission__url",
                                                               "permission__caption", "permission__menu__caption",
                                                               "permission__menu__parent").filter(
            Q(permission__url__in=rbac_menu_permission.keys()) & Q(role__caption=role_caption["role__caption"])))
        for i in rbac_list:
            i["permission__url"] = i["permission__url"].split("$")[0]
        return render(request, "rbac/roleToAuth/index.html", locals())


class roleToAuthAdd(View):
    def get(self, request, *args, **kwargs):
        role_auth_objs = Permission.objects.all()
        actions = Action.objects.all()
        roles = Role.objects.all()
        role_objs = Role.objects.values("id", "caption", "note").all()
        rbac_menu_permission = request.session.get("rbac_permission_session_key")
        username = request.session.get("user_info").get("username")
        role_caption = User2Role.objects.values("role__caption").filter(user__username=username).first()
        rbac_list = list(Permission2Action2Role.objects.values("permission__menu", "action__code", "permission__url",
                                                               "permission__caption", "permission__menu__caption",
                                                               "permission__menu__parent").filter(
            Q(permission__url__in=rbac_menu_permission.keys()) & Q(role__caption=role_caption["role__caption"])))
        for i in rbac_list:
            i["permission__url"] = i["permission__url"].split("$")[0]
        return render(request, "rbac/roleToAuth/add.html", locals())

    def post(self, request, *args, **kwargs):
        """
        授权添加
        :param request:  ra_val，id，me_list，ro_list
        :param args:
        :param kwargs:
        :return: json
        """
        try:
            permission = request.POST.get("ra_val").split("-")[0]
            k = Permission.objects.values("id").filter(caption=permission).first()
            actions = request.POST.getlist("me_list[]")
            roles = request.POST.getlist("ro_list[]")
            old_auth2role = Permission2Action2Role.objects.filter(permission__caption=permission).first()
            if not old_auth2role:
                z = Permission2Action2Role.objects.create(permission_id=int(k['id']))
                for i in actions:
                    ac = Action.objects.values("id").filter(caption=i).first()
                    z.action.add(ac["id"])
                for j in roles:
                    ro = Role.objects.values("id").filter(caption=j).first()
                    z.action.add(ro["id"])
                z.save()
                DIC_CODE["code"] = 1
                DIC_CODE["msg"] = "添加成功"
            else:
                DIC_CODE["code"] = 0
                DIC_CODE["msg"] = "权限不能重复"
        except Exception as e:
            print(e)
            DIC_CODE["code"] = 0
            DIC_CODE["msg"] = "{}".format(e)
        return JsonResponse(DIC_CODE)


class roleToAuthDel(RbacView,View):
    def delete(self, request, *args, **kwargs):
        """
        授权删除
        :param request:  zid，
        :param args:
        :param kwargs:
        :return:
        """
        try:
            zid = request.POST.get("zid")
            role_obj = Permission2Action2Role.objects.filter(id=zid).first()
            role_obj.delete()
            DIC_CODE["code"] = 1
            DIC_CODE["msg"] = "删除成功"
        except Exception as e:
            DIC_CODE["code"] = 0
            DIC_CODE["msg"] = "{}".format(e)
            print(e)
        return JsonResponse(DIC_CODE)


class roleToAuthSave(RbacView,View):
    def post(self, request, *args, **kwargs):
        """
        授权编辑后保存
        :param request: zid，method_list_name，role_list_name
        :param args:
        :param kwargs:
        :return:
        """
        zid = request.POST.get("zid")
        menu = request.POST.get("menu")
        method_list_name = request.POST.getlist("method_list[]")
        method_list_id = []
        role_list_id = []
        old_method_list_id = []
        old_role_list_id = []
        role_list_name = request.POST.getlist("role_list[]")

        old_p2a2r = Permission2Action2Role.objects.values("permission__caption","permission__permission2action2role__action",
                                                  "permission__permission2action2role__role").\
            filter(permission__permission2action2role=zid).all()

        # method
        old_method_list = Action.objects.values("id").filter(permission2action2role=zid).all()
        for old_method_id in old_method_list:
            old_method_list_id.append(old_method_id["id"])
        for method_name in method_list_name:
            method_id = Action.objects.values("id").filter(caption=method_name).first()["id"]
            method_list_id.append(method_id)

        # role
        old_role_list = Role.objects.values("id").filter(permission2action2role=zid).all()
        for old_role_id in old_role_list:
            old_role_list_id.append(old_role_id["id"])

        for role_name in role_list_name:
            role_id = Role.objects.values("id").filter(caption=role_name).first()["id"]
            role_list_id.append(role_id)

        ac = Permission2Action2Role.objects.get(id=zid)
        for old_m in old_method_list_id:
            if old_m not in method_list_id:
                # 删除action
                ac.action.remove(old_m)
            else:
                method_list_id.pop(method_list_id.index(old_m))

        for m in method_list_id:
            # 增加action
            ac.action.add(m)

        for old_r in old_role_list_id:
            if old_r not in role_list_id:
                # 删除action
                print("删除",old_r)
                ac.role.remove(old_r)
            else:
                role_list_id.pop(role_list_id.index(old_r))

        for r in role_list_id:
            # 增加action
            print(r,"增加")
            ac.role.add(r)

        ac.save()
        print(old_method_list_id,method_list_id)

        # for k in old_p2a2r:
        #
        # Permission2Action2Role.objects.filter(permission__permission2action2role=zid).update(p=zid)
        # for i in method_list:
        #
        try:
            DIC_CODE["code"] = 1
            DIC_CODE["msg"] = "保存成功"
        except Exception as e:
            DIC_CODE["code"] = 0
            DIC_CODE["msg"] = "保存失败，{}".format(e)
            print(e)
        return JsonResponse(DIC_CODE)


"""
用户功能
"""
from aliyun.service.othHandler import ali_rbac


class usersView(RbacView,View):


    def get(self, request, *args, **kwargs):
        rbac_menu_permission = request.session.get("rbac_permission_session_key")
        username = request.session.get("user_info").get("username")
        role_caption = User2Role.objects.values("role__caption").filter(user__username=username).first()
        rbac_list = list(Permission2Action2Role.objects.values("permission__menu", "action__code", "permission__url",
                                                               "permission__caption", "permission__menu__caption",
                                                               "permission__menu__parent").filter(
            Q(permission__url__in=rbac_menu_permission.keys()) & Q(role__caption=role_caption["role__caption"])))
        for i in rbac_list:
            i["permission__url"] = i["permission__url"].split("$")[0]
        user_list = User.objects.values("id","username","userprofile__phone","userprofile__mobile","userprofile__email",
                                        "roles__role__caption","create_date","userprofile__login_state","userprofile__nickname").all()
        return render(request, "rbac/user/admin-list.html", locals())


class userAdd(View):
    def get(self, request, *args, **kwargs):
        role_list = Role.objects.values().all()
        print(role_list)
        return render(request, "rbac/user/admin-add.html", locals())

    def post(self, request, *args, **kwargs):
        print(request.POST)
        username = request.POST.get("username") # 登录

        nickname = request.POST.get("nickname")
        mobile = request.POST.get("phone")
        email = request.POST.get("email")
        sex = request.POST.get("sex")
        password = request.POST.get("password")

        isUser = User.objects.filter(username=username).first()
        if not isUser:
            # 用户创建
            user = User.objects.create(username=username,password=password)
            user.save()
            user_id = User.objects.values("id").filter(username=user).first()["id"]
            role_id = Role.objects.values("id").filter(caption=sex).first()["id"]
            print(role_id)
            user2role = User2Role.objects.create(user_id=user_id,role_id=role_id)
            print(user2role)
            user2role.save()

            userprofile = UserProfile.objects.create(nickname=nickname,email=email,mobile=mobile,user_id=user_id,)
            userprofile.save()
            # UserProfile.objects.create(nickname=nickname,email=email,mobile=mobile,)
        else:
            print("用户已经存在")
        return JsonResponse(DIC_CODE)


class userDel(View):
    def post(self, request, *args, **kwargs):
        return JsonResponse(DIC_CODE)


class userEdit(View):
    def get(self, request, *args, **kwargs):
        role_auth_objs = Permission.objects.all()
        actions = Action.objects.all()
        roles = Role.objects.all()
        return render(request, "rbac/user/admin-list.html", locals())

    def post(self, request, *args, **kwargs):
        """

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        return JsonResponse(DIC_CODE)


class stateEdit(View):
    def post(self, request, *args, **kwargs):
        id = request.POST.get("id")
        login_state = request.POST.get("login_state")
        ses = UserProfile.objects.values("session").filter(user_id=id).first()["session"]
        if login_state == 0:
            session = UserProfile.objects.values("session").filter(user_id=id)
            session.update(login_state=login_state)
            session.update(session="None")
        else:
            session = UserProfile.objects.values("session").filter(user_id=id). \
                update(login_state=login_state, session='None')
        from django.core.cache import cache
        cache.delete("django.contrib.sessions.cache{}".format(ses))
        return JsonResponse(DIC_CODE)


