from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from AdminApp.models import *
from WebApp.models import *
from django.contrib import messages
from twilio.rest import Client
import razorpay
from django.conf import settings
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
import qrcode
from io import BytesIO
import base64
import os
from dotenv import load_dotenv
from django.http import FileResponse

load_dotenv()



# Create your views here.


def home(request):

    if 'st_login' not in request.session:
        return redirect('st_login')

    student = StudentDb.objects.get(id=request.session['st_login'])

    if request.method == "POST":
        msg = request.POST.get("message")

        if msg:
            ChatMessage.objects.create(
                student_name=student.Name,
                message=msg
            )

        # redirect prevents duplicate submission
        return redirect('home')

    chats = ChatMessage.objects.filter(
        student_name=student.Name
    ).order_by("created_at")
    
    notices = NoticeDb.objects.all().order_by('-Created_At')[:3]

    return render(request,'Home.html',{
        'student':student,
        'chats':chats,
        'notices':notices
    })

def profile(request): 
    data=StudentDb.objects.get(id=request.session['st_login']) 
    if 'st_login' not in request.session:
        return redirect('st_login')
    student = StudentDb.objects.get(id=request.session['st_login'])
    return render(request,'Profile.html',{'data':data,
                                          'student':student})
def st_login(request):
    return render(request,'StudentLogin.html')





load_dotenv()

ACCOUNT_SID = os.getenv("ACCOUNT_SID")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")
VERIFY_SID = os.getenv("VERIFY_SID")

client = Client(ACCOUNT_SID, AUTH_TOKEN)
def student_login(request):

    if request.method == "POST":

        roll = request.POST.get("roll")
        dob = request.POST.get("dob")

        student = StudentDb.objects.filter(Roll_Number=roll, Dob=dob).first()

        if student:

            phone = student.Phone_number

            verification = client.verify.services(VERIFY_SID).verifications.create(
                to="+91" + phone,
                channel="sms"
            )

            request.session['phone'] = phone
            request.session['student_id'] = student.id

            return redirect("verify_otp")

        else:
            return render(request,"st_login",{"error":"Invalid Details"})

    return render(request,"st_login")

def verify_otp(request):

    if request.method == "POST":

        otp = request.POST.get("otp")
        phone = request.session.get("phone")
        student_id = request.session.get("student_id")

        verification_check = client.verify.services(VERIFY_SID).verification_checks.create(
            to='+91' + phone,
            code=otp
        )

        if verification_check.status == "approved":

            request.session['st_login'] = student_id

            return redirect("home")

        else:

            return render(request,"verify_otp.html",{"error":"Invalid OTP"})

    return render(request,"verify_otp.html")

    if request.method == "POST":

        otp = request.POST.get("otp")
        phone = request.session.get("phone")

        verification_check = client.verify.services(VERIFY_SID).verification_checks.create(
            to='+91' + phone,
            code=otp
        )

        if verification_check.status == "approved":

            request.session['st_login'] = request.session.get('student_id')

            return redirect("home")

        else:

            return render(request,"verify_otp.html",{"error":"Invalid OTP"})

    return render(request,"verify_otp.html")
def student_logout(request):
    request.session.flush()
    return redirect('st_login')

def edit_profile(request):
    student_id = request.session.get('student_id')

    data = StudentDb.objects.get(id=student_id)

    if request.method == "POST":
        data.Name = request.POST.get('name')
        data.Email = request.POST.get('email')
        data.Phone = request.POST.get('phone')

        # Update photo if uploaded
        if 'photo' in request.FILES:
            data.Student_Photo = request.FILES['photo']

        # Save after updating everything
        data.save()

        return redirect('profile')

    return render(request,'Edit_Profile.html',{'data':data})

#-------------------------------------------------------------





