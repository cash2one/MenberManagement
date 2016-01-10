from django.shortcuts import render, render_to_response
from django.template import Context, RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.contrib.auth.models import User
from django.contrib import auth
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from management.models import *
from datetime import *  
import time


def index(req):
	username = req.session.get('username', '')
	if username:
		user = Menbers.objects.get(user__username=username)
	else:
		user = ''
	content = {'active_menu': 'homepage', 'user': user}
	return render_to_response('index.html', content)


def signup(req):
	if req.session.get('username', ''):
		return HttpResponseRedirect('/')
	status = ''
	if req.POST:
		post = req.POST
		passwd = post.get('passwd', '')
		repasswd = post.get('repasswd', '')
		if passwd != repasswd:
			status = 're_err'
		else:
			username = post.get('username', '')
			if User.objects.filter(username=username):
				status = 'user_exist'
			else:
				newuser = User.objects.create_user(username=username, password=passwd, email=post.get('email', ''))
				newuser.save()
				new_menber = Menbers(
					user=newuser, \
					menber_name =post.get('menber_name'),\
					menber_address = post.get('menber_address',''), \
					menber_city = post.get('menber_city','') , \
					menber_tel = post.get('menber_tel',''), \
					menber_store = post.get('menber_store',''),\
					menber_typ = post.get('menber_typ',''),\
					menber_brand = post.get('menber_brand',''),\
					permission=1,\
				)
				new_menber.save()
				status = 'success'
	content = {'active_menu': 'homepage', 'status': status, 'user': ''}
	return render_to_response('signup.html', content, context_instance=RequestContext(req))


def login(req):
	if req.session.get('username', ''):
		return HttpResponseRedirect('/')
	status = ''
	if req.POST:
		post = req.POST
		username = post.get('username', '')
		password = post.get('passwd', '')
		user = auth.authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				auth.login(req, user)
				req.session['username'] = username
				return HttpResponseRedirect('/')
			else:
				status = 'not_active'
		else:
			status = 'not_exist_or_passwd_err'
	content = {'active_menu': 'homepage', 'status': status, 'user': ''}
	return render_to_response('login.html', content, context_instance=RequestContext(req))


def logout(req):
	auth.logout(req)
	return HttpResponseRedirect('/')


def setpasswd(req):
	username = req.session.get('username', '')
	if username != '':
		user = Menbers.objects.get(user__username=username)
	else:
		return HttpResponseRedirect('/login/')
	status = ''
	if req.POST:
		post = req.POST
		if user.user.check_password(post.get('old', '')):
			if post.get('new', '') == post.get('new_re', ''):
				user.user.set_password(post.get('new', ''))
				user.user.save()
				status = 'success'
			else:
				status = 're_err'
		else:
			status = 'passwd_err'
	content = {'user': user, 'active_menu': 'homepage', 'status': status}
	return render_to_response('setpasswd.html', content, context_instance=RequestContext(req))



def getMenber_list():
	menber_list = Menbers.objects.all()
	menberTypList = set()
	for menber in menber_list:
		menberTypList.add(menber.menber_typ)
	return list(menberTypList)

def viewmenber(req):
	username = req.session.get('username', '')
	if username != '':
		user = Menbers.objects.get(user__username=username)
	else:
		user = ''
	menberTypeList = getMenber_list()
	menber_type = req.GET.get('menber_typ', 'all')
	if menber_type == '':
		menber_lst = Menbers.objects.all()
	elif menber_type not in menberTypeList:
		menber_type = 'all'
		menber_lst = Menbers.objects.all()
	else:
		menber_lst = Menbers.objects.filter(menber_typ=menber_type)

	if req.POST:
		post = req.POST
		keywords = post.get('keywords','')
		menber_lst = Menbers.objects.filter(menber_name__contains=keywords)
		menber_type = 'all'

	paginator = Paginator(menber_lst, 5)
	page = req.GET.get('page')
	try:
		menber_list = paginator.page(page)
	except PageNotAnInteger:
		menber_list = paginator.page(1)
	except EmptyPage:
		menber_list = paginator.page(paginator.num_pages)

	content = {'user': user, 'active_menu': 'viewmenber', 'menberTypeList': menberTypeList, 'menber_type': menber_type, 'menber_list': menber_list}
	return render_to_response('viewmenber.html', content, context_instance=RequestContext(req))


def menber_detail(req):
	username = req.session.get('username','')
	if username != '':
		user = Menbers.objects.get(user__username=username)
	else:
		user = ''
	Id = req.GET.get('id','')
	if Id == '':
		return HttpResponseRedirect('/viewmenber/')
	try:
		menber = Menbers.objects.get(pk=Id)
	except:
		return HttpResponseRedirect('/viewmenber/')

	content = {'user': user, 'active_menu': 'viewmenber', 'menber': menber}
	return render_to_response('menber_detail.html', content)

def getCourse_list():
	course_list = Courses.objects.all()
	courseList = set()
	for clist in course_list:
		courseList.add(clist.course_name)
	return list(courseList)


def qiandao(req):
	username = req.session.get('username','')
	if username != '':
		user = Menbers.objects.get(user__username=username)
	else:
		return HttpResponseRedirect('/login/')
	dt = datetime.now().strftime('%y-%m-%d %I:%M:%S %p') 
	status=''
	course_list = Courses.objects.all()
	#course_nameList = getCourse_list()
	if req.POST:
		post = req.POST  
		sign_mood = post.get('sign_mood','') 
		#cs = Courses.objects.get(pk=Id)
		qiandao = Sign(menber=user,sign_mood=sign_mood)
		qiandao.save()
		status='success'
	content = {'active_menu': 'qiandao', 'user': user,'datetime':dt,'course':course_list,'status': status}
	return render_to_response('qiandao.html', content, context_instance=RequestContext(req))



def viewsign(req):
	username = req.session.get('username', '')
	if username != '':
		user = Menbers.objects.get(user__username=username)
	else:
		user = ''
	sign_list = Sign.objects.filter(menber=user)
	for x in sign_list:
		print(sign_list.sign_date)
		
	paginator = Paginator(sign_list, 5)
	page = req.GET.get('page')
	try:
		sign_list = paginator.page(page)
	except PageNotAnInteger:
		sign_list = paginator.page(1)
	except EmptyPage:
		sign_list = paginator.page(paginator.num_pages)

	content = {'user': user, 'active_menu': 'viewsign','sign_list': sign_list}
	return render_to_response('viewsign.html', content, context_instance=RequestContext(req))




