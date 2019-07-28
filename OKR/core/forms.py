from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import *

class ExtendedUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)

        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()
        return user

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ('role', 'team_id')


class TeamForm(ModelForm):
    class Meta:
        model = Team
        fields = ('name',)

#=================================================================================

class OKR_Form(ModelForm):
    class Meta:
        model = OKR
        fields = ('name',)


    def save(self, commit=True):
        okr = super().save(commit=False)

        okr.name = self.cleaned_data['name']

        if commit:
            okr.save()
        return okr


class Team_OKR_Form(ModelForm):
    class Meta:
        model = Team_OKR
        fields = ( 'team_id',)

class Employee_OKR_Form(ModelForm):
    class Meta:
        model = Employee_OKR
        fields = ('employee_id',)


class KR_Form(ModelForm):
    class Meta:
        model = KR
        fields = ('name','goal', )


    def save(self, commit=True):
        kr = super().save(commit=False)

        kr.name = self.cleaned_data['name']
        kr.goal = self.cleaned_data['goal']
##        kr.okr_id = self.cleaned_data['okr_id']

        if commit:
            kr.save()
        return kr

class Team_KR_Form(ModelForm):
    class Meta:
        model = Team_KR
        fields = ('team_id',)

class Employee_KR_Form(ModelForm):
    class Meta:
        model = Employee_KR
        fields = ('employee_id',)

class Progress_Form(ModelForm):
    class Meta:
        model = KR
        fields = ('progress',)
