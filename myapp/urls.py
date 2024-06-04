from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('showtable/', views.show_table, name='show_table'),
    path('insert/', views.choose_table_insert, name='choose_table_insert'),
    path('insert/<str:table>/', views.insert_table, name='insert_table'),
    path('insert/project/', views.insert_table, name='new_project'),  
    path('delete/', views.delete_object, name='delete_object'),
    path('get_attributes/', views.get_attributes, name='get_attributes'),
    path('get/', views.get_object, name='get_object'),
    path('update/', views.choose_object, name='choose_object'),
    path('update/<str:table>/<str:attribute>/<str:value>/', views.update_object, name='update_object'),
    path('report/', views.generate_report, name='choose_project'), 
    path('report/<int:project_id>/', views.report, name='report'),
    path('export/<int:project_id>/', views.export_pdf, name="export_pdf" ),
    path('<str:table>/<int:id>/', views.manage, name='manage'),
]
