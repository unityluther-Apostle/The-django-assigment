from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Announcement(models.Model):
	CATEGORY_CHOICE = [
		('news' , 'School News'),
		('entertainment','Entertainment'),
	]
	title = models.CharField(max_length=200)
	body = models.TextField()
	
	category = models.CharField(max_length=20, choices=CATEGORY_CHOICE)
	published_date = models.DateTimeField(auto_now_add=True)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	
	class Meta:
		
		ordering = ['-published_date']
		
	def __str__(self):
		return self.title
		
class ReadStatus(models.Model):
	student = models.ForeignKey(User, on_delete=models.CASCADE)
	announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)
	read_at = models.DateTimeField(auto_now_add=True)
	
	class Meta:
		unique_together = ('student','announcement')
		
	def __str__(self):
		return f"{self.student.username} read '{self.announcement.title}'"
