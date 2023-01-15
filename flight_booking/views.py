from django.shortcuts import render
from Airline.models import Airline
from Flight.models import Flight
import math


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


def start(request):
    
    for i in Flight.objects.all():
        print(i.Airline_id.Airline_Id)
        str1 = i.Routes
        str2 = i.Dist_bet_airports
        start_time = float(i.Arriving_time)
        depart_str = 'surat'
        arrive_str = 'kolkata'

        routes_path = str1.split(",")
        test_dist = str2.split(",")
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
            print("flight found")
            print(depart_str + " to " + arrive_str)
            print("total Duration is " + duration_time)
            print("depart time is " + depart_time)
            print("arrive time is " + arrive_time)
        else:
            print("flight not found")

    return render(request, 'index.html')
