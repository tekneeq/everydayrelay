from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /
    #url(r'^$', views.review_list, name='review_list'),
    url(r'^$', views.user_review_list, name='review_list'),
    url(r'^home/$', views.home, name='home'),
    url(r'^home_next$', views.homenext, name='homenext'),
    url(r'^home_next_relay$', views.homenextrelay, name='homenextrelay'),
    url(r'^accountsignup$', views.accountsignup, name='accountsignup'),
    url(r'^faq$', views.faq, name='faq'),
    url(r'^news$', views.news, name='news'),
    url(r'^home/deleteemail$', views.delete_acc_email, name='delete_acc_email'),
    url(r'^home/relay_email/$', views.get_relay_email, name='get_relay_email'),
    url(r'^home/relay_pass/$', views.get_relay_pass, name='get_relay_pass'),
    url(r'^home/pay/$', views.pay, name='pay'),

    url(r'^review/user/$', views.user_review_list, name='user_review_list'),
    url(r'^review/user/(?P<username>\w+)/$', views.user_review_list, name='user_review_list'),
    url(r'^review/user/(?P<username>\w+)/(?P<errmsg>\w+.*)$', views.user_review_list, name='user_review_list'),
    url(r'^review/user/(?P<username>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/$', views.user_review_list, name='user_review_list'),
    url(r'^review/user/(?P<username>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/(?P<errmsg>\w+.*)$', views.user_review_list, name='user_review_list'),
    #url(r'^review/user/(?P<username>\w+)/(?P<errmsg>\w+)$', views.user_review_list, name='user_review_list'),

    # ex: /review/5/
    url(r'^review/(?P<review_id>[0-9]+)/$', views.user_review_list, name='review_detail'),
    # ex: /wine/
    url(r'^wine$', views.wine_list, name='wine_list'),
    # ex: /wine/5/
    url(r'^wine/(?P<wine_id>[0-9]+)/$', views.wine_detail, name='wine_detail'),
    url(r'^wine/(?P<wine_id>[0-9]+)/add_review/$', views.add_review, name='add_review'),
    url(r'^wine/add_wine/$', views.add_wine, name='add_wine'),
    # ex: /review/user - get reviews for the logged user
]
