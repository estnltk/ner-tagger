"""untitled URL Configuration

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
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as django_admin_views

from ui import views

urlpatterns = [
    url(r'^$', views.corpus_list_view, name='corpus-list-view'),
    url(r'^annotation/(?P<corpus>\d+)/$', login_required(TemplateView.as_view(template_name='annotation.html')), name='annotation-view'),
    url(r'^help/$', TemplateView.as_view(template_name='help.html'), name='help-view'),
    url(r'^load-sentences-view/$', views.load_sentences_view, name='load-sentences-view'),
    url(r'^submit-sentences-view/$', views.submit_sentences_view, name='submit-sentences-view'),
    url(r'^accounts/login/$', django_admin_views.login, {'template_name': 'login.html'}),
    url(r'^logout/$', django_admin_views.logout, {'next_page': '/'}),

    url(r'^admin/', admin.site.urls),
]
