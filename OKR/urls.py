
from django.contrib import admin
from django.urls import path, include
from OKR.core import views
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/employees', views.employee_list, name='employee_list'),
    path('accounts/employees/update/<int:id>/', views.employee_update, name='employee_update'),
    path('accounts/employees/delete/<int:id>/', views.employee_delete, name='employee_delete'),
    path('teams/add_team/', views.add_team, name='add_team'),
    path('teams/team_list/', views.team_list, name='team_list'),
    path('teams/team_update/<int:id>/', views.team_update, name='team_update'),
    path('teams/team_delete/<int:id>/', views.team_delete, name='team_delete'),

    path('company/add_okr/', views.company_add_okr, name='company_add_okr'),
    path('company/list_okr/', views.company_list_okr, name='company_list_okr'),
    path('company/edit/<int:id>/', views.company_update_okr, name='company_update_okr'),
    path('company/delete_okr/<int:id>/', views.company_delete_okr, name='company_delete_okr'),

    path('team/add_okr/', views.team_add_okr, name='team_add_okr'),
    path('team/edit/<int:id>', views.team_update_okr, name='team_update_okr'),
    path('team/list_okr/', views.team_list_okr, name='team_list_okr'),
    path('team/delete_okr/<int:id>', views.team_delete_okr, name='team_delete_okr'),

    path('team/add_kr/<int:id>/', views.team_add_kr, name='team_add_kr'),

    path('employee/add_kr/<int:id>/', views.employee_add_kr, name='employee_add_kr'),

    path('employee/add_okr/', views.employee_add_okr, name='employee_add_okr'),
    path('employee/edit/<int:id>/', views.employee_update_okr, name='employee_update_okr'),
    path('employee/list_okr/', views.employee_list_okr, name='employee_list_okr'),
    path('employee/delete_okr/<int:id>', views.employee_delete_okr, name='employee_delete_okr'),

    path('edit_kr/<int:id>/', views.edit_kr, name='edit_kr'),

    path('delete_kr/<int:id>/', views.delete_kr, name='delete_kr'),

    path('add_progress/<int:id>', views.add_progress, name='add_progress')

]

