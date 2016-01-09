from django.contrib import admin
from management.models import *

class MenberAdmin(admin.ModelAdmin):
    list_display =('menber_name','menber_address','menber_city','menber_store','menber_tel')
    search_fields = ('menber_name',)


class CourseAdmin(admin.ModelAdmin):
    list_display =('course_name','course_subject','beizhu')
    search_fields =('course_name',)

class SignAdmin(admin.ModelAdmin):
    list_display = ('sign_mood','sign_date','course','menber')

admin.site.register(Menbers,MenberAdmin)
admin.site.register(Courses,CourseAdmin)
admin.site.register(Sign,SignAdmin)


