from django.conf.urls import url,include
from . import views

urlpatterns = [
    url(r'^$',views.home.as_view(),name='home'),
    url(r'^project/', include('project.urls', namespace='project')),
    url(r'^gacha/', include('gacha.urls', namespace='gacha')),
]
