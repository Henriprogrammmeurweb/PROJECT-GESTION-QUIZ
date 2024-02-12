from django.shortcuts import redirect, render
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required,permission_required 
from django.contrib import messages
from AppQuiz.models import Quiz,QuizCategory,LevelQuiz
from AppAswer.models import AnswerUserQuiz
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
