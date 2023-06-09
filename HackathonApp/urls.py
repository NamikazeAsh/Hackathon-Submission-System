"""HackathonSubmissionSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.urls import path
from HackathonApp import views

from django.conf.urls.static import static

urlpatterns = [
    
    path('',views.Dashboard,name='dashboard'),
    path('login',views.LogIn,name='login'),
    path('logout',views.LogOut,name='logout'),
    path('signup',views.SignUp,name='signup'),
    path('newHackathon',views.newHackathon,name='new-hackathon'),
    path('hackathonDetail/newSubmission/<int:id>',views.newSubmission,name='new-submission'),
    path('hackathonDetail/<int:id>',views.HackathonDetail,name='hackathon-details'),
    path('hackathonDetail/submissionDetail/<int:id>',views.SubmissionDetail,name='submission-details'),
    path('downloadSubmission/<int:id>',views.DownloadSubmission,name='download-submission'),
    path('submissionList',views.SubmissionsList,name='submission-list'),
    path('submissionEdit/<int:id>',views.SubmissionEdit,name='submission-edit'),
    path('submissionDelete/<int:id>',views.SubmissionDelete,name='submission-delete'),
    path('favoriteSubmission/<int:id>',views.FavoriteSubmission,name='favorite-submission'),
    path('favoriteSubmissionRemove/<int:id>',views.FavoriteSubmissionRemove,name='favorite-submission-remove'),
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
