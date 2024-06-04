from django.db import models
import re
from django.core.exceptions import ValidationError

def validate_email(value):
    email_regex = re.compile(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
    if not email_regex.match(value):
        raise ValidationError(f'{value} is not a valid email address.')


class Employee(models.Model):
    employee_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, validators=[validate_email])
    phone_number = models.CharField(max_length=20)
    def __str__(self):
        return str(self.name) 

class Project(models.Model):
    project_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    estimated_start_date = models.DateField()
    estimated_end_date = models.DateField()
    official_start_date = models.DateField()
    official_end_date = models.DateField()
    status = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class ProjectTeam(models.Model):
    team_id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    manager = models.ForeignKey(Employee, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.team_id)

class Budget(models.Model):
    budget_id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2)
    allocated_amount = models.DecimalField(max_digits=15, decimal_places=2)
    remaining_amount = models.DecimalField(max_digits=15, decimal_places=2)
    def __str__(self):
        return str(self.budget_id)
    def update_remaining_amount(self):
        self.remaining_amount = self.allocated_amount - self.total_amount
        self.save()

class Invoice(models.Model):
    invoice_id = models.AutoField(primary_key=True)
    invoice_number = models.CharField(max_length=50)
    invoice_concept = models.CharField(max_length=50)
    ruc = models.CharField(max_length=50)
    emission_date = models.DateField()
    def __str__(self):
        return str(self.invoice_number)

class Activity(models.Model):
    activity_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    responsible = models.ForeignKey(Employee, on_delete=models.CASCADE)
    description = models.TextField()
    estimated_start_date = models.DateField()
    estimated_end_date = models.DateField()
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=50)
    def __str__(self):
        return self.title

class Task(models.Model):
    task_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    description = models.TextField()
    priority = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    due_date = models.DateField()
    responsible = models.ForeignKey(Employee, on_delete=models.CASCADE)
    def __str__(self):
        return self.title

class Expense(models.Model):
    expense_id = models.AutoField(primary_key=True)
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    description = models.TextField()
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, default='default_number')
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    def __str__(self):
        return str(self.expense_id)
    def save(self, *args, **kwargs):
        super(Expense, self).save(*args, **kwargs)
        total_expense_amount = Expense.objects.filter(budget=self.budget).aggregate(total_amount=models.Sum('amount'))['total_amount'] or 0
        self.budget.total_amount = total_expense_amount
        self.budget.update_remaining_amount()

class Deliverable(models.Model):
    deliverable_id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    description = models.TextField()
    deadline = models.DateField()
    status = models.CharField(max_length=50)
    def __str__(self):
        return str(self.deliverable_id)

class ProjectTeamEmployee(models.Model):
    team = models.ForeignKey(ProjectTeam, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    class Meta:
        unique_together = (('team', 'employee'))
