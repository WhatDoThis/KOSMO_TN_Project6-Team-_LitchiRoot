"""pj_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name='index'),
    path("introduce/", views.introduce, name='introduce'),
    path("map/", views.map, name='map'),
    path("subsidiary/", views.subsidiary, name='subsidiary'),
    path("terms/", views.terms, name='terms'),
    path("join/", views.join, name="join"),
    path("join/join_ok/", views.join_ok, name="join_ok"),
    path("login/", views.login, name="login"),
    path('login_ok/',views.login_ok, name='login_ok'),
    path('logout',views.logout, name='logout'),
    path("list/", views.list, name='list'),
    path("search/", views.search, name='search'),
    path("apply/<int:company>/<int:recruitment>", views.apply, name='apply'),
    path("apply_ok/", views.apply_ok, name='apply_ok'),
    path("apply_delete/<int:recruitment>", views.apply_delete, name='apply_delete'),
    path('download/', views.fileDownload, name='fileDownload'),
    path('myPage/', views.myPage, name='myPage'),
    path("info/", views.info, name='info'),
    path("info/info_ok", views.info_ok, name='info_ok'),
    path("ask/", views.ask, name='ask'),
    path("ask/ask_ok", views.ask_ok, name='ask_ok'),
    path("selectCompany/<int:company>", views.selectCompany, name='selectCompany'),
]