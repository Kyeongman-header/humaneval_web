from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import *
from .load_csv import *

# load_csv("wp_embedding_generations_outputs")

def login(request):
    try:
        subject_list=Subject.objects.all()
        context = {"subject_list" : subject_list , "none" : False}
    except:
        context = {"subject_list" : 0, "none" : True}
    return render(request, "survey/login.html", context)

def index(request):

    user_name=request.GET.get('user_name') # get method로 받아야지만 back에서 정상적으로 처리 가능하다(javascript 없이.)
    if len(Subject.objects.filter(username=user_name))>0:
        user = Subject.objects.get(username=user_name)
    else:
        user = Subject.objects.create(username=user_name)
    # print(user)
    case_list = Case.objects.all()
    context = {"case_list": case_list, "user" : user}
    return render(request, "survey/index.html", context)

def survey(request, case_name, text_num, user_name):
    case = Case.objects.get(name=case_name)
    text = case.text_set.get(text_num=text_num)
    user = Subject.objects.get(username=user_name)
    
    if text.is_fake:
        fake_or_real="fake"
    else:
        fake_or_real="real"
    
    score=Score.objects.filter(subject__username=user_name,text__case__name=case_name,text__text_num=text_num)
    # print("text_num : " + str(text_num) + " score len : " + str(len(score)))
    # print("request.Post len : " + str(len(request.POST)))
    existing_score=None
    if len(score)!=0:
        existing_score=Score.objects.get(subject__username=user_name,text__case__name=case_name,text__text_num=text_num)

    if len(request.POST) >=4:
        Q1=request.POST['Q1']
        Q2=request.POST['Q2']
        Q3=request.POST['Q3']
        
        if len(score)==1:
            existing_score.q1=Q1
            existing_score.q2=Q2
            existing_score.q3=Q3
            existing_score.save()
        else:
            existing_score=Score.objects.create(text=text, subject=user, q1=Q1, q2=Q2, q3=Q3,uploaded=True)
            # print("created")
    for_root_scores=Score.objects.filter(text__case__name=case_name,text__text_num=text.text_num)
    avg=[-1,-1,-1,-1,-1,-1]
    if len(for_root_scores)>0:
        q1_fake=[]
        q2_fake=[]
        q3_fake=[]
        q1_real=[]
        q2_real=[]
        q3_real=[]

        for score in for_root_scores:
            if text.is_fake:
                q1_fake.append(score.q1)
                q2_fake.append(score.q2)
                q3_fake.append(score.q3)
            else:
                q1_real.append(score.q1)
                q2_real.append(score.q2)
                q3_real.append(score.q3)
        avg=[np.mean(np.array(q1_fake)),np.mean(np.array(q2_fake)),np.mean(np.array(q3_fake)),np.mean(np.array(q1_real)),np.mean(np.array(q2_real)),np.mean(np.array(q3_real))]
        print(avg)
    if existing_score is None:
        context = {"case": case, "text" : text, "user_name" : user_name,"is_answered" : False, "fake_or_real" : fake_or_real,"avg_score":avg}
    else:
        context = {"case": case, "text" : text, "user_name" : user_name,"is_answered" : existing_score.uploaded, "Q1" : existing_score.q1, "Q2" : existing_score.q2, "Q3" : existing_score.q3, "fake_or_real" : fake_or_real,"avg_score":avg}
    
    return render(request, "survey/survey.html", context)

import numpy as np

def analysis(request,case_name,user_name):
    case = Case.objects.get(name=case_name)
    q1_fake=[]
    q2_fake=[]
    q3_fake=[]
    q1_real=[]
    q2_real=[]
    q3_real=[]
    for text in case.text_set.all():
        
        scores=Score.objects.filter(text__case__name=case_name,text__text_num=text.text_num)
        print(len(scores))
        for score in scores:
            if text.is_fake:
                q1_fake.append(score.q1)
                q2_fake.append(score.q2)
                q3_fake.append(score.q3)
            else:
                q1_real.append(score.q1)
                q2_real.append(score.q2)
                q3_real.append(score.q3)
    

    q1_fake=np.array(q1_fake)
    q2_fake=np.array(q2_fake)
    q3_fake=np.array(q3_fake)
    q1_real=np.array(q1_real)
    q2_real=np.array(q2_real)
    q3_real=np.array(q3_real)
    context={case : case,"q1_fake_avg": np.mean(q1_fake), "q2_fake_avg" : np.mean(q2_fake), "q3_fake_avg" :np.mean(q3_fake),"q1_real_avg": np.mean(q1_real), "q2_real_avg" : np.mean(q2_real), "q3_real_avg" :np.mean(q3_real), 
             "num_fake" : len(q1_fake), "num_real" : len(q1_real), "user_name" : user_name }

    return render(request, "survey/analysis.html", context)


def load(request):
    case_list = Case.objects.all()
    context = {"case_list": case_list}
    return render(request, "survey/load.html", context)

def load_text(request):
    name = request.POST['case_name']
    # try:
    case=Case.objects.get(name=name)
    if case.uploaded==True:
        return HttpResponse("Already loaded the " + name)
    
    load_csv(case.name)
    return HttpResponse("Successfully loaded the " + name)
    # except:
    #     return HttpResponse("There is no case " + name + " or no csv datas in ./csv.")