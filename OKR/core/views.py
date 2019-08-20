from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.views.generic import UpdateView
from django.db.models import Count
from django.http import HttpResponseRedirect        #dqwwqqwdwq
from django.shortcuts import redirect
from django.contrib import messages

from .forms import *


def home(request):
    context = {"home_page":"active bg-secondary rounded"}
    return render(request, 'home.html', context)

@login_required
def register(request):
    if request.method == 'POST':
        form = ExtendedUserCreationForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if form.is_valid() and profile_form.is_valid():
            user= form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
##            username = form.cleaned_data.get('username')
##            password = form.cleaned_data.get('password1')
##            user = authenticate(username=username, password=password)
##            login(request, user)
            return redirect('employee_list')
    else:
        form = ExtendedUserCreationForm()
        profile_form = UserProfileForm(request.POST)

    context = {'form':form, 'profile_form':profile_form}
    return render(request, 'registration/register.html', context)

#=================================================================================

@login_required
def add_team(request):
    if request.method =='POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('team_list')
    else:
        form = TeamForm()
    return render(request, 'teams/add_team.html', {'form':form})

#=================================================================================

@login_required
def team_list(request):
    teams = Team.objects.all().prefetch_related()
    return render(request, 'teams/team_list.html', {'teams':teams,})

#=================================================================================

@login_required
def employee_list(request):
    employees = Employee.objects.all().prefetch_related()
    return render(request, 'registration/employee_list.html', {'employees':employees})

#=================================================================================

@login_required
def team_update(request, id):
    instance = get_object_or_404(Team, id=id)
    form = TeamForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return redirect('team_list')

    context = {'instance':instance, 'form':form, 'name':instance.name}
    return render(request, 'teams/team_update.html' ,context)

#=================================================================================

@login_required
def team_delete(request, id):
    instance = get_object_or_404(Team, id=id)
    instance.delete()
    #messages.succes(request, 'usunięto zespoł')
    return redirect('team_list')

#=================================================================================

@login_required
def employee_update(request, id):
    instance = get_object_or_404(Employee, id=id)
    form = UserProfileForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return redirect('team_list')
    context = {'instance':instance, 'form':form, 'role':instance.role, 'team_id':instance.team_id}
    return render(request, 'registration/employee_update.html' ,context)

#=================================================================================

@login_required
def employee_delete(request, id):
    instance = get_object_or_404(Employee, id=id)
    instance.delete()
    return redirect('team_list')

#=================================================================================

@login_required
def company_add_okr(request):
    if request.method =='POST':
        form = OKR_Form(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "dodano cel firmowy")
            return redirect('company_list_okr')
    else:
        form = OKR_Form()
    return render(request, 'company/add_okr.html', {'form':form})

@login_required
def company_list_okr(request):
    okrs = OKR.objects.all().prefetch_related().filter(team_okr__isnull=True).filter(employee_okr__isnull=True)
    context = {"company_page":"active bg-secondary rounded", "okrs":okrs,}
    return render(request, 'company/list_okr.html', context)

@login_required
def company_delete_okr(request, id):
    instance = get_object_or_404(OKR, id=id)
    instance.delete()
    return redirect('company_list_okr')

