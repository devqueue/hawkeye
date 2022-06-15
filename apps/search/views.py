from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Attandance, Student, Course
import pandas as pd
from django.http import HttpResponse
from apps.utils import allowed_users
# Create your views here.


@login_required(login_url='accounts/login_user')
@allowed_users(allowed_roles=['compute', 'search'])
def search_gene(request):
    context = {
        'segment': 'Info-search',
        
    }
    course_set = Course.objects.all().values()
    courses = [i['Code'] for i in course_set]

    student_set = Student.objects.all().values()
    print(student_set)
    years = set([i['Year'] for i in student_set])
    Division = set([i['Division'] for i in student_set])

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

