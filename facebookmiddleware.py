from django.conf import settings
from django.http import HttpRequest

class SetFacebookAccessToken(object):
	def process_request(self, request):
		if (settings.YOUR_APP_ID and settings.YOUR_APP_SECRET):
			try:
				access_key = request.COOKIES['fbs_' + settings.YOUR_APP_ID]
				request.facebook = access_key
			except:
				request.facebook = None

			return None
				
		else:
			raise Exception
