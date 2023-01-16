from django.shortcuts import render
from Airline.models import Airline
from Flight.models import Flight, Flight_component
import math
# from flight_booking import core_funtion

def fetchsearch(request):
    depart_str = 'mumbai'
    arrive_str = 'banglore'
    fetch_flights = []
    No = 0;
    
    for i in Flight.objects.all():
        
        routes_dist_str = i.Dist_bet_airports
        routes_str = i.Routes
        Airline_logo = i.Airline_id.Airline_Photo
        Airline_name = i.Airline_id.Airline_name
        start_time = float(i.Depart_time)
        Price = 100
        
        routes_path = routes_str.split(",")
        test_dist = routes_dist_str.split(",")
        routes_distance = [int(i) for i in test_dist]
        routes_time = find_time_between_place(routes_distance)
        dist = {}

        for i in range(len(routes_distance)+1):
            dist[routes_path[i]] = i

        depart_index = dist[depart_str]
        arrive_index = dist[arrive_str]

        if depart_index < arrive_index:
            # cover_path1  include all place which would cover into flight path
            cover_path1 = [routes_time[i] for i in range(
                len(routes_distance)) if i < arrive_index and i >= depart_index]
            # cover_path2  include all place which are come before starting place
            cover_path2 = [routes_time[i]
                           for i in range(len(routes_distance)) if i < depart_index]
            # result
            depart_time = convert12(convert_timeduration(start_time + sum(cover_path2)))
            arrive_time = convert12(convert_timeduration(sum(cover_path1)+start_time+sum(cover_path2)))
            duration_time = convert12(convert_timeduration(sum(cover_path1)))
            temp_duration = duration_time.split(":")
            duration_time = str(temp_duration[0]) + \
                " Hour " + str(temp_duration[1]) + " minute"
            fetch_flights.append(Flight_component(No,Airline_logo, Airline_name,depart_str,arrive_str,duration_time,Price, depart_time,arrive_time))
            No+=1;
            
            # print("flight found")
            # print(depart_str + " to " + arrive_str)
            # print("total Duration is " + duration_time)
            # print("depart time is " + depart_time)
            # print("arrive time is " + arrive_time)
        else:
            print("flight not found")
                      
    return render(request, 'fetchflights.html', {"Flights": fetch_flights})

def Home(request):
    
    if request.method == 'POST':
        depart_str   = request.POST.get('depart')
        arrive_str = request.POST.get('arrive')
        Arriving_time = request.POST.get('depart_date')
        Total_ticket = request.POST.get('passenger_number')
        
        
        # User.objects.create_user(depart_str,email,password)
    
    return render(request, 'home.html')
def find_time_between_place(dist):
    result = []
    for i in range(len(dist)):
        result.append(abs(dist[i])/115)
    return result


def convert_timeduration(time):
    floor_hour = math.floor(time)
    hour = f'{floor_hour:02d}'
    min = f'{int(abs(time - floor_hour)*60):02d}'
    result = str(hour)+":"+str(min)+":00"
    return result


def convert12(str):
    ans = ""
    h1 = ord(str[0]) - ord('0')
    h2 = ord(str[1]) - ord('0')
    hh = h1 * 10 + h2
    Meridien = ""
    if (hh < 12):
        Meridien = "AM"
    else:
        Meridien = "PM"
    hh %= 12
    if (hh == 0):
        ans = ans + "12"
        for i in range(2, 8):
            ans = ans + str[i]
    else:
        ans = ans + "{}".format(hh)
        for i in range(2, 8):
            ans = ans + str[i]
    return ans + " " + Meridien

