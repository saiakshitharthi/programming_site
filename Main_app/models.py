import re
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.
class Problems(models.Model):
    Title = models.CharField(max_length=1000)
    Problem_statement = models.TextField()
    Author = models.CharField(max_length=1000)
    Number_of_submissions = models.IntegerField(default=0)
    Number_of_accepted = models.IntegerField(default=0)
    Test_cases = models.TextField()
    Example_test_cases = models.TextField()
    Solution = models.TextField()
    points = models.IntegerField(default=0)

    def __str__(self):

        return self.Title
    def get_absolute_url(self):
        return reverse('Main_app:problem',kwargs={'pk':self.pk})
class User_info(models.Model):

    user = models.OneToOneField(User,on_delete=models.CASCADE,default=True,related_name='user_info')
    is_problemsetter = models.BooleanField(default=False)
    points = models.IntegerField(default=0)
    profile_pic = models.ImageField(upload_to='profile_pics',blank=True)
    def __str__(self):
        return self.user
class Friends(models.Model):
    user1 = models.ForeignKey(User,on_delete=models.CASCADE,related_name='my_friends1')
    user2 = models.ForeignKey(User,on_delete=models.CASCADE,related_name='my_friends2')
    total_challenges = models.IntegerField(default=0)
    number_of_won = models.IntegerField(default=0)
    

class Submissions(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE,default=True,related_name='submissions')
    problem = models.ForeignKey(Problems,on_delete=models.CASCADE,default=True)
    solution = models.TextField()
    accepted = models.BooleanField(default=False)
    def __str__(self):
        t = self.user.username +' '+ self.problem.Title
        return t