@login_required
def company_update_okr(request, id):
    instance = get_object_or_404(OKR, id=id)
    form = OKR_Form(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return redirect('company_list_okr')

    context = {'instance':instance, 'form':form, 'name':instance.name}
    return render(request, 'company/update_okr.html' ,context)

#==================================================================================

@login_required
def team_add_okr(request):
    if request.method =='POST':
        form = OKR_Form(request.POST)
        team_okr_form = Team_OKR_Form(request.POST)
        if form.is_valid() and team_okr_form.is_valid():
            okr = form.save()
            team_okr = team_okr_form.save(commit=False)
            team_okr.okr = okr
            team_okr.save()
            return redirect('team_list_okr')
    else:
        form = OKR_Form()
        team_okr_form = Team_OKR_Form(request.POST)

    context = {'form':form, 'team_okr_form':team_okr_form}
    return render(request, 'team/add_okr.html', context)

@login_required
def team_update_okr(request, id):
    instance = get_object_or_404(Team_OKR, id=id)
    okr_form = OKR_Form(request.POST or None, instance = instance.okr)
    team_okr_form = Team_OKR_Form(request.POST or None, instance=instance)
    if okr_form.is_valid() and team_okr_form.is_valid():
        okr_form.save()
        team_okr_form = team_okr_form.save()
        return redirect('team_list_okr')
    context = {'instance':instance, 'okr_form':okr_form, 'team_okr_form':team_okr_form }
    return render(request, 'team/update_okr.html' ,context)

@login_required
def team_list_okr(request):
    team_okrs = Team_OKR.objects.all().prefetch_related()
    context = {"team_page":"active bg-secondary rounded", "team_okrs":team_okrs,}
    return render(request, 'team/list_okr.html', context)



@login_required
def team_delete_okr(request, id):
    instance = get_object_or_404(Team_OKR, id=id)
    instance.delete()
    return redirect('team_list_okr')

#===================================================================================

@login_required
def employee_add_okr(request):
    if request.method =='POST':
        form = OKR_Form(request.POST)
        employee_okr_form = Employee_OKR_Form(request.POST)
        if form.is_valid() and employee_okr_form.is_valid():
            okr = form.save()
            employee_okr = employee_okr_form.save(commit=False)
            employee_okr.okr = okr
            employee_okr.save()
            return redirect('employee_list_okr')
    else:
        form = OKR_Form()
        employee_okr_form = Employee_OKR_Form(request.POST)
    context = {'form':form, 'employee_okr_form':employee_okr_form}
    return render(request, 'employee/add_okr.html', context)

@login_required
def employee_update_okr(request, id):
    instance = get_object_or_404(Employee_OKR, id=id)
    okr_form = OKR_Form(request.POST or None, instance = instance.okr)
    employee_okr_form = Employee_OKR_Form(request.POST or None, instance=instance)
    if okr_form.is_valid() and employee_okr_form.is_valid():
        okr_form.save()
        employee_okr_form = employee_okr_form.save()
        return redirect('employee_list_okr')
    context = {'instance':instance, 'okr_form':okr_form, 'employee_okr_form':employee_okr_form}
    return render(request, 'employee/update_okr.html' ,context)

@login_required
def employee_list_okr(request):
    employee_okrs = Employee_OKR.objects.all().prefetch_related()
    context = {"employee_page":"active bg-secondary rounded", "employee_okrs":employee_okrs,}
    return render(request, 'employee/list_okr.html', context)



@login_required
def employee_delete_okr(request, id):
    instance = get_object_or_404(Employee_OKR, id=id)
    instance.delete()
    return redirect('employee_list_okr')

#===================================================================================

@login_required
def team_add_kr(request, id):
    if request.method == 'POST':
        instance = get_object_or_404(OKR, id=id)
        form = KR_Form(request.POST)
        team_kr_form =  Team_KR_Form(request.POST)
        if form.is_valid() and team_kr_form.is_valid():
            kr = form.save(commit=False)
            kr.okr_id = instance
            kr = form.save()
            team_kr = team_kr_form.save(commit=False)
            team_kr.kr = kr
            team_kr.save()
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('team_list_okr')


    else:
        form = KR_Form()
        team_kr_form = Team_KR_Form(request.POST)

    context = {'form':form, 'team_kr_form':team_kr_form}
    return render(request, 'team/add_kr.html', context)

@login_required
def employee_add_kr(request, id):
    if request.method == 'POST':
        instance = get_object_or_404(OKR, id=id)
        form = KR_Form(request.POST)
        employee_kr_form =  Employee_KR_Form(request.POST)
        if form.is_valid() and employee_kr_form.is_valid():
            kr = form.save(commit=False)
            kr.okr_id = instance
            kr = form.save()
            employee_kr = employee_kr_form.save(commit=False)
            employee_kr.kr = kr
            employee_kr.save()
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('team_list_okr')

    else:
        form = KR_Form()
        employee_kr_form = Employee_KR_Form(request.POST)

    context = {'form':form, 'employee_kr_form':employee_kr_form}
    return render(request, 'employee/add_kr.html', context)

#=================================================================================

@login_required
def edit_kr(request, id):
    instance = get_object_or_404(KR, id=id)
    try:
        kr_form = KR_Form(request.POST or None, instance=instance)
        team_kr_form = Team_KR_Form(request.POST or None, instance=instance.team_kr)
        if kr_form.is_valid() and team_kr_form.is_valid():
            kr_form.save()
            team_kr_form = team_kr_form.save()
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('employee_list_okr')
        context = {'instance':instance, 'kr_form':kr_form, 'team_kr_form':team_kr_form}
        return render(request, 'team/update_kr.html' ,context)
    except:
        kr_form = KR_Form(request.POST or None, instance=instance)
        employee_kr_form = Employee_KR_Form(request.POST or None, instance=instance.employee_kr)
        if kr_form.is_valid() and employee_kr_form.is_valid():
            kr_form.save()
            employee_kr_form = employee_kr_form.save()
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('employee_list_okr')
        context = {'instance':instance, 'kr_form':kr_form, 'employee_kr_form':employee_kr_form}
        return render(request, 'employee/update_kr.html' ,context)


@login_required
def delete_kr(request, id):
    instance = get_object_or_404(KR, id=id)
    instance.delete()
    return redirect(request.GET.get('next'))

@login_required
def add_progress(request, id):
    instance = get_object_or_404(KR, id=id)
    form = Progress_Form(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        if 'next' in request.POST:
            return redirect(request.POST.get('next'))
        else:
            return redirect('company_list_okr')

    context = {'instance':instance, 'form':form, 'progress':instance.progress}
    return render(request, 'add_progress.html' ,context)

#==============================================================================


