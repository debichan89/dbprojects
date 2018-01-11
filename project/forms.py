from django import forms

##Create S3 bucket forms
class S3Form(forms.Form):
    name = forms.CharField()
