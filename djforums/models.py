#coding:utf-8
from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
	name      = models.CharField(max_length=30)#分类名
	admins    = models.ManyToManyField(User)#管理员

class Topic(models.Model):#主题类
	subject    = models.CharField(max_length=1024)#主题
	content    = models.TextField()#记录
	num_views  = models.IntegerField(default=1)#浏览数
	num_replys = models.IntegerField(default=0)#回帖数
	category   = models.ForeignKey(Category)#类别
	author     = models.ForeignKey(User)#用户
	created    = models.DateTimeField(auto_now=True)#创建时间
	updated    = models.DateTimeField(auto_now=True)#更新时间
	last_date  = models.DateTimeField(auto_now=True)#最后更新时间
	def _get_photo(self):
		p = UserProfile.objects.get(user=self.author)
		return p
	p =property(_get_photo)

class Reply(models.Model):#回复类
	content    = models.TextField()#记录
	author     = models.ForeignKey(User)#用户
	topic      = models.ForeignKey(Topic)#
	created    = models.DateTimeField(auto_now=True)#创建时间
	updated    = models.DateTimeField(auto_now=True)#更新时间
	def _get_photo(self):
		p = UserProfile.objects.get(user=self.author)
		return p
	p =property(_get_photo)

class UserProfile(models.Model):
	photo      = models.ImageField(upload_to = 'photo',blank=True,null=True)
	nick       = models.CharField(max_length=64,blank=True,null=True)
	email      = models.CharField(max_length=1024,blank=True,null=True)
	url        = models.CharField(max_length=64,blank=True,null=True)
	tel        = models.CharField(max_length=64,blank=True,null=True)
	qq         = models.CharField(max_length=64,blank=True,null=True)
	bio        = models.CharField(max_length=64,blank=True,null=True)
	user       = models.ForeignKey(User,unique=True)
	def _get_photo(self):
		if self.photo:
			return self.photo
		else:
			image = Defaultimg.objects.filter(desc="avatar").order_by('?')
			if len(image):
				return image[0].img
			else:
				return 'default/default.gif'
	get_photo =property(_get_photo)

class Defaultimg(models.Model):
	img      = models.ImageField(upload_to = 'picture',blank=True,null=True)
	desc	 = models.CharField(max_length=64,blank=True,null=True)
