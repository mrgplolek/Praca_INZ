from django.shortcuts import render, redirect
import datetime

from django.views.decorators.csrf import csrf_exempt
from .models import dane_podstacji, dane_pojazdu, dane_wyjazdu, \
    historia_przegladu, historia_ubezpieczenia, historia_naprawy, zdjecie_naprawa_przed, zdjecie_naprawa_po, faktura
from django.db.models import Prefetch
from django.contrib import messages
from django.core.files.storage import FileSystemStorage

# Create your views here.

def home(request):
    return render(request, 'loggedIn/home.html')

def add_station(request):
    if request.method == 'POST':
        city = request.POST['city']
        address = request.POST['address']
        desc = request.POST['description']
        station = dane_podstacji(miasto=city, adres=address, opis=desc)
        station.save()
        return redirect('/')
    else:
        return render(request, 'loggedIn/admin/addStation.html')

def add_vehicle(request):
    if request.method == 'POST':
        vin = request.POST["vin"]
        make = request.POST["make"]
        model = request.POST["model"]
        engine = request.POST["engine"]
        transmission = request.POST["transmission"]
        mileage = request.POST["mileage"]
        ambulance_type = request.POST["type"]
        licence_cat = request.POST["driver_cat"]
        plates = request.POST["reg_num"]
        status = request.POST["status"]
        station = request.POST["station"]
        vehicle = dane_pojazdu(numer_VIN=vin,
                               marka_pojazdu=make,
                               model=model,
                               silnik=engine,
                               typ_skrzyni=transmission,
                               przebieg=mileage,
                               rodzaj=ambulance_type,
                               kategoria_PJ=licence_cat,
                               numer_rejestracyjny=plates,
                               status=status,
                               podstacja_id=station
                               )
        vehicle.save()
        return redirect('/')
    else:
        stations = dane_podstacji.objects.all()
        return render(request, 'loggedIn/admin/addVehicle.html', {'stations': stations})

def show_vehicle_list(request):
    vehicles = dane_pojazdu.objects.select_related('podstacja').all()
    return render(request, 'loggedIn/vehicleList.html', {'vehicles': vehicles})

def show_vehicle_details(request, pk):
    vehicle = dane_pojazdu.objects.get(id=pk)

    #Data for latest interventions history
    interventions = list(dane_wyjazdu.objects.prefetch_related(Prefetch('pojazd')).filter(pojazd__id=pk).order_by('-data_powrotu'))
    i = 0
    latest_interventions = []
    while i < 6:
        if len(interventions) > i:
            latest_interventions.append(interventions[i])
        else:
            latest_interventions.append(None)
        i = i + 1
    #END

    #Data for insurance
    insurance_history = list(historia_ubezpieczenia.objects.prefetch_related(Prefetch('pojazd')).filter(pojazd__id=pk).order_by('-data_wykupu'))
    if insurance_history:
        insurance = insurance_history[0]
        insurance_end_date = insurance.data_wykupu.replace(year=insurance.data_wykupu.year + 1)
        today = datetime.date.today()
        insurance_diff = (insurance_end_date.date() - today).days
    else:
        insurance_end_date = None
        insurance_diff = None
    #END

    #Data for inspection
    inspection_history = list(historia_przegladu.objects.prefetch_related(Prefetch('pojazd')).filter(pojazd__id = pk).order_by('-data_przegladu'))
    if inspection_history:
        inspection = inspection_history[0]
        inspection_end_date = inspection.data_przegladu.replace(year=inspection.data_przegladu.year + 1)
        inspection_diff = (inspection_end_date.date() - today).days
    else:
        inspection_end_date = None
        inspection_diff = None
    #END

    return render(request, 'loggedIn/vehicleDetails.html', {'data': vehicle,
                                                            'interventions': latest_interventions,
                                                            'latest_insurance': insurance_end_date,
                                                            'insurance_days_left': insurance_diff,
                                                            'latest_inspection': inspection_end_date,
                                                            'inspection_diff': inspection_diff,
                                                            })

def add_intervention(request, pk):
    if request.method == "POST":
        go_out = request.POST["go_out"]
        come_back = request.POST["come_back"]
        desc = request.POST["desc"]
        intervention = dane_wyjazdu(data_wyjazdu=go_out, data_powrotu=come_back, notatka=desc, pojazd_id=pk)
        intervention.save()
        return redirect('/interventionHistory/{0}'.format(pk))
    else:
        return render(request, 'loggedIn/addIntervention.html')

def show_intervention_history(request, pk):
    interventions = dane_wyjazdu.objects.prefetch_related(Prefetch('pojazd')).filter(pojazd__id = pk).order_by('-data_powrotu')
    return render(request, 'loggedIn/interventionHistory.html', {'data': interventions, 'car_id': pk })

