from django import forms
from .models import *
import re
from django.core.exceptions import  ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from captcha.fields import CaptchaField

class ContactForm(forms.Form):
    subject = forms.CharField(label='Тема',widget=forms.TextInput(attrs={'class': 'form-control'}))
    content = forms.CharField(label='Предложение/жалоба', widget=forms.Textarea(attrs={'class': 'form-control','rows':7,}))
    captcha = CaptchaField(label="Решите:")


class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control','autocomplete':'off'}))
    last_name = forms.CharField(label='Фамилия пользователя', widget=forms.TextInput(attrs={'class': 'form-control','autocomplete':'off'}))
    username = forms.CharField(label='Логин пользователя',widget= forms.TextInput(attrs={'class': 'form-control','autocomplete':'off'}))
    email = forms.EmailField(label='E-mail',widget= forms.EmailInput(attrs={'class': 'form-control','autocomplete':'off'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control','autocomplete':'off'}))
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput(attrs={'class': 'form-control','autocomplete':'off'}))
    captcha = CaptchaField(label="Решите:")
    class Meta:
        model = User
        fields = ('first_name','last_name','username','email','password1','password2')

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин пользователя',widget= forms.TextInput(attrs={'class': 'form-control','autocomplete':'off'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control','autocomplete':'off'}))
    captcha = CaptchaField(label="Решите:")

class PresForm(forms.ModelForm):
    captcha = CaptchaField(label="Решите:")
    class Meta:
        model = Pres
        fields = ['title','content','category','document']
        widgets = {
            'title':forms.TextInput(attrs={'class':'form-control'}),
            'content':forms.Textarea(attrs={'class':'form-control','rows':5,})
        }
    def clean_document(self):
        document = (self.cleaned_data['document'])
        document2 = str(self.cleaned_data['document'])
        if not re.search(r'.\.pptx$',document2):
            raise ValidationError('Выберите презентацию')
        return document

class PresForm1(forms.Form):
    title = forms.CharField(max_length=200,label = 'Название',widget=forms.TextInput(attrs={'class':'form-control'}))
    content = forms.CharField(label='Описание',required=False,widget=forms.Textarea(attrs={
        'class':'form-control',
        'rows':5,
    }))
    document = forms.FileField(label='Файл презентации',required=False)
    category = forms.ModelChoiceField(empty_label='Выберите категорию',label='Категория',queryset=Category.objects.all(),
                                      widget=forms.Select(attrs={
                                          'class':'form-control',
                                      }))