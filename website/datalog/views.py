from django.shortcuts import render

# Create your views here.
def base(request):
  views_name = "<a href='link'>Click</a>"
  return  render(request,"base.html", {"name":views_name})