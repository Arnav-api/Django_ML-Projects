"""
URL configuration for Cnn project.

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
from deep_learning import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path("admin/", admin.site.urls),
    path("home/" , views.home , name="home"),
    path("upload_view", views.upload_view , name = "upload_view"),
    path("Heart_disease",views.Heart_disease,name="Heart_Disease"),
    path("prediction",views.prediction,name="prediction"),
    path("requirement_details/",views.requirement_details,name="requirement_details"),
    path("Contact",views.Contact,name = "Contact"),
    path("feedback",views.feedback,name = "feedback"),
    path("support",views.support,name="support"),
    path("sign_prediction", views.sign_prediction, name="sign_prediction"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)