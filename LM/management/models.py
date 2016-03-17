from django.db import models
from django.contrib.auth.models import User

'''
class Courses(models.Model):
    course_name = models.CharField(max_length=50,verbose_name=u"课程名")
    course_subject = models.TextField(verbose_name=u"课程纲要")
    teacher = models.TextField(verbose_name=u"老师")
    organize = models.CharField(max_length=50,verbose_name=u"培训机构")
    course_date = models.DateField(verbose_name=u"培训日期")
    course_address = models.CharField(max_length=50,verbose_name=u"授课场地")
    beizhu = models.TextField(verbose_name=u"备注")
    
    def __str__(self):
        return self.course_name
    class Meta:
        verbose_name = "课程"
        verbose_name_plural ="课程"

class Sign(models.Model):
    sign_mood = models.CharField(max_length=50,verbose_name=u"一句话")
    sign_date = models.DateTimeField(auto_now_add=True,verbose_name=u"签到时间")
    courses = models.ForeignKey(Courses)
   
    def __str__(self):
        return self.sign_mood
    class Meta:
        verbose_name = "签到"
        verbose_name_plural ="签到"
        ordering = ["-sign_date"]

class Menbers(models.Model):
    user = models.OneToOneField(User)
    permission = models.IntegerField()
    menber_name = models.CharField(max_length=30,verbose_name=u"姓名")
    menber_address = models.CharField(max_length=60,verbose_name=u"地址")
    menber_city = models.CharField(max_length=50,verbose_name=u"城市")
    menber_tel = models.CharField(max_length=50,verbose_name=u"电话")
    menber_store = models.CharField(max_length=50,verbose_name=u"店名")
    menber_brand = models.CharField(max_length=50,verbose_name=u"品牌")
    menber_typ = models.CharField(max_length = 60,verbose_name="级别")
    sign = models.ManyToManyField(Sign)

    def __str__(self):
        return u'%s %s' % (self.menber_name,self.menber_city)
    class Meta:
        verbose_name = "学员"
        verbose_name_plural ="学员"

class Menbers(models.Model):
    user = models.OneToOneField(User)
    permission = models.IntegerField()
    menber_name = models.CharField(max_length=30,verbose_name=u"姓名")
    partment = models.CharField(max_length=30,verbose_name=u"部门")
    menber_tel = models.CharField(max_length=30,verbose_name=u"电话")
    reg_date = models.DateField(auto_now_add=True,verbose_name=u"注册日期")
    def __str__(self):
        return self.user.username
    class Meta:
        verbose_name = "员工"
        verbose_name_plural ="员工"
'''
class Department(models.Model):
    depart_name = models.CharField(max_length=30,verbose_name=u"部门名")
    depart_num =models.IntegerField()
    leader = models.CharField(blank=True,max_length=30,verbose_name=u"部门领导")
    depart_mark = models.CharField(blank=True,max_length=30,verbose_name="部门介绍")
    def __str__(self):
        return u'%s' %(self.depart_name)
    class Meta:
        verbose_name="部门"
        verbose_name_plural="部门"
        ordering = ["depart_num"]

#面试人员基础信息
class Employee(models.Model):
    user = models.OneToOneField(User)  #django一对一的关系，扩展了系统user
    department = models.ForeignKey(Department) #部门与员工一对多的关系

    job = models.CharField(blank=True,max_length=30,verbose_name=u"职位")
    permission = models.IntegerField()
    registdate  = models.DateField(blank=True,auto_now_add=True,verbose_name=u"填表日期")
    name = models.CharField(max_length=30,verbose_name=u"姓名")
    sex = models.CharField(blank=True,max_length=10,verbose_name=u"性别")
    birthday = models.DateField(blank=True,auto_now_add=True,verbose_name=u"出生日期")
    height = models.CharField(blank=True,max_length=10,verbose_name=u"身高")
    weight = models.CharField(blank=True,max_length=10,verbose_name=u"体重")
    birthplace = models.CharField(blank=True,max_length=10,verbose_name=u"籍贯")
    character = models.CharField(blank=True,max_length=30,verbose_name=u"性格")
    national = models.CharField(blank=True,max_length=10,verbose_name=u"民族")
    marry = models.CharField(blank=True,max_length=10,verbose_name=u"婚姻")
    tel = models.CharField(blank=True,max_length=30,verbose_name=u"手机")
    skill = models.CharField(blank=True,max_length=30,verbose_name=u"特长")
    diploma = models.CharField(blank=True,max_length=30,verbose_name=u"文化程度")
    identity = models.CharField(blank=True,max_length=40,verbose_name=u"身份证")
    working = models.CharField(blank=True,max_length=30,verbose_name=u"到岗时间")
    huji = models.CharField(blank=True,max_length=30,verbose_name=u"户籍")
    address = models.CharField(blank=True,max_length=60,verbose_name=u"性别")
    salary = models.CharField(blank=True,max_length=30,verbose_name=u"期望薪水")
    obey = models.CharField(blank=True,max_length=10,verbose_name=u"是否服从")
    other = models.TextField(blank=True,verbose_name=u"其他说明")
    evaluate = models.TextField(blank=True,verbose_name=u"综合评估")
    qq = models.CharField(blank=True,max_length=20,verbose_name='QQ')
    email = models.CharField(max_length=50,blank=True)
    status = models.CharField(max_length=10,blank=True,verbose_name=u'类型')
    emergcontact = models.CharField(max_length=30,blank=True,verbose_name=u'紧急联系人')
    emergcall = models.CharField(max_length=30,blank=True,verbose_name=u'联系电话')

    def __str__(self):
        return u'%s %s' %(self.name,self.job)
    class Meta:
        verbose_name="人才登记表"
        verbose_name_plural="人才登记表"
        ordering = ["-registdate"]
