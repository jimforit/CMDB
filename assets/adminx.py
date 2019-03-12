#!/usr/bin/env python
# -*- coding=utf-8 -*-
__author__ = 'jim'
__CreateAt__ = '2019\3\12 13:55'

from assets import models
from . import asset_handler
import xadmin
from xadmin import views

class BaseSetting(object):
    # 开启主题功能
    enable_themes = True
    use_bootswatch = True

# 全局修改，固定写法
class GlobalSettings(object):
    # 修改title
    site_title = '长城物业设备管理界面'
    # 修改footer
    site_footer = '长城物业有限公司'
    # 收起菜单
    menu_style = 'accordion'

class NewAssetAdmin(object):
    list_display = ['asset_type', 'sn', 'model', 'manufacturer', 'c_time', 'm_time']
    list_filter = ['asset_type', 'manufacturer', 'c_time']
    search_fields = ('sn',)

    actions = ['approve_selected_new_assets']

    def approve_selected_new_assets(self, request, queryset):
        # 获得被打钩的checkbox对应的资产
        selected = request.POST.getlist(xadmin.ACTION_CHECKBOX_NAME)
        success_upline_number = 0
        for asset_id in selected:
            obj = asset_handler.ApproveAsset(request, asset_id)
            ret = obj.asset_upline()
            if ret:
                success_upline_number += 1
        # 顶部绿色提示信息
        self.message_user(request, "成功批准  %s  条新资产上线！" % success_upline_number)
    approve_selected_new_assets.short_description = "批准选择的新资产"


class AssetAdmin(object):
    list_display = ['asset_type', 'name', 'status', 'approved_by', 'c_time', "m_time"]


xadmin.site.register(models.Asset, AssetAdmin)
xadmin.site.register(models.Server)
xadmin.site.register(models.StorageDevice)
xadmin.site.register(models.SecurityDevice)
xadmin.site.register(models.BusinessUnit)
xadmin.site.register(models.Contract)
xadmin.site.register(models.CPU)
xadmin.site.register(models.Disk)
xadmin.site.register(models.EventLog)
xadmin.site.register(models.IDC)
xadmin.site.register(models.Manufacturer)
xadmin.site.register(models.NetworkDevice)
xadmin.site.register(models.NIC)
xadmin.site.register(models.RAM)
xadmin.site.register(models.Software)
xadmin.site.register(models.Tag)
xadmin.site.register(models.NewAssetApprovalZone, NewAssetAdmin)
# 将基本配置管理与view绑定
xadmin.site.register(views.BaseAdminView,BaseSetting)

# 将title和footer信息进行注册
xadmin.site.register(views.CommAdminView,GlobalSettings)