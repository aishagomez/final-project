from django.contrib import admin
from .models import Employee, Project, ProjectTeam, Budget, Invoice, Activity, Task, Expense, Deliverable, ProjectTeamEmployee
# Register your models here.

admin.site.register(Project)