from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class FacebookUser(models.Model):
	id     = models.IntegerField(primary_key=True)
	wins   = models.IntegerField(default=0)
	losses = models.IntegerField(default=0)
	user   = models.ForeignKey(User, unique=True)

class GameSession(models.Model):
	id       = models.AutoField(primary_key=True)
	player1  = models.ForeignKey(FacebookUser, related_name="player1_set")
	player2  = models.ForeignKey(FacebookUser, related_name="player2_set")
	turn     = models.IntegerField()
	gameData = models.TextField()
	STATUS_CHOICES = (
		('open',     'open'),
		('closed',   'closed'),
		('finished', 'finished'),
	)
	status   = models.CharField(max_length=16, choices=STATUS_CHOICES)
