from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_delete
from django.dispatch import receiver
#
from datetime import datetime

ROLES = (
         (1, 'Administrator'),
         (2, 'Szef'),
         (3, 'Kierownik zespolu'),
         (4, 'Pracownik')
        )

class Team(models.Model):
    name = models.CharField(max_length=60)

    def __str__(self):
        return format(self.name)

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    team_id = models.ForeignKey(Team, on_delete=models.CASCADE,  related_name='belongs')
    role = models.IntegerField(choices=ROLES, default=4)
##blank=True, null=True, db_constraint=False,
    def __str__(self):
        return format(self.user.username)

@receiver(post_delete, sender=Employee)
def delete_user(sender, instance, **kwargs):
    instance.user.delete()

class OKR(models.Model):
    name = models.CharField(max_length=60)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField

    def __str__(self):
        return format(self.name)

class Team_OKR(models.Model):
    okr = models.OneToOneField(OKR, on_delete=models.CASCADE)
    team_id = models.ForeignKey(Team, on_delete=models.CASCADE,  related_name='team_owns')

    def __str__(self):
        return format(self.name)

class Employee_OKR(models.Model):
    okr = models.OneToOneField(OKR, on_delete=models.CASCADE)
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE,  related_name='employee_owns')

    def __str__(self):
        return format(self.name)

@receiver(post_delete, sender=Team_OKR)
def team_delete_okr(sender, instance, **kwargs):
    instance.okr.delete()

@receiver(post_delete, sender=Employee_OKR)
def employee_delete_okr(sender, instance, **kwargs):
    instance.okr.delete()

class KR(models.Model):
    okr_id = models.ForeignKey(OKR, on_delete=models.CASCADE,  related_name='contains')
    name = models.CharField(max_length=60)
    goal = models.IntegerField(default=0)
    progress = models.IntegerField(default=0)

    def __str__(self):
        return format(self.name)

class Employee_KR(models.Model):
    kr = models.OneToOneField(KR, on_delete=models.CASCADE)
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE,  related_name='employee_execute')

    def __str__(self):
        return format(self.name)

class Team_KR(models.Model):
    kr = models.OneToOneField(KR, on_delete=models.CASCADE)
    team_id = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team_execute')

    def __str__(self):
        return format(self.name)

@receiver(post_delete, sender=Team_KR)
def team_delete_kr(sender, instance, **kwargs):
    instance.kr.delete()

@receiver(post_delete, sender=Employee_KR)
def employee_delete_kr(sender, instance, **kwargs):
    instance.kr.delete()