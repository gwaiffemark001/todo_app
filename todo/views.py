from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import TodoItemForm
from todo.models import TodoItem


def index(request):
    context = {
        'is_authenticated': request.user.is_authenticated,
        'total_todos': 0,
        'completed_todos': 0,
        'pending_todos': 0,
    }
    if request.user.is_authenticated:
        user_todos = TodoItem.objects.filter(user=request.user)
        context['total_todos'] = user_todos.count()
        context['completed_todos'] = user_todos.filter(is_completed=True).count()
        context['pending_todos'] = context['total_todos'] - context['completed_todos']

    return render(request, 'index.html', context)


def _filter_user_todos(request):
    todos = TodoItem.objects.filter(user=request.user)

    query = request.GET.get('q', '').strip()
    category = request.GET.get('category', '').strip()
    status = request.GET.get('status', '').strip()

    if query:
        todos = todos.filter(title__icontains=query)

    if category in {'Work', 'Personal'}:
        todos = todos.filter(category=category)

    if status == 'completed':
        todos = todos.filter(is_completed=True)
    elif status == 'pending':
        todos = todos.filter(is_completed=False)

    todos = todos.order_by('is_completed', 'date_due')

    filters = {
        'q': query,
        'category': category,
        'status': status,
    }
    return todos, filters


@login_required
def todo_list(request):
    todos, filters = _filter_user_todos(request)
    context = {
        'todos': todos,
        'form': TodoItemForm(),
        'editing_todo': None,
        'filters': filters,
    }
    return render(request, 'todo.html', context)


@login_required
def todo_create(request):
    if request.method != 'POST':
        return redirect('todo:todo_list')

    form = TodoItemForm(request.POST)
    if form.is_valid():
        todo = form.save(commit=False)
        todo.user = request.user
        todo.save()
        messages.success(request, 'Todo created successfully.')
    else:
        messages.error(request, 'Could not create todo. Please fix the form errors.')

    return redirect('todo:todo_list')


@login_required
def todo_edit(request, todo_id):
    todo = get_object_or_404(TodoItem, id=todo_id, user=request.user)

    if request.method == 'POST':
        form = TodoItemForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Todo updated successfully.')
            return redirect('todo:todo_list')
        messages.error(request, 'Could not update todo. Please fix the form errors.')
    else:
        form = TodoItemForm(instance=todo)

    todos, filters = _filter_user_todos(request)
    context = {
        'todos': todos,
        'form': form,
        'editing_todo': todo,
        'filters': filters,
    }
    return render(request, 'todo.html', context)


@login_required
def todo_toggle(request, todo_id):
    if request.method != 'POST':
        return redirect('todo:todo_list')

    todo = get_object_or_404(TodoItem, id=todo_id, user=request.user)
    todo.is_completed = not todo.is_completed
    todo.save(update_fields=['is_completed'])
    return redirect('todo:todo_list')


@login_required
def todo_delete(request, todo_id):
    if request.method != 'POST':
        return redirect('todo:todo_list')

    todo = get_object_or_404(TodoItem, id=todo_id, user=request.user)
    todo.delete()
    messages.success(request, 'Todo deleted successfully.')
    return redirect('todo:todo_list')