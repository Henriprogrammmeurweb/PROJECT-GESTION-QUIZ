from django.db import models
from AppAccount.models import MyUser
from AppQuiz.models import Quiz



class AnswerQuiz(models.Model):
    response=models.TextField()
    quiz=models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user=models.ForeignKey(MyUser, on_delete=models.CASCADE)
    responseTrue=models.BooleanField(default=False)
    date_created=models.DateTimeField(auto_now_add=True)
    date_updated=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.response
    

    @property
    def getResponseTrue(self):
        responseuser=self.answeruserquiz_set.all()
        getAnswerTrue=[ligne.response_possible for ligne in responseuser if ligne.response_possible.responseTrue==True]
        sommesForAnswer=sum(ligne.quiz.note for ligne in getAnswerTrue)
        return sommesForAnswer


class AnswerUserQuiz(models.Model):
    response_possible=models.ForeignKey(AnswerQuiz, on_delete=models.PROTECT)
    quiz=models.ForeignKey(Quiz, on_delete=models.CASCADE, null=True, blank=True)
    user=models.ForeignKey(MyUser, on_delete=models.CASCADE)
    date_created=models.DateTimeField(auto_now_add=True)
    date_updated=models.DateTimeField(auto_now=True)




    @property
    def getResponseNote(self):
        if self.response_possible.responseTrue:
            return 10
        return 0


    @property
    def getResponseValide(self):
        if self.response_possible.responseTrue:
            return 'Validé ✅'
        return 'Non validé ❌'



    def save(self, *args, **kwargs):
        if not self.quiz:
            self.quiz=self.response_possible.quiz
        return super().save(*args, **kwargs)



    def __str__(self):
        return f'{self.user.getUser}'
