from django.shortcuts import render, render_to_response
from django.template import Context, RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.contrib.auth.models import User
from django.contrib import auth
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from management.models import *
from django.utils import timezone


def index(req):
	username = req.session.get('username', '')
	if username:
		user = Employee.objects.get(user__username=username)
	else:
		user = ''
	content = {'active_menu': 'homepage', 'user': user}
	return render_to_response('index.html', content)


def signup(req):
	if req.session.get('username', ''):
		return HttpResponseRedirect('/')
	status = ''
	departs = Department.objects.all()
	if req.POST:
		post = req.POST
		passwd = post.get('passwd', '')
		repasswd = post.get('repasswd', '')
		depart_name = post.get('partment','')
		depart = Department.objects.get(depart_name=depart_name)
		if passwd != repasswd:
			status = 're_err'
		else:
			username = post.get('username', '')
			if User.objects.filter(username=username):
				status = 'user_exist'
			else:
				newuser = User.objects.create_user(username=username, password=passwd, email=post.get('email', ''))
				newuser.save()
				new_employee = Employee(
					user=newuser, \
					name =post.get('name',''),\
					tel = post.get('tel',''), \
					department = depart,\
					permission=1,\
				)
				new_employee.save()
				status = 'success'
	content = {'active_menu': 'homepage', 'status': status, 'user': '','departs':departs}
	return render_to_response('sign.html', content, context_instance=RequestContext(req))


def login(req):
	if req.session.get('username',''):
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
	dt = timezone.localtime(timezone.now())
	#dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	status=''
	course_list = Courses.objects.all()
	#course_nameList = getCourse_list()
	if req.POST:
		post = req.POST  
		sign_mood = post.get('sign_mood','') 
		Id = post.get('course_id','')
		live = post.get('live','')
		if Id != '' and live=='huangguan':
			cs = Courses.objects.get(pk=Id)
			qiandao = Sign(courses=cs,sign_mood=sign_mood)
			qiandao.save()
			user.sign.add(qiandao)
			status='success'
		else:
			status = 'sign_er'
			content = {'active_menu': 'qiandao','status':status, 'user': user ,'course':course_list }
			return render_to_response('qiandao.html', content)
			#return HttpResponseRedirect('/qiandao/')
	content = {'active_menu': 'qiandao', 'user': user,'datetime':dt,'course':course_list,'status': status}
	return render_to_response('qiandao.html', content, context_instance=RequestContext(req))



def viewsign(req):
	username = req.session.get('username', '')
	if username != '':
		user = Menbers.objects.get(user__username=username)
	else:
		user = ''
	sign_list = user.sign.all()
	
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


def getPerson_typ():
	persons = Person.objects.all()
	partTypList = set()
	for part in persons:
		partTypList.add(part.partment)
	return list(partTypList)


def songli(req):
	#persons = Person.objects.all()
	person_typlst = getPerson_typ()
	person_type = req.GET.get('partment', 'all')
	if person_type == '':
		persons = Person.objects.all()
	elif person_type not in person_typlst:
		person_type = 'all'
		persons = Person.objects.all()
	else:
		persons = Person.objects.filter(partment=person_type)
	if req.POST:
		post = req.POST
		keywords = post.get('keywords','')
		persons = Person.objects.filter(tel__contains=keywords)
		person_type = 'all'

	paginator = Paginator(persons, 5)
	page = req.GET.get('page')
	try:
		persons = paginator.page(page)
	except PageNotAnInteger:
		persons = paginator.page(1)
	except EmptyPage:
		persons = paginator.page(paginator.num_pages)

	content = {'active_menu': 'songli', 'person_lst': persons, 'person_typlst': person_typlst, 'person_type': person_type,}
	return render_to_response('songliren.html', content, context_instance=RequestContext(req))

def lingfou(friends):
	lipin = set()
	for fd in friends:
		p = Person.objects.filter(tel=fd.f_tel)
		if p[0] != []:
			lipin.add('yiling')
		else:
			lipin.add('weiling')

	return list(lipin)

def songli_detail(req):
	Id = req.GET.get('id','')
	#status=''
	if Id == '':
		return HttpResponseRedirect('/songli/')
	try:
		person = Person.objects.get(pk=Id)
		friends = person.friends_set.all()
		#linglipin = lingfou(friends)
		#status = 'success'
	except:
		return HttpResponseRedirect('/songli/')
	content = {'active_menu': 'songli', 'p_friends': friends,'person':person}
	return render_to_response('friends.html', content, context_instance=RequestContext(req))

