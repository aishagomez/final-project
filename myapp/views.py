import json
from django.http import JsonResponse, HttpResponseNotAllowed, HttpResponseBadRequest, HttpResponse
from .models import Employee, Project, ProjectTeam, Budget, Invoice, Activity, Task, Expense, Deliverable, ProjectTeamEmployee
from myapp.forms import GetInp, InsertForm, TableForm, UpdateForm, TableFormIns, ProjectSelectionForm
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from xhtml2pdf import pisa

model_map = {
    'employee': Employee,
    'project': Project,
    'projectteam': ProjectTeam,
    'budget': Budget,
    'invoice': Invoice,
    'activity': Activity,
    'task': Task,
    'expense': Expense,
    'deliverable': Deliverable,
    'projectteamemployee': ProjectTeamEmployee,
}

def manage(request, table, id):
    context = {}
    not_displayed_keys = ['Project', 'Budget', 'Activity', 'Employee', 'Expense']
    context['displayed_keys'] = not_displayed_keys
    context['table'] = table.replace('_', ' ')
    if table == 'Project':
        project = get_object_or_404(Project, project_id=id)
        activities = Activity.objects.filter(project_id=project)
        budgets = Budget.objects.filter(project_id=id)
        derivables = Deliverable.objects.filter(project_id=id)
        project_team = ProjectTeam.objects.get(project_id=project)
        project_team_employees_ids = ProjectTeamEmployee.objects.filter(team_id=project_team).values_list('employee_id', flat=True)
        employees = Employee.objects.filter(employee_id__in=project_team_employees_ids)

        related_employees=[]
        related_activities = [[(field_name.replace('_', ' '), value) for field_name, value in activity.__dict__.items()][1:] for activity in activities]
        related_budgets = [[(field_name.replace('_', ' '), value) for field_name, value in budget.__dict__.items()][1:] for budget in budgets]
        related_employees = [[(field_name.replace('_', ' '), value) for field_name, value in employee.__dict__.items()][1:] for employee in employees]
        related_derivables = [[(field_name.replace('_', ' '), value) for field_name, value in derivable.__dict__.items()][1:] for derivable in derivables]
        
        context['entity'] = [(field_name.replace('_', ' '), value) for field_name, value in project.__dict__.items()][1:]
        context['Team'] = [(field_name.replace('_', ' '), value) for field_name, value in project_team.__dict__.items()][1:]
        context['related_entities'] = {
            'Activity': related_activities,
            'Budget': related_budgets,
            'Employee': related_employees,
            'Derivable': related_derivables,
        }

    elif table == 'Activity':
        activity = get_object_or_404(Activity, activity_id=id)
        tasks = Task.objects.filter(activity_id=id)
        related_tasks = [[(field_name.replace('_', ' '), value) for field_name, value in task.__dict__.items()][1:] for task in tasks]
        context['entity'] = [(field_name.replace('_', ' '), value) for field_name, value in activity.__dict__.items()][1:]
        context['related_entities'] = {
            'Task': related_tasks,
        }

    elif table == 'Budget':
        budget = get_object_or_404(Budget, budget_id=id)
        expenses = Expense.objects.filter(budget_id=id)
        related_expenses = [[(field_name.replace('_', ' '), value) for field_name, value in expense.__dict__.items()][1:] for expense in expenses]
        context['entity'] = [(field_name.replace('_', ' '), value) for field_name, value in budget.__dict__.items()][1:]
        context['related_entities'] = {
            'Expense': related_expenses,
        }

    elif table == 'Employee':
        employee = get_object_or_404(Employee, employee_id=id)
        tasks = Task.objects.filter(responsible=id)
        related_tasks = [[(field_name.replace('_', ' '), value) for field_name, value in task.__dict__.items()][1:] for task in tasks]
        context['entity'] = [(field_name.replace('_', ' '), value) for field_name, value in employee.__dict__.items()][1:]
        context['related_entities'] = {
            'Task': related_tasks,
        }

    elif table == 'Expense':
        expense = get_object_or_404(Expense, expense_id=id)
        tasks = Task.objects.filter(task_id=expense.task_id)
        invoices = Invoice.objects.filter(invoice_id=expense.invoice_id)
        related_tasks = [[(field_name.replace('_', ' '), value) for field_name, value in task.__dict__.items()][1:] for task in tasks]
        related_invoice = [[(field_name.replace('_', ' '), value) for field_name, value in invoice.__dict__.items()][1:] for invoice in invoices]
        context['entity'] = [(field_name.replace('_', ' '), value) for field_name, value in expense.__dict__.items()][1:]
        context['related_entities'] = {
            'Task': related_tasks,
            'Invoice':related_invoice,
        }

    return render(request, 'manage.html', context)

