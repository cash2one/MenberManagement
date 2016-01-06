from django.db import models
from django.contrib.auth.models import User

class MyUser(models.Model):
	user = models.OneToOneField(User)
	nickname = models.CharField(max_length = 16)
	permission = models.IntegerField()

	def __unicode__(self):
		return self.user.username

class Book(models.Model):
	name = models.CharField(max_length = 128)
	price = models.FloatField()
	author = models.CharField(max_length = 128)
	pubDate = models.DateField()
	typ = models.CharField(max_length = 128)

	class META:
		ordering = ['name']

	def __unicode__(self):
		return self.name

class Img(models.Model):
	name = models.CharField(max_length = 128)
	desc = models.TextField()
	img = models.ImageField(upload_to = 'image')
	book = models.ForeignKey(Book)

	class META:
		ordering = ['name']

	def __unicode__(self):
		return self.name

class  Stores(models.Model):
    store_name = models.CharField(max_length=50,verbose_name=u"店名")
    store_brand = models.CharField(max_length=50,verbose_name=u"品牌")
    store_size = models.CharField(max_length=30,verbose_name=u"规模")
    store_address = models.CharField(max_length=60,verbose_name=u"地址")
    stroe_city = models.CharField(max_length=30,verbose_name=u"城市")
    store_boss = models.CharField(max_length=30,verbose_name=u"老板")
    store_tel = models.CharField(max_length=30,verbose_name=u"电话")
    def __str__(self):
        return self.store_name
    class Meta:
        verbose_name = "店铺"
        verbose_name_plural ="店铺"


class Teacher(models.Model):
    teacher_name = models.CharField(max_length=30,verbose_name=u"姓名")
    teacher_sex = models.CharField(max_length=10,verbose_name=u"性别")
    teacher_organize = models.CharField(max_length=50,verbose_name=u"机构")
    teacher_address = models.CharField(max_length=60,verbose_name=u"地址")
    teacher_contact = models.CharField(max_length=30,verbose_name=u"联系人")
    teacher_tel = models.CharField(max_length=50,verbose_name=u"联系电话")
    beizhu = models.TextField(verbose_name=u"备注")
    def __str__(self):
        return u'%s %s' % (self.teacher_name,self.teacher_organize)
    class Meta:
        verbose_name = "讲师"
        verbose_name_plural = "讲师"


class Courses(models.Model):
    course_name = models.CharField(max_length=50,verbose_name=u"课程名")
    course_subject = models.TextField(verbose_name=u"课程纲要")
    teacher = models.ManyToManyField(Teacher)
    beizhu = models.TextField(verbose_name=u"备注")
    def __str__(self):
        return self.course_name
    class Meta:
        verbose_name = "课程"
        verbose_name_plural ="课程"

class Menbers(models.Model):
    menber_name = models.CharField(max_length=30,verbose_name=u"姓名")
    menber_address = models.CharField(max_length=60,verbose_name=u"地址")
    menber_city = models.CharField(max_length=50,verbose_name=u"城市")
    menber_tel = models.CharField(max_length=50,verbose_name=u"电话")
    menber_store = models.ForeignKey(Stores,verbose_name="店名")
    course = models.ManyToManyField(Courses)

    def __str__(self):
        return u'%s %s' % (self.menber_name,self.menber_city)
    class Meta:
        verbose_name = "学员"
        verbose_name_plural ="学员"