def toaddperson(req):
	status = ''
	p = Person.objects.all()
	if req.GET:
		Id = req.GET.get('id','')
		part = req.GET.get('part','')
		fd = Friends.objects.get(pk=Id)
		if Person.objects.filter(tel__contains=fd.f_tel):
			status = 'user_exist'
			content = {'active_menu': 'addsongli'}
			return render_to_response('user_exist.html', content,context_instance=RequestContext(req))
		else:
			person = Person(name=fd.f_name,tel=fd.f_tel,gift=fd.f_gift,remarks=fd.f_remarks,partment=part)
			person.save()
			status='success'
	content = {'active_menu': 'addsongli','person_lst':p}
	return render_to_response('addlingli.html', content, context_instance=RequestContext(req))


def addsongli(req):
	persons = Person.objects.all()

	paginator = Paginator(persons,5)
	page = req.GET.get('page')
	try:
		persons = paginator.page(page)
	except PageNotAnInteger:
		persons = paginator.page(1)
	except EmptyPage:
		persons = paginator.page(paginator.num_pages)

	content = {'active_menu': 'addsongli', 'person_lst': persons}
	return render_to_response('addlingli.html', content, context_instance=RequestContext(req))

def friendsqiaojie(req):
	status = ''
	if req.GET:
		Id = req.GET.get('id','')
		if Id == '':
			return HttpResponseRedirect('/addsongli/')
		try:
			person = Person.objects.get(pk=Id)

		except:
			status = 'error'
			return  HttpResponseRedirect('/addsongli/')


	content = {'active_menu': 'addsongli', 'person': person,'status': status}
	return render_to_response('addfriends.html', content, context_instance=RequestContext(req))

def modifyfriendslingli(req):
	status = ''
	if req.GET:
		Id = req.GET.get('id','')

		if Id == '':
			return HttpResponseRedirect('/addsongli/')
		try:
			Friends.objects.filter(id=Id).update(f_gift=u'水晶吊坠')
			friend = Friends.objects.get(pk=Id)
			status = 'sucess'
		except:
			status = 'error'
			return HttpResponseRedirect('/addsongli/')

	content = {'active_menu': 'addsongli', 'friend': friend,'status': status}
	return render_to_response('friendslingli.html', content, context_instance=RequestContext(req))


def addfriends(req):
	status=''
	if req.POST:
		post = req.POST
		name = post.get('f_name','')
		tel = post.get('f_tel','')
		gift = u'未领'
		remarks = post.get('f_remarks','')
		Id = post.get('f_id','')
		person = Person.objects.get(pk=Id)

		if Friends.objects.filter(f_tel__contains=tel):
			status = 'user_exist'
			content = {'active_menu': 'addsongli'}
			return render_to_response('user_exist.html', content,context_instance=RequestContext(req))

		else:
			friend = Friends(person=person,f_name=name,f_tel=tel,f_gift=gift,f_remarks=remarks)
			friend.save()
			status='success'
	content = {'active_menu': 'addsongli', 'person': person,'status': status}
	return render_to_response('addfriends.html', content, context_instance=RequestContext(req))

def addperson(req):
	status=''

	if req.POST:
		post = req.POST
		name = post.get('name','')
		tel = post.get('tel','')
		gift = post.get('gift','')
		partment = post.get('partment','')
		remarks = post.get('remarks','')

		if Person.objects.filter(tel=tel):
			status = 'user_exist'
			content = {'active_menu': 'addlingli','status':status }
			return render_to_response('addperson.html', content)
		else:
			person = Person(name=name,tel=tel,gift=gift,remarks=remarks,partment=partment)
			person.save()
			status='success'

	content = {'active_menu': 'addlingli','status': status}
	return render_to_response('addperson.html', content, context_instance=RequestContext(req))

