from django.db import models
from django.urls import reverse
from django.contrib.auth.models import Permission, User

# Create your models here.
class Category(models.Model):
	user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
	category_title = models.CharField(max_length=200) 


	def __str__(self):
		return self.category_title 


class Thing(models.Model):
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	thing_title = models.CharField(max_length=500)
	description = models.CharField(max_length=500)
	thing_picture = models.FileField()
	location = models.CharField(max_length=500)
	notes = models.CharField(max_length=500)

	# def get_absolute_url(self):
	# 	return reverse('things:detail', kwargs={'pk': self.pk})

	def __str__(self):
		return self.thing_title + ' - ' + self.location

	class Meta:
	        verbose_name = 'thing'
	        verbose_name_plural = 'things'
	    

	
