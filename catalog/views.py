from django.shortcuts import render

# Create your views here.
def home(request):
    """
    Контролер главной страницы
    """
    return render(request, 'home.html')

def contacts(request):
    """
    Контролер страницы контактов
    """
    return render(request, 'contacts.html')