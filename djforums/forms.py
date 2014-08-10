#coding:utf-8
from django.forms import ModelForm
from .models import UserProfile
from .models import Defaultimg
class UserProfileForm(ModelForm):
	class Meta:
		model = UserProfile
		exclude = ['user']
class DefaultimgForm(ModelForm):
	class Meta:
		model = Defaultimg

