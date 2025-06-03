from django.contrib import admin
from .models import skin ,customer,cart,order ,bid, Admin
# Register your models here.
admin.site.register(skin)
admin.site.register(customer)
admin.site.register(bid)
admin.site.register(cart)
admin.site.register(order)
admin.site.register(Admin)
