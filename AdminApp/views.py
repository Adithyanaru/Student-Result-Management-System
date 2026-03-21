from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from AdminApp.models import *
from django.contrib import messages
from collections import defaultdict
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Avg





# Create your views here.
# def dashboard(request):
    # total_student=StudentDb.objects.count()
    # context={'total_student':total_student,
    #          'total_class':ClassDb.objects.count(),
    #          'total_subject':SubjectDb.objects.count(),
    #          'total_result':ResultDb.objects.values('Class_id').distinct().count(),}
    # return render(request,'Dashboard.html',context)
def dashboard(request):

    total_student = StudentDb.objects.count()

    class_performance = (
        ResultDb.objects
        .values('Class__Class_Name','Class__Section')
        .annotate(avg_marks=Avg('Marks'))
    )

    class_labels = []
    class_marks = []

    for c in class_performance:
        label = f"{c['Class__Class_Name']} - {c['Class__Section']}"
        class_labels.append(label)
        class_marks.append(round(c['avg_marks'],2))


    context = {
        'total_student': total_student,
        'total_class': ClassDb.objects.count(),
        'total_subject': SubjectDb.objects.count(),
        'total_result': ResultDb.objects.count(),
        'class_labels': class_labels,
        'class_marks': class_marks
    }

    return render(request,'Dashboard.html',context)
def login(request):
    return render(request,'Login.html')

def add_student(request):
    classes=ClassDb.objects.all()
    return render(request,'Add_Student.html',{'classes':classes})
def manage_subject(request):
    data=SubjectDb.objects.all()
    return render(request,'Manage_Subject.html',{'data':data})
def admin_logout(request):
    return render(request,'Login.html')

def admin_login(request):
    uname=request.POST.get('username')
    pswd=request.POST.get('password')
    if User.objects.filter(username__contains=uname).exists():
        user=authenticate(username=uname,password=pswd)
        if user is not None:
            # login(request,user)
            request.session['username']=uname
            request.session['password']=pswd
            return redirect(dashboard)
        else:
            return redirect(login)
    else:
        return redirect(login)
def admin_logout(request):
    del request.session['username']
    del request.session['password'] 
    return redirect(login)


def manage_student(request):
    student=StudentDb.objects.all()
    return render(request,'Manage_Student.html',{'student':student})
def add_class(request):
    return render(request,'Add_Class.html')
# def manage_class(request):
#     return render(request,'Manage_Class.html') 
def add_subject(request):
    return render(request,'Add_Subject.html')

def save_class(request):
    if request.method=='POST':
        Class_Name=request.POST.get('class_name')
        Section=request.POST.get('section')
        obj= ClassDb(Class_Name=Class_Name,Section=Section)
        obj.save()
        messages.success(request,"Class Added Successfully")
        return redirect(add_class)        
def manage_class(request):
    data=ClassDb.objects.all()
    return render(request,'Manage_Class.html',{'data':data})
def delete_class(request,c_id):
    c=ClassDb.objects.get(id=c_id)
    c.delete()
    messages.success(request,"Class Deleted Successfully")
    return redirect(manage_class)
def edit_class(request,cl_id):
    data=ClassDb.objects.get(id=cl_id)
    return render(request,'Edit_Class.html',{'data':data})
def update_class(request,cl_id):
    if request.method=='POST':
        
        Class_Name=request.POST.get('class_name')
        Section=request.POST.get('section')
        c=ClassDb.objects.get(id=cl_id)  
        c.Class_Name=Class_Name
        c.Section=Section   
        c.save()
        messages.success(request,"Class Updated Successfully")
        return redirect(manage_class)   
def save_subject(request):
    if request.method=='POST':
        Subject_Name=request.POST.get('subject_name')
        Subject_Code=request.POST.get('subject_code')
        Subject_Credit=request.POST.get('subject_credit')
        obj= SubjectDb(Subject_Name=Subject_Name,Subject_Code=Subject_Code,Credit=Subject_Credit)
        obj.save()
        messages.success(request,"Subject Added Successfully")
        return redirect(add_subject)  
