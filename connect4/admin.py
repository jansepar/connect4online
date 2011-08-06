from django.contrib import admin
from connect4online.connect4.models import *

class FacebookUserAdmin(admin.ModelAdmin):
	pass

class GameSessionAdmin(admin.ModelAdmin):
	pass

admin.site.register(FacebookUser, FacebookUserAdmin)
admin.site.register(GameSession, GameSessionAdmin)
