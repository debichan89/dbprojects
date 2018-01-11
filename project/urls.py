from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'bienbox/$',views.s3.as_view(),name='bienbox'),
    url(r'bienbox/create$',views.createS3.as_view(),name='creates3'),
    url(r'bienbox/delete/$',views.deleteBucket.as_view(),name='deleteBucket'),
    url(r'bienbox/bucket/(?P<bucket>\w+)$',views.bucketPage.as_view(),name='bucket'),
    url(r'bienbox/bucket/createFolder/$',views.createFolder.as_view(),name='createFolder'),
    url(r'bienbox/bucket/uploadFile/$',views.uploadFile.as_view(),name='uploadFile'),
    url(r'bienbox/bucket/downloadFile/$',views.downloadFile.as_view(),name='downloadFile'),
    url(r'bienbox/bucket/deleteFile/$',views.deleteFile.as_view(),name="deleteFile"),
    url(r'bienpute/$',views.ec2.as_view(),name='ec2'),
    url(r'architect/$',views.architect.as_view(),name='architect'),
]
