from django.shortcuts import render
from Airline.models import Airline
from Flight.models import Flight
from Flight.models import Flight_component
import math
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import Image, Table, TableStyle
from django.db import IntegrityError
import uuid  
from django.views.decorators.csrf import csrf_protect

def addpassengerdetails(request, Temparal_ID):

    print("adding details")     
    No_ticket = request.POST.get('Ticket')
    flight_id = Flight_component.objects.get(pk=Temparal_ID).Flight_Id
    # print(flight_id)
    Current_ticket = Flight.objects.get(pk=flight_id).Total_ticket
    # print(Current_ticket)
    update_ticket = Current_ticket-int(No_ticket)
    Flight.objects.filter(pk=flight_id).update(Total_ticket=update_ticket)
    
    return render(request, 'passanger_register.html', {"Temparal_ID":Temparal_ID})

def handle_confirmation(request, Temparal_ID):
    
    flight = Flight_component.objects.get(pk=Temparal_ID)
    file_name = str(flight.Flight_Id)+".pdf"
    airline_name = flight.Airline_name
    airline_logo = flight.Airline_logo 
    passenger_name1 = request.POST.get('passenger1')
    passenger_name2 = request.POST.get('passenger2')
    departure = flight.Flightname1
    arrival = flight.Flightname2
    boarding_Time = flight.Depart_time
    # flight_date = ""
    # flight_id = ""
    # seat_no = ""
    
    pdf_generator(file_name, airline_name, airline_logo, passenger_name1, passenger_name2,
                  departure, arrival, boarding_Time)
    
    
    return render(request, "confirmation.html")
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
            No+=1;
        else:
            print("flight not found")
        
    print(fetch_flights)
                      
    return render(request, 'fetchflights.html', {"Flights": fetch_flights})

def Home(request):
    return render(request, 'home.html')

def pdf_generator(file_name, airline_name, airline_logo, passenger_name1, passenger_name2 ,departure, arrival, boarding_Time):
    flight_date = "12-3-2-2023"
    flight_id = "b-10234"
    seat_no = "ce008"
    passenger_name = 'nishant'
    
    pdf_file = canvas.Canvas(file_name, pagesize=letter)

    # # Add the airline logo
    img = Image(airline_logo)
    img.drawHeight = 1.5*inch*img.drawHeight / img.drawWidth
    img.drawWidth = 1.5*inch
    img.drawOn(pdf_file, 100, 610)

    # Add the airline name
    pdf_file.setFont("Helvetica-Bold", 16)
    pdf_file.drawString(100, 585, airline_name)

    # Create a table for the passenger information
    data = [['Passenger Name:', passenger_name],
            ['Departure:', departure],
            ['Arrival:', arrival],
            ['boarding_Time:', boarding_Time],
            ['Flight Date:', flight_date],
            ['Flight ID:', flight_id],
            ['Seat No:', seat_no],
        ]
    table = Table(data, colWidths=[100, 200])

    # Set the table style
    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                       ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                       ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                       ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                       ('BACKGROUND', (0, -1), (-1, -1), colors.beige),
                       ('GRID', (0, 0), (-1, -1), 1, colors.black)])
    table.setStyle(style)

    # Draw the table on the PDF
    table.wrapOn(pdf_file, 200, 600)
    table.drawOn(pdf_file, 20, 450)

    # Save the PDF
    pdf_file.save()



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

