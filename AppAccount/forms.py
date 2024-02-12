from django import forms
from .import models

class FormUserSignUp(forms.ModelForm):
    class Meta:
        model=models.MyUser
        
        fields=['username','last_name','email','genre','password', 'confirme_password']


        widgets={
            'username':forms.TextInput(attrs={"class":'form-control'}),
            'last_name':forms.TextInput(attrs={"class":'form-control'}),
            'email':forms.EmailInput(attrs={"class":'form-control'}),
            'genre':forms.Select(attrs={"class":'form-control'}),
            'password':forms.PasswordInput(attrs={"class":'form-control'}),
            'confirme_password':forms.PasswordInput(attrs={"class":'form-control'}),
        }



class FormUserLogin(forms.Form):
    Email=forms.CharField(widget=forms.EmailInput(attrs={"class":'form-control'}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":'form-control'}))
    remember_me=forms.BooleanField(required=False)






class FormUserAdminAddUser(forms.ModelForm):
    class Meta:
        model=models.MyUser

        fields=[
                'username',
                'last_name',
                'email','genre',
                'password', 
                'confirme_password', 
                'is_superuser',
                'is_active',
                
        ]


        widgets={
            'username':forms.TextInput(attrs={"class":'form-control'}),
            'last_name':forms.TextInput(attrs={"class":'form-control'}),
            'email':forms.EmailInput(attrs={"class":'form-control'}),
            'genre':forms.Select(attrs={"class":'form-control'}),
            'password':forms.PasswordInput(attrs={"class":'form-control'}),
            'confirme_password':forms.PasswordInput(attrs={"class":'form-control'}),
            'user_permissions':forms.SelectMultiple(attrs={"class":'form-control'}),
        }
