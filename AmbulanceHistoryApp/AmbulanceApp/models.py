from django.db import models as md

# Create your models here.

class dane_podstacji(md.Model):
    miasto = md.CharField(max_length=100)
    adres = md.TextField()
    opis = md.TextField()

class dane_pojazdu(md.Model):
    numer_VIN = md.CharField(max_length=100, unique=True)
    marka_pojazdu = md.CharField(max_length=100)
    model = md.CharField(max_length=100)
    silnik = md.CharField(max_length=100)
    typ_skrzyni = md.CharField(max_length=100)
    przebieg = md.IntegerField()
    rodzaj = md.CharField(max_length=100)
    kategoria_PJ = md.CharField(max_length=100)
    numer_rejestracyjny = md.CharField(max_length=100, unique=True)
    status = md.CharField(max_length=100)
    podstacja = md.ForeignKey(dane_podstacji, on_delete=md.RESTRICT)

class historia_ubezpieczenia(md.Model):
    data_wykupu = md.DateTimeField(auto_now=False, auto_now_add=False)
    przebieg = md.IntegerField()
    rodzaj = md.CharField(max_length=100)
    pojazd = md.ForeignKey(dane_pojazdu, on_delete=md.RESTRICT)

class historia_przegladu(md.Model):
    data_przegladu = md.DateTimeField(auto_now=False, auto_now_add=False)
    przebieg = md.IntegerField()
    wynik = md.CharField(max_length=100)
    opis_usterek = md.TextField(blank=True)
    pojazd = md.ForeignKey(dane_pojazdu, on_delete=md.RESTRICT)

class dane_wyjazdu(md.Model):
    data_wyjazdu = md.DateTimeField(auto_now=False, auto_now_add=False)
    data_powrotu = md.DateTimeField(auto_now=False, auto_now_add=False)
    notatka = md.TextField(blank=True)
    pojazd = md.ForeignKey(dane_pojazdu, on_delete=md.RESTRICT)

class zdjecie_wyjazd(md.Model):
    url = md.ImageField(upload_to="files/interventions")
    wyjazd = md.ForeignKey(dane_wyjazdu, on_delete=md.CASCADE)

class historia_naprawy(md.Model):
    data_naprawy = md.DateTimeField(auto_now=False, auto_now_add=False)
    przebieg = md.IntegerField()
    opis_usterek = md.TextField()
    kategoria = md.CharField(max_length=100)
    pojazd = md.ForeignKey(dane_pojazdu, on_delete=md.RESTRICT)

class zdjecie_naprawa_przed(md.Model):
    url = md.ImageField(upload_to="files/repair/before")
    naprawa = md.ForeignKey(historia_naprawy, on_delete=md.CASCADE)

class zdjecie_naprawa_po(md.Model):
    url = md.ImageField(upload_to="files/repair/after")
    naprawa = md.ForeignKey(historia_naprawy, on_delete=md.CASCADE)

class faktura(md.Model):
    url = md.FileField(upload_to="files/repair/invoice")
    naprawa = md.ForeignKey(historia_naprawy, on_delete=md.CASCADE)

