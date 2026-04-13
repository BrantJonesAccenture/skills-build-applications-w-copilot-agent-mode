from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import connection
from djongo import models

from octofit_tracker import models as octo_models

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):

        User = get_user_model()
        Team = octo_models.Team
        Activity = octo_models.Activity
        Leaderboard = octo_models.Leaderboard
        Workout = octo_models.Workout

        # Clear existing data
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()

        # Create Teams
        marvel = Team.objects.create(name='Team Marvel')
        dc = Team.objects.create(name='Team DC')

        # Create Users
        users = [
            User(email='tony@stark.com', username='IronMan', team=marvel),
            User(email='steve@rogers.com', username='CaptainAmerica', team=marvel),
            User(email='bruce@wayne.com', username='Batman', team=dc),
            User(email='clark@kent.com', username='Superman', team=dc),
        ]
        for user in users:
            user.set_password('password')
            user.save()

        # Create Activities
        activities = [
            Activity(user=users[0], type='Run', duration=30, distance=5),
            Activity(user=users[1], type='Swim', duration=45, distance=2),
            Activity(user=users[2], type='Bike', duration=60, distance=20),
            Activity(user=users[3], type='Yoga', duration=50, distance=0),
        ]
        Activity.objects.bulk_create(activities)

        # Create Workouts
        workouts = [
            Workout(name='Morning Cardio', description='Cardio for all heroes'),
            Workout(name='Strength Training', description='Strength for all heroes'),
        ]
        Workout.objects.bulk_create(workouts)

        # Create Leaderboard
        Leaderboard.objects.create(team=marvel, points=100)
        Leaderboard.objects.create(team=dc, points=90)

        # Ensure unique index on email
        with connection.cursor() as cursor:
            cursor.db_conn['users'].create_index('email', unique=True)

        self.stdout.write(self.style.SUCCESS('octofit_db populated with test data.'))

# Models for reference (to be created in octofit_tracker/models.py):
# class Team(models.Model):
#     name = models.CharField(max_length=100)
#
# class Activity(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     type = models.CharField(max_length=50)
#     duration = models.IntegerField()
#     distance = models.FloatField()
#
# class Workout(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.TextField()
#
# class Leaderboard(models.Model):
#     team = models.ForeignKey(Team, on_delete=models.CASCADE)
#     points = models.IntegerField()
