from django.conf.urls import patterns, include, url
from ls.feed_view import FeedView
from ls.feed_share_view import FeedShareView
from ls.topic_view import TopicView,Topic,TopicReplyView

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'myhome.views.home', name='home'),
    # url(r'^myhome/', include('myhome.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    (url(r'^$',FeedView.as_view(page_size=30))),
    (url(r'^share$',FeedShareView.as_view())),
    (url(r'^topic/(?P<topicid>\d+)/(?P<page>\d+)$',TopicView.as_view())),
    (url(r'^topic/(?P<topicid>\d+)/add_reply$',TopicReplyView.as_view())),
    (url(r'^topic/(?P<topicid>\d+)/(?P<page>\d+)$',TopicView.as_view())),
    (r'^add$','album.views.add'),
    (r'^detail/(?P<doc_id>\d+)$','album.views.detail'),
    
    #base
    (r'^setup$','base.views.setup'),
    (r'^setpass','base.views.setpass'),
    (r'^setavatar','base.views.setAvatar'),
    (r'^cropAvatar','base.views.cropAvatar'),
    (r'^login$','base.views.do_login'),
    (r'^logout$','base.views.do_logout'),
    (r'^register','base.views.register'),
    (r'^regsuccess','base.views.reg_success'),
    (r'^do_register','base.views.do_register'),
    (r'^404','base.views.page_404'),
    
    #admin
    (r'^admin$','base.admin_views.index'),
    (r'^admin/user/list$','base.admin_views.user_list'),
    (r'^admin/user/edit/(?P<user_id>\d+)$','base.admin_views.user_edit'),
    
)