def delete_subject(request,sub_id):
    s=SubjectDb.objects.get(id=sub_id)
    s.delete()
    messages.success(request,"Subject Deleted Successfully")
    return redirect(manage_subject)
def edit_subject(request,s_id):
    data=SubjectDb.objects.get(id=s_id)
    return render(request,'Edit_Subject.html',{'data':data})
def update_subject(request,s_id):
    if request.method=='POST':
        
        Subject_Name=request.POST.get('subject_name')
        Subject_Code=request.POST.get('subject_code')
        Subject_Credit=request.POST.get('subject_credit')
        s=SubjectDb.objects.get(id=s_id)  
        s.Subject_Name=Subject_Name
        s.Subject_Code=Subject_Code 
        s.Credit=Subject_Credit  
        s.save()
        messages.success(request,"Subject Updated Successfully")
        return redirect(manage_subject)


def save_student(request):
    if request.method == 'POST':
        Name = request.POST.get('name')
        Email = request.POST.get('email')
        Dob = request.POST.get('dob')
        Class_id = request.POST.get('class')
        Roll_number = request.POST.get('roll_number')
        Gender = request.POST.get('gender')
        Phone_number = request.POST.get('phone_number')

        Photo = request.FILES.get('photo')

        obj = StudentDb(
            Name=Name,
            Email=Email,
            Dob=Dob,
            Class_id=Class_id,
            Roll_Number=Roll_number,
            gender=Gender,
            Phone_number=Phone_number,
            Student_Photo=Photo
        )

        obj.save()

        # 🔹 Send Email Notification
        subject = "Student Registration Successful"
        message = f"""
Hello {Name},

You have been successfully registered in the Student Portal.

Roll Number: {Roll_number}

You can now login and access your profile and results.

Thank You
Student Result Management System
"""

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [Email],
            fail_silently=False
        )

        messages.success(request, "Student Added Successfully")
        return redirect(add_student)
    if request.method == 'POST':
        Name = request.POST.get('name')
        Email = request.POST.get('email')
        Dob = request.POST.get('dob')
        Class_id = request.POST.get('class')
        Roll_number = request.POST.get('roll_number')
        Gender = request.POST.get('gender')
        Phone_number = request.POST.get('phone_number')

        Photo = request.FILES.get('photo')   

        obj = StudentDb(
            Name=Name,
            Email=Email,
            Dob=Dob,
            Class_id=Class_id,
            Roll_Number=Roll_number,
            gender=Gender,
            Phone_number=Phone_number,
            Student_Photo=Photo  
        )

        obj.save()
        messages.success(request, "Student Added Successfully")
        return redirect(add_student)    
def delete_student(request,s_id):
    s=StudentDb.objects.get(id=s_id)
    s.delete()
    messages.success(request,"Student Deleted Successfully")
    return redirect(manage_student)
def edit_student(request, st_id):
    studata = StudentDb.objects.get(id=st_id)
    classes = ClassDb.objects.all()
    return render(request,'Edit_Student.html',{'studata':studata,'classes':classes})


def update_student(request, st_id):
    if request.method == 'POST':

        Name = request.POST.get('name')
        Email = request.POST.get('email')
        Dob = request.POST.get('dob')
        Roll_number = request.POST.get('roll_number')
        Class_id = request.POST.get('class')
        Gender = request.POST.get('gender')
        Phone_number = request.POST.get('phone_number')
        Photo = request.FILES.get('photo')

        s = StudentDb.objects.get(id=st_id)

        s.Name = Name
        s.Email = Email
        s.Dob = Dob
        s.Roll_Number = Roll_number
        s.Class_id = Class_id
        s.gender = Gender
        s.Phone_number = Phone_number


        if Photo:
            s.Student_Photo = Photo

        s.save()

        messages.success(request, "Student Updated Successfully")

        return redirect('manage_student')