def add_inspection(request, pk):
    if request.method == "POST":
        date = request.POST["date"]
        mileage = request.POST["mileage"]
        desc = request.POST["desc"]
        type = request.POST["type"]
        inspection = historia_przegladu(data_przegladu=date, przebieg=mileage, opis_usterek=desc, wynik=type, pojazd_id=pk)
        inspection.save()
        return redirect('/vehicleDetails/{0}'.format(pk))
    else:
        return render(request, 'loggedIn/addInspection.html')

def add_insurance(request, pk):
    if request.method == "POST":
        date = request.POST["date"]
        type = request.POST["type"]
        mileage = request.POST["mileage"]
        insurance = historia_ubezpieczenia(data_wykupu=date, rodzaj=type, przebieg=mileage, pojazd_id=pk)
        insurance.save()
        return redirect('/vehicleDetails/{0}'.format(pk))
    else:
        return render(request, 'loggedIn/addInsurance.html')

def add_repair(request, pk):
    if request.method == "POST":
        date = request.POST["date"]
        type = request.POST["type"]
        mileage = request.POST["mileage"]
        desc = request.POST["desc"]
        repair = historia_naprawy(data_naprawy=date, kategoria=type, przebieg=mileage, pojazd_id=pk, opis_usterek=desc)
        repair.save()
        return redirect('/vehicleDetails/{0}'.format(pk))
    else:
        return render(request, 'loggedIn/addIncident.html')

def view_insurance(request, pk):
    insurance_history = list(historia_ubezpieczenia.objects.prefetch_related(Prefetch('pojazd')).filter(pojazd__id=pk).order_by('-data_wykupu'))
    return render(request, 'loggedIn/insuranceHistory.html', { 'data': insurance_history, 'car_id': pk } )

def view_inspection(request, pk):
    inspection_history = list(historia_przegladu.objects.prefetch_related(Prefetch('pojazd')).filter(pojazd__id = pk).order_by('-data_przegladu'))
    return render(request, 'loggedIn/inspectionHistory.html', { 'data': inspection_history, 'car_id': pk})

@csrf_exempt
def view_repair(request, pk):
    repair_history = historia_naprawy.objects.prefetch_related(Prefetch('pojazd')).filter(pojazd__id=pk).order_by(
        '-data_naprawy')
    if request.method == "POST":
        if 'beforeForm' in request.POST and request.FILES['upload_before']:
            image = request.FILES['upload_before']
            fss = FileSystemStorage()
            file = fss.save(image.name, image)
            file_url = fss.url(file)
            repair_id = request.POST['repairId']
            imgBefore = zdjecie_naprawa_przed(naprawa_id=repair_id, url=file_url)
            imgBefore.save()
            messages.info(request, 'Zdjęcie przed naprawą dodane poprawnie')
            return redirect('/repairList/{0}'.format(pk))
        elif 'afterForm' in request.POST and request.FILES['upload_after']:
            upload_before = request.FILES["upload_after"]
            fss = FileSystemStorage()
            file = fss.save(upload_before.name, upload_before)
            file_url = fss.url(file)
            repair_id = request.POST['repairId']
            imgAfter = zdjecie_naprawa_po(naprawa_id=repair_id, url=file_url)
            imgAfter.save()
            messages.info(request, 'Zdjęcie po naprawie dodane poprawnie')
            return redirect('/repairList/{0}'.format(pk))
        elif 'acceptInvoice' in request.POST and request.FILES['upload_invoice']:
            invoice = request.FILES['upload_invoice']
            fss = FileSystemStorage()
            file = fss.save(invoice.name, invoice)
            file_url = fss.url(file)
            repair_id = request.POST['repairId']
            invoice_file = faktura(naprawa_id=repair_id, url=file_url)
            invoice_file.save()
            messages.info(request, 'Faktura dodana poprawnie')
            return redirect('/repairList/{0}'.format(pk))
    else:
        return render(request, 'loggedIn/repairHistory.html', { 'data': repair_history})

def show_images(request, pk):
    repair = historia_naprawy.objects.get(id=pk)
    if zdjecie_naprawa_przed.objects.filter(naprawa_id=pk).exists() or zdjecie_naprawa_po.objects.filter(naprawa_id=pk).exists():
        images_before = zdjecie_naprawa_przed.objects.all().filter(naprawa_id=pk)
        images_after = zdjecie_naprawa_po.objects.all().filter(naprawa_id=pk)
        return render(request, 'loggedIn/showImages.html', { 'imgBefore': images_before, 'imgAfter': images_after })
    else:
        messages.info(request, 'Do tej naprawy nie ma wgranych zdjęć')
        return redirect('/repairList/{0}'.format(repair.pojazd_id))

def show_invoices(request, pk):
    repair = historia_naprawy.objects.get(id=pk)
    if faktura.objects.all().filter(naprawa_id=pk).exists():
        invoices = faktura.objects.all().filter(naprawa_id=pk)
        return render(request, 'loggedIn/showInvoices.html', {'invoices': invoices})
    else:
        messages.info(request, 'Do tej naprawy nie ma przypisanych faktur')
        return redirect('/repairList/{0}'.format(repair.pojazd_id))