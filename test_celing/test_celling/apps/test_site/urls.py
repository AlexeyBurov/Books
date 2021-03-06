import django
from django.conf.urls import url
from django.contrib import admin
from django.views.static import serve

from test_celling import settings
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^orders$', views.orders),
    url(r'^dealers$', views.dealers),
    url(r'^finance$', views.finance),
    url(r'^materials$', views.materials_list_tmpl),
    url(r'^material_groups$', views.materials_group_tmpl),
    url(r'^add_material$', views.add_material_tmpl),
    url(r'^add_order_start$', views.file_upload_template),
    url(r'^add_dealer_page$', views.add_dealer_form),
    url(r'^admin/', admin.site.urls),
    url(r'^save_file$', views.save_file),
    url(r'^add_celling_material$', views.add_celling_material),
    url(r'^get_dealer$', views.get_dealers),
    url(r'^get_orders$', views.get_orders),
    url(r'^login', views.LoginFormView.as_view()),
    url(r'^register/$', views.RegisterFormView.as_view()),
    url(r'^logout$', views.user_logout),
    url(r'^add_order$', views.add_order),
    url(r'^add_dealer$', views.add_dealer),
    url(r'^get_dealer_info$', views.dealer_info),
    url(r'^dealer_payment$', views.dealer_add_payment),
    url(r'^material_group_info$', views.get_available_colors),
    url(r'^materials_expense$', views.materials_expense),
    url(r'^expense_page$', views.expense_page),
    url(r'^add_color_api$', views.add_color_api),
    url(r'^material_group_add$', views.add_material_group_tmpl),
    url(r'^add_material_group_api$', views.add_material_group_api),
    url(r'^add_material_color$', views.add_material_color),
    url(r'^material_colors$', views.colors_list_tmpl),
    url(r'^get_colors_table$', views.get_colors_table),
    url(r'^materials_groups_json$', views.groups_json),
    url(r'^delete_dealer$', views.delete_dealer),
    url(r'^add_material_api$', views.add_material_api),
    url(r'^finance_orders_json$', views.finance_orders),
    url(r'^get_materials_json$', views.get_materials_json),
    url(r'^dealer_edit_api$', views.dealer_edit_api),
    url(r'^get_discounts_for_dealer$', views.get_discounts_for_dealer),
    url(r'^edit_discount$', views.edit_discount),
    url(r'^add_discount$', views.add_discount),
    url(r'^delete_color$', views.delete_color),
    url(r'^delete_material_group$', views.delete_material_group),
    url(r'^material_group_info$', views.material_group_info),
    url(r'^delete_material$', views.delete_material),
    url(r'^edit_material_group$', views.edit_material_group),
    url(r'^get_material_json$', views.get_material_json),
    url(r'^edit_material$', views.edit_material),
    url(r'^delete_order$', views.delete_order),
    url(r'^order_info$', views.order_info),
    url(r'^edit_order$', views.edit_order)
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
