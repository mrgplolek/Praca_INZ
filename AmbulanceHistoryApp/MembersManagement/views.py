from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.models import User, auth
from django.contrib import messages


from .forms import NewUserForm

# Create your views here.
class AddNewUser(generic.CreateView):
    model = User
    form_class = NewUserForm
    template_name = 'loggedIn/admin/register_test.html'
    success_url = reverse_lazy('')

def login_test(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Niepoprawne dane logowania')
            return redirect('/accounts/login')

    else:
        return render(request, 'loggedOut/login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')
