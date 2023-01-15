from django.db import models
# from django.db.models import Model

# Create your models here.
# flight_id, Airline_id, path_detail, Ticket_charge, Dist_bet_airports, Departing time, arriving time, total_ticket
from Airline.models import Airline

class Flight(models.Model):
    Flight_id = models.IntegerField(primary_key=True)
    Airline_id = models.ForeignKey(Airline, on_delete=models.CASCADE)
    Routes = models.CharField(max_length=500)
    Dist_bet_airports= models.CharField(max_length=500)
    Arriving_time = models.CharField(max_length=100)
    Total_ticket = models.IntegerField(default=0)
    