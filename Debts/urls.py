from django.conf.urls import url
from . import views
from django.views.generic import RedirectView



from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    url(r'^all/$', views.all, name='all'),
    url(r'^tbl_profiles/$', views.profiles, name='profiles'),
    url(r'^Customer_debt_information.csv$', views.csv, name='csv'),
    url(r'^tbl_due_listing/$', views.duelisting, name='duelisting'),
    url(r'^search/$', views.search, name='search'),
]

urlpatterns += staticfiles_urlpatterns()