def addpersonnels(req):
	status = ''
	personnel = ''
	username = req.session.get('username','')
	if username != '':
		user = Menbers.objects.get(user__username=username)
	else:
		return HttpResponseRedirect('/login/')
	'''
	if user.permission < 2:
		return HttpResponseRedirect('/')
		'''
	if req.POST:
		post = req.POST
		personnel = Personnel(
			job = post.get('job',''),\
			form_date = post.get('form_date',''),\
			name = post.get('name',''),\
			sex = post.get('sex',''),\
			birth_date = post.get('birth_date',''),\
			height = post.get('height',''),\
			weight = post.get('weight',''),\
			jiguan = post.get('jiguan',''),\
			xingge = post.get('xingge',''),\
			minzu = post.get('minzu',''),\
			marry = post.get('marry',''),\
			tel = post.get('tel',''),\
			skill = post.get('skill',''),\
			wenping = post.get('wenping',''),\
			shenfenzheng = post.get('shenfenzheng',''),\
			daogang = post.get('daogang',''),\
			huji = post.get('huji',''),\
			address = post.get('address',''),\
			salary = post.get('salary',''),\
			obey  = post.get('obey',''),\
			other = post.get('other',''),\
			evaluate = post.get('evaluate',''),\
			qq = post.get('qq',''),\
			email = post.get('email',''),\
			personnel_typ = post.get('personnel_typ',''),\
		)
		personnel.save()
      #教育培训背景
		edu_start = post.getlist('edu_start',[])
		edu_end = post.getlist('edu_end',[])
		college = post.getlist('college',[])
		professional = post.getlist('professional',[])
		education = post.getlist('education',[])
		nature = post.getlist('nature',[])
		mark = post.getlist('mark',[])

		for index in range(len(college)):
			if college[index] != '':
				edu = Education(
					personnel = personnel,\
					edu_start = edu_start[index],\
					edu_end = edu_end[index],\
					college = college[index],\
					professional = professional[index],\
					education = education[index],\
					nature = nature[index],\
					mark = mark[index],\
				)
				edu.save()
			else:
				break

		#家庭背景
		re_name = post.getlist('re_name',[])
		relation = post.getlist('relation',[])
		work = post.getlist('work',[])
		re_job = post.getlist('re_job',[])
		re_tel = post.getlist('re_tel',[])
		for reindex in range(len(re_name)):
			if re_name[reindex] != '':
				relative = Relative(
					personnel = personnel,\
					re_name = re_name[reindex],\
					relation = relation[reindex],\
					work = work[reindex],\
					re_job = re_job[reindex],\
					re_tel = re_tel[reindex],\
				)
				relative.save()
			else:
				break

        #工作经验
		w_start = post.getlist('w_start',[])
		w_end = post.getlist('w_end',[])
		company = post.getlist('company',[])
		w_job = post.getlist('w_job',[])
		w_salary = post.getlist('w_salary',[])
		quit = post.getlist('quit','')
		references = post.getlist('references',[])
		w_tel = post.getlist('w_tel',[])
		for windex in range(len(company)):
			if company[windex] != '':
				exp = WorkExperience(
					personnel = personnel,\
					w_start = w_start[windex],\
					w_end = w_end[windex],\
					company = company[windex],\
					w_job = w_job[windex],\
					w_salary = w_salary[windex],\
					quit = quit[windex],\
					references = references[windex],\
					w_tel = w_tel[windex],\
					)
				exp.save()
			else:
				break

		status = 'success'
	content = {'active_menu': 'addpersonnel','status': status,'user':user,'personnel':personnel}
	return render_to_response('personnel.html', content, context_instance=RequestContext(req))

def getDpartment():
	employee_list = Employee.objects.all()
	employeeTypList = set()
	for employee in employee_list:
		employeeTypList.add(employee.department)
	return list(employeeTypList)


def viewEmployee(req):
	username = req.session.get('username','')
	if username != '':
		user = Employee.objects.get(user__username=username)
	else:
		user = ''
	departments = getDpartment()
	department_type = req.GET.get('department','all')
	depart = Department.objects.get(depart_name=department_type)
	if department_type == '':
		employee_list = Employee.objects.all()
	elif department_type not in departments:
		department_type = 'all'
		employee_list = Employee.objects.all()
	else:
		employee_list = depart.employee_set.all()

	if req.POST:
		post = req.POST
		keywords = post.get('keyword','')
		employee_list = Employee.objects.filter(name__contains=keywords)
		department_type = 'all'

	paginator = Paginator(employee_list,5)
	page = req.GET.get('page')
	try:
		employee_list = paginator.page(page)
	except PageNotAnInteger:
		employee_list = paginator.page(1)
	except EmptyPage:
		employee_list = paginator.page(paginator.num_pages)

	content = {'active_menu': 'viewEmployee','departments':departments,'department_type':department_type,'user':user,'employee_list':employee_list}
	return render_to_response('viewEmployee.html', content, context_instance=RequestContext(req))

