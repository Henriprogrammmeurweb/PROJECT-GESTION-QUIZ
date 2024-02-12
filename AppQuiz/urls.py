from django.urls import path
from .import views


urlpatterns=[
    path('start=<str:id>', views.startquiz, name='startquiz'),
    path('FirstQuiz=<str:id>', views.FirstQuiz, name='FirstQuiz'),
    path('deletestartQuiz=<str:id>', views.deletestartQuiz, name='deletestartQuiz'),
    path('addlevel', views.addLevelQuiz, name='addLevelQuiz'),
    path("submitData", views.submitData, name="submitData"),
    path('addNewCategoryQuiz', views.addNewCategoryQuiz, name="addNewCategoryQuiz"),
    path('listeCategoryLangage', views.listeCategoryLangage, name="listeCategoryLangage"),
    path('updateCategoryQuiz=<str:id>', views.updateCategoryQuiz, name="updateCategoryQuiz"),
    path('deleteCategoryQuiz=<str:id>', views.deleteCategoryQuiz, name="deleteCategoryQuiz"),
    path('quizByCategory=<str:id>', views.quizByCategory, name="quizByCategory"),
    path('addQuiz', views.addQuiz, name="addQuiz"),
    path('updateQuiz=<str:id>', views.updateQuiz, name="updateQuiz"),
    path('deleteQuiz=<str:id>', views.deleteQuiz, name="deleteQuiz")
]