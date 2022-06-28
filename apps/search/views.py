from wsgiref.util import request_uri
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Attandance, Student, Course
from .serializers import AttandanceSerializer
import pandas as pd
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
# Create your views here.


@login_required(login_url='accounts/login_user')
def search_gene(request):
    context = {
        'segment': 'Info-search',
        
    }
    course_set = Course.objects.all().values()
    courses = [i['Code'] for i in course_set]

    student_set = Student.objects.all().values()
    years = set([i['Year'] for i in student_set])
    Division = list(set([i['Division'] for i in student_set]))
    Division = list(sorted(Division))

    context['courses'] = courses
    context['years'] = years
    context['divisions'] = Division


    if request.method == 'POST':
        try:
            course = request.POST.get("course")
            year = request.POST.get("Year")
            division = request.POST.get('division')
            
            export = request.POST.get('export')

            context['sel_course'] = course
            context['sel_year'] = year
            context['sel_division'] = division

            result = Attandance.objects.filter(course=course).values()
            student = Student.objects.all().values()

            df = pd.DataFrame(list(result))
            df_stud = pd.DataFrame(list(student))

            df_joined = df.merge(df_stud, left_on='Student_id', right_on='PRN')

            if division:
                df_joined = df_joined[(df_joined['Division'] == division)]
            if year:
                df_joined = df_joined[ (df_joined['Year'] == year)]

            context['df'] = df_joined.to_dict('records')
            context['df_header'] = list(df_joined.columns)

            if export:
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = f'attachment; filename=exported.csv'
                
                df_joined.to_csv(path_or_buf=response, index=False)
                return response

            return render(request, 'labs/index.html', context)

        except Exception as e:
            print('[ERROR]:', e)

            return render(request, 'labs/index.html', context)
    else:
        return render(request, 'labs/index.html', context)


@api_view(['GET', 'POST'])
def postdata_api(request):

    if request.method == 'GET':
        attandances = Attandance.objects.all()
        serializer = AttandanceSerializer(attandances, many=True)

        return JsonResponse({"Data": serializer.data})

    if request.method == 'POST':
        serializer = AttandanceSerializer(data=request.data)
        print(serializer.initial_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response("BAD REQUEST", status=status.HTTP_400_BAD_REQUEST)
        