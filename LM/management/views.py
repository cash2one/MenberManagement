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
		user = Members.objects.get(user__username=username)
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
		membername = post.get('membername','')
		membertel = post.get('membertel','')
		if passwd != repasswd:
			status = 're_err'
		else:
			username = post.get('username', '')
			if User.objects.filter(username=username):
				status = 'user_exist'
			else:
				newuser = User.objects.create_user(username=username, password=passwd, email=post.get('email', ''))
				newuser.save()
				member = Members(
					user=newuser, \
					membername =membername,\
					membertel = membertel, \
					permission=1,\
				)
				member.save()
				status = 'success'
	content = {'active_menu': 'homepage', 'status': status, 'user': ''}
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
		user = Members.objects.get(user__username=username)
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

def viewmember(req):
	username = req.session.get('username', '')
	if username != '':
		user = Members.objects.get(user__username=username)
	else:
		return HttpResponseRedirect('/login/')


	memberlist = Members.objects.all()

	paginator = Paginator(memberlist, 10)
	page = req.GET.get('page')
	try:
		memberlist = paginator.page(page)
	except PageNotAnInteger:
		memberlist = paginator.page(1)
	except EmptyPage:
		memberlist = paginator.page(paginator.num_pages)


	content = {'user': user, 'active_menu':'member', 'memberlist':memberlist}
	return render_to_response('viewmemberlist.html', content, context_instance=RequestContext(req))

'''
def getMember_list():
	member_list = Members.objects.all()
	memberTypList = set()
	for member in member_list:
		memberTypList.add(member.member_typ)
	return list(memberTypList)

def viewmember(req):
	username = req.session.get('username', '')
	if username != '':
		user = Members.objects.get(user__username=username)
	else:
		user = ''
	memberTypeList = getMember_list()
	member_type = req.GET.get('member_typ', 'all')
	if member_type == '':
		member_lst = Members.objects.all()
	elif member_type not in memberTypeList:
		member_type = 'all'
		member_lst = Members.objects.all()
	else:
		member_lst = Members.objects.filter(member_typ=member_type)

	if req.POST:
		post = req.POST
		keywords = post.get('keywords','')
		member_lst = Members.objects.filter(member_name__contains=keywords)
		member_type = 'all'

	paginator = Paginator(member_lst, 5)
	page = req.GET.get('page')
	try:
		member_list = paginator.page(page)
	except PageNotAnInteger:
		member_list = paginator.page(1)
	except EmptyPage:
		member_list = paginator.page(paginator.num_pages)

	content = {'user': user, 'active_menu': 'viewmember', 'memberTypeList': memberTypeList, 'member_type': member_type, 'member_list': member_list}
	return render_to_response('viewmember.html', content, context_instance=RequestContext(req))


def member_detail(req):
	username = req.session.get('username','')
	if username != '':
		user = Members.objects.get(user__username=username)
	else:
		user = ''
	Id = req.GET.get('id','')
	if Id == '':
		return HttpResponseRedirect('/viewmember/')
	try:
		member = Members.objects.get(pk=Id)
	except:
		return HttpResponseRedirect('/viewmenber/')

	content = {'user': user, 'active_menu': 'viewmember', 'member': member}
	return render_to_response('member_detail.html', content)

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
			return render_to_response('modifyemployee.html', content)
		else:
			person = Person(name=name,tel=tel,gift=gift,remarks=remarks,partment=partment)
			person.save()
			status='success'

	content = {'active_menu': 'addlingli','status': status}
	return render_to_response('modifyemployee.html', content, context_instance=RequestContext(req))

	'''

def addemployee(req):
	status  = ''
	username = req.session.get('username','')
	if username != '':
		user = Members .objects.get(user__username=username)
	else:
		user = ''
		return HttpResponseRedirect('/login/')
	departs = Department.objects.all()
	if req.POST:
		post = req.POST
		name = post.get('name', '')
		tel = post.get('tel', '')
		email = post.get('email','')
		depart_name = post.get('partment','')
		if depart_name == '0' or depart_name == 0:
			status = 're_err'
		else:
			depart = Department.objects.get(depart_name=depart_name)
			if Employee.objects.filter(name=name):
				status = 'user_exist'
			else:
				new_employee = Employee(
					name =name,\
					tel = tel, \
					department = depart,\
					email = email,\
					permission=1,\
					)
				new_employee.save()
				status = 'success'

	content = {'active_menu': 'addemployee','user':user,'status':status,'departs':departs}
	return render_to_response('addemployee.html', content, context_instance=RequestContext(req))


