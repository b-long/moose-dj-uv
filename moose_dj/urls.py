"""
URL configuration for moose_dj project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

# from moose_dj.news.views import start_task, get_task_status
from moose_dj.news.views_celery import start_task, get_task_status

urlpatterns = [
    path('admin/', admin.site.urls),

    path('start_task', start_task, name="start_task"),
    path('get_task_status/<str:task_id>', get_task_status, name="get_task_status")
]