def add_subject_combination(request):
    classes=ClassDb.objects.all()
    subjects=SubjectDb.objects.all()
    return render(request,'Add_Subject_Combination.html',{'classes':classes,'subjects':subjects})
def save_subject_combination(request):
    if request.method=='POST':
        Class_id = request.POST.get('class')
        Subject_id = request.POST.get('subject')

        obj = SubjectCombinationDb(
            Class_Section_id=Class_id,      # foreign key id save
            Subject_Name_id=Subject_id
        )
        obj.save()

        messages.success(request,"Subject Combination Added Successfully")
        return redirect(add_subject_combination)
def manage_subject_combination(request):
    data=SubjectCombinationDb.objects.all() 
    return render(request,'Manage_Subject_Combination.html',{'data':data}) 
def delete_subject_combination(request,sc_id):
    s=SubjectCombinationDb.objects.get(id=sc_id)
    s.delete()
    messages.success(request,"Subject Combination Deleted Successfully")
    return redirect(manage_subject_combination)
def add_notice(request):
    return render(request,'Add_Notice.html')
def save_notice(request):
    if request.method=='POST':
        Notice_Title=request.POST.get('notice_title')
        Notice_details=request.POST.get('notice_details')
        obj= NoticeDb(Notice_Title=Notice_Title,Notice_Details=Notice_details)
        obj.save()
        messages.success(request,"Notice Added Successfully")
        return redirect(add_notice)
def manage_notice(request):
    data=NoticeDb.objects.all()
    return render(request,'Manage_Notice.html',{'data':data})

def add_result(request):
    classes=ClassDb.objects.all()
    return render(request,'Add_Result.html',{'classes':classes})

# from django.http import JsonResponse
# def get_students_subjects(request):
#     class_id = request.GET.get('class_id')
#     if class_id:
#         students = list(StudentDb.objects.filter(Class_id=class_id).values('id', 'Name', 'Roll_Number'))
#         subject_combinations = list(SubjectCombinationDb.objects.filter(Class_Section_id=class_id).select_related('Subject_Name').values( 'Subject_Name'))
#         subject=[{'id':sc.Subject_Name.id,'name':sc.Subject_Name.Subject_Name} for sc in subject_combinations]
#         return JsonResponse({'students': students, 'subjects': subject})

#     return JsonResponse({'students': [], 'subjects': []})


from django.http import JsonResponse

def get_students_subjects(request):
    class_id = request.GET.get('class_id')

    if class_id:
        # students
        students = StudentDb.objects.filter(Class=class_id)
        student_list = []
        for s in students:
            student_list.append({
                'id': s.id,
                'Name': s.Name
            })

        # subjects for that class
        subjects = SubjectCombinationDb.objects.filter(Class_Section_id=class_id).select_related('Subject_Name')

        subject_list = []
        for sub in subjects:
            subject_list.append({
                'id': sub.Subject_Name.id,
                'name': sub.Subject_Name.Subject_Name
            })

        return JsonResponse({
            'students': student_list,
            'subjects': subject_list
        })

    return JsonResponse({'students': [], 'subjects': []})



# def save_result(request):
#     if request.method == "POST":
#         class_id = request.POST.get('class')
#         student_id = request.POST.get('student')

#         # get all marks
#         for key, value in request.POST.items():
#             if key.startswith("marks_"):
#                 subject_id = key.split("_")[1]
#                 mark = value

#                 if mark != "":
#                     ResultDb.objects.create(
#                         Class_id=class_id,
#                         Student_id=student_id,
#                         Subject_id=subject_id,
#                         Marks=mark
#                     )

#         return redirect('add_result')  # back to page





