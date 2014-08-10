#coding:utf-8
from django.contrib.auth.forms import *
from django.contrib.auth.views import *
from django.contrib.auth.models import *
from django.contrib.auth import authenticate,login
from django.shortcuts import render_to_response,redirect
from django.http import HttpResponseRedirect,HttpResponse
from django.template import RequestContext
from .models import *
from .forms import *
import settings
import Image
import json


def register(request):
        form = UserCreationForm()
        if request.method == 'GET':#只是刷新浏览网页为GET
                return render_to_response('register.html',{'form':form},context_instance=RequestContext(request))
        if request.method == 'POST':#往表单提交数据为POST
                form = UserCreationForm(request.POST)
                if form.is_valid():#判断是否是正确的数据（函数实现）
                        form.save()
                        new_user = authenticate(username=request.POST['username'], password=request.POST['password1'])
                        login(request, new_user)
                        return redirect("/useradmin")#返回到userinfoadmin函数
                return render_to_response('register.html',{'form':form},context_instance=RequestContext(request))

def index(request):
	cates = Category.objects.all()
	top20 = Topic.objects.all().order_by("-id")[:10]#根据ID倒序取出10条
	top22 = Topic.objects.all().order_by("-num_replys")[:9]#根据回复数降序序取出10条
	top23 = Reply.objects.all().order_by("-author")[:1]#最后回复用户 

	top24 =	UserProfile.objects.all().count
	top25 = Topic.objects.all().count
	top26 = Reply.objects.all().count

	if request.user.is_authenticated():
		try:
			u = User.objects.get(id=request.user.id)
			top21 = UserProfile.objects.get(user=u)
			top27 = Topic.objects.filter(author=u).count
			top28 = Reply.objects.filter(author=u).count
			print top27,top28
			d = {'cates':cates, 'top20':top20, 'top21':top21, 'top22':top22, 'top23':top23, 'top24':top24, 'top25':top25, 'top26':top26, 'top27':top27, 'top28':top28}
			return render_to_response('index.html', d, context_instance=RequestContext(request))
		except:
			pass
	d = {'cates':cates, 'top20':top20, 'top22':top22, 'top23':top23, 'top24':top24, 'top25':top25, 'top26':top26, 'top27':0, 'top28':0}
	return render_to_response('index.html', d, context_instance=RequestContext(request))

def addcate(request):
	if request.method == 'POST':
		name = request.POST['name']
		a = Category.objects.filter(name=name)
		if len(a):
			return HttpResponse(json.dumps({'code':'no'}))
		else:
			n = Category()
			n.name = request.POST['name']
			n.save()
			return HttpResponse(json.dumps({'code':'ok','id':n.id}))

def cateshow(request,id):
	cate = Category.objects.get(id=int(id))
	topics = Topic.objects.filter(category=cate).order_by("-id")
	top22 = Topic.objects.all().order_by("-num_replys")[:9]#根据回复数降序序取出10条
	top23 = Reply.objects.all().order_by("-author")[:1]#最后回复用户
	if request.user.is_authenticated():
		try:
			u = User.objects.get(id=request.user.id)
			top21 = UserProfile.objects.get(user=u)
			top27 = Topic.objects.filter(author=u).count
			top28 = Reply.objects.filter(author=u).count
			d = {'topics':topics, 'cate':cate, 'top21':top21, 'top22':top22, 'top23':top23, 'top27':top27, 'top28':top28}
			return render_to_response('cateshow.html', d, context_instance=RequestContext(request))
		except:
			pass
	d = {'topics':topics, 'cate':cate, 'top22':top22, 'top23':top23, 'top27':0, 'top28':0}
	return render_to_response('cateshow.html', d, context_instance=RequestContext(request))
	
def addtopic(request,id):
	if request.method =="POST":
		cate = Category.objects.get(id=int(id))
		t = Topic()
		t.category = cate
		t.subject = request.POST['subject']
		t.content = request.POST['content']
		if request.user.is_authenticated():
			t.author = User.objects.get(id=request.user.id)
			t.save()
			return redirect('/cate/%s'%id)
		else:
			return redirect('/')
			
def replytopic(request,id):
	if request.method =="POST":
		t = Topic.objects.get(id=int(id))
		t.num_replys +=1
		t.save()
		r = Reply()
		r.topic = t
		r.content = request.POST['content']
		r.author = User.objects.get(id=request.user.id)
		r.save()
		return redirect('/topic/%s'%id)