def view_result(request):
    if 'st_login' not in request.session:
        return redirect('st_login')
    student = StudentDb.objects.get(id=request.session['st_login'])
    if 'student_id' not in request.session:
        return redirect('student_login')

    student_id = request.session['student_id']

    # Student details
    data = StudentDb.objects.get(id=student_id)

    # All results
    results = ResultDb.objects.filter(Student_id=student_id)

    # Arrear subjects
    arrear_subjects = results.filter(Status="Arrear")

    # Check if student already applied for arrear exam
    applied = ArrearApplication.objects.filter(Student_id=student_id).exists()

    total_credit = 0
    total_points = 0

    pass_count = 0
    fail_count = 0

    for r in results:

        marks = r.Marks or 0
        credit = r.Subject.Credit or 0

        if marks < 40:
            status = "Arrear"
            grade = "F"
            gp = 0
            fail_count += 1
        else:
            status = "Pass"
            pass_count += 1

            if marks >= 90:
                grade = "A+"
                gp = 10
            elif marks >= 80:
                grade = "A"
                gp = 9
            elif marks >= 70:
                grade = "B+"
                gp = 8
            elif marks >= 60:
                grade = "B"
                gp = 7
            elif marks >= 50:
                grade = "C"
                gp = 6
            else:
                grade = "D"
                gp = 5

        r.Status = status
        r.Grade = grade
        r.save()

        total_credit += credit
        total_points += credit * gp

    # SGPA calculation
    sgpa = 0
    if total_credit > 0:
        sgpa = total_points / total_credit

    context = {
        "results": results,
        "sgpa": round(sgpa, 2),
        "data": data,
        "pass_count": pass_count,
        "fail_count": fail_count,
        "arrear_subjects": arrear_subjects,
        "applied": applied,
        "student":student,
    }

    return render(request, "View_Result.html", context)
def apply_arrear(request):

    student_id = request.session['student_id']
    arrears = ResultDb.objects.filter(Student_id=student_id, Status="Arrear")

    if request.method == "POST":

        subjects = request.POST.getlist("subjects")

        # store selected subjects in session
        request.session['arrear_subjects'] = subjects

        amount = len(subjects) * 200

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        payment = client.order.create({
            "amount": amount * 100,
            "currency": "INR",
            "payment_capture": "1"
        })

        return render(request,"Apply_Arrear.html",{
            "payment": payment,
            "amount": amount
        })

    return render(request,"Apply_Arrear.html",{"arrears": arrears})
def save_arrear_payment(request):

    student_id = request.session['student_id']
    subjects = request.session.get("arrear_subjects", [])

    student = StudentDb.objects.get(id=student_id)

    for sub in subjects:

        subject = SubjectDb.objects.get(id=sub)

        ArrearApplication.objects.create(
            Student=student,
            Subject=subject,
            Amount=200,
            Payment_Status="Paid"
        )

    return redirect('home')
def payment_list(request):

    payments = ArrearApplication.objects.select_related('Student','Subject').all()

    return render(request, "manage/payment.html", {
        "payments": payments
    })
