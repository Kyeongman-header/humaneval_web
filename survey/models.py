from django.db import models

# Create your models here.

class Subject(models.Model):
    username=models.CharField(max_length=500, default="root")
    pub_date=models.DateTimeField(auto_now=True)

class Case(models.Model):
    name = models.CharField(max_length=500)
    uploaded=models.BooleanField(default=False)
    pub_date=models.DateTimeField(auto_now=True)

class Text(models.Model):
    case=models.ForeignKey(Case, on_delete=models.CASCADE)
    text = models.CharField(max_length=20000)
    korean_text=models.CharField(max_length=20000,default="nan")
    text_num=models.IntegerField(default=0)
    is_fake= models.BooleanField(default=True)
    pub_date=models.DateTimeField(auto_now=True)


class Score(models.Model):
    text = models.ForeignKey(Text, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True)
    q1 = models.IntegerField(default=1)
    q2 = models.IntegerField(default=1)
    q3 = models.IntegerField(default=1)
    uploaded=models.BooleanField(default=False)
    pub_date=models.DateTimeField(auto_now=True)

