from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Script)
admin.site.register(Rating)
admin.site.register(Comment)
admin.site.register(Suggestion)
admin.site.register(Reading)
admin.site.register(ReadLater)
admin.site.register(Favorite)
admin.site.register(Note)