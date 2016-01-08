from django.contrib import admin
from management.models import *

class MenberAdmin(admin.ModelAdmin):
    list_display =('menber_name','menber_address','menber_city','menber_store','menber_tel')
    search_fields = ('menber_name',)
    def menber_store(self,obj):
        return self.menber_store

class CourseAdmin(admin.ModelAdmin):
    list_display =('course_name','course_subject','beizhu')
    search_fields =('course_name',)

class TeacherAdmin(admin.ModelAdmin):
    list_display = ('teacher_name','teacher_organize','teacher_address','teacher_contact','teacher_tel','beizhu')
    search_fields = ('teacher_name','teacher_organize')

class StoreAdmin(admin.ModelAdmin):
    list_display = ('store_name','store_brand','store_address','store_boss','store_tel')

admin.site.register(Stores,StoreAdmin)
admin.site.register(Menbers,MenberAdmin)
admin.site.register(Teacher,TeacherAdmin)
admin.site.register(Courses,CourseAdmin)
admin.site.register(MyUser)
admin.site.register(Book)
admin.site.register(Img)
