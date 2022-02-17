from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

class NewUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password', 'is_superuser')

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', "placeholder" : "Imię"}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', "placeholder" : "Nazwisko"}),
            'email': forms.EmailInput(attrs={'class': 'form-control', "placeholder" : "Adres e-mail"}),
            'username': forms.TextInput(attrs={'class': 'form-control', "placeholder" : "Nazwa użytkownika"}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', "placeholder" : "Hasło"}),
            'is_superuser': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'first_name': "",
            'last_name': "",
            'email': "",
            'username': "",
            'password': "",
            'is_superuser': "Konto administratora",
        }
        help_texts= {
            'username': None,
            'is_superuser': "      Uwaga! Ta opcja tworzy konto z uprawnieniami administratora.",
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs=({'class': 'form-control', "placeholder" : "Username"})))
    password = forms.CharField(widget=forms.PasswordInput(attrs=({'class': 'form-control', "placeholder" : "Password"})))