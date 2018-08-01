from django.contrib.auth.models import User
from django import forms
from .models import Thing, Category




class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ['category_title']


class ThingForm(forms.ModelForm):

	class Meta:
		model = Thing
		fields = ['category', 'thing_title', 'description', 'thing_picture', 'location', 'notes']


class UserForm(forms.ModelForm):
	password =forms.CharField(widget=forms.PasswordInput)


	class Meta:
		model = User
		fields = ['username', 'email', 'password']