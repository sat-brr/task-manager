from django.shortcuts import render


def home_page(request):
    if request.user.is_authenticated:
        return render(request, 'home_auth.html')
    else:
        return render(request, 'home.html')