def topicshow(request,id):
	cates = Category.objects.all()
	top22 = Topic.objects.all().order_by("-num_replys")[:9]#根据回复数降序序取出10条
	t = Topic.objects.get(id=int(id))
	t.num_views +=1
	t.save()
	replys = Reply.objects.filter(topic=t)	
	if request.user.is_authenticated():
		try:
			u = User.objects.get(id=request.user.id)
			top21 = UserProfile.objects.get(user=u)
			top27 = Topic.objects.filter(author=u).count
			top28 = Reply.objects.filter(author=u).count
			d = {'cates':cates, 't':t, 'replys':replys, 'top21':top21, 'top22':top22, 'top27':top27, 'top28':top28}
			return render_to_response('topicshow.html', d, context_instance=RequestContext(request))
		except:
			pass
	d = {'cates':cates, 't':t, 'replys':replys, 'top22':top22, 'top27':0, 'top28':0}
	return render_to_response('topicshow.html', d, context_instance=RequestContext(request))		

########################################################

def userinfoadmin(request):
	if request.user.is_authenticated():
		try:
			u = User.objects.get(id=request.user.id)
			p = UserProfile.objects.get_or_create(user=u)[0]
			top21 = UserProfile.objects.get(user=u)
			top22 = Topic.objects.all().order_by("-num_replys")[:9]#根据回复数降序序取出10条
			top27 = Topic.objects.filter(author=u).count
			top28 = Reply.objects.filter(author=u).count
			d = {'u':u, 'p':p, 'top21':top21, 'top22':top22, 'top27':top27, 'top28':top28}
			return render_to_response('userinfoadmin.html', d, context_instance=RequestContext(request))
		except:
			pass
	d = {'u':u, 'p':p, 'top21':top21, 'top22':top22, 'top27':0, 'top28':0}
	return render_to_response('userinfoadmin.html', d, context_instance=RequestContext(request))
		
def updatephoto(request):
	if request.user.is_authenticated():
		try:
			u = User.objects.get(id=request.user.id)
			profile = UserProfile.objects.get(user=u)
			if request.method == "POST":
				p = UserProfileForm(request.POST,request.FILES,instance=profile)#POST图片数据，FILES图片内容，profile用户原始图片信息
				if	p.is_valid():
					p.save()
			return HttpResponse(json.dumps({"image":'%s' % profile.photo}))
		except:
			pass
########################################################
 
def imgCrop(request):
	yimage = request.POST['yimage']
	imageFile = settings.BASE_DIR + yimage
	im1 = Image.open(imageFile)
	(w,h) = im1.size
	if request.POST['cx'] != "":
		x = int(request.POST['cx'])
		y = int(request.POST['cy'])
		x1 = int(request.POST['cx2'])
		y1 = int(request.POST['cy2'])
		box = (x * w / 400, y * h / 400, x1 * w / 400, y1 * h / 400)
		region = im1.crop(box)
		region.save(imageFile)
		return redirect("/useradmin")
	else:
		return redirect("/useradmin")

########################################################

def upload(request):
	if request.user.is_superuser:
		p = Defaultimg.objects.all()# 获取随机头像
		top22 = Topic.objects.all().order_by("-num_replys")[:9]#根据回复数降序序取出10条
		d = {'p':p, 'top22':top22, 'top27':0, 'top28':0}
		return render_to_response('upload.html', d, context_instance=RequestContext(request))
	else:
		return redirect("/")

def uploadphoto(request):
	if request.user.is_superuser:
		if request.method == "POST":
			p = DefaultimgForm(request.POST,request.FILES)#POST图片数据，FILES图片内容，profile用户原始图片信息
			if p.is_valid():
				p.save()
		return redirect('/upload')
	else:
		return redirect('/')

########################################################

def UserProfile_update_save(request):
	if request.user.is_authenticated():
		try:
			u = User.objects.get(id=request.user.id)
			b = UserProfile.objects.get_or_create(user=u)[0]
			b.nick = request.POST['nick']
			b.email = request.POST['email']
			b.url = request.POST['url']
			b.tel = request.POST['tel']
			b.qq = request.POST['qq']
			b.bio = request.POST['bio']
			b.save()
			return redirect('/useradmin')
		except:
			pass

########################################################

def topic_delete(request,id):
	u = Topic.objects.get(id=int(id))
	if request.user == u.author:
		Topic.objects.get(id=int(id)).delete()
		return redirect('/')
	else:
		return redirect('/')

def topic_update(request,id):
	b = Topic.objects.get(id=int(id))
	if request.user == b.author:
		b.subject = request.POST['subject']
		b.content = request.POST['content']
		b.save()
		return redirect('/topic/%s'%id)
	else:
		return redirect('/')

########################################################


