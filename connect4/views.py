from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.conf import settings

from connect4online.connect4.models import *

import urllib, json

# Create your views here.

def send_move(request):
	'''
	Recieves the move sent by the player.
	'''

	response_dict = {}
	if request.user.is_authenticated():
		# get the facebook user associated with this user
		fb_user = request.user.fb_set.all()[0]

		if request.GET.__contains__('column') and request.GET.__contains__('gameid'):
			column = int(request.GET.get('column'))
			gameid = int(request.GET.get('gameid'))
			try:
				game = GameSession.objects.get(id=gameid)
				print column, gameid

				if game.player1 == fb_user or game.player2 == fb_user:
					# print "column: " + column + " NUM_COLS: " + int(settings.NUM_COLS)
					if column < settings.NUM_COLS and column >= 0:
						print "B"
						# set the previous field to the recent column
						game.previous = column

						# load the game board and update appropriately
						game_data = json.loads(game.gameData) #TODO: fix potential problem with unicode
						game_board = game_data[u'game_board']
						columns = game_data[u'columns']
						player = -1

						if game.player1 == fb_user:
							player = 1
						else:
							player = 2

				else:
					response_dict.update({'success': False, 
											'error': "This game session does not belong to the user associated",
										})
			except Exception, e:
				print e
				response_dict.update({'success': False, 
										'error': "No game session of id %s exists" %gameid,
									})
				
		
		else:
			response_dict.update({'success': False, 
									'error': "No game id and/or column passed to request",
								})

	print response_dict
	return HttpResponse(json.dumps(response_dict), mimetype='application/javascript')

def get_turn(request):
	'''
	Gets the turn, as well as previous move made.
	'''
	pass

def get_challenger(request):
	'''
	Checks to see if a challenger has joined a game session. Call invoked when waiting for opponent
	'''
	response_dict = {}
	if request.user.is_authenticated():
		# get the facebook user associated with this user
		fb_user = request.user.fb_set.all()[0]

		if request.GET.__contains__('gameid'):
			gameid = request.GET.get('gameid')
			try:
				game = GameSession.objects.get(id=gameid)

				if game.player1 == fb_user:
					# Check if the game has an opponent
					if (game.player2 is not None) and (game.status == "closed"):
						response_dict.update({'success': True,
												'gameStatus': "COMPLETE",
												'opponent': game.player2.user.first_name,
											})
					else:
						response_dict.update({'success': True,
												'gameStatus': "PENDING",
											})
						
						
				else:
					response_dict.update({'success': False, 
											'error': "This game session does not belong to this user"
										})
					
			except Exception, e:
				response_dict.update({'success': False, 
										'error': "Game session with that id does not exist"
									})
				

		else:
			response_dict.update({'success': False, 
									'error': "No game id passed to request"
								})

	return HttpResponse(json.dumps(response_dict), mimetype='application/javascript')

def initialize_game(request):
	'''
	Creates a game session on request from /initialize_game/
	If there are no open games, create new game
	If there are open games, join player to that game
	'''
	response_dict = {}
	if request.user.is_authenticated():

		# get the facebook user associated with this user
		fb_user = request.user.fb_set.all()[0]

		# grab all open games
		open_games = GameSession.objects.filter(status="open")

		# check if open session with this player already exists (user likely refreshed)
		if len(open_games) > 0 and open_games[0].player1 == fb_user:
			game = open_games[0]
			player = 1
		else:
			player = None
			if len(open_games) == 0:

				# create json formated 2d array representing game board
				# using dictionary of lists
				game_board = {}
				for row in range(0, settings.NUM_ROWS):
					game_board[row] = [0 for i in range(settings.NUM_COLS)]

				columns = [0 for i in range(settings.NUM_COLS)]

				game_data = {"game_board": game_board, "columns": columns}

				# There are no games open, must create one
				game = GameSession.objects.create(player1=fb_user, gameData=json.dumps(game_data), status="open")
				player = 1
			else:
				# TODO: Must deal with mutual exclusion here. This could result in issues
				game = open_games[0]
				game.player2 = fb_user
				game.status = "closed"
				game.save()
				player = 2
				response_dict.update( {'opponent': game.player1.user.first_name}  );


		response_dict.update({'success': True, 
								'game_id': game.id, 
								'player': player, 
								'gameStatus': game.status }) 
	else:
		response_dict.update({'success': False, 
								'error': 'Not authenticated'})

	return HttpResponse(json.dumps(response_dict), mimetype='application/javascript')




def home_login(request, template_name="connect4/login.html"):
	'''
	Authenticates the user with Facebook, creates accounts
	or loads accounts and authorizes them and creates sessionid
	'''

	if (request.user.is_authenticated()):
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