#教育经历
class Education(models.Model):
    employee = models.ForeignKey(Employee)
    edu_start = models.DateField(auto_now_add=True,verbose_name=u"入学时间")
    edu_end = models.DateField(auto_now_add=True,verbose_name=u"毕业时间")
    college = models.CharField(max_length=30,verbose_name=u"院校")
    professional = models.CharField(blank=True,max_length=20,verbose_name=u"专业")
    education = models.CharField(blank=True,max_length=30,verbose_name=u"学历")
    nature = models.CharField(blank=True,max_length=30,verbose_name=u"性质")
    mark = models.CharField(blank=True,max_length=30,verbose_name=u"备注")
    def __str__(self):
        return u'%s %s' %(self.college,self.education)
    class Meta:
        verbose_name="教育培训"
        verbose_name_plural="教育培训"
        ordering = ["-edu_end"]
#亲戚关系
class Relative(models.Model):
    employee = models.ForeignKey(Employee)
    re_name = models.CharField(max_length=20,verbose_name=u"姓名")
    relation = models.CharField(max_length=20,verbose_name=u"关系")
    work = models.CharField(blank=True,max_length=20,verbose_name=u"工作")
    re_job = models.CharField(blank=True,max_length=20,verbose_name=u"职务")
    re_tel = models.CharField(blank=True,max_length=30,verbose_name=u"联系电话")
    def __str__(self):
        return u'%s %s' %(self.re_name,self.relation)
    class Meta:
        verbose_name="家庭背景"
        verbose_name_plural="家庭背景"

#工作经验
class WorkExperience(models.Model):
    employee = models.ForeignKey(Employee)
    w_start = models.DateField(auto_now_add=True,verbose_name=u"入职时间")
    w_end = models.DateField(auto_now_add=True,verbose_name=u"离职时间")
    company = models.CharField(blank=True,max_length=50,verbose_name=u"工作单位")
    w_job = models.CharField(blank=True,max_length=20,verbose_name=u"职务")
    w_salary = models.CharField(blank=True,max_length=30,verbose_name=u"薪水")
    quit = models.CharField(blank=True,max_length=50,verbose_name=u"离职原因")
    references = models.CharField(blank=True,max_length=20,verbose_name=u"证明人")
    w_tel = models.CharField(blank=True,max_length=30,verbose_name=u"电话")
    def __str__(self):
        return u'%s %s' %(self.company,self.w_job)
    class Meta:
        verbose_name="工作经验"
        verbose_name_plural="工作经验"
        ordering = ["-w_end"]


#送礼发起人
class Person(models.Model):
    tel = models.CharField(max_length=30,verbose_name=u"电话")
    name = models.CharField(max_length=30,verbose_name=u"姓名")
    gift = models.CharField(max_length=30,verbose_name=u"礼品")
    pdate = models.DateField(auto_now_add=True,verbose_name=u"领取日期")
    partment = models.CharField(max_length=36,verbose_name=u"部门")
    remarks = models.TextField(blank=True,verbose_name=u"备注")

    def __str__(self):
        return u'%s %s'%(self.name,self.gift)
    class Meta:
        verbose_name = "发起人"
        verbose_name_plural ="发起人"
        ordering = ["-pdate"]

#送礼给朋友
class Friends(models.Model):
    f_tel = models.CharField(max_length=30,verbose_name=u"朋友电话")
    f_name = models.CharField(max_length=30,verbose_name=u"朋友姓名")
    f_gift = models.CharField(max_length=30,verbose_name=u"朋友礼品")
    f_date  = models.DateField(auto_now_add=True,verbose_name=u"送礼日期")
    f_remarks = models.TextField(blank=True,verbose_name=u"备注")
    person = models.ForeignKey(Person)

    def __str__(self):
        return u'%s %s '%(self.f_name,self.f_gift)
    class Meta:
        verbose_name = "朋友"
        verbose_name_plural = "朋友"

#周工作推荐表
class WeekMeeting(models.Model):
    week = models.CharField(max_length=30,verbose_name=u"第几周")
    meeting = models.TextField(blank=True,verbose_name=u"会议记录")
    startweek = models.DateField(auto_now_add=True,verbose_name=u"开会时间")
    employee = models.ForeignKey(Employee)

    def __str__(self):
        return u'%s %s'%(self.week,self.meeting)
    class Meta:
        verbose_name = "周列会"
        verbose_name_plural = "周列会"

class LastSummary(models.Model):
    weekmeeting = models.ForeignKey(WeekMeeting)
    lastweek = models.TextField(blank=True,verbose_name=u"上周工作内容")
    last_exeperson = models.CharField(max_length=50,verbose_name=u"上周执行人")
    last_comletiontime = models.DateField(auto_now_add=True,verbose_name=u"上周完成时间")
    comletioneffect = models.CharField(max_length=50,verbose_name=u"完成效果")
    def __str__(self):
        return u'%s %s'%(self.lastweek,self.last_exeperson)
    class Meta:
        verbose_name= "上周总结"
        verbose_name_plural = "上周总结"

class NextPlan(models.Model):
    weekmeeting = models.ForeignKey(WeekMeeting)
    nextweek = models.TextField(blank=True,verbose_name=u"本周工作内容")
    next_exeperson = models.CharField(max_length=50,verbose_name=u"本周执行人")
    next_comletiontime = models.DateField(auto_now_add=True,verbose_name=u"本周完成时间")
    def __str__(self):
        return u'%s %s'%(self.nextweek,self.next_exeperson)
    class Meta:
        verbose_name="下周计划"
        verbose_name_plural ="下周计划"



