import pandas as pd
from .models import *

def load_csv(name="wp_embedding_generations_outputs"):
    f=pd.read_csv('csv/'+name+'.csv',sep=',')
    #ensure fields are named~ID,Product_ID,Name,Ratio,Description
    #concatenate name and Product_id to make a new field a la Dr.Dee's answer

    c=Case.objects.get(name__startswith=name)
    c.uploaded=True
    c.save()
    print("load compliete. " + c.name)
    text_num=0
    for step, line in f.iterrows():
        text_num=line[0]
        text=line[1]
        korean_text=line[2]
        label=line[3]
        if "f" in label:
            label=True
        else:
            label=False
        text=str(text)
        korean_text=str(korean_text)
        c.text_set.create(text_num=text_num,text=text,korean_text=korean_text, is_fake=label)
        print("load text " + str(text_num))
        