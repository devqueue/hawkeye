from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import CsvModelForm
from .models import Csv
import pandas as pd
# Create your views here.


@login_required(login_url='/login')
def upload_file(request):
    form = CsvModelForm(request.POST or None, request.FILES or None)
    context = {
        'segment': 'upload',
        'form': form
    }
    if form.is_valid():
        context['post'] = True
        form.save()
        form = CsvModelForm()
        obj = Csv.objects.get(activated=False)
        obj = Csv.objects.get(activated=False)

        # populate the database
        df = pd.read_excel(obj.file_name.path)
        print(df)
        obj.activated = True
        obj.save()
        context['message'] = 'File was uploaded sucessfully.'
        return render(request, 'home/upload.html', context)

    else:
        return render(request, 'home/upload.html', context)
