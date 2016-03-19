from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from management import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'LM.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index),
    url(r'^signup/$', views.signup),
    url(r'^login/$',views.login),
    url(r'^logout/$',views.logout),
    url(r'^setpasswd/$',views.setpasswd),
    #url(r'^viewmember/$',views.viewmember),
    #url(r'^viewmember/member_detail/$',views.member_detail),
    #url(r'^qiandao/$',views.qiandao),
    #url(r'^viewsign/$',views.viewsign),
    #url(r'^songli/$',views.songli),
    #url(r'^songli/songli_detail/$',views.songli_detail),
    #url(r'^addsongli/$',views.addsongli),
    #url(r'^addsongli/toaddperson/$',views.toaddperson),
    #url(r'^addsongli/friendsqiaojie/$',views.friendsqiaojie),
    #url(r'^addsongli/addfriends/$',views.addfriends),
    #url(r'^addlingli/addlingli_detail/$',views.modifyfriendslingli),
    #url(r'^addlingli/$',views.addperson),
    url(r'^addemployee/$',views.addemployee),
    url(r'^modifyemployee/$',views.modifyemployee),
    url(r'^viewemployee/$',views.viewemployee),
    url(r'^viewpersonnels/personnel_detail/$',views.personnel_detail),
    url(r'^viewpersonnels/modify_typ/$',views.modify_typ),
    url(r'^viewmeeting/addweekmeeting/$',views.addweekmeeting),
    url('^viewmeeting/$',views.viewmeeting),
    url('^viewmeeting/modifyemployee/$',views.modifyemployee),
    url('^viewmeeting/employeemeeting/$',views.employeemeeting),
    url('^viewmeeting/emplogyeeweekmeeting/$',views.emplogyeeweekmeeting),
    url('^viewmeeting/updateweekmeeting/$',views.updateweekmeeting),
    url('^viewmeeting/beforemeeting/$',views.beforemeeting),
    url('^viewmeeting/beforemeetingdetail/$',views.beforemeetingdetail),
    url('^viewmeeting/leadership/$',views.leadership),
    url('^viewmember/$',views.viewmember),
    #url('^viewemployee/basemployee/$',views.basemployee),


    #url('^viewmeeting/modifymeeting/$',views.modifymeeting),
    #url(r'^addmenber/$',views.addMenber),
   # url(r'^viewmenber/menber_detail/$',views.menber_detail),
    url(r'^image/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_PATH}),
)
