"""MovieHunter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from re_paths import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import include, re_path
from django.contrib import admin
from django.shortcuts import render
from . import views

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^movie/', include('movie.urls')),
    re_path(r'^user/', include('user.urls')),
    re_path(r'^$', views.index, name='index'),
    re_path(r'.*', lambda request: render(request, '404.html'), name='404'),
]
