from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response

# Create your views here.

def login(request, template_name="connect4/login.html"):
	return render_to_response( template_name,
								{}, 
								context_instance=RequestContext(request)
								)

def game(request, template_name="connect4/index.html"):
	return render_to_response( template_name,
								{}, 
								context_instance=RequestContext(request)
								)