def modifyemployee(req):
	status = ''
	username = req.session.get('username','')
	if username != '':
		user = Employee.objects.get(user__username=username)
	else:
		return HttpResponseRedirect('/login/')

	if req.GET:
		Id = req.GET.get('id','')

	if Id == '':
		return HttpResponseRedirect('/viewmeeting/')
	else:
		employee = Employee.objects.get(pk=Id)
	'''
	if user.permission < 2:
		return HttpResponseRedirect('/')
		'''
	if req.POST:
		post = req.POST
		employee = Employee(
			job = post.get('job',''),\
			registdate = post.get('registdate',''),\
			sex = post.get('sex',''),\
			birthday = post.get('birthday',''),\
			height = post.get('height',''),\
			weight = post.get('weight',''),\
			birthplace = post.get('jiguan',''),\
			character = post.get('character',''),\
			national = post.get('national',''),\
			marry = post.get('marry',''),\
			skill = post.get('skill',''),\
			diploma = post.get('diploma',''),\
			identity = post.get('identity',''),\
			working = post.get('working',''),\
			huji = post.get('huji',''),\
			address = post.get('address',''),\
			salary = post.get('salary',''),\
			obey  = post.get('obey',''),\
			other = post.get('other',''),\
			evaluate = post.get('evaluate',''),\
			qq = post.get('qq',''),\
			status = post.get('status',''),\
			emergcontact = post.get('emergcontact',''),\
			emergcall = post.get('emergcall',''),\
			profileimg = post.get('profileimg',''),\
			eduimg = post.get('eduimg',''),\
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
	content = {'active_menu': 'modifyemployee','status': status,'user':user,'employee':employee}
	return render_to_response('employee.html', content, context_instance=RequestContext(req))


def viewemployee(req):
	username = req.session.get('username','')
	if username != '':
		user = Members.objects.get(user__username=username)
	else:
		user = ''
		return HttpResponseRedirect('/login/')


	alldepartment = Department.objects.all()

	Id = req.GET.get('id','')
	if Id == '' or Id == 'all':
		Id = 'all'
		employee_list = Employee.objects.all()
	else:
		try:
			department = Department.objects.get(pk=Id)
			employee_list = Employee.objects.filter(department=department)
		except:
			return HttpResponseRedirect('/viewemployee/')

	paginator = Paginator(employee_list,9)
	page = req.GET.get('page')
	try:
		employee_list = paginator.page(page)
	except PageNotAnInteger:
		employee_list = paginator.page(1)
	except EmptyPage:
		employee_list = paginator.page(paginator.num_pages)

	content = {'active_menu': 'viewemployee','departments':alldepartment,'Id':Id,'user':user,'employee_list':employee_list}
	return render_to_response('allemployee.html', content, context_instance=RequestContext(req))

#添加员工基础信息
def basemployee(req):
	result = ''
	username = req.session.get('username','')
	if username != '':
		user = Members.objects.get(user__username=username)
	else:
		return HttpResponseRedirect('/login/')

	if req.GET:
		Id = req.GET.get('id','')
		employee = Employee.objects.get(pk=Id)

	if req.POST:
		post = req.POST
		eid = post.get('eid','')
		job = post.get('job','')
		registdate = post.get('registdate','')
		sex = post.get('sex','')
		birthday = post.get('birthday','')
		height = post.get('height','')
		weight = post.get('weight','')
		birthplace = post.get('birthplace','')
		character = post.get('character','')
		national = post.get('national','')
		marry = post.get('marry','')
		skill = post.get('skill','')
		diploma = post.get('diploma','')
		identity = post.get('identity','')
		working = post.get('working','')
		huji = post.get('huji','')
		address = post.get('address','')
		salary = post.get('salary','')
		obey = post.get('obey','')
		other = post.get('other','')
		evaluate = post.get('evaluate','')
		qq = post.get('qq','')
		emergcontact = post.get('emergcontact','')
		emergcall = post.get('emergcall')

		try:
			Employee.objects.filter(id=eid).update(job=job,registdate=registdate,sex=sex,birthday=birthday,height=height,weight=weight,\
												   birthplace=birthplace,character=character,national=national,marry=marry,skill=skill,\
												   diploma=diploma,working=working,huji=huji,address=address,salary=salary,obey=obey,\
												   other=other,evaluate=evaluate,qq=qq,emergcontact=emergcontact,emergcall=emergcall,identity=identity)
			result = 'success'

		except:
			result = 'error'


	content = {'active_menu': 'viewemployee','result': result,'user':user,'employee':employee}
	return render_to_response('basemployee.html', content, context_instance=RequestContext(req))

#员工添加教育培训经历
def eduemployee(req):
	status = ''
	username = req.session.get('username','')
	if username != '':
		user = Members.objects.get(user__username=username)
	else:
		return HttpResponseRedirect('/login/')

	if req.GET:
		Id = req.GET.get('id','')
		employee = Employee.objects.get(pk=Id)

	if req.POST:
		post = req.POST
		eduid = post.get('eduid','')
		employee = Employee.objects.get(pk=eduid)

		#教育培训背景
		edu_start = post.getlist('edu_start',[])
		edu_end = post.getlist('edu_end',[])
		college = post.getlist('college',[])
		professional = post.getlist('professional',[])
		education = post.getlist('education',[])
		nature = post.getlist('nature',[])
		mark = post.getlist('mark',[])

		edulist = len(college)
		for index in range(edulist):
			if college[index] != '':
				try:
					edu = Education(
						employee = employee,\
						edu_start = edu_start[index],\
						edu_end = edu_end[index],\
						college = college[index],\
						professional = professional[index],\
						education = education[index],\
						nature = nature[index],\
						mark = mark[index],\
						)
					edu.save()
					status = 'success'
				except:
					status= 'error'
			else:
				break

	content = {'active_menu': 'viewemployee','status': status,'user':user,'employee':employee}
	return render_to_response('edumployee.html', content, context_instance=RequestContext(req))

#员工添加亲属关系
def relationemployee(req):
	status = ''
	username = req.session.get('username','')
	if username != '':
		user = Members.objects.get(user__username=username)
	else:
		return HttpResponseRedirect('/login/')

	if req.GET:
		Id = req.GET.get('id','')
		employee = Employee.objects.get(pk=Id)

	if req.POST:
		post = req.POST
		reid = post.get('reid','')
		employee = Employee.objects.get(pk=reid)

		re_name = post.getlist('re_name',[])
		relation = post.getlist('relation',[])
		work = post.getlist('work',[])
		re_job = post.getlist('re_job',[])
		re_tel = post.getlist('re_tel',[])

		relationcount = len(re_name)
		for reindex in range(relationcount):
			if re_name[reindex] != '':
				try:
					relative = Relative(
						employee = employee,\
						re_name = re_name[reindex],\
						relation = relation[reindex],\
						work = work[reindex],\
						re_job = re_job[reindex],\
						re_tel = re_tel[reindex],\
						)
					relative.save()
					status = 'success'
				except:
					status ='error'
			else:
				break

	content = {'active_menu': 'viewemployee','status': status,'user':user,'employee':employee}
	return render_to_response('relationemployee.html', content, context_instance=RequestContext(req))

#工作经历
def workemployee(req):
	status = ''
	username = req.session.get('username','')
	if username != '':
		user = Members.objects.get(user__username=username)
	else:
		return HttpResponseRedirect('/login/')

	if req.GET:
		Id = req.GET.get('id','')
		employee = Employee.objects.get(pk=Id)

	if req.POST:
		post = req.POST
		wkid = post.get('wkid','')
		employee = Employee.objects.get(pk=wkid)

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
					employee = employee,\
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
				status = 'success'
			else:
				break


	content = {'active_menu': 'viewemployee','status': status,'user':user,'employee':employee}
	return render_to_response('workemployee.html', content, context_instance=RequestContext(req))

def imgemployee(req):
	status = ''
	username = req.session.get('username','')
	if username != '':
		user = Members.objects.get(user__username=username)
	else:
		return HttpResponseRedirect('/login/')

	if req.GET:
		Id = req.GET.get('id','')
		employee = Employee.objects.get(pk=Id)

	if req.POST:
		try:
			eid = req.POST.get('eid','')
			employee = Employee.objects.get(pk=eid)
			new_img = Img(
				employee = employee,\
				name = req.POST.get('name',''),\
				description = req.POST.get('description',''),\
				img = req.FILES.get('img',''),\
			)
			new_img.save()
			status = 'success'
		except:
			status = 'error'

	content = {'active_menu': 'viewemployee','status': status,'user':user,'employee':employee}
	return render_to_response('imgemployee.html', content, context_instance=RequestContext(req))


def becomemployee(req):
	result = ''
	username = req.session.get('username','')
	if username != '':
		user = Members.objects.get(user__username=username)
	else:
		return HttpResponseRedirect('/login/')

	if req.GET:
		Id = req.GET.get('id','')
		employee = Employee.objects.get(pk=Id)

	if req.POST:
		post = req.POST
		bid = post.get('bid','')
		evaluate = post.get('evaluate','')
		status = post.get('status','')

		try:
			Employee.objects.filter(id=bid).update(evaluate=evaluate,status=status)
			result = 'success'
		except:
			result = 'error'

	content = {'active_menu': 'viewemployee','result': result,'user':user,'employee':employee}
	return render_to_response('becomemployee.html', content, context_instance=RequestContext(req))



def employeedetail(req):

	status  = ''
	username = req.session.get('username','')
	if username != '':
		user = Members .objects.get(user__username=username)
	else:
		user = ''
		return HttpResponseRedirect('/login/')
	Id = req.GET.get('id','')
	if Id == '':
		return HttpResponseRedirect('/viewemployee/')
	try:
		employee = Employee.objects.get(pk=Id)
		education = employee.education_set.all()
		relation = employee.relative_set.all()
		workexperience = employee.workexperience_set.all()
		image = employee.img_set.all()
	except:
		return HttpResponseRedirect('/viewemployee/')

	content = {'active_menu': 'viewemployee','user':user,'employee':employee,'education':education,'relation':relation,'workexperience':workexperience,'image':image}
	return render_to_response('employeedetail.html', content, context_instance=RequestContext(req))




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
		user = Members.objects.get(user__username=username)
	else:
		return HttpResponseRedirect('/login/')
	name = req.GET.get('name','')
	if name == '':
		status = 'error'
		return  HttpResponseRedirect('/viewmeeting/')
	try:
		employee = Employee.objects.get(name=name)
	except:
		return HttpResponseRedirect('/viewmeeting/')

	if req.POST:
		post = req.POST
		meeting  = WeekMeeting(
			week = post.get('week',''),\
			employee = employee,\
		)
		meeting.save()
		#上周工作总结
		lastweek = post.getlist('lastweek',[])
		last_exeperson = post.getlist('last_exeperson',[])
		last_comletiontime = post.getlist('last_comletiontime',[])
		comletioneffect = post.getlist('comletioneffect',[])
		lastlen = len(lastweek)
		for index in range(lastlen):
			if lastweek[index] !='':
				last = LastSummary(
					weekmeeting = meeting,\
					lastweek = lastweek[index],\
					last_exeperson = last_exeperson[index],\
					last_comletiontime = last_comletiontime[index],\
					comletioneffect = comletioneffect[index],\
				)
				last.save()
			else:
				break
		#本周工作计划
		nextweek = post.getlist('nextweek',[])
		next_exeperson = post.getlist('next_exeperson',[])
		next_comletiontime = post.getlist('next_comletiontime',[])
		nextlen = len(nextweek)
		for index in range(nextlen):
			if nextweek[index] != '':
				next = NextPlan(
					weekmeeting = meeting,\
					nextweek = nextweek[index],\
					next_exeperson = next_exeperson[index],\
					next_comletiontime = next_comletiontime[index],\
				)
				next.save()
			else:
				break

		status = 'success'

	content = {'active_menu': 'viewmeeting','status':status,'user':user,'employee':employee}
	return render_to_response('weekmeeting.html', content, context_instance=RequestContext(req))

def getDepartment():
	weekmeeting = WeekMeeting.objects.all()
	depart_list = set()
	for meeting in weekmeeting:
		depart_list.add(meeting.employee.department.depart_name)
	return list(depart_list)


def viewmeeting(req):
	username = req.session.get('username','')
	if username != '':
		user = Members .objects.get(user__username=username)
	else:
		user = ''
		return HttpResponseRedirect('/login/')
	alldepartment = Department.objects.all()  #getDepartment()所有部门

	'''
	depart = req.GET.get('depart','all')
	if depart =='':
		employee_list = Employee.objects.all()
	elif depart not in alldepartment:
		depart = 'all'
		employee_list = Employee.objects.all()
	else:
		try:
			department =  Department.objects.get(depart_name=depart)
			employee_list = Employee.objects.filter(department=department)
		except:
			return HttpResponseRedirect('/viewmeeting/')


	content = {'active_menu': 'viewmeeting','departments':alldepartment,'depart':depart,'user':user,'employee_list':employee_list}
	'''
	content = {'active_menu': 'viewmeeting','departments':alldepartment,'user':user}
	return render_to_response('viewmeeting.html', content, context_instance=RequestContext(req))

def getSummary(employee):
	pingyu = ''
	weekmeeting = WeekMeeting.objects.filter(employee=employee)[0:2]
	for index in weekmeeting:
		if index.meeting != '':
			pingyu = index.meeting
			break
		else:
			continue
	return pingyu


def employeemeeting(req):
	status = ''
	username = req.session.get('username','')
	if username != '':
		user = Members .objects.get(user__username=username)
	else:
		user = ''
		return HttpResponseRedirect('/login/')
	wid = req.GET.get('id','')
	if wid == '':
		return HttpResponseRedirect('/viewmeeting/')
	try:
		#employee = Employee.objects.select_related('weekmeeting__employee').get(name=name)

		weekmeeting = WeekMeeting.objects.get(pk=wid)
		cahier = weekmeeting.cahier_set.all()
		lastsummary = weekmeeting.lastsummary_set.all()
		nextplan = weekmeeting.nextplan_set.all()

		#employee = Cahier.objects.select_related('weekmeeting__employee').get(name=name)
		#employee = Employee.objects.get(name=name)
		#weekmeeting = WeekMeeting.objects.filter(employee=employee)[0:1]
		#pingyu = getSummary(employee)


	except:
		return HttpResponseRedirect('/viewmeeting/')
	'''
	for week in weekmeeting:
		if week.meeting == '':
			lastsummary = week.lastsummary_set.all()
			nextplan = week.nextplan_set.all()
			startmeeting = week
		else:
			lastsummary = ''
			nextplan = ''
			status  = 'error'
			break
    '''
	content = {'active_menu': 'viewmeeting','status':status,'user':user,'weekmeeting':weekmeeting,'lastsummary':lastsummary,'nextplan':nextplan,'cahier':cahier}
	return render_to_response('weekmeetingplan.html', content, context_instance=RequestContext(req))

def beforemeeting(req):
	username = req.session.get('username','')
	if username != '':
		user = Members .objects.get(user__username=username)
	else:
		user = ''
		return HttpResponseRedirect('/login/')
	name = req.GET.get('name','')
	if name == '':
		return HttpResponseRedirect('/viewmeeting/')
	try:
		employee = Employee.objects.get(name=name)
		weekmeeting = WeekMeeting.objects.filter(employee=employee)[0:8]
	except:
		return HttpResponseRedirect('/viewmeeting/')

	content = {'active_menu': 'viewmeeting','user':user,'weekmeeting':weekmeeting,'employee':employee}
	return render_to_response('beforemeeting.html', content, context_instance=RequestContext(req))

#缩短路径作废方法
def beforemeetingdetail(req):
	username = req.session.get('username','')
	if username != '':
		user = Members .objects.get(user__username=username)
	else:
		user = ''
		return HttpResponseRedirect('/login/')
	Id = req.GET.get('id','')
	if Id == '':
		return HttpResponseRedirect('/viewmeeting/')
	try:
		weekmeeting = WeekMeeting.objects.get(pk=Id)
		lastsummary = weekmeeting.lastsummary_set.all()
		nextplan = weekmeeting.nextplan_set.all()
		cahier = weekmeeting.cahier_set.all()
	except:
		return HttpResponseRedirect('/viewmeeting/')

	content = {'active_menu': 'viewmeeting','user':user,'weekmeeting':weekmeeting,'lastsummary':lastsummary,'nextplan':nextplan,'cahier':cahier}
	return render_to_response('beforemeetingdetail.html', content, context_instance=RequestContext(req))

def emplogyeeweekmeeting(req):
	username = req.session.get('username','')
	if username != '':
		user = Members .objects.get(user__username=username)
	else:
		user = ''
		return HttpResponseRedirect('/login/')
	Id = req.GET.get('id','')
	pingyu = req.GET.get('pingyu','')
	if Id == '':
		return HttpResponseRedirect('/viewmeeting/')
	try:
		weekmeeting = WeekMeeting.objects.get(pk=Id)
		lastsummary = weekmeeting.lastsummary_set.all()
		nextplan = weekmeeting.nextplan_set.all()

	except:
		return HttpResponseRedirect('/viewmeeting/')

	content = {'active_menu': 'viewmeeting','pingyu':pingyu,'user':user,'weekmeeting':weekmeeting,'lastsummary':lastsummary,'nextplan':nextplan}
	return render_to_response('weekmeetingplan.html', content, context_instance=RequestContext(req))

def updateweekmeeting(req):
	status  = ''
	updatemeeting  = ''
	username = req.session.get('username','')
	if username != '':
		user = Members .objects.get(user__username=username)
	else:
		user = ''
		return HttpResponseRedirect('/login/')
	wid = req.GET.get('id','')
	if wid == '':
		return HttpResponseRedirect('/viewmeeting/')
	try:
		weekmeeting = WeekMeeting.objects.get(pk=wid)
	except:
		return HttpResponseRedirect('/viewmeeting/')

	if req.POST:
		post = req.POST
		weekid = post.get('pid','')
		startweek = post.get('startweek','')
		postmeeting = WeekMeeting.objects.get(pk=weekid)
		WeekMeeting.objects.filter(id=weekid).update(startweek=startweek)

		cahier_content = post.getlist('cahier_content',[])
		operator = post.getlist('operator',[])
		finish_date = post.getlist('finish_date',[])

		cahierlen = len(cahier_content)
		for index in range(cahierlen):
			if cahier_content[index] != '':
				cahier = Cahier(
					weekmeeting = postmeeting,\
					cahier_content = cahier_content[index],\
					operator = operator[index],\
					finish_date = finish_date[index],\
				)
				cahier.save()
			else:
				break
		status = "success"
	content = {'active_menu': 'viewmeeting','user':user,'weekmeeting':weekmeeting,'status':status}
	return render_to_response('updateweekmeeting.html', content, context_instance=RequestContext(req))

def lastmodifymeeting(req):
	status = ''
	username = req.session.get('username','')
	if username != '':
		user = Members .objects.get(user__username=username)
	else:
		user = ''
		return HttpResponseRedirect('/login/')

	if req.GET:
		lid = req.GET.get('lid','')

		if lid == '':
			return HttpResponseRedirect('/viewmeeting/')
		try:
			lastweek = LastSummary.objects.get(pk=lid)
		except:
			return HttpResponseRedirect('/viewmeeting/')

	if req.POST:
		post = req.POST
		last = post.get('last','')
		lastweek = post.get('lastweek','')
		comletioneffect = post.get('comletioneffect','')

		try:
			LastSummary.objects.filter(id=last).update(lastweek=lastweek,comletioneffect=comletioneffect)
		except:
			status = 'error'
			return HttpResponseRedirect('/viewmeeting/')

		status = 'success'
	content = {'active_menu': 'viewmeeting','user':user,'status':status,'lastweek':lastweek}
	return render_to_response('lastmodifymeeting.html', content, context_instance=RequestContext(req))

def nextmodifymeeting(req):
	status = ''
	username = req.session.get('username','')
	if username != '':
		user = Members .objects.get(user__username=username)
	else:
		user = ''
		return HttpResponseRedirect('/login/')

	if req.GET:
		nid = req.GET.get('nid','')

		if nid == '':
			return HttpResponseRedirect('/viewmeeting/')
		try:
			nextweek = NextPlan.objects.get(pk=nid)
		except:
			return HttpResponseRedirect('/viewmeeting/')

	if req.POST:
		post = req.POST
		next = post.get('next','')
		nextweek = post.get('nextweek','')
		try:
			NextPlan.objects.filter(id=next).update(nextweek=nextweek)
		except:
			status = 'error'
			return HttpResponseRedirect('/viewmeeting/')

		status = 'success'
	content = {'active_menu': 'viewmeeting','user':user,'status':status,'nextweek':nextweek}
	return render_to_response('nextmodifymeeting.html', content, context_instance=RequestContext(req))

def cahiermodifymeeting(req):
	status = ''
	username = req.session.get('username','')
	if username != '':
		user = Members .objects.get(user__username=username)
	else:
		user = ''
		return HttpResponseRedirect('/login/')

	if req.GET:
		cid = req.GET.get('id','')
		if cid == '':
			return HttpResponseRedirect('/viewmeeting/')
		try:
			cahier = Cahier.objects.get(pk=cid)
		except:
			return HttpResponseRedirect('/viewmeeting/')

	if req.POST:
		post = req.POST
		cid = post.get('cid','')
		cahier_content = post.get('cahier_content','')
		try:
			Cahier.objects.filter(id=cid).update(cahier_content=cahier_content)
		except:
			status = 'error'
			return HttpResponseRedirect('/viewmeeting/')

		status = 'success'
	content = {'active_menu': 'viewmeeting','user':user,'status':status,'cahier':cahier}
	return render_to_response('cahiermodifymeeting.html', content, context_instance=RequestContext(req))




def leadership(req):
	status  = ''
	username = req.session.get('username','')
	if username != '':
		user = Members .objects.get(user__username=username)
	else:
		user = ''
		return HttpResponseRedirect('/login/')
	Id = req.GET.get('id','')
	if Id == '':
		return HttpResponseRedirect('/viewmeeting/')
	try:
		weekmeeting = WeekMeeting.objects.get(pk=Id)
		lastsummary = weekmeeting.lastsummary_set.all()
		nextplan = weekmeeting.nextplan_set.all()
	except:
		return HttpResponseRedirect('/viewmeeting/')
	if req.POST:
		post = req.POST
		weekid = post.get('pid','')
		leadership = post.get('leadership','')
		try:
			WeekMeeting.objects.filter(id=weekid).update(leadership=leadership)
			status = "success"
		except:
			return HttpResponseRedirect('/viewmeeting')


	content = {'active_menu': 'viewmeeting','user':user,'weekmeeting':weekmeeting,'status':status,'lastsummary':lastsummary,'nextplan':nextplan}
	return render_to_response('leadership.html', content, context_instance=RequestContext(req))




"""

lastweek = post.get('lastweek',''),\
			nextweek = post.get('nextweek',''),\
			last_exeperson = post.get('last_exeperson',''),\
			last_comletiontime = post.get('last_comletiontime',''),\
			comletioneffect = post.get('comletioneffect',''),\
			meeting = post.get('meeting',''),\
			next_comletiontime = post.get('next_comletiontime',''),\
			next_exeperson = post.get('next_exeperson',''),\


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




