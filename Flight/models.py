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
    Depart_time = models.CharField(max_length=100)
    Total_ticket = models.IntegerField(default=0)
    
    def __str__(self):
        return str(self.Flight_id)
    
class Flight_component(models.Model):
    component_Id = models.IntegerField(default=0)
    Airline_logo = models.ImageField(upload_to ='media/')
    Airline_name = models.CharField(max_length=100)
    Flightname1 = models.CharField(max_length=100)
    Flightname2 = models.CharField(max_length=100)
    Timeduration = models.CharField(max_length=100)
    Price = models.IntegerField(default=0)
    Depart_time = models.CharField(max_length=100,default='SOME STRING')
    Arrive_time = models.CharField(max_length=100,default='SOME STRING')
    
    def __init__(self,No,Airline_logo,Airline_name,Flightname1,Flightname2,Timeduration,Price,Depart_time,Arrive_time):
        self.component_Id=No 
        self.Airline_logo=Airline_logo
        self.Airline_name=Airline_name
        self.Flightname1=Flightname1
        self.Flightname2=Flightname2
        self.Timeduration=Timeduration
        self.Price=Price
        self.Depart_time=Depart_time
        self.Arrive_time=Arrive_time
    
    def __str__(self):
        str = self.Flightname1 + "to "+ self.Flightname2
        return str
    
    
    
    
