from django.contrib import admin
from .models import User, Categories, Listing, Bid, Comments
# Register your models here.

admin.site.register(User)
admin.site.register(Categories)
admin.site.register(Listing)
admin.site.register(Bid)
admin.site.register(Comments)
