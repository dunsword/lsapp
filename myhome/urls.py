from django.conf.urls import patterns, include, url
from ls.feed_view import FeedView
from ls.feed_share_view import FeedShareView
from ls.topic_view import TopicView,Topic,TopicReplyView,TopicEditView,TopicReplyEditView,ProxyView
from ls.m_topic_view import MTopicView,MTopicReplyPageView,MTopicComment
from ls.bookmark_views import MBookmarkView
from ls.category_view import CategoryView,CategoryNewTopicView
from base.login_views import LoginView
from ls.index_view import IndexView
from ls.user_home_view import MyTopicView
from ls.search_view import SearchView
from ls.tuijian_views import TuijianViews

from base.register_view import RegisterView,EmailBindView,EmailActiveView
from base.user_edit_view import UserEditView,UserEditAvatarView
from api.WeixinTokenInvalidView import WeixinTokenInvalidView

from sync.htsync_view import HtSyncView,ThreadSyncView
from sync.author_view import AuthorListView,AuthorEditView
from sync.hxsync_view import HxSyncView, HxThreadSyncView, HxIndexSyncView
from sync.qdsync_view import QDSyncView, QDThreadSyncView, QDIndexSyncView, QDSyncHotView

from sync.weixin_views import WeixinView

# Uncomment the next two lines to enable the sync:
# from django.contrib import sync
# sync.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'myhome.views.home', name='home'),
    # url(r'^myhome/', include('myhome.foo.urls')),

    # Uncomment the sync/doc line below to enable sync documentation:
    # url(r'^sync/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the sync:
    # url(r'^sync/', include(sync.site.urls)),
    #(url(r'^$',FeedView.as_view(page_size=30))),
    (url(r'^share$',FeedShareView.as_view())),
    (url(r'^$',IndexView.as_view())),
    (url(r'^cat/(?P<categoryid>\d+)/(?P<page>\d+)$',CategoryView.as_view())),
    (url(r'^cat/new_topic$',CategoryNewTopicView.as_view())),

    (url(r'^topic/(?P<topicid>\d+)/(?P<page>\d+)$',TopicView.as_view())),
    (url(r'^m/topic/(?P<topicid>\d+)/(?P<page>\d+)$',MTopicView.as_view())),
    (url(r'^m/my/bookmarks/(?P<page>\d+)$',MBookmarkView.as_view())),
    (url(r'^m/comment/(?P<topicid>\d+)/(?P<replyid>\d+)$',MTopicComment.as_view())),
    (url(r'^m/comment/(?P<topicid>\d+)$',MTopicComment.as_view())),

    (url(r'^(?P<version>\w)/topic/(?P<topicid>\d+)/reply/(?P<replyid>\d+)$',MTopicReplyPageView.as_view())),
    (url(r'^(?P<version>\w)/daren/(?P<source_uid>\d+)$',TuijianViews.as_view())),
    (url(r'^proxy/(?P<tid>\d+)',ProxyView.as_view())),


    (url(r'^topic/(?P<topicid>\d+)/add_reply$',TopicReplyView.as_view())),
    (url(r'^topic/reply/(?P<replyid>\d+)$',TopicReplyView.as_view())),
    (url(r'^topic/(?P<topicid>\d+)/(?P<page>\d+)$',TopicView.as_view())),
    (url(r'^topic/edit/(?P<topicid>\d+)$',TopicEditView.as_view())),
    (url(r'^reply/edit$',TopicReplyEditView.as_view())),
    (url(r'^user/(?P<userid>\d+)$',MyTopicView.as_view())),
    (url(r'^search/(?P<keyword>\w*)$',SearchView.as_view())),
    (r'^add$','album.views.add'),
    (r'^detail/(?P<doc_id>\d+)$','album.views.detail'),
    
    #base
    (r'^setup$','base.views.setup'),
    (r'^setpass','base.views.setpass'),
    (r'^setavatar','base.views.setAvatar'),
    (r'^cropAvatar','base.views.cropAvatar'),
    (r'^login$','base.views.do_login'),
    (url(r'^login/form',LoginView.as_view())),
    (url(r'^(?P<version>\w)/login/form',LoginView.as_view())),
    (r'^logout$','base.views.do_logout'),
    (url(r'^register',RegisterView.as_view())),
    (url(r'^email_bind',EmailBindView.as_view())),
    (url(r'^email_active',EmailActiveView.as_view())),
    (url(r'^sync/user/edit/(?P<userid>\d+)',UserEditView.as_view())),
    (url(r'^sync/user/edit/avatar/(?P<userid>\d+)',UserEditAvatarView.as_view())),
    (r'^regsuccess','base.views.reg_success'),
    (r'^do_register','base.views.do_register'),
    (r'^404','base.views.page_404'),
    (r'^500','base.views.page_404'),

    #api
    (url(r'^api/weixin/token$',WeixinTokenInvalidView.as_view())),


    #admin
    (r'^admin$','base.admin_views.index'),
    (r'^admin/user/list$','base.admin_views.user_list'),
    (r'^sync/user/edit/(?P<user_id>\d+)$','base.admin_views.user_edit'),
    (url(r'^sync/htsync/(?P<bid>\d+)$',HtSyncView.as_view())),
    (url(r'^sync/htsync/t/(?P<tid>\d+)$',ThreadSyncView.as_view())),
    (url(r'^sync/htsync/t/(?P<tid>\d+)/(?P<page>\d+)$',ThreadSyncView.as_view())),
    (url(r'^sync/authors/(?P<page>\d+)$',AuthorListView.as_view())),
    (url(r'^sync/author/edit/(?P<uid>\d+)$',AuthorEditView.as_view())),
    (url(r'^sync$',HtSyncView.as_view())),
    (url(r'^sync/hxsync$', HxSyncView.as_view())),
    (url(r'^sync/hxsync/index$', HxIndexSyncView.as_view())),
    (url(r'^sync/hxsync/t/(?P<tid>\d+)$', HxSyncView.as_view())),
    (url(r'^sync/hxsync/t/(?P<tid>\d+)/(?P<page>\d+)$', HxThreadSyncView.as_view())),
    (url(r'^sync/qdsync/index$', QDIndexSyncView.as_view())),
    (url(r'^sync/qdsync/top$', QDSyncHotView.as_view())),
    (url(r'^sync/qdsync/t/(?P<tid>\d+)$', QDSyncView.as_view())),
    (url(r'^sync/qdsync/t/(?P<tid>\d+)/(?P<page>\d+)$', QDThreadSyncView.as_view())),
    (r'^weixin$','sync.weixin_views.wexin'),

    #author
    (r'^oauthor/qzone','api.oauth.qzone.qqAuthor'),

    (r'^cron/add$', 'cron.views.newDocument'),
    (r'^cron/update$', 'cron.views.updateDocument'),
    (r'^cron/addCharpter$', 'cron.views.newCharpters'),
)
