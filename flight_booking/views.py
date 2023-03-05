from django.shortcuts import render
from Airline.models import Airline
from Flight.models import Flight
from Flight.models import Flight_component
from user.models import User_profile
from django.utils.functional import SimpleLazyObject
from django.contrib.auth import get_user
import math
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import Image, Table, TableStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from django.db import IntegrityError
import uuid  
from django.views.decorators.csrf import csrf_protect

def addpassengerdetails(request, Temparal_ID):
    print("adding details")     
    No_ticket = request.POST.get('Ticket')
    Flight_component_object = Flight_component.objects.get(pk=Temparal_ID)
    flight_id = Flight_component_object.Flight_Id
    Current_ticket = Flight.objects.get(pk=flight_id).Total_ticket
    update_ticket = Current_ticket-int(No_ticket)
    Flight.objects.filter(pk=flight_id).update(Total_ticket=update_ticket)
    
    print(Flight_component_object)
    number_list = []
    for i in range(1, int(No_ticket)+1):
        number_list.append(str(i))
    
    return render(request, 'passanger_register.html', {"number_list":number_list,"No_ticket": No_ticket,"flight_object":Flight_component_object})

def handle_confirmation(request, Temparal_ID, No_ticket):
    
    flight = Flight_component.objects.get(pk=Temparal_ID)
    
    file_name = str(Temparal_ID)[0:6]+".pdf"
    airline_name = flight.Airline_name
    airline_logo = flight.Airline_logo 
    
    departure = flight.Flightname1
    arrival = flight.Flightname2
    boarding_Time = flight.Depart_time
    # flight_date = ""
    # seat_no = ""
    list_passenger = []
    
    for i in range(1, int(No_ticket)+1):
        
        passenger_dict = {
            "passenger_name": request.POST.get("p_"+str(i)+"_name"),
            "passenger_dob": request.POST.get("p_"+str(i)+"_dob"),
            "passenger_gender": request.POST.get("p_"+str(i)+"_gender")
        }
        list_passenger.append(passenger_dict)
    
    pdf_generator(file_name, airline_name, list_passenger,
                  departure, arrival, boarding_Time)
    
    
    return render(request, "confirmation.html", {"pdfname": file_name})

def fetchsearch(request):
    depart_str   = request.POST.get('depart')
    arrive_str = request.POST.get('arrive')
    # print(depart_str + ' ' +arrive_str)
    # depart_str = 'mumbai'
    # arrive_str = 'banglore'
    fetch_flights = []
    No = 0;
    
    for i in Flight.objects.all():
        routes_dist_str = i.Dist_bet_airports
        routes_str = i.Routes
        Airline_logo = i.Airline_id.Airline_Photo
        Airline_name = i.Airline_id.Airline_name
        Flight_Id = i.Flight_id
        start_time = float(i.Depart_time)
        Total_ticket = i.Total_ticket
        
        print("flight_id",Flight_Id)
        
        routes_path = routes_str.split(",")
        # print("flight_id",routes_path)
        test_dist = routes_dist_str.split(",")
        routes_distance = [int(i) for i in test_dist]
        routes_time = find_time_between_place(routes_distance)
        dist = {}

        for i in range(len(routes_distance)+1):
            dist[routes_path[i]] = i
        
        # print(dist)

        depart_index = dist[depart_str]
        arrive_index = dist[arrive_str]

        if depart_index < arrive_index: 
            # cover_path1  include all place which would cover into flight path
            cover_path1 = [routes_time[i] for i in range(len(routes_distance)) if i < arrive_index and i >= depart_index]
            # cover_path2  include all place which are come before starting place
            cover_path2 = [routes_time[i] for i in range(len(routes_distance)) if i < depart_index]
            # result
            Price = int(sum(cover_path1)*5)
            depart_time = convert12(convert_timeduration(start_time + sum(cover_path2)))
            arrive_time = convert12(convert_timeduration(sum(cover_path1)+start_time+sum(cover_path2)))
            duration_time = convert12(convert_timeduration(sum(cover_path1)))
            temp_duration = duration_time.split(":")
            duration_time = str(temp_duration[0]) + \
                " Hour " + str(temp_duration[1]) + " minute"
            
            unique_id = str(uuid.uuid4())
            print(unique_id)
        
            Flight_component.objects.create(
                Temparal_ID=unique_id,
                Flight_Id=Flight_Id,
                Airline_logo=Airline_logo,
                Airline_name=Airline_name,
                Flightname1=depart_str,
                Flightname2=arrive_str,
                Timeduration=duration_time,
                Price=Price,
                Total_ticket=Total_ticket,
                Depart_time=depart_time,
                Arrive_time=arrive_time
            )
            fetch_flights.append(Flight_component.objects.get(pk=unique_id))
            print(Flight_component.objects.get(pk=unique_id).Total_ticket)
        else:
            print("flight not found")
        
    print(fetch_flights)
                      
    return render(request, 'fetchflights.html', {"Flights": fetch_flights})

def Home(request):
    user = get_user(request)
    
    if user.is_authenticated:
        print(user.username)
        profile = User_profile.objects.filter(Username = user).first().Profile
        return render(request, 'home.html', {'profile_pic': profile})
    
    return render(request, 'home.html')
    

def pdf_generator(file_name, airline_name, list_passenger ,departure, arrival, boarding_Time):
    # Create a new PDF document
    doc = SimpleDocTemplate(file_name)
    # Create a list to hold the elements to be included in the PDF document
    elements = []
    # Add the airline name and logo to the document
    elements.append(Paragraph(airline_name, getSampleStyleSheet()['Heading1']))
    # airline_logo = 'path/to/airline_logo.png'
    # elements.append(Paragraph(f'<img src="{airline_logo}" width="80" height="80"/>', getSampleStyleSheet()['Normal']))

    # Add the departure, arrival, and boarding time to the document
    elements.append(Paragraph(f'Departure: {departure}', getSampleStyleSheet()['Normal']))
    elements.append(Paragraph(f'Arrival: {arrival}', getSampleStyleSheet()['Normal']))
    elements.append(Paragraph(f'Boarding Time: {boarding_Time}', getSampleStyleSheet()['Normal']))

    # Create a list of lists to hold the data for the table
    data = [['Passenger Name', 'Date of Birth', 'Gender']]
    for passenger in list_passenger:
        data.append([passenger['passenger_name'], passenger['passenger_dob'], passenger['passenger_gender']])

    # Create the table and set its style
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
    ]))

    # Add the table to the document
    elements.append(table)

    # Build the PDF document and save it to disk
    doc.build(elements)
   

    
    

        


    
    
    
    
    



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

