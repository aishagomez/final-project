from django import forms
from .models import Employee, Project, ProjectTeam, Budget, Invoice, Activity, Task, Expense, Deliverable, ProjectTeamEmployee

class ProjectSelectionForm(forms.Form):
    project = forms.ModelChoiceField(queryset=Project.objects.all(), label='Select Project', empty_label="---Choose Project---")


class TableFormIns(forms.Form):
    TABLE_CHOICES = [
        ('', '---Choose Table---'),
        ('Employee', 'Employee'),
        ('Project', 'Project'),
        ('ProjectTeam', 'Project Team'),
        ('Budget', 'Budget'),
        ('Invoice', 'Invoice'),
        ('Activity', 'Activity'),
        ('Task', 'Task'),
        ('Expense', 'Expense'),
        ('Deliverable', 'Deliverable'),
        ('ProjectTeamEmployee', 'Add employee to team'),
    ]

    table = forms.ChoiceField(label='Table', choices=TABLE_CHOICES)

class TableForm(forms.Form):
    TABLE_CHOICES = [
        ('', '---Choose Table---'),
        ('Employee', 'Employee'),
        ('Project', 'Project'),
        ('ProjectTeam', 'Project Team'),
        ('Budget', 'Budget'),
        ('Invoice', 'Invoice'),
        ('Activity', 'Activity'),
        ('Task', 'Task'),
        ('Expense', 'Expense'),
        ('Deliverable', 'Deliverable'),
        ('ProjectTeamEmployee', 'Employee in team'),
    ]

    table = forms.ChoiceField(label='Table', choices=TABLE_CHOICES)

class GetInp(forms.Form):
    TABLE_CHOICES = [
        ('', '---Choose Table---'),
        ('Employee', 'Employee'),
        ('Project', 'Project'),
        ('ProjectTeam', 'Project Team'),
        ('Budget', 'Budget'),
        ('Invoice', 'Invoice'),
        ('Activity', 'Activity'),
        ('Task', 'Task'),
        ('Expense', 'Expense'),
        ('Deliverable', 'Deliverable'),
        ('ProjectTeamEmployee', 'Employee in team'),
    ]
    table = forms.ChoiceField(label='Table', choices=TABLE_CHOICES)
    attribute = forms.ChoiceField(label='Attribute', choices=[], required=True)
    value = forms.CharField(label='Value', max_length=50, widget=forms.TextInput, required=True)

class InsertForm(forms.Form):
    def __init__(self, *args, table_fields=None, **kwargs):
        super(InsertForm, self).__init__(*args, **kwargs)
        if table_fields:
            for field_name, field_type in table_fields.items():
                field_name = field_name.replace('_', ' ')
                if field_type == 'CharField':
                    self.fields[field_name] = forms.CharField(label=field_name, max_length=255)
                elif field_type == 'EmailField':
                    self.fields[field_name] = forms.EmailField(label=field_name, max_length=255)
                elif field_type == 'IntegerField':
                    self.fields[field_name] = forms.IntegerField(label=field_name)
                elif field_type == 'ForeignKey':
                    self.fields[field_name] = forms.IntegerField(label=field_name)
                elif field_type == 'DateField':
                    self.fields[field_name] = forms.DateField(label=field_name)
                elif field_type == 'TextField':
                    self.fields[field_name] = forms.CharField(label=field_name, widget=forms.Textarea)
                elif field_type == 'DecimalField':
                    self.fields[field_name] = forms.DecimalField(label=field_name, max_digits=15, decimal_places=2)

class UpdateForm(forms.Form):
    def __init__(self, *args, table_fields=None, **kwargs):
        super(UpdateForm, self).__init__(*args, **kwargs)
        if table_fields:
            for field_name, field_type in table_fields.items():
                field_name = field_name.replace('_', ' ')
                if field_type == 'CharField':
                    self.fields[field_name] = forms.CharField(label=field_name, max_length=255, required=False)
                elif field_type == 'EmailField':
                    self.fields[field_name] = forms.EmailField(label=field_name, max_length=255, required=False)
                elif field_type == 'IntegerField':
                    self.fields[field_name] = forms.IntegerField(label=field_name, required=False)
                elif field_type == 'ForeignKey':
                    self.fields[field_name] = forms.IntegerField(label=field_name, required=False)
                elif field_type == 'DateField':
                    self.fields[field_name] = forms.DateField(label=field_name, required=False)
                elif field_type == 'TextField':
                    self.fields[field_name] = forms.CharField(label=field_name, widget=forms.Textarea, required=False)
                elif field_type == 'DecimalField':
                    self.fields[field_name] = forms.DecimalField(label=field_name, max_digits=15, decimal_places=2, required=False)