def personnel_detail(req):

	username = req.session.get('username','')
	if username != '':
		user = Menbers.objects.get(user__username=username)
	else:
		return HttpResponseRedirect('/login/')

	Id = req.GET.get('id','')
	try:
		personnel = Personnel.objects.get(pk=Id)
		relation = personnel.relative_set.all()
		education = personnel.education_set.all()
		work = personnel.workexperience_set.all()
	except:
		return HttpResponseRedirect('/viewpersonnels')

	content = {'active_menu': 'viewpersonnels','user':user,'personnel':personnel,'education':education,'work':work,'relation':relation}
	return render_to_response('personnel_detail.html', content, context_instance=RequestContext(req))

def modify_typ(req):
	status = ''
	username = req.session.get('username','')
	if username != '':
		user = Menbers.objects.get(user__username=username)
	else:
		return HttpResponseRedirect('/login/')

	Id = req.GET.get('id','')
	try:
		personnel = Personnel.objects.get(pk=Id)
	except:
		return HttpResponseRedirect('/viewpersonnels')

	if req.POST:
		post = req.POST
		pid = post.get('pid','')
		personnel_type = post.get('personnel_typ','')
		personnel_evaluate = post.get('evaluate','')

		try:
			Personnel.objects.filter(id=pid).update(personnel_typ=personnel_type,evaluate=personnel_evaluate)
			status = "success"
		except:
			return HttpResponseRedirect('/viewpersonnels/')

	content = {'active_menu': 'viewpersonnels','status':status,'user':user,'personnel':personnel}
	return render_to_response('modify_typ.html', content, context_instance=RequestContext(req))



def addweekmeeting(req):
	status = ''
	username = req.session.get('username','')
	if username != '':
		user = Menbers.objects.get(user__username=username)
	else:
		return HttpResponseRedirect('/login/')

	if req.POST:
		post = req.POST
		meeting  = weekmeeting(
			week = post.get('week',''),\
			lastweek = post.get('lastweek',''),\
			nextweek = post.get('nextweek',''),\
			last_exeperson = post.get('last_exeperson',''),\
			last_comletiontime = post.get('last_comletiontime',''),\
			comletioneffect = post.get('comletioneffect',''),\
			meeting = post.get('meeting',''),\
			next_comletiontime = post.get('next_comletiontime',''),\
			next_exeperson = post.get('next_exeperson',''),\
			menber = user,\
		)
		meeting.save()
		status = 'success'

	content = {'active_menu': 'addweekmeeting','status':status,'user':user}
	return render_to_response('weekmeeting.html', content, context_instance=RequestContext(req))


def viewmeeting(req):
	username = req.session.get('username','')
	if username != '':
		user = Menbers.objects.get(user__username=username)
	else:
		user = ''

	meetings = weekmeeting.objects.all()

	content = {'active_menu': 'addweekmeeting','status':status,'user':user}
	return render_to_response('weekmeeting.html', content, context_instance=RequestContext(req))



"""
edu_satrt = post.getlist('edu_start',[])
		edu_end = post.getlist('edu_end',[])
		college = post.getlist('college',[])
		professional = post.getlist('professional',[])
		education = post.getlist('education',[])
		nature = post.getlist('nature',[])
		mark = post.getlist('mark',[])

		re_name = post.getlist('re_name',[])
		relation = post.getlist('relation',[])
		work = post.getlist('work',[])
		re_job = post.getlist('re_job',[])
		re_tel = post.getlist('re_tel',[])

		w_start = post.getlist('w_start',[])
		w_end = post.getlist('w_end',[])
		company = post.getlist('company',[])
		w_job = post.getlist('w_job',[])
		w_salary = post.getlist('w_salary',[])
		quit = post.getlist('quit','')
		references = post.getlist('references',[])
		w_tel = post.getlist('w_tel',[])
代码重构，共性的东西抽取出来。
urlpatterns = patterns(
(r'^events/$',views.object_list,{'model':models.Event}),
(r'^blog/entries/$',view.object_list,{'model':model.BlogEntry}),
)

def object_list(request,model):
   obj_list = model.objects.all()
   template_name = 'mysite/%s_list.html'%model.__name__.lower()
   return render_to_response(template_name,{'object_list':boj_list})
"""




