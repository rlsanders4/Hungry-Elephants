from django.shortcuts import render

# Create your views here.
def index(request):
    context = {'name': 'Hungry Elephants Data Visualisation', }
    return render(request, 'datalog/index.html', context)