def download_marksheet(request):

    student_id = request.session['student_id']

    student = StudentDb.objects.get(id=student_id)
    results = ResultDb.objects.filter(Student_id=student_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="marksheet.pdf"'

    doc = SimpleDocTemplate(response, pagesize=A4)

    elements = []

    styles = getSampleStyleSheet()

    # Centered title styles
    title_style = ParagraphStyle(
        'title',
        parent=styles['Title'],
        alignment=TA_CENTER
    )

    subtitle_style = ParagraphStyle(
        'subtitle',
        parent=styles['Heading2'],
        alignment=TA_CENTER
    )

    # Titles
    elements.append(Paragraph("STUDENT RESULT MANAGEMENT", title_style))
    elements.append(Paragraph("Semester Marksheet", subtitle_style))
    elements.append(Spacer(1,30))

    # Student Details
    elements.append(Paragraph(f"<b>Name :</b> {student.Name}", styles['Normal']))
    elements.append(Paragraph(f"<b>Register No :</b> {student.Roll_Number}", styles['Normal']))
    elements.append(Paragraph(f"<b>Class :</b> {student.Class.Class_Name}", styles['Normal']))
    elements.append(Spacer(1,20))

    # Table Header
    data = [["Subject","Marks","Grade"]]

    total_marks = 0
    fail = False

    for r in results:

        data.append([
            r.Subject.Subject_Name,
            r.Marks,
            r.Grade
        ])

        total_marks += r.Marks

        if r.Marks < 40:
            fail = True

    # Table
    table = Table(data, colWidths=[250,100,100])

    table.setStyle(TableStyle([
        ('GRID',(0,0),(-1,-1),1,colors.black),
        ('BACKGROUND',(0,0),(-1,0),colors.lightgrey),
        ('ALIGN',(1,1),(-1,-1),'CENTER')
    ]))

    elements.append(table)

    elements.append(Spacer(1,20))

    # SGPA Calculation
    sgpa = round(total_marks/(len(results)*10),2)

    elements.append(Paragraph(f"<b>SGPA : {sgpa}</b>", styles['Heading3']))

    # PASS / FAIL
    result_status = "FAIL" if fail else "PASS"

    elements.append(Paragraph(f"<b>Result : {result_status}</b>", styles['Heading3']))

    elements.append(Spacer(1,40))

    # Signature Area
    elements.append(Paragraph("Controller of Examination", styles['Normal']))

    doc.build(elements)

    return response



    data = StudentDb.objects.get(id=request.session['st_login'])

    qr_data = f"Student: {data.Name}, Roll: {data.Roll_Number}"

    qr = qrcode.make(qr_data)

    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    qr_image = base64.b64encode(buffer.getvalue()).decode()

    return render(request,'student_id_card.html',{
        'data':data,
        'qr_image':qr_image
    })


    student_id = request.session['student_id']

    student = StudentDb.objects.get(id=student_id)
    results = ResultDb.objects.filter(Student_id=student_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="marksheet.pdf"'

    doc = SimpleDocTemplate(response, pagesize=A4)

    elements = []

    styles = getSampleStyleSheet()


    elements.append(Paragraph("STUDENT RESULT MANAGEMENT", styles['Title']))
    elements.append(Paragraph("Semester Marksheet", styles['Heading2']))
    elements.append(Spacer(1,20))


    elements.append(Paragraph(f"Name : {student.Name}", styles['Normal']))
    elements.append(Paragraph(f"Register No : {student.Roll_Number}", styles['Normal']))
    elements.append(Spacer(1,20))

 
    data = [["Subject","Marks","Grade"]]

    total_marks = 0

    for r in results:

        data.append([
            r.Subject.Subject_Name,
            r.Marks,
            r.Grade
        ])

        total_marks += r.Marks

    table = Table(data, colWidths=[250,100,100])

    table.setStyle(TableStyle([
        ('GRID',(0,0),(-1,-1),1,colors.black),
        ('BACKGROUND',(0,0),(-1,0),colors.lightgrey),
        ('ALIGN',(1,1),(-1,-1),'CENTER')
    ]))

    elements.append(table)

    elements.append(Spacer(1,20))

    sgpa = round(total_marks/(len(results)*10),2)

    elements.append(Paragraph(f"SGPA : {sgpa}", styles['Heading3']))

    doc.build(elements)

    return response
def notes(request):
    notes = NotesDb.objects.all().order_by('-id')
    if 'st_login' not in request.session:
        return redirect('st_login')
    student = StudentDb.objects.get(id=request.session['st_login'])
    return render(request, "Notes.html", {"notes": notes,
                                          "student":student})
def download_note(request, id):
    note = NotesDb.objects.get(id=id)
    return FileResponse(note.Notes.open(), as_attachment=True)
def contact(request):
    return render(request,'Contact.html')









   