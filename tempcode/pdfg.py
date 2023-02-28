# from reportlab.pdfgen import canvas
# from reportlab.lib.units import inch
# pdf=canvas.Canvas("air_ticket.pdf",bottomup=0)
# pdf.setTitle("air_tickets")
# pdf.drawString(10,10,"test.pdf")
# pdf.showPage()
# pdf.save()
# # pdf.translate(inch,inch)
# # pdf.rect(5,5,width=10,height=30,stroke=1,fill=0)


def convert_time_to_string(time):
    hour = int(time.split(':')[0])
    minutes = int(time.split(':')[1])
    print(minutes/60)
    result = str(round(float(hour+(minutes/60)),2))

    print(result)
convert_time_to_string("11:50:00")