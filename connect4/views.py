from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from connect4online.connect4.models import *

import urllib, json

# Create your views here.

def home_login(request, template_name="connect4/login.html"):

	if (request.user.is_authenticated()):
		print "hurray!"
		template_name = "connect4/index.html"

	elif request.facebook:
		# If we have the access token in the string, use the index template
		template_name = "connect4/index.html"
		
		# Try to access user information with the token
		try:
			content = urllib.urlopen("https://graph.facebook.com/me?%s" % request.facebook).read()
			print content
		except:
			raise Exception # TODO: Change this to some kind of "facebook is down" error page

		data = json.loads(content)
		if "id" not in data:
			template_name = "connect4/login.html"
			# TODO: Clear the cookie in this case, because the access key did not validate
		else:
			# Get or Create a new FacebookUser and User
			username = data['first_name'] + data['id']
			try:
				fb_user = FacebookUser.objects.get(id=data['id'])
			except:
				pass
				# Create new user
				new_user = User.objects.create_user(username, 
													data['email'].decode('utf8'), 
													data['id']
													)
				new_user.first_name = data['first_name']
				new_user.last_name = data['last_name']
				new_user.save()

				# Create new facebook user
				fb_user = FacebookUser.objects.create(id=data['id'], user=new_user)
				fb_user.save()

			# Log user in to create sessionid 
			auth_user = authenticate(username=username, password=data['id'])
			login(request, auth_user)
			

	return render_to_response( template_name,
								{}, 
								context_instance=RequestContext(request)
								)

