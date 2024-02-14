from django.shortcuts import redirect, render
from django.db.models import Sum, Max, Min, Count
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required,permission_required 
from django.contrib import messages
from AppQuiz.models import Quiz,QuizCategory,LevelQuiz
from AppAswer.models import AnswerUserQuiz, AnswerQuiz,AnswerUserQuiz
from .import models
from .import forms



def index(request):
    """Home page for site"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'index/index.html')



def signUp(request):
    """This Function signup user"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    form=forms.FormUserSignUp()
    if request.method == "POST":
        form=forms.FormUserSignUp(request.POST)
        if form.is_valid():
            info_newUser={
                'username':form.cleaned_data['username'],
                'last_name':form.cleaned_data['last_name'],
                'email':form.cleaned_data['email'],
                'genre':form.cleaned_data['genre'],
                'password':form.cleaned_data['password'],
                'confirme_password':form.cleaned_data['confirme_password']
            }
            if len(info_newUser['password']) < 6:
                messages.warning(request, 'Le mot de passe doit être au moins de 6 caractères !')
            elif info_newUser['password'].isdigit():
                messages.error(request, "Le mot de passe ne doit être composé uniquement des chiffres")
            elif info_newUser['password'] != info_newUser['confirme_password']:
                messages.warning(request, "Désolé le mot de passe ne correspond pas !")
            else:
                new_user=models.MyUser.objects.create_user(**info_newUser)
                new_user.save()
                messages.warning(request, 'Votre compte a été crée, vous pouvez maintenant vous connectez !')
                form=forms.FormUserSignUp()
        else:
            messages.warning(request, 'Compte non crée, veuillez ressayer ! ')
    else:
        form=forms.FormUserSignUp()
    return render(request, 'user/signUp/signUp.html',{"form":form})




