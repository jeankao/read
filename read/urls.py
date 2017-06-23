from django.conf.urls import include, url
from django.contrib import admin
from account import views

urlpatterns = [
        url(r'^admin/', include(admin.site.urls)),
        url(r'^$', views.homepage, name='homepage'),
        url(r'^account/', include('account.urls')),  
]