def manage_result(request):

    class_id = request.GET.get('class')
    classes = ClassDb.objects.all()

    grouped = []
    subjects = []
    subject_list = []

    if class_id:

        subjects = SubjectCombinationDb.objects.filter(
            Class_Section_id=class_id
        ).select_related('Subject_Name')

        subject_list = [s.Subject_Name for s in subjects]

        results = ResultDb.objects.select_related(
            'Class', 'Student', 'Subject'
        ).filter(Class_id=class_id)

        temp = defaultdict(lambda: {
            'class': None,
            'student': None,
            'marks': {},
            'total': 0,
            'status': 'PASS'
        })

        for r in results:

            temp[r.Student.id]['class'] = r.Class
            temp[r.Student.id]['student'] = r.Student
            temp[r.Student.id]['marks'][r.Subject.id] = r.Marks
            temp[r.Student.id]['total'] += r.Marks

            if r.Marks < 40:
                temp[r.Student.id]['status'] = 'FAIL'

        grouped = list(temp.values())

        # 📧 Send email
        for g in grouped:

            student = g['student']

            if not student.Email:
                continue   # skip if email empty

            total = g['total']
            status = g['status']

            subject_marks = ""

            for sub_id, mark in g['marks'].items():
                subject = SubjectDb.objects.get(id=sub_id)
                subject_marks += f"{subject.Subject_Name} : {mark}\n"

            message = f"""
    Hello {student.Name},

    Your exam results have been declared.

    {subject_marks}

    Total Marks: {total}
    Status: {status}

    Login to the student portal to view full details.

    Student Result Management System
    """

            print("Sending email to:", student.Email)  # debug

            send_mail(
                "Exam Result Declared",
                message,
                settings.EMAIL_HOST_USER,
                [student.Email],
                fail_silently=False
            )

    context = {
        'grouped_results': grouped,
        'subjects': subject_list,
        'classes': classes,
        'selected_class': class_id
    }

    return render(request, 'Manage_Result.html', context)
    class_id = request.GET.get('class')
    classes = ClassDb.objects.all()

    grouped = []
    subjects = []
    subject_list = []

    if class_id:

        subjects = SubjectCombinationDb.objects.filter(
            Class_Section_id=class_id
        ).select_related('Subject_Name')

        subject_list = [s.Subject_Name for s in subjects]

        results = ResultDb.objects.select_related(
            'Class', 'Student', 'Subject'
        ).filter(Class_id=class_id)

        temp = defaultdict(lambda: {
            'class': None,
            'student': None,
            'marks': {},
            'total': 0,
            'status': 'PASS'
        })

        for r in results:
            temp[r.Student.id]['class'] = r.Class
            temp[r.Student.id]['student'] = r.Student
            temp[r.Student.id]['marks'][r.Subject.id] = r.Marks
            temp[r.Student.id]['total'] += r.Marks

            if r.Marks < 40:
                temp[r.Student.id]['status'] = 'FAIL'

        grouped = temp.values()

        # 📧 Send Email to Each Student
        for g in grouped:

            student = g['student']
            total = g['total']
            status = g['status']

            subject_marks = ""
            for sub_id, mark in g['marks'].items():
                subject = SubjectDb.objects.get(id=sub_id)
                subject_marks += f"{subject.Subject_Name} : {mark}\n"

            message = f"""
    Hello {student.Name},

    Your exam results have been declared.

    {subject_marks} 

    Total Marks: {total}
    Status: {status}

    Login to the student portal to view full details.

    Student Result Management System
    """

            send_mail(
                "Exam Result Declared",
                message,
                settings.EMAIL_HOST_USER,
                [student.Email],
                fail_silently=False
            )

    context = {
        'grouped_results': grouped,
        'subjects': subject_list,
        'classes': classes,
        'selected_class': class_id
    }

    return render(request, 'Manage_Result.html', context)



def save_result(request):

    if request.method == "POST":

        class_id = request.POST.get('class')
        student_id = request.POST.get('student')

        student = StudentDb.objects.get(id=student_id)

        # DELETE OLD RESULTS
        ResultDb.objects.filter(Class_id=class_id, Student_id=student_id).delete()

        total = 0
        status = "PASS"
        subject_marks = ""

        # SAVE NEW RESULTS
        for key, value in request.POST.items():

            if key.startswith("mark_") and value != "":

                subject_id = key.split("_")[1]
                marks = int(value)

                ResultDb.objects.create(
                    Class_id=class_id,
                    Student_id=student_id,
                    Subject_id=subject_id,
                    Marks=marks
                )

                subject = SubjectDb.objects.get(id=subject_id)

                subject_marks += f"{subject.Subject_Name} : {marks}\n"

                total += marks

                if marks < 40:
                    status = "FAIL"

        # 📧 SEND EMAIL
        message = f"""
Hello {student.Name},

Your exam result has been published.

{subject_marks}

Total Marks: {total}
Status: {status}

Login to the student portal to view full details.

Student Result Management System
"""

        send_mail(
            "Exam Result Declared",
            message,
            settings.EMAIL_HOST_USER,
            [student.Email],
            fail_silently=False
        )

        return redirect('add_result')
    if request.method == "POST":
        class_id = request.POST.get('class')
        student_id = request.POST.get('student')

        #  DELETE OLD RESULT FIRST 
        ResultDb.objects.filter(Class_id=class_id, Student_id=student_id).delete()

        #  SAVE NEW RESULT
        for key, value in request.POST.items():
            if key.startswith("mark_") and value != "":
                subject_id = key.split("_")[1]

                ResultDb.objects.create(
                    Class_id=class_id,
                    Student_id=student_id,
                    Subject_id=subject_id,
                    Marks=value
                )

        return redirect('add_result')



def manage_result(request):
    class_id = request.GET.get('class')
    classes = ClassDb.objects.all()

    grouped = []
    subjects = []

    if class_id:

        subjects = SubjectCombinationDb.objects.filter(
            Class_Section_id=class_id
        ).select_related('Subject_Name')

        subject_list = [s.Subject_Name for s in subjects]

        results = ResultDb.objects.select_related(
            'Class', 'Student', 'Subject'
        ).filter(Class_id=class_id)

        temp = defaultdict(lambda: {
            'class': None,
            'student': None,
            'marks': {},
            'total': 0,
            'status': 'PASS'
        })

        for r in results:

            student = temp[r.Student.id]

            student['class'] = r.Class
            student['student'] = r.Student
            student['marks'][r.Subject.id] = r.Marks
            student['total'] += r.Marks

            #FAIL CONDITION
            if r.Marks < 40:
                student['status'] = 'FAIL'

        grouped = temp.values()

    context = {
        'grouped_results': grouped,
        'subjects': subject_list if class_id else [],
        'classes': classes,
        'selected_class': class_id
    }

    return render(request, 'Manage_Result.html', context)
    class_id = request.GET.get('class')
    classes = ClassDb.objects.all()

    grouped = []
    subjects = []

    if class_id:
        # 🔥 Get subjects only for selected class
        subjects = SubjectCombinationDb.objects.filter(
            Class_Section_id=class_id
        ).select_related('Subject_Name')

        subject_list = [s.Subject_Name for s in subjects]

        results = ResultDb.objects.select_related(
            'Class', 'Student', 'Subject'
        ).filter(Class_id=class_id)

        temp = defaultdict(lambda: {
            'class': None,
            'student': None,
            'marks': {},
            'total': 0
        })

        for r in results:
            temp[r.Student.id]['class'] = r.Class
            temp[r.Student.id]['student'] = r.Student
            temp[r.Student.id]['marks'][r.Subject.id] = r.Marks
            temp[r.Student.id]['total'] += r.Marks

        grouped = temp.values()

    context = {
        'grouped_results': grouped,
        'subjects': subject_list if class_id else [],
        'classes': classes,
        'selected_class': class_id
    }

    return render(request, 'Manage_Result.html', context)
def delete_result(request, student_id, class_id):
    ResultDb.objects.filter(Student_id=student_id, Class_id=class_id).delete()
    messages.success(request, "Result deleted successfully!")
    return redirect(f'/manage/manage_result/?class={class_id}')