def export_pdf(request, project_id):
    project = Project.objects.get(pk=project_id)
    try:
        project_team = ProjectTeam.objects.get(project_id=project)
    except Exception as e:
        project_team = None
    try:
        ProjectTeamEmployee_set=ProjectTeamEmployee.objects.filter(team_id=project_team.pk)
        project_team_employees_ids = ProjectTeamEmployee_set.values_list('employee_id', flat=True)
        project_team_employees = Employee.objects.filter(employee_id__in=project_team_employees_ids)
    except Exception as e:
            project_team_employees = None
    try:
        activities = Activity.objects.filter(project=project)
    except Exception as e:
        activities = None
    try:
        activities_id = activities.values_list('activity_id', flat=True)
        tasks = Task.objects.filter(activity_id__in=activities_id)
    except Exception as e:
        tasks = None

    try:
        budget = Budget.objects.get(project_id=project)
    except Exception as e:
        budget = None
    try:
        expenses = Expense.objects.filter(budget=budget.pk)
    except Exception as e:
        expenses = None
    try:    
        deliverables = Deliverable.objects.filter(project_id=project)
    except Exception as e:
        deliverables = None
    context = {
        'project': project,
        'project_team': project_team,
        'activities': activities,
        'budget': budget,
        'expenses': expenses,
        'deliverables': deliverables,
        'project_team_employees': project_team_employees,
        'tasks_act': tasks,
    }
    html = render_to_string("report.html", context)

    pdf_file = HttpResponse(content_type='application/pdf')
    pdf_file['Content-Disposition'] = 'attachment; filename="report.pdf"'

    pisa.CreatePDF(html, dest=pdf_file)

    return pdf_file

def report(request, project_id):
    project = Project.objects.get(pk=project_id)
    try:
        project_team = ProjectTeam.objects.get(project_id=project)
    except Exception as e:
        project_team = None
    try:
        ProjectTeamEmployee_set=ProjectTeamEmployee.objects.filter(team_id=project_team.pk)
        project_team_employees_ids = ProjectTeamEmployee_set.values_list('employee_id', flat=True)
        project_team_employees = Employee.objects.filter(employee_id__in=project_team_employees_ids)
    except Exception as e:
            project_team_employees = None
    try:
        activities = Activity.objects.filter(project=project)
    except Exception as e:
        activities = None
    try:
        activities_id = activities.values_list('activity_id', flat=True)
        tasks = Task.objects.filter(activity_id__in=activities_id)
    except Exception as e:
        tasks = None

    try:
        budget = Budget.objects.get(project_id=project)
    except Exception as e:
        budget = None
    try:
        expenses = Expense.objects.filter(budget=budget.pk)
    except Exception as e:
        expenses = None
    try:    
        deliverables = Deliverable.objects.filter(project_id=project)
    except Exception as e:
        deliverables = None
    context = {
        'project': project,
        'project_team': project_team,
        'activities': activities,
        'budget': budget,
        'expenses': expenses,
        'deliverables': deliverables,
        'project_team_employees': project_team_employees,
        'tasks_act': tasks,
    }
    return render(request, 'report.html', context)

def generate_report(request):
    if request.method == 'POST':
        form = ProjectSelectionForm(request.POST)
        if form.is_valid():
            project_id = form.cleaned_data['project'].pk
            return redirect('report', project_id=project_id)
    else:
        form = ProjectSelectionForm()
    return render(request, 'generate_report.html', {'form': form})

def home(request):
    projects = Project.objects.all()
    obj_values = []
    field_names = [field.name for field in Project._meta.fields]
    for project in projects:
        values = [(field_name, getattr(project, field_name)) for field_name in field_names]
        obj_values.append(values)
    return render(request, 'home.html', {'projects': projects, 'obj_values': obj_values})

