import django
from django.conf.urls import url
from django.contrib import admin

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
    url(r'^add_color_api$', views.add_material_api),
    url(r'^material_group_add$', views.add_material_group_tmpl),
    url(r'^add_material_color$', views.add_material_color),
    url(r'^material_colors$', views.colors_list_tmpl),
    url(r'^get_colors_table$', views.get_colors_table),
    url(r'^materials_groups_json$', views.groups_json),
    url(r'^delete_dealer$', views.delete_dealer)
]

