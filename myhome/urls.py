from django.conf.urls import patterns, include, url

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
    (r'^$','album.views.index'),
    (r'^add$','album.views.add'),
    (r'^detail/(?P<doc_id>\d+)$','album.views.detail'),
    
    #base
    (r'^setup$','base.views.setup'),
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
