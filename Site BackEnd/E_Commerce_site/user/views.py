from django.contrib.auth import authenticate, login, get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from .algorithms import get_client_ip

User = get_user_model()


# Create your views here.


def register_user(request):
    if request.user.is_authenticated:
        return False

    """View for register"""

    if request.method == 'POST':
        pass

    return render(request, 'user/register.html')


def login_user(request):
    if request.user.is_authenticated:
        return False

    """Login view """
    if request.method == 'POST' and not request.user.is_authenticated:
        user = authenticate(request, email=request.POST['email'], password=request.POST['password'])

        if user:
            login(request, user)
            return JsonResponse({
                'login': True
            })
        else:
            return JsonResponse({
                'login': False
            })
    return render(request, 'user/login.html')


@login_required
def logout_user(request):
    if not request.user.is_authenticated:
        return redirect('/login')

    """Logs out a user"""

    logout(request)
    return redirect('/')

# Create your views here.
