from django.db import models

# class Flight(models.Model):
#     Flight_id = models.IntegerField(primary_key=True)
#     Airline_id = models.ForeignKey(Airline, on_delete=models.CASCADE) 
#     Routes = models.CharField(max_length=500)
#     Dist_bet_airports= models.CharField(max_length=500)
#     Depart_time = models.CharField(max_length=100)
#     Total_ticket = models.IntegerField(default=0)
    
#     def __str__(self):
#         return str(self.Flight_id)

class User(models.Model):
    User_name = models.CharField(max_length='20')
    Name = models.CharField(max_length='20')
    Email = models.CharField(max_length='20')
    Phone = models.IntegerField(default=0)
    
    def __str__(self):
        return str(self.User_name)