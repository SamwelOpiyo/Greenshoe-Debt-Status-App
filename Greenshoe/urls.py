"""Greenshoe URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import RedirectView, TemplateView

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/accounts/login/')),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^debts/', include('Debts.urls')),
    url(r'^logout/$', RedirectView.as_view(url='/accounts/logout/'), name="logout"),
    url(r'^login/$', RedirectView.as_view(url='/accounts/login/')),
    url(r'^signup/$', RedirectView.as_view(url='/accounts/signup/')),
    url(r'^help/$', TemplateView.as_view(template_name="help.html"), name='help'),
]

from django.conf import settings
from django.views import static

if settings.DEBUG :
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', static.serve, {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
	url(r'^static/(?P<path>.*)$', static.serve, {'document_root': settings.STATIC_ROOT, 'show_indexes': True}),
    ]