def about(request):
    return render(request, 'about.html')

def show_table(request):
    if request.method == 'GET':
        form = TableForm(request.GET)
        if form.is_valid():
            table = form.cleaned_data['table']
            model = model_map.get(table.lower())
            if not model:
                return render(request, 'error.html', {'error_message': f"Table {table} not found"})
            try:
                obj = model.objects.all()
                field_names = [field.name for field in model._meta.fields]
                obj_values = [[getattr(instance, field) for field in field_names] for instance in obj]
                field_names = []
                for field in model._meta.fields:
                    name = field.name.replace('_', ' ')
                    if ' id' in name and 'budget' not in name and 'team' not in name and 'derivable' not in name and 'expense' not in name:
                        name = name.split(' ')[0]
                    field_names.append(name)
                return render(request, 'show_table.html', {'form': form, 'obj_values': obj_values, 'field_names': field_names})
            except Exception as e:
                return render(request, 'error.html', {'error_message': f"Unexpected error: {str(e)}"})
    else:
        form = TableForm()
    return render(request, 'show_table.html', {'form': form})

def choose_table_insert(request):
    if request.method == 'POST':
        table = request.POST.get('table')
        if table:
            return redirect('insert_table', table=table)
        else:
            return render(request, 'error.html', {'error_message': f"Table is required"})
    else:
        table_form = TableFormIns()
        return render(request, 'choose_table.html', {'table_form': table_form})

def insert_table(request, table):
    if request.method == 'GET':
        model = model_map.get(table.lower())
        if not model:
            return render(request, 'error.html', {'error_message': f"Table {table} not found"})
        table_fields = {field.name: field.get_internal_type() for field in model._meta.fields}
        form = InsertForm(table_fields=table_fields)        
        return render(request, 'insert_form.html', {'form': form, 'table_name': table, 'insert_success': False})
    
    elif request.method == 'POST':
        model = model_map.get(table.lower())
        if not model:
            return render(request, 'error.html', {'error_message': f"Table {table} not found"})
        try:
            table_fields = {field.name: field.get_internal_type() for field in model._meta.fields}
            form = InsertForm(request.POST, table_fields=table_fields)
            if form.is_valid():
                data = {field_name.replace(' ', '_'): form.cleaned_data[field_name] for field_name in form.cleaned_data}
                
                for field in model._meta.fields:
                    if field.get_internal_type() == 'ForeignKey':
                        related_model = field.related_model
                        if data.get(field.name):
                            data[field.name] = related_model.objects.get(pk=data[field.name])
                
                obj = model.objects.create(**data)
                obj_pk = obj.pk
                form = InsertForm(table_fields=table_fields) 
                return render(request, 'insert_form.html', {'form': form, 'table_name': table, 'insert_success': True, 'obj_pk': obj_pk})
            else:
                return render(request, 'error.html', {'errors': f"Unexpected error: {form.errors}"})
        except Exception as e:
            return render(request, 'error.html', {'error_message': f"Unexpected error: {str(e)}"})
    else:
        return render(request, 'error.html', {'error_message': "Method not allowed: Only GET AND POST requests are allowed."})

def delete_object(request):
    if request.method == 'GET':
        rqt=request.GET
        if rqt:
            table=rqt['table']
            attribute=rqt['attribute']
            value=rqt['value']
            model = model_map.get(table.lower())
            if not model:
                return render(request, 'error.html', {'error_message': f"Table {table} not found"})
            try:
                filter={attribute: value}
                obj = model.objects.get(**filter)
                if not obj:
                    return render(request, 'error.html', {'error_message': f"Object with {attribute}: {value} not found"})
                obj.delete()
                return render(request, 'delete.html', {'form': GetInp(), 'obj_data': [attribute, value]})
            except Exception as e:
                return render(request, 'error.html', {'error_message': f"Unexpected error: {str(e)}"})
        else:
            return render(request, 'delete.html', {'form': GetInp()})
    else:
        return render(request, 'error.html', {'error_message': "Method not allowed: Only GET requests are allowed."})

