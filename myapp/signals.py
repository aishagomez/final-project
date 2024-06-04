from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Expense, Budget
from myapp import models

@receiver(post_save, sender=Expense)
def update_budget_on_save(sender, instance, **kwargs):
    budget = instance.budget
    total_expense_amount = Expense.objects.filter(budget=budget).aggregate(total_amount=models.Sum('amount'))['total_amount'] or 0
    budget.total_amount = total_expense_amount
    budget.remaining_amount = budget.allocated_amount - budget.total_amount
    budget.save()

@receiver(post_delete, sender=Expense)
def update_budget_on_delete(sender, instance, **kwargs):
    budget = instance.budget
    total_expense_amount = Expense.objects.filter(budget=budget).aggregate(total_amount=models.Sum('amount'))['total_amount'] or 0
    budget.total_amount = total_expense_amount
    budget.remaining_amount = budget.allocated_amount - budget.total_amount
    budget.save()