def loginUser(request):
    """This function Login user to site"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    form=forms.FormUserLogin()
    if request.method == "POST":
        form=forms.FormUserLogin(request.POST)
        if form.is_valid():
            email=form.cleaned_data['Email']
            password=form.cleaned_data['password']
            user=authenticate(email=email,password=password)
            if user:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.warning(request, 'Authentification échouée !')
        else:
            messages.warning(request, 'Formulaire invalide !')
    else:
        form=forms.FormUserLogin()
    return render(request, 'user/login/login.html',{"form":form})


@login_required
def logoutUser(request):
    logout(request)
    return redirect('loginUser')


@login_required
def dashboard(request):
    liste_quiz=QuizCategory.objects.all().order_by('-date_created')
    liste_answerUser=AnswerUserQuiz.objects.filter(user=request.user).order_by('-date_created')[:5]
    context={
        'liste_quiz':liste_quiz,
        'liste_answerUser':liste_answerUser
    }
    return render(request, 'dashboard/dashboard.html',context)




@login_required
def listeUser(request):
    liste_user=models.MyUser.objects.all().order_by('username')
    context={
        "liste_user":liste_user
    }
    return render(request, 'user/crud/listeUser.html', context)




@login_required
def adminAddUser(request):
    form=forms.FormUserAdminAddUser()
    if request.method == "POST":
        form=forms.FormUserAdminAddUser(request.POST)
        if form.is_valid():
            info_newUser={
                'username':form.cleaned_data['username'],
                'last_name':form.cleaned_data['last_name'],
                'email':form.cleaned_data['email'],
                'genre':form.cleaned_data['genre'],
                'password':form.cleaned_data['password'],
                'confirme_password':form.cleaned_data['confirme_password'],
                'is_superuser':form.cleaned_data['is_superuser'],
                'is_active':form.cleaned_data['is_active']
            }
            if len(info_newUser['password']) < 6:
                messages.warning(request, 'Le mot de passe doit être au moins de 6 caractères !')
            elif info_newUser['password'].isdigit():
                messages.error(request, "Le mot de passe ne doit être composé uniquement des chiffres")
            elif info_newUser['password'] != info_newUser['confirme_password']:
                messages.warning(request, "Désolé le mot de passe ne correspond pas !")
            else:
                new_user=models.MyUser.objects.create_user(**info_newUser)
                new_user.save()
                messages.warning(request, 'Le compte a été  bien crée !')
                form=forms.FormUserAdminAddUser()
        else:
            messages.warning(request, 'Compte non crée, veuillez ressayer ! ')
    else:
        form=forms.FormUserAdminAddUser()
    return render(request, 'user/crud/addUser.html',{"form":form})




@login_required
def adminUpdateUser(request,id):
    getUserId=models.MyUser.objects.get(id=id)
    form=forms.FormUserAdminUpdateUser(instance=getUserId)
    if request.method == "POST":
        form=forms.FormUserAdminUpdateUser(request.POST,instance=getUserId)
        if form.is_valid():
            form.save()
            messages.warning(request, 'Informations modifiées avec succès !')
            return redirect('listeUser')
        else:
            messages.warning(request, 'Modification non apportée ! ')
    else:
        form=forms.FormUserAdminUpdateUser(instance=getUserId)
    return render(request, 'user/crud/adminUpdateUser.html',{"form":form})


@login_required
def adminDeleteUser(request,id):
    getUserId=models.MyUser.objects.get(id=id)
    if request.method == "POST":
        try:
            getUserId.delete()
            messages.warning(request, 'Utilisateur supprimé avec succès !')
            return redirect('listeUser')
        except:
            messages.warning(request, "Impossible de supprimer cet utilisateur !")
    return render(request, 'user/crud/adminDeleteUser.html', {"getUserId":getUserId})


@login_required
def GetQuizUserPlay(request, id):
    getUserId=models.MyUser.objects.get(id=id)
    get_userPlay=AnswerUserQuiz.objects.filter(user=getUserId,
                                               response_possible__responseTrue=True
                                               ).values('quiz__catgory__id','quiz__catgory__title',
                                                        'quiz__catgory__Level__title').annotate(
                                                            Nombre_reponse=Count('quiz__question'),
                                                            NoteTotal=Sum('quiz__note'))
    for item in get_userPlay:
        categorysQuiz=QuizCategory.objects.get(id=item['quiz__catgory__id'])
        liste_quiz=Quiz.objects.filter(catgory=categorysQuiz)
        totalNote=sum([ligne.note for ligne in liste_quiz])
        NumberQuizForCategory=len([ligne.catgory for ligne in liste_quiz])
        item['quiz']=NumberQuizForCategory
        item['Score']=format((item['NoteTotal'] * 100) / totalNote, '.0f')
        series=AnswerQuiz.objects.filter(quiz__catgory=categorysQuiz).filter(id__in=AnswerUserQuiz.objects.filter(
            user=getUserId).values_list('response_possible__id', flat=True)).count()
        ResponseFalse=AnswerQuiz.objects.filter(quiz__catgory=categorysQuiz, responseTrue=False).filter(
            id__in=AnswerUserQuiz.objects.filter(user=getUserId).values_list('response_possible__id', flat=True)).count()
        item['ResponseFalse']=ResponseFalse
        if series == NumberQuizForCategory:
            item['Termine'] = "Terminé"
        else :
            item['Termine'] = "Non"
    context={
                "getUserId":getUserId,
                "get_userPlay":get_userPlay
            }
    return render(request, "user/detail/GetQuizUserPlay.html", context)




# def my_view(request):
#     getUserId = request.user.id
#     user_play_data = AnswerUserQuiz.objects.filter(user=getUserId).values('quiz__catgory__title', 'quiz__catgory__Level__title').annotate(Nombre_reponse=Count('quiz__question'))

#     # Appliquer votre méthode d'instance à chaque instance de AnswerUserQuiz
#     for item in user_play_data:
#         answer_user_quiz_instance = AnswerUserQuiz.objects.get(pk=item['id'])  # Supposons que 'id' est le champ clé primaire de AnswerUserQuiz
#         item['nombre_possible_reponses'] = answer_user_quiz_instance.calculate_possible_answers()

#     return render(request, 'template.html', {'user_play_data': user_play_data})