def get_attributes(request):
    table = request.GET.get('table')
    model = model_map.get(table.lower())
    if not model:
        return render(request, 'error.html', {'error_message': f"Table is required"})
    attributes = [field.name for field in model._meta.fields]
    return JsonResponse({'attributes': attributes})

def get_object(request):
    if request.method == 'GET':
        rqt = request.GET
        if rqt:
            table = rqt.get('table')
            attribute = rqt.get('attribute')
            value = rqt.get('value')
            model = model_map.get(table.lower())
            if not model:
                return render(request, 'error.html', {'error_message': f"Table {table} not found"})
            try:
                filter_kwargs = {attribute: value}
                objs = model.objects.filter(**filter_kwargs)
                if not objs.exists():
                    return render(request, 'error.html', {'error_message': f"No objects found with {attribute}: {value}"})
                field_names = [field.name for field in model._meta.fields]
                obj_values = [[getattr(instance, field) for field in field_names] for instance in objs]
                field_names = []
                for field in model._meta.fields:
                    name = field.name.replace('_', ' ')
                    if ' id' in name and 'budget' not in name and 'team' not in name and 'derivable' not in name and 'expense' not in name:
                        name = name.split(' ')[0]
                    field_names.append(name)
                return render(request, 'get.html', {'form': GetInp(), 'obj_values': obj_values, 'field_names': field_names})
            except Exception as e:
                return render(request, 'error.html', {'error_message': f"Unexpected error: {str(e)}"})
        else:
            return render(request, 'get.html', {'form': GetInp()})
    else:
        return render(request, 'error.html', {'error_message': "Method not allowed: Only GET requests are allowed."})

def choose_object(request):
    if request.method == 'GET':
        form = request.GET
        if form:
            table = str(form.get('table'))
            attribute = str(form.get('attribute'))
            value = str(form.get('value'))
            if table and attribute and value:
                model = model_map.get(table.lower())
                if not model:
                    return render(request, 'error.html', {'error_message': f"Table {table} not found"})
                try:
                    obj = model.objects.get(**{attribute: value})
                    return redirect('update_object', table=table, attribute=attribute, value=value)
                except model.DoesNotExist:
                    return render(request, 'error.html', {'error_message': f"Object with {attribute} = {value} not found in {table}"})
            else:
                return render(request, 'error.html', {'error_message': f"Data is required"})
        else:
            form = GetInp()
            return render(request, 'choose_object.html', {'form': form})
    else:
        return render(request, 'error.html', {'error_message': "Method not allowed: Only GET requests are allowed."})

def update_object(request, table, attribute, value):
    model = model_map.get(table.lower())
    if not model:
        return render(request, 'error.html', {'error_message': f"Tabla {table} no encontrada"})

    try:
        obj = model.objects.get(**{attribute: value})
    except model.DoesNotExist:
        return render(request, 'error.html', {'error_message': f"Objeto con {attribute} = {value} no encontrado en {table}"})

    if request.method == 'GET':
        table_fields = {field.name: field.get_internal_type() for field in model._meta.fields if field.name != model._meta.pk.name}
        form = UpdateForm(table_fields=table_fields)
        return render(request, 'update_form.html', {'form': form, 'table_name': table, 'attribute': attribute, 'value': value, 'update_success': False})

    elif request.method == 'POST':
        table_fields = {field.name: field.get_internal_type() for field in model._meta.fields if field.name != model._meta.pk.name}
        form = UpdateForm(request.POST, table_fields=table_fields)
        if form.is_valid():
            data = {field_name.replace(' ', '_'): form.cleaned_data[field_name] for field_name in form.cleaned_data}
            print(data)
            for key, value in data.items():
                if hasattr(obj, key) and key and value:
                    setattr(obj, key, value)
            obj.save()
            return render(request, 'update_form.html', {'attribute': attribute, 'value': obj.pk, 'update_success': True})
        else:
            return render(request, 'update_form.html', {'form': form, 'table_name': table, 'attribute': attribute, 'value': value, 'update_success': False, 'errors': form.errors})
    else:
        return render(request, 'error.html', {'error_message': "Método no permitido: Solo se permiten solicitudes GET y POST."})


