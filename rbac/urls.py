from django.conf.urls import url,include
from django.contrib import admin
from rbac.views import rbac


urlpatterns = [
    # url(r'^admin/', admin.site.urls)
    url(r'^$',rbac.rbacView.as_view(),name="rbac"),
    url(r'user$',rbac.usersView.as_view(),name="user_list"),
    url(r'^user/add',rbac.userAdd.as_view(),name="userAdd"),
    url(r'^user/del',rbac.userDel.as_view(),name='userDel'),
    url(r'^user/edit',rbac.userEdit.as_view(),name='userEdit'),
    url(r'^user/state/edit',rbac.stateEdit.as_view(),name='stateEdit'),


    url(r'^menu$',rbac.menu.as_view()),
    url(r'^menu/add',rbac.menuAdd.as_view(),name="menuAdd"),
    url(r'^menu/del',rbac.menuDel.as_view(),name='menuDel'),
    url(r'^menu/edit',rbac.menuEdit.as_view(),name='menuEdit'),
    url(r'^menu/select$',rbac.menuSelect.as_view(),name="menuSelect"),


    url(r'^auth$',rbac.authView.as_view()),
    url(r'^auth/edit$',rbac.authMenuSave.as_view(),name="authMenuSave"),
    url(r'^auth/del$',rbac.authDel.as_view(),name="authDel"),
    url(r'^auth/add$',rbac.authAdd.as_view(),name="authAdd"),


    url(r'^role$',rbac.roleView.as_view()),
    url(r'^role/add$',rbac.roleAdd.as_view(),name="roleAdd"),
    url(r'^role/del$',rbac.roleDel.as_view(),name="roleDel"),
    url(r'^role/edit$',rbac.roleEdit.as_view(),name="roleEdit"),


    url(r'^role2auth$',rbac.roleAuthView.as_view()),
    url(r'^role2auth/add$',rbac.roleToAuthAdd.as_view(),name="roleToAuthAdd"),
    url(r'^role2auth/del$',rbac.roleToAuthDel.as_view(),name="roleToAuthDel"),
    url(r'^role2auth/save$',rbac.roleToAuthSave.as_view(),name="roleToAuthSave"),

]
