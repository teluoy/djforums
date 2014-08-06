#coding:utf-8
from django.contrib.auth.forms import *
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
	top22 = Topic.objects.all().order_by("-num_replys")[:10]#根据回复数降序序取出10条
	if request.user.is_authenticated():
		try:
			u = User.objects.get(id=request.user.id)
			top21 = UserProfile.objects.get(user=u)

			d = {'cates':cates, 'top20':top20, 'top21':top21, 'top22':top22}
			return render_to_response('index.html', d, context_instance=RequestContext(request))
		except:
			pass
	d = {'cates':cates, 'top20':top20, 'top22':top22}
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
	u = User.objects.get(id=request.user.id)
	top21 = UserProfile.objects.get(user=u)
	d = {'topics':topics, 'cate':cate, 'top21':top21}
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
	t = Topic.objects.get(id=int(id))
	t.num_views +=1
	t.save()
	replys = Reply.objects.filter(topic=t)
	u = User.objects.get(id=request.user.id)
	top21 = UserProfile.objects.get(user=u)
	d = {'cates':cates, 't':t, 'replys':replys, 'top21':top21}
	return render_to_response('topicshow.html', d, context_instance=RequestContext(request))
		
########################################################

def userinfoadmin(request):
	u = User.objects.get(id=request.user.id)
	p = UserProfile.objects.get_or_create(user=u)[0]
	u = User.objects.get(id=request.user.id)
	top21 = UserProfile.objects.get(user=u)
	d = {'u':u, 'p':p, 'top21':top21}
	return render_to_response('userinfoadmin.html', d, context_instance=RequestContext(request))
		
def updatephoto(request):
	u = User.objects.get(id=request.user.id)
	profile = UserProfile.objects.get(user=u)
	if request.method == "POST":
		p = UserProfileForm(request.POST,request.FILES,instance=profile)#POST图片数据，FILES图片内容，profile用户原始图片信息
		if	p.is_valid():
			p.save()
	return HttpResponse(json.dumps({"image":'%s' % profile.photo}))

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
	p = Defaultimg.objects.all()
	u = User.objects.get(id=request.user.id)
	top21 = UserProfile.objects.get(user=u)
	d = {'p':p, 'top21':top21}
	return render_to_response('upload.html', d, context_instance=RequestContext(request))

def uploadphoto(request):
	if request.method == "POST":
		p = DefaultimgForm(request.POST,request.FILES)#POST图片数据，FILES图片内容，profile用户原始图片信息
		if p.is_valid():
			p.save()
	return redirect('/upload')

########################################################

def UserProfile_update_save(request):
	u = User.objects.get(id=request.user.id)
	b = UserProfile.objects.get_or_create(user=u)[0]
	b.nick = request.POST['nick']
	b.email = request.POST['email']
	b.qq = request.POST['qq']
	b.save()
	return redirect("/useradmin")

########################################################

