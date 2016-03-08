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
    url(r'^viewmenber/$',views.viewmenber),
    url(r'^viewmenber/menber_detail/$',views.menber_detail),
    url(r'^qiandao/$',views.qiandao),
    url(r'^viewsign/$',views.viewsign),
    url(r'^songli/$',views.songli),
    url(r'^songli/songli_detail/$',views.songli_detail),
    url(r'^addsongli/$',views.addsongli),
    url(r'^addsongli/toaddperson/$',views.toaddperson),
    url(r'^addsongli/friendsqiaojie/$',views.friendsqiaojie),
    url(r'^addsongli/addfriends/$',views.addfriends),
    url(r'^addlingli/addlingli_detail/$',views.modifyfriendslingli),
    url(r'^addlingli/$',views.addperson),
    url(r'^addpersonnel/$',views.addpersonnels),
    url(r'^viewpersonnels/$',views.viewpersonnels),
    #url(r'^addmenber/$',views.addMenber),
   # url(r'^viewmenber/menber_detail/$',views.menber_detail),
    url(r'^image/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_PATH}),
)
