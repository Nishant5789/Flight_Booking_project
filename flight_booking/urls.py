from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings 
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Home),
    path('fetchflights/', views.fetchsearch),
    path('fetchflights/<slug:Temparal_ID>/', views.addpassengerdetails, name="addpassengerdetails"),
    path('bookticket/<slug:Temparal_ID>/', views.handle_confirmation, name="handle_confirmation"),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
