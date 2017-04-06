from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^articles/$', views.article_list, name='articles'),
    url(r'^article/(?P<pk>\d+)/$', views.article_detail, name='article_detail'),
    url(r'^article/new/$', views.article_new, name='article_new'),
    url(r'^article/(?P<pk>\d+)/edit/$', views.article_edit, name='article_edit'),
    url(r'^login/jsignup$', views.json_signup, name='jsignup'),
]
