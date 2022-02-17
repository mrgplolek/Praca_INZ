from django import forms
from django.contrib.auth.models import User

from .models import zdjecie_naprawa_przed


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
            'is_superuser': "      Uwaga! Zaznaczając tę opcję tworzysz konto administratora.",
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
