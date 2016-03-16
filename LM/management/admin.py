from django.contrib import admin
from management.models import *

class EmployeeAdmin(admin.ModelAdmin):
    list_display =('tel','name')
    search_fields = ('name',)

'''
class CourseAdmin(admin.ModelAdmin):
    list_display =('course_name','course_subject','beizhu')
    search_fields =('course_name',)

class SignAdmin(admin.ModelAdmin):
    list_display = ('sign_mood','sign_date')
'''
class PersonAdmin(admin.ModelAdmin):
    list_display = ('tel','name','gift')
    search_fields = ('name',)

class FriendsAdmin(admin.ModelAdmin):
    list_display = ('f_tel','f_name','f_gift')

class EducationAdmin(admin.ModelAdmin):
    list_display = ('college','professional')

class RelativeAdmin(admin.ModelAdmin):
    list_display = ('re_name','relation')

class WorkExperienceAdmin(admin.ModelAdmin):
    list_display = ('company','w_job')

class weekmeetingAdmin(admin.ModelAdmin):
    list_display = ('lastweek','nextweek')


admin.site.register(Department)
admin.site.register(NextPlan)
admin.site.register(LastSummary)
admin.site.register(Employee,EmployeeAdmin)
admin.site.register(Education,EducationAdmin)
admin.site.register(Relative,RelativeAdmin)
admin.site.register(WorkExperience,WorkExperienceAdmin)
#admin.site.register(Courses,CourseAdmin)
#admin.site.register(Sign,SignAdmin)
admin.site.register(weekmeeting,weekmeetingAdmin)
admin.site.register(Person,PersonAdmin)
admin.site.register(Friends,FriendsAdmin)


