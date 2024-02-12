from django import forms
from AppAswer.models import AnswerUserQuiz,AnswerQuiz
from .import models


class FormAnswerUser(forms.ModelForm):
    class Meta:
        model=AnswerUserQuiz

        fields=['quiz']

        widgets={
            'quiz':forms.RadioSelect(attrs={"class":"form-control"})
        }

class FormAddLevel(forms.ModelForm):
    class Meta:
        model=models.LevelQuiz

        fields=['title']

        widgets={
            'title':forms.TextInput(attrs={"class":"form-control"})
        }


class FormAddCategoryQuiz(forms.ModelForm):
    class Meta:
        model=models.QuizCategory

        fields=['title', 'Level', 'description']


        widgets={
            'title':forms.TextInput(attrs={"class":"form-control"}),
            'Level':forms.Select(attrs={"class":"form-control"}),
            'description':forms.Textarea(attrs={"class":"form-control"})
        }



class FormAddQuiz(forms.ModelForm):
    class Meta:
        model=models.Quiz

        fields=['question', 'catgory']

        widgets={
            'question':forms.Textarea(attrs={"class":"form-control"}),
            'catgory':forms.Select(attrs={"class":"form-control"}),
        }



class FormUpdateQuiz(forms.ModelForm):
    class Meta:
        model=models.Quiz

        fields=['question', 'catgory','active']

        widgets={
            'question':forms.Textarea(attrs={"class":"form-control"}),
            'catgory':forms.Select(attrs={"class":"form-control"}),
        }