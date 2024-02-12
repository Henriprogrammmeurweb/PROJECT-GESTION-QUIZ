from django.shortcuts import render,redirect
from django.db.models import Count,Sum,Max,Min
from django.urls import reverse
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib import messages
from django.http import JsonResponse  
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
import random
from .import models
from .import forms
from AppAswer.models import AnswerQuiz,AnswerUserQuiz



@login_required
def startquiz(request,id):
    """This Function display description for category quiz"""
    getCategoryId=models.QuizCategory.objects.get(id=id)
    list_quiz=models.Quiz.objects.filter(catgory=getCategoryId)
    getNoteQuizCategory=sum([ligne.note for ligne in list_quiz])
    users=AnswerUserQuiz.objects.filter(quiz__catgory=getCategoryId, response_possible__responseTrue=True).values('user__username','user__last_name','user__genre').annotate(total=Sum('quiz__note')*100/getNoteQuizCategory).order_by('-total')
    context={
        "getCategoryId":getCategoryId,
        "users":users
    }
    return render(request, 'quiz/startquiz.html',context)

@login_required
def FirstQuiz(request,id):
    """This Function display a first quiz if user click to start"""
    listesMessages=[
        'Bravo Continues comme ça 🧡 ', 
        'Bravo ! Bien joué bonne réponse, courage 🧡', 
        'Tu es Fort ! bonne reponse 🧡',
        'Hum ! Très nice ta réponse 🧡',
        'Coup de chapeau ! félicitations 🧡'
    ]
    answer:int=0
    scoreQuizCategoryOfUser:float=0
    getCategoryId=models.QuizCategory.objects.get(id=id)
    list_quiz=models.Quiz.objects.filter(catgory=getCategoryId,active=True).order_by('-date_created')
    getNoteQuizCategory=sum([ligne.note for ligne in list_quiz])
    userResponse=AnswerUserQuiz.objects.filter(quiz__catgory=getCategoryId, user=request.user)
    noteForResponseIfIsTrue=sum(
        [
            ligne.response_possible.quiz.note for ligne in userResponse 
            if ligne.response_possible.responseTrue
        ])
    if getNoteQuizCategory > 0:
        scoreQuizCategoryOfUser=format((noteForResponseIfIsTrue * 100) / getNoteQuizCategory, '.0f')
    form=forms.FormAnswerUser()
    if request.method == "POST":
        response=request.POST.get('response')
        answer=AnswerQuiz.objects.get(id=response)
        getuserResponse=AnswerUserQuiz.objects.filter(quiz=answer.quiz, user=request.user).exists()
        if getuserResponse:
            messages.warning(request, 'Tu as déjà donné une réponse à cette question !')
        elif answer.responseTrue == True:
            new_response=AnswerUserQuiz.objects.create(response_possible=answer, user=request.user)
            new_response.save()
            messages.warning(request, f'{random.choice(listesMessages)}')
            return redirect(reverse('FirstQuiz', kwargs={"id":id}))
        else:
            new_response=AnswerUserQuiz.objects.create(response_possible=answer, user=request.user)
            new_response.save()
            messages.warning(request, "Mauvaise réponse, votre réponse ne pas tout vraie ! ")
            return redirect(reverse('FirstQuiz', kwargs={"id":id}))
    context={
        'list_quiz':list_quiz.exclude(id__in=AnswerUserQuiz.objects.filter(
            user=request.user).values_list('quiz__id', flat=True)),
        'form':form,
        'getCategoryId':getCategoryId,
        "answer":answer,
        "scoreQuizCategoryOfUser":scoreQuizCategoryOfUser,
        "userResponse":userResponse,
    }
    print(context['list_quiz'])
    return render(request, 'quiz/listeQuiz.html',context)


def deletestartQuiz(request,id):
    getCategoryId=models.QuizCategory.objects.get(id=id)
    userResponse=AnswerUserQuiz.objects.filter(quiz__catgory=getCategoryId, user=request.user)
    if request.method == "POST":
        users_responses=AnswerUserQuiz.objects.filter(id__in=[ligne.id for ligne in userResponse])
        users_responses.delete()
        return redirect(reverse("FirstQuiz",kwargs={"id":id}))
    return render(request, 'quiz/RetartQuiz.html')


def addLevelQuiz(request):
    form=forms.FormAddLevel()
    return render(request, "levelQuiz/AddLevel.html",{"form":form})



