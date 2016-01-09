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

admin.site.register(Menbers,MenberAdmin)
admin.site.register(Courses,CourseAdmin)
admin.site.register(MyUser)

