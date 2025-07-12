"""
URL configuration for text_tutils project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("",views.index,name='index'),
    path("personal",views.personal,name='personal'),
    path("Django_learn",views.Django_learn,name='Django_learn'),
    path("Machine_Learning",views.Machine_Learning,name='Machine_Learning'),
    path("Functionality",views.Functionality,name='Functionality'),
    path("sentence_transformation",views.sentence_transformation,name='sentence_transformation'),
    path("user_feedback",views.user_feedback,name='user_feedback'),
    path("github_ML",views.github_ML,name='github_ML'),
    path("github_DJANGO",views.github_DJANGO,name='github_DJANGO'),
]
