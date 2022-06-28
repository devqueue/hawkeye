from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import CsvModelForm
import pandas as pd
from apps.utils import required, allowed_users
from apps.search.models import Attandance, Student, Course
import traceback
# Create your views here.


@login_required(login_url='/login')
@allowed_users(allowed_roles=['compute'])
def upload_file(request):
    form = CsvModelForm(request.POST or None, request.FILES or None)
    is_csv = False
    is_excel = False
    context = {
        'segment': 'Info-upload',
        'form': form
    }

    Type = request.POST.get("Type")
    print(Type)
    if form.is_valid():
        context['post'] = True
        file_name = form.cleaned_data.get('file_name')
        file_path = form.cleaned_data.get('file_name').temporary_file_path()

        if (str(file_name)).endswith('.csv'):
            is_csv = True
        if (str(file_name)).endswith('.xlsx') or (str(file_name)).endswith('.xls'):
            is_excel = True
        
        try:
            if is_csv:
                df1 = pd.read_csv(file_path)
            elif is_excel:
                df1 = pd.read_excel(file_path)

            # TODO: Create the attandance objects
            if Type == 'Student':

                Students = [Student(
                    PRN=record['PRN No'],
                    Name=record['Candidate Name'],
                    Roll=record['Roll No'],
                    Year=record['Class'],
                    Division=record['Division']
                ) for record in df1.to_dict('records')]

                for row in Students:
                    row.save()
                
            elif Type == 'Attendance':
                df1['Date'] = pd.to_datetime(df1['Date'])

                Attendance = [Attandance(
                    Student=Student.objects.get(Roll=record['Roll No']),
                    course=Course.objects.get(Name=record['Course']),
                    Day=record['Date'],
                    TimeSlot=record['TimeSlot'],
                    present=record['Attendance']
                ) for record in df1.to_dict('records')]

                for row in Attendance:
                    row.save()

            elif Type == 'Course':
                Courses = [Course(
                    Code=record['Course Code'],
                    Name=record['Course Name'],
                    Credit=record['Credit'],
                    Description=record['Description'],
                ) for record in df1.to_dict('records')]

                for row in Courses:
                    row.save()

            context['icon'] = 'success'
            context['Title'] = 'Success'
            context['Text'] = 'Your file has been uploaded sucessfully'
            form.cleaned_data['activated'] = True
            form.save()

        except Exception:
            traceback.print_exc()
            context['icon'] = 'error'
            context['Title'] = 'Error'
            context['Text'] = "Invalid file data. An error occured, please upload again"

    return render(request, 'labs/upload.html', context)



