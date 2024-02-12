from django import forms
from .import models


class FormAddAnswer(forms.ModelForm):
    class Meta:
        model=models.AnswerQuiz

        fields=['quiz', 'response', 'responseTrue']

        widgets={
            'quiz':forms.Select(attrs={"class":"form-control"}),
            'response':forms.TextInput(attrs={"class":"form-control"}),
        }