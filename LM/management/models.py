from django.db import models
from django.contrib.auth.models import User


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




class Person(models.Model):
    tel = models.CharField(max_length=30,verbose_name=u"电话")
    name = models.CharField(max_length=30,verbose_name=u"姓名")
    gift = models.CharField(max_length=30,verbose_name=u"礼品")
    pdate = models.DateField(auto_now_add=True,verbose_name=u"领取日期")
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
    f_date  = models.DateField(verbose_name=u"送礼日期")
    f_remarks = models.TextField(blank=True,verbose_name=u"备注")
    person = models.ForeignKey(Person)
    def __str__(self):
        return u'%s %s '%(self.f_name,self.f_gift)
    class Meta:
        verbose_name = "朋友"
        verbose_name_plural = "朋友"



        
