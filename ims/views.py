from django.shortcuts import render, redirect
from .models import *
from .forms import *
# Create your views here.


def home(request):
    title = "welcome: this is the our homepage"
    context = {"title": title}
    return render(request, 'home.html', context)


def list_items(request):
    title = 'list of items'
    queryset = Stock.objects.all()
    context = {
        "title": title,
        "queryset": queryset
    }
    return render(request, "list_items.html",  context)


def add_items(request):
    form = StockCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('/list_items')
    context = {
        "form": form,
        "title": "Add item",
    }
    return render(request, "add_items.html", context)
