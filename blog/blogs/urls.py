"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path,include
from blogs import views

urlpatterns = [
    path('post/<int:pk>',views.singleView.as_view(),name='single'),
    path('archives/<int:year>/<int:month>',views.first_archivesView.as_view(),name='archives'),
    path('archives/<int:year>/<int:month>/<int:pagenum>',views.archivesView.as_view(),name='archives'),
    path('archives/<int:year>/<int:month>', views.first_single_archivesView.as_view(), name='archives'),
    path('archives/<int:year>/<int:month>/<int:pagenum>',views.single_archivesView, name='archives'),
    path('category/<int:pk>/<int:pagenum>',views.first_categoryView.as_view(),name='category'),
    path('category/<int:pk>',views.categoryView.as_view(),name='category'),
    path('category/<int:pk>/<int:pagenum>',views.first_single_categoryView.as_view(),name='category'),
    path('category/<int:pk>',views.single_categoryView,name='category'),
    path('tag/<int:pk>/<int:pagenum>',views.tagView.as_view(),name='tag'),
    path('tag/<int:pk>',views.firsttagView.as_view(),name='tag'),
    path('tag/<int:pk>/<int:pagenum>',views.first_single_tagView.as_view(),name='tag'),
    path('tag/<int:pk>',views.single_tagView.as_view(),name='tag'),
    path('index/<int:pagenum>',views.indexView.as_view(),name='index'),
    path('',views.firstView.as_view(),name='index')
]