def edit_result(request, student_id, class_id):

    student = StudentDb.objects.get(id=student_id)
    class_obj = ClassDb.objects.get(id=class_id)

    subjects = SubjectCombinationDb.objects.filter(Class_Section_id=class_id)

    results = ResultDb.objects.filter(Student=student)

    marks = {}

    for r in results:
        marks[r.Subject.id] = r.Marks

    context = {
        'student': student,
        'class': class_obj,
        'subjects': subjects,
        'marks': marks
    }

    return render(request,'Edit_Result.html',context)
def update_result(request, student_id, class_id):

    student = StudentDb.objects.get(id=student_id)

    subjects = SubjectCombinationDb.objects.filter(Class_Section_id=class_id)

    for sub in subjects:

        mark = request.POST.get(f'mark_{sub.Subject_Name.id}')

        result = ResultDb.objects.get(Student=student, Subject=sub.Subject_Name)

        result.Mark = mark
        result.save()

    return redirect('manage_results')

    if request.method=='POST':
        old_passord=request.POST.get('oldpassword')
        new_password=request.POST.get('newpassword')
        confirm_password=request.POST.get('confirmpassword')
        if newpassword != confirmpassword:
            messages.error(request,"Password doesn't match")
        user=authenticate(username=request.user.username,password=oldpassword)
        if user is not None:
            user.set_password(new_password)
            user.save()
            messages.success(request,"Password changed successfully")
            return redirect(login)
        else:
            return redirect(change_password)
    return render(request,'Change_Password.html')
def payment(request):
    arrear_payments = ArrearApplication.objects.all().order_by('-Created_At')
    return render(request,'Payments.html',{'arrear_payments':arrear_payments})

def add_note(request):
    return render(request,'Add_Note.html')

    if request.method=='POST':
        Subject=request.POST.get('subject')
        Semester=request.POST.get('semester')
        Department=request.POST.get('department')
        Note=request.FILES.get('note')
        obj=NotesDb(Subject=Subject,Semester=Semester,Department=Department,Note=Note)
        obj.save()
        
        return redirect('add_note')
    
def save_note(request):
    if request.method == 'POST':

        subject = request.POST.get('subject')
        semester = request.POST.get('semester')
        department = request.POST.get('department')
        note = request.FILES.get('note')

        obj = NotesDb(
            Subject=subject,
            Semester=semester,
            Department=department,
            Notes=note
        )

        obj.save()

        return redirect('add_note')
def manage_notes(request):
    notes = NotesDb.objects.all()
    return render(request, 'Manage_Notes.html', {'notes': notes})
def delete_note(request, note_id):
    note = NotesDb.objects.get(id=note_id)
    note.delete()
    return redirect('manage_notes')
def edit_note(request, note_id):
    note = NotesDb.objects.get(id=note_id)
    return render(request, 'Edit_Notes.html', {'note': note})
def update_note(request, note_id):
    note = NotesDb.objects.get(id=note_id)
    note.Subject = request.POST.get('subject')
    note.Semester = request.POST.get('semester')
    note.Department = request.POST.get('department')
    note.Notes = request.FILES.get('note')
    note.save()
    return redirect('manage_notes')


def student_chat(request):

    if request.method == "POST":
        chat_id = request.POST.get("chat_id")
        reply = request.POST.get("reply")

        chat = ChatMessage.objects.get(id=chat_id)
        chat.reply = reply
        chat.save()

    chats = ChatMessage.objects.all().order_by("-created_at")

    return render(request, "Admin_Chat.html", {"chats": chats})
def admin_chat(request):

    if request.method == "POST":
        chat_id = request.POST.get("chat_id")
        reply = request.POST.get("reply")

        chat = ChatMessage.objects.get(id=chat_id)
        chat.reply = reply
        chat.save()

    chats = ChatMessage.objects.all().order_by("-created_at")

    return render(request,"Admin_Chat.html",{"chats":chats})
def delete_chat(request, id):
    chat = ChatMessage.objects.get(id=id)
    chat.delete()
    return redirect('student_chat')