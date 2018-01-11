from django.conf.urls import url,include
from . import views

urlpatterns = [
    url(r'gacha/$',views.gacha.as_view(), name="gacha"),
    url(r'gacha/singlepull/$',views.singlePull.as_view(), name="singlePull"),
    url(r'gacha/multiplepull/$',views.multiplePull.as_view(), name="multiplePull"),
]
