from django.shortcuts import render
from django.views.generic import View,TemplateView,ListView,DeleteView,CreateView
from django.core.urlresolvers import reverse_lazy
from django.core import serializers
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
import boto3
from .forms import S3Form
import os
import time
import datetime
# Create your views here.
def file_size(num, suffix="B"):
    for unit in ['','K','M','G','T','P','E']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, "Yi", suffix)

class s3(TemplateView):
    template_name = 'project/s3.html'
    def get_context_data(self, **kwargs):
        context = super(s3, self).get_context_data(**kwargs)
        data = []
        aws = boto3.resource('s3')
        buckets = aws.buckets.all()
        #Get data from each bucket
        for bucket in buckets:
            bucketData = {}
            totalSize = 0
            bucketName = bucket.name
            if bucketName != "dbgachaimages2":
                fileBuckets = boto3.resource('s3').Bucket(bucketName)
                #Get data for each object inside each bucket
                for file in fileBuckets.objects.all():
                    totalSize += file.size
                bucketData['bucketName'] = bucket.name
                bucketData['createdAt'] = bucket.creation_date
                bucketData['totalSize'] = file_size(totalSize)
                data.append(bucketData)
        context['buckets'] = data
        return context

class createS3(TemplateView):
    template_name = 'project/create_s3.html'

    def createBucket(self, bucketName):
        s3 = boto3.resource('s3')
        s3.create_bucket(Bucket=bucketName, CreateBucketConfiguration={'LocationConstraint': "eu-west-2"})

    def post(self, request):
        bucketName = request.POST.get("newBucketName")
        self.createBucket(bucketName)
        return JsonResponse("ok", safe=False)

#///////////
class deleteBucket(TemplateView):
    template_name = "project/delete_bucket.html"

    def deleteBucket(self, name):
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(name)
        for object in bucket.objects.all():
            object.delete()
        bucket.delete()

    def post(self, request):
        bucketName = request.POST.get("deleteBucket")
        self.deleteBucket(bucketName)
        return JsonResponse(bucketName, safe=False)

class bucketPage(TemplateView):
    template_name = "project/bucket.html"

    def get_context_data(self, *args, **kwargs):
        context = super(bucketPage, self).get_context_data(**kwargs)
        bucketName = self.kwargs['bucket']

        #Display all items
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(bucketName)
        objects = bucket.objects.all()
        data = []
        totalSize = 0
        for object in objects:
            fileData = {}
            fileName = object.key
            size = object.size
            fileSize = file_size(object.size)
            modified = object.last_modified
            fileData['fileSize'] = fileSize
            fileData['fileName'] = fileName
            fileData['modified'] = modified
            totalSize += size
            data.append(fileData)
        context['bucketName'] = bucketName
        context['totalSize'] = totalSize
        context['convertedSize'] = file_size(totalSize)
        context['objects'] = data
        return context

class createFolder(TemplateView):
    template_name = "project/createFolder.html"

    def post(self, request):
        folderName = request.POST.get('folderName')
        bucketName = request.POST.get('bucketName')
        self.newFolder(bucketName, folderName)
        return JsonResponse("Folder Created!", safe=False)

    def newFolder(self, bucket, folder):
        aws = boto3.client('s3')
        aws.put_object(Bucket=bucket,
                       Body='',
                       Key=folder + "/")

class uploadFile(TemplateView):
    template_name = "project/uploadFile.html"

    def uploadFileToS3(self, fileData, bucket, fileName):
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(bucket)
        bucket.put_object(Key=fileName, Body=fileData)

    def post(self, request):
        fileName = request.POST.get('fileName')
        bucket = request.POST.get('bucket')
        fileData = request.FILES['file']
        self.uploadFileToS3(fileData, bucket, fileName)
        return JsonResponse("Good", safe=False)

class downloadFile(TemplateView):
    template_name = "project/downloadFile.html"

    def post(self, request):
        fileName = request.POST.get('fileName')
        bucketName = request.POST.get('bucketName')
        presignedUrl = self.downloadFile(bucketName, fileName)
        return JsonResponse(presignedUrl, safe=False)

    def downloadFile(self, bucket, fileToDownload):
        s3 = boto3.client('s3')
        url = s3.generate_presigned_url('get_object', Params = {'Bucket': bucket,
                                  'Key': fileToDownload}, ExpiresIn = 100)
        return url

class deleteFile(TemplateView):
    template_name = "project/deleteFile.html"

    def post(self, request):
        fileName = request.POST.get('fileName')
        bucketName = request.POST.get('bucketName')
        self.fileDelete(bucketName, fileName)
        return JsonResponse("Deleted", safe=False)

    def fileDelete(self, bucket, fileName):
        s3 = boto3.resource('s3')
        s3.Object(bucket, fileName).delete()

class ec2(TemplateView):
    template_name = 'project/ec2.html'
class architect(TemplateView):
    template_name = 'project/architect.html'
