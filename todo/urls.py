from . import views
from django.urls import path

app_name = 'todo'
urlpatterns=[
  path('', views.index, name='index'),
  path('todos/', views.todo_list, name='todo_list'),
]