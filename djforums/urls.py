from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()
import settings
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'djforums.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),



    url(r'^$', 'djforums.views.index', name='index'),
    url(r'^addcate$', 'djforums.views.addcate', name='addcate'),
    url(r'^cate/(\d+)$', 'djforums.views.cateshow', name='cateshow'),
    url(r'^topic/(\d+)/addtopic$', 'djforums.views.addtopic', name='addtopic'),
    url(r'^topic/(\d+)$', 'djforums.views.topicshow', name='topicshow'),
    url(r'^topic/(\d+)/replytopic$', 'djforums.views.replytopic', name='replytopic'),

    url(r'^useradmin$', 'djforums.views.userinfoadmin', name='userinfoadmin'),
    url(r'^useradmin/updatephoto$', 'djforums.views.updatephoto', name='updatephoto'),
    url(r'^upload$', 'djforums.views.upload', name='upload'),
    url(r'^uploadphoto$', 'djforums.views.uploadphoto', name='uploadphoto'),

    url(r'^UserProfile_update_save$', 'djforums.views.UserProfile_update_save'),
    url(r'^imgCrop$', 'djforums.views.imgCrop'),


    url(r'^accounts/register/$', 'djforums.views.register'),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login',{'template_name': 'login.html'}),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout'),
    url(r'^media(?P<path>.*)$', 'django.views.static.serve',{'document_root':settings.MEDIA_ROOT,'show_indexes':True}),

#    url(r'^topic_delete$', 'zhyblog.views.topic_delete'),
#    url(r'^topic_update$', 'zhyblog.views.topic_update'),
#    url(r'^topic_update_save$', 'zhyblog.views.topic_update_save'),

    url(r'^admin/', include(admin.site.urls)),
)	
