from django.shortcuts import render

# Create your views here.
def show_details(request):
    context = {
        'application_name' : 'Glorious Goals Shop',
        'name': 'Aldebaran Rahman Adhitya',
        'class': 'PBP KKI'
    }

    return render(request, "main.html", context)