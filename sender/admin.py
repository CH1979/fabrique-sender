from django.contrib import admin

from .models import Customer, Maillist, Message, Operator, Tag


admin.site.register(Customer)
admin.site.register(Maillist)
admin.site.register(Message)
admin.site.register(Operator)
admin.site.register(Tag)
