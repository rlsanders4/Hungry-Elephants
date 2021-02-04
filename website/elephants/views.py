from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render


def index(request):
    context = {'name': 'Hungry Elephants', }
    return render(request, 'elephants/index.html', context)