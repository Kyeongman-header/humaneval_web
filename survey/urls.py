from django.urls import path

from . import views

app_name = "survey"
urlpatterns = [
    path("", views.login, name="login"),
    path("index/",views.index,name="index"),
    path("<str:case_name>/<int:text_num>/<str:user_name>/",views.survey, name="survey"),
    path("analysis/<str:case_name>/<str:user_name>/",views.analysis, name="analysis"),
    path("load/",views.load,name="load"),
    path("load_text/",views.load_text,name="load_text"),
]