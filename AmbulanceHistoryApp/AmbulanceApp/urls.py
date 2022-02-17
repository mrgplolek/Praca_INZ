from . import views
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('addStation', views.add_station, name='add_station'),
    path('addVehicle', views.add_vehicle, name='add_vehicle'),
    path('vehicleList', views.show_vehicle_list, name='vehicle_list'),
    path('vehicleDetails/<int:pk>', views.show_vehicle_details, name='vehicle_details'),
    path('interventionHistory/<int:pk>', views.show_intervention_history, name="intervention_history"),
    path('newIntervention/<int:pk>', views.add_intervention, name='add_intevention'),
    path('newInspection/<int:pk>', views.add_inspection, name='add_inspection'),
    path('newInsurance/<int:pk>', views.add_insurance, name='add_insurance'),
    path('newRepair/<int:pk>', views.add_repair, name='add_repair'),
    path('insuranceDetails/<int:pk>', views.view_insurance, name='insurance_list'),
    path('inspectionDetails/<int:pk>', views.view_inspection, name='inspection_list'),
    path('repairList/<int:pk>', views.view_repair, name='repair_list'),
    path('showImages/<int:pk>', views.show_images, name='show_images'),
    path('showInoices/<int:pk>', views.show_invoices, name='show_invoices'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)