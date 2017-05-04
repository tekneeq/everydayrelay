"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include, patterns
from django.contrib import admin
from reviews import views
from reviews.models import UserProfile
from registration.backends.simple.views import RegistrationView

admin.autodiscover()

class MyRegistrationView(RegistrationView):
    def get_success_url(self, request, user):
        up = UserProfile()
        up.user = user
        up.email_limit = 3
        up.save()  
        return '/reviews/review/user'

urlpatterns = [
    url(r'^$', views.home),
    url(r'^reviews/', include('reviews.urls', namespace="reviews")),
    url(r'^admin/', admin.site.urls),
    url(r'^emailprocess/', views.emailprocess),
    url(r'^google129995e25dc40331.html', views.googleverify),
    url(r'^robots.txt', views.robots),
    url(r'^sitemap.xml', views.sitemap),
    #url(r'^accounts/register/$', MyRegistrationView.as_view(), name='registration_register'),
    #url(r'^accounts/', include('registration.backends.simple.urls')),
    #url(r'^accounts/', include('django.contrib.auth.urls', namespace="auth")),
    url(r'^accounts/', include('allauth.urls')),
]