@csrf_exempt
def submitData(request):
    if request.method == "POST":
        title=request.POST.get('title')
        newLevel=models.LevelQuiz.objects.create(title=title)
        newLevel.save()
        return JsonResponse({"status":'sucess'})
    return JsonResponse({"status":'error'})



@login_required
def listeCategoryLangage(request):
    liste_langage=models.QuizCategory.objects.all().order_by('-date_created')
    context={
        "liste_langage":liste_langage
    }
    return render(request, "langage/listeCategoryLangage.html", context)



@login_required
def addNewCategoryQuiz(request):
    form=forms.FormAddCategoryQuiz()
    if request.method == "POST":
        form=forms.FormAddCategoryQuiz(request.POST)
        if form.is_valid():
            title=form.cleaned_data['title']
            Level=form.cleaned_data['Level']
            description=form.cleaned_data['description']
            verifyIfCategory=models.QuizCategory.objects.filter(title=title)
            if verifyIfCategory:
                messages.error(request, "Cette Catégorie ou Langage existe déjà !")
            else:
                form.save()
                messages.warning(request, 'Catégorie ou langage ajouté avec succès !')
                form=forms.FormAddCategoryQuiz()
        else:
            messages.warning(request, "Formulaire invalide !")
    else:
        form=forms.FormAddCategoryQuiz()
    return render(request, "langage/addLangage.html", {"form":form})



@login_required
def updateCategoryQuiz(request, id):
    getCategory=models.QuizCategory.objects.get(id=id)
    form=forms.FormAddCategoryQuiz(instance=getCategory)
    if request.method == "POST":
        form=forms.FormAddCategoryQuiz(request.POST,instance=getCategory)
        if form.is_valid():
            form.save()
            messages.warning(request, 'Les modifications ont été apportées avec succès !')
            return redirect('listeCategoryLangage')
        else:
            messages.warning(request, "Formulaire invalide !")
    else:
        form=forms.FormAddCategoryQuiz(instance=getCategory)
    return render(request, "langage/updateLangage.html", {"form":form})


@login_required
def deleteCategoryQuiz(request,id):
    getCategory=models.QuizCategory.objects.get(id=id)
    if request.method == "POST":
        try:
            getCategory.delete()
            messages.warning(request, 'Suppression effectuée avec succès !')
            return redirect('listeCategoryLangage')
        except:
            messages.warning(request, "Impossible de supprimer cette catégorie !")
    return render(request, "langage/deleteLangage.html")





@login_required
def quizByCategory(request, id):
    getCategory=models.QuizCategory.objects.get(id=id)
    liste_quiz=models.Quiz.objects.filter(catgory=getCategory).order_by('-date_created')
    context={
        "getCategory":getCategory,
        "liste_quiz":liste_quiz
    }
    return render(request, "quiz/quizByCategory.html", context)



@login_required
def addQuiz(request):
    form=forms.FormAddQuiz()
    if request.method == "POST":
        form=forms.FormAddQuiz(request.POST)
        if form.is_valid():
            new_quiz=form.save(commit=False)
            new_quiz.user=request.user
            new_quiz.save()
            form=forms.FormAddQuiz()
            messages.warning(request, "Question ajoutée avec succès !")
        else:
            messages.warning(request, "Formulaire invalide !")
    else:
        form=forms.FormAddQuiz()
    return render(request, "quiz/addQuiz.html", {"form":form})



@login_required
def updateQuiz(request, id):
    getIdQuiz=models.Quiz.objects.get(id=id)
    form=forms.FormUpdateQuiz(instance=getIdQuiz)
    if request.method == "POST":
        form=forms.FormUpdateQuiz(request.POST,instance=getIdQuiz)
        if form.is_valid():
            form.save()
            messages.warning(request, "Modification apportée avec succès !")
            return redirect(reverse('quizByCategory', kwargs={"id":form["catgory"].value()}))
        else:
            messages.error(request, "Formulaire invalide !")
    else:
        form=forms.FormUpdateQuiz(instance=getIdQuiz)
    context={
        "form":form
    }
    return render(request, "quiz/updateQuiz.html", context)




@login_required
def deleteQuiz(request, id):
    getIdQuiz=models.Quiz.objects.get(id=id)
    if request.method =="POST":
        try:
            getIdQuiz.delete()
            messages.warning(request, "Question supprimé avec succès !")
            return redirect(reverse('quizByCategory', kwargs={"id":getIdQuiz.catgory.id}))
        except:
            messages.warning(request, "Suppression impossible !")
    return render(request, 'quiz/deleteQuiz.html',{"getIdQuiz":getIdQuiz})



