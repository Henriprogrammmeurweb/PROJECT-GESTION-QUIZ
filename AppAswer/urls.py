from django.urls import path
from .import views


urlpatterns=[
    path('listeResponseByQuiz=<str:id>', views.listeResponseByQuiz, name="listeResponseByQuiz"),
    path('addAnswer', views.addAnswer, name="addAnswer"),
    path('updateAnswer=<str:id>', views.updateAnswer, name="updateAnswer"),
    path('deleteAswer=<str:id>', views.deleteAswer, name="deleteAswer"),
]