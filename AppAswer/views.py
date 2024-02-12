from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib import messages
from AppQuiz.models import Quiz, QuizCategory
from .import models
from .import forms



def listeResponseByQuiz(request,id):
    getQuizId=Quiz.objects.get(id=id)
    liste_response=models.AnswerQuiz.objects.filter(quiz=getQuizId).order_by('-date_created')
    context={
        "getQuizId":getQuizId,
        "liste_response":liste_response
    }
    return render(request, "answer/listeResponseByQuiz.html", context)



def addAnswer(request):
    form=forms.FormAddAnswer()
    if request.method == "POST":
        form=forms.FormAddAnswer(request.POST)
        if form.is_valid():
            new_response=form.save(commit=False)
            new_response.user=request.user
            new_response.save()
            messages.warning(request, "Réponse ajoutée avec succès !")
            form=forms.FormAddAnswer()
        else:
            messages.error(request, "Formulaire invalide !")
    else:
        form=forms.FormAddAnswer()
    return render(request, 'answer/addAnswer.html', {'form':form})



def updateAnswer(request,id):
    getIdAnswer=models.AnswerQuiz.objects.get(id=id)
    form=forms.FormAddAnswer(instance=getIdAnswer)
    if request.method == "POST":
        form=forms.FormAddAnswer(request.POST, instance=getIdAnswer)
        if form.is_valid():
            new_response=form.save(commit=False)
            new_response.user=request.user
            new_response.save()
            messages.warning(request, "Réponse modifiée avec succès !")
            return redirect(reverse('listeResponseByQuiz', kwargs={"id":form['quiz'].value()}))
        else:
            messages.error(request, "Formulaire invalide !")
    else:
        form=forms.FormAddAnswer(instance=getIdAnswer)
    return render(request, 'answer/updateAnswer.html', {'form':form})

def deleteAswer(request, id):
    getIdAnswer=models.AnswerQuiz.objects.get(id=id)
    if request.method == "POST":
        try:
            getIdAnswer.delete()
            messages.warning(request, "Réponse supprimée avec succès !")
            return redirect(reverse('listeResponseByQuiz', kwargs={"id":getIdAnswer.quiz.id}))
        except:
            messages.warning(request, "Impossible de supprimer cette réponse !")
    return render(request, 'answer/deleteAswer.html',{"getIdAnswer":getIdAnswer})