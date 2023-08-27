from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm

@csrf_exempt
def task_list(request):
    tasks = Task.objects.all()
    response_text = '\n'.join([str(task) for task in tasks])
    return HttpResponse(response_text)

def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'testapp/task_detail.html', {'task': task})

from django.http import JsonResponse
import json

@csrf_exempt
def task_new(request):
    if request.method == "POST":
        data = json.loads(request.body)
        form = TaskForm(data)
        if form.is_valid():
            form.save()
            return JsonResponse({"message": "Task added successfully!"}, status=201)
        else:
            return JsonResponse(form.errors, status=400)
    else:
        return HttpResponse("Please send a POST request to add a task.")


def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_detail', pk=task.pk)
    else:
        form = TaskForm(instance=task)
    return render(request, 'testapp/task_edit.html', {'form': form})

def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    return redirect('task_list')
