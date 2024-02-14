from django.db import models
from AppAccount.models import MyUser
from ProjectQuiz.settings import AUTH_USER_MODEL


class LevelQuiz(models.Model):
    title=models.CharField(max_length=254)
    date_created=models.DateTimeField(auto_now_add=True)
    date_updated=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title.lower()

class QuizCategory(models.Model):
    title=models.CharField(max_length=254)
    Level=models.ForeignKey(LevelQuiz, on_delete=models.PROTECT)
    description=models.CharField(max_length=254)
    date_created=models.DateTimeField(auto_now_add=True)
    date_updated=models.DateTimeField(auto_now=True)

    @property
    def getNumberQuiz(self):
        getListQuiz=self.quiz_set.all()
        numberquiz=len([ligne.catgory for ligne in getListQuiz])
        return numberquiz
    
    @property
    def numberQuiz(self):
        listeQuizCategory=self.quiz_set.all()
        getQuiz=[ligne.catgory for ligne in listeQuizCategory]
        return len(getQuiz)

    
    def __str__(self):
        return self.title



class Quiz(models.Model):
    question=models.TextField()
    user=models.ForeignKey(MyUser, on_delete=models.PROTECT)
    catgory=models.ForeignKey(QuizCategory, on_delete=models.PROTECT)
    note=models.IntegerField(null=True, blank=True, default=10)
    active=models.BooleanField(default=False)
    date_created=models.DateTimeField(auto_now_add=True)
    date_updated=models.DateTimeField(auto_now=True)


    @property
    def getNumberResponse(self):
        responses=self.answerquiz_set.all()
        numberTotal=[ligne.quiz for ligne in responses]
        return len(numberTotal)
    
   

    def __str__(self):
        return self.question