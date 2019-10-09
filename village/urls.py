"""village URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from village_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.sign_in),
    path('check_reg', views.check_reg),
    path('check_log', views.check_log),
    path('char_validation', views.char_validation),
    path('createChar', views.char_create),
    path('dashboard', views.dashboard),
    path('findJob', views.find_job),
    path('postJob', views.post_job),
    path('validJob', views.job_valid),
    path('jobDetails/<int:id>', views.job_details),
    path('jobResult/<int:id>', views.job_result),
    path('tookJob', views.took_job),
    path('delete/<int:id>', views.job_delete),
    path('character/<int:id>', views.char_bio),
    path('edit/<int:id>', views.edit),
    path('edit_form', views.edit_form),
    path('villagers', views.friends),
    path('addFriend/<int:id>', views.add_friend),
    path('removeFriend/<int:id>', views.remove_friend),
    path('messages', views.messages),
    path('send', views.send),
    path('viewMess/<message_id>', views.viewMess),
    path('logout', views.logout),
] 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
