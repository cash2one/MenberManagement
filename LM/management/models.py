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
'''
class Menbers(models.Model):
    user = models.OneToOneField(User)
    permission = models.IntegerField()
    menber_name = models.CharField(max_length=30,verbose_name=u"姓名")
    menber_tel =  models.CharField(max_length=30,verbose_name=u"电话")
    menber_mail = models.CharField(max_length=30,verbose_name=u"邮箱")
    reg_date  = models.DateField(auto_now_add=True,verbose_name=u"注册日期")
    def __str__(self):
        return u'%s %s' %(self.menber_name,self.menber_tel)
    class Meta:
        verbose_name = "员工"
        verbose_name_plural ="员工"

class Personnel(models.Model):
    job = models.CharField(max_length=30,verbose_name=u"职位")
    form_date = models.DateField(auto_now_add=True,verbose_name=u"填表日期")
    name = models.CharField(max_length=30,verbose_name=u"姓名")
    sex = models.CharField(max_length=10,verbose_name=u"性别")
    birth_date = models.DateField(auto_now_add=True,verbose_nadme=u"填表日期")
    height = models.CharField(max_length=10,verbose_name=u"身高")
    weight = models.CharField(max_length=10,verbose_name=u"体重")
    jiguan = models.CharField(max_length=10,verbose_name=u"籍贯")
    xingge = models.CharField(max_length=30,verbose_name=u"性格")
    minzu = models.CharField(max_length=10,verbose_name=u"民族")
    marry = models.CharField(max_length=10,verbose_name=u"婚姻")
    tel = models.CharField(max_length=30,verbose_name=u"手机")
    skill = models.CharField(max_length=30,verbose_name=u"特长")
    wenping = models.CharField(max_length=30,verbose_name=u"文化程度")
    shenfenzheng = models.CharField(max_length=40,verbose_name=u"身份证")
    daogang = models.CharField(max_length=30,verbose_name=u"到岗时间")
    huji = models.CharField(max_length=30,verbose_name=u"户籍")
    address = models.CharField(max_length=60,verbose_name=u"性别")
    master_start = models.DateField(auto_now_add=True,verbose_name=u"硕士开始")
    master_end = models.DateField(auto_now_add=True,verbose_name=u"硕士结束")
    university_start = models.DateField(auto_now_add=True,verbose_name=u"大学开始")
    university_end = models.DateFieldd(auto_now_add=True,vebose_name=u"大学结束")
    middle_start = models.DateField(auto_now_add=True,verbose_name=u"中学开始")
    moddle_end = models.DateField(auto_now_add=True,verbose_name=u"中学开始")
    name_first  = models.CharField(max_length=30,verbose_name=u"1亲属姓名")
    relative_first = models.CharField(max_length=30,verbose_name=u"1关系")
    company_first = models.CharField(max_length=60,verbose_name=u"1工作单位")
    job_first = models.CharField(max_length=30,verbose_name=u"1职位")
    tel_first = models.CharField(max_length=30,verbose_name=u"1联系电话")
    name_second  = models.CharField(max_length=30,verbose_name=u"2亲属姓名")
    relative_second = models.CharField(max_length=30,verbose_name=u"2关系")
    company_second = models.CharField(max_length=60,verbose_name=u"2工作单位")
    job_second = models.CharField(max_length=30,verbose_name=u"2职位")
    tel_second = models.CharField(max_length=30,verbose_name=u"2联系电话")
    name_third  = models.CharField(max_length=30,verbose_name=u"3亲属姓名")
    relative_third = models.CharField(max_length=30,verbose_name=u"3关系")
    company_third = models.CharField(max_length=60,verbose_name=u"3工作单位")
    job_third = models.CharField(max_length=30,verbose_name=u"3职位")
    tel_third = models.CharField(max_length=30,verbose_name=u"3联系电话")
    work_firstart = models.CharField(max_length=30,verbose_name=u"1工作开始")
    work_firstend = models.CharField(max_length=30,verbose_name=u"1工作结束")
    first_company = models.CharField(max_length=30,verbose_name=u"1工作单位")
    first_job = models.CharField(max_length=30,verbose_name=u"1职务")
    first_tel = models.CharField(max_length=30,verbose_name=u"1联系电话")
    work_secondtart = models.CharField(max_length=30,verbose_name=u"2工作开始")
    work_secondend = models.CharField(max_length=30,verbose_name=u"2工作结束")
    second_company = models.CharField(max_length=30,verbose_name=u"2工作单位")
    second_job = models.CharField(max_length=30,verbose_name=u"2职务")
    second_tel = models.CharField(max_length=30,verbose_name=u"2联系电话")
    work_thirdstart = models.CharField(max_length=30,verbose_name=u"3工作开始")
    work_thirdend = models.CharField(max_length=30,verbose_name=u"3工作结束")
    third_company = models.CharField(max_length=30,verbose_name=u"3工作单位")
    third_job = models.CharField(max_length=30,verbose_name=u"3职务")
    third_tel = models.CharField(max_length=30,verbose_name=u"3联系电话")
    salary = models.CharField(max_length=30,verbose_name=u"期望薪水")
    obey = models.CharField(max_length=10,verbose_name=u"是否服从")
    other = models.TextField(verbose_name=u"其他说明")
    evaluate = models.TextField(verbose_name=u"综合评估")

    def __str__(self):
        return u'%s %s' %(self.name,self.job)
    class Meta:
        verbose_name="人才登记表"
        verbose_name_plural="人才登记表"
        ordering = ["-form_date"]

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

