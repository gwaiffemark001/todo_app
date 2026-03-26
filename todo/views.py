from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from todo.models import TodoItem

# Create your views here.
def index(request):
    return render(request, 'index.html')
@login_required
def todo_list(request):
    todos = TodoItem.objects.filter(user=request.user).order_by('date_due')
    context={'todos': todos}
    return render(request, 'todo.html', context)