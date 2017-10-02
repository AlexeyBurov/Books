from django.contrib import admin
from test_celling.apps.test_site.models import Celling, MaterialDealerPrice, MaterialGroup, Payment, MaterialColor, \
    Setting
from test_celling.apps.test_site.models import Dealer
from test_celling.apps.test_site.models import Order
# Register your models here.

admin.site.register(Celling)
admin.site.register(Order)
admin.site.register(Dealer)
admin.site.register(MaterialDealerPrice)
admin.site.register(MaterialGroup)
admin.site.register(Payment)
admin.site.register(MaterialColor)
admin.site.register(Setting)
