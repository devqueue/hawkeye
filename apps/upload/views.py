from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from core.settings import UPLOAD_PATH
from .forms import CsvModelForm
import pandas as pd
from apps.utils import required, allowed_users
from apps.search.models import Attandance, Student, Course
from datetime import datetime
import traceback
import os
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

            
            # test = df1[['PRN', 'Roll No', 'Name', 'Branch']]

            # check of the same file exists in the file system.
            os.makedirs(UPLOAD_PATH, exist_ok=True)
            file_list = [i for i in os.listdir(UPLOAD_PATH) if i.endswith('.csv')]


            if str(file_name) in file_list:
                context['icon'] = 'error'
                context['Title'] = 'Error'
                context['Text'] = 'File already exists. Please upload a new file'
                return render(request, 'home/upload.html', context)
            else:
                # After sucessfully uploading
                # TODO: Create the attandance objects
                rows = [Student(PRN=record['PRN No'],
                Name=record['Candidate Name'],
                Roll=record['Roll No'],
                Year=record['Class'],
                Division=record['Division']

                ) for record in df1.to_dict('records')]

                try:
                    Student.objects.bulk_create(rows)
                except:
                    Student.objects.bulk_update(rows, fields=['Roll', 'Name', 'Year', 'Division'])

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





@login_required(login_url='/login')
@allowed_users(allowed_roles=['compute'])
def compute(request):
    context = {
        'segment': 'compute',
    }
    if request.method == 'POST':
        start = datetime.now()
        context['post'] = True
        file_list = [os.path.join(UPLOAD_PATH, i)
                    for i in os.listdir(UPLOAD_PATH) if i.endswith('.csv')]
        df_list = []
        try:
            for file in file_list:
                headers = pd.read_csv(file, nrows=0).columns.tolist()
                req = set(headers) & set(required)
                df = pd.read_csv(file, usecols=req, low_memory=False)
                df['filename'] = [file.split('/')[-1]] * len(df)
                df_list.append(df)

            frame = pd.concat(df_list, axis=0, ignore_index=True)


            # def processing(frame):
            frame.columns = frame.columns.str.replace(' ', '_')
            grouped = frame.groupby(['chromosome', 'start_pos', 'end_pos',
                                    'observed']).agg(lambda x: x.tolist())

            grouped = grouped.astype(str).replace(
                "'", "", regex=True).replace("\[", "", regex=True).replace("\]", "", regex=True).replace("\,", ";", regex=True)


            grouped['count_hom'] = grouped['zygosity'].apply(lambda x: x.count('hom'))
            grouped['count_het'] = grouped['zygosity'].apply(lambda x: x.count('het'))

            grouped['count_total'] = grouped['count_het'] + grouped['count_hom']
            grouped['files_uploaded'] = [len(df_list)] * len(grouped)
            grouped['New_allele_frequency'] = (grouped['count_het'] + 2*grouped['count_hom']) / (grouped['files_uploaded'] * 2)

            dtypes = {
                'count_het': 'int16',
                'count_hom': 'int16',
                'count_total': 'int16',
                'files_uploaded': 'int16',
                'New_allele_frequency': 'float32',
            }
            grouped = grouped.astype(dtypes)
            grouped = grouped.reset_index()

            rows = [GeneStorage(
                    # id=record[" "],
                    chromosome=record["chromosome"],
                    start_pos=record["start_pos"],
                    end_pos=record["end_pos"],
                    reference=record["reference"],
                    observed=record["observed"],
                    zygosity=record["zygosity"],
                    refGene_function=record.get("refGene_function", None),
                    refGene_gene=record["refGene_gene"],
                    quality=record.get('quality', None),
                    refGene_exonic_function=record.get(
                        "refGene_exonic_function", None),
                    AC=record.get("AC", None),
                    AC_hom=record.get("AC_hom", None),
                    aug_all=record.get("1000g2015aug_all", None),
                    ExAC_ALL=record.get("ExAC_ALL", None),
                    gnomAD_exome_AF=record.get("gnomAD_exome_AF", None),
                    Kaviar_AF=record.get("Kaviar_AF", None),
                    SIFT_pred_41a=record.get("SIFT_pred_41a", None),
                    SIFT4G_pred_41a=record.get("SIFT4G_pred_41a", None),
                    Polyphen2_HDIV_pred_41a=record.get(
                        "Polyphen2_HDIV_pred_41a", None),
                    Polyphen2_HVAR_pred_41a=record.get(
                        "Polyphen2_HVAR_pred_41a", None),
                    CADD_phred_41a=record.get("CADD_phred_41a", None),
                    CLNSIG=record.get("CLNSIG", None),
                    filename=record['filename'],
                    count_hom=record["count_hom"],
                    count_het=record["count_het"],
                    count_total=record['count_total'],
                    files_uploaded=record['files_uploaded'],
                    New_allele_frequency=record['New_allele_frequency']
                    ) for record in grouped.to_dict('records')]

            GeneStorage.objects.all().delete()
            GeneStorage.objects.bulk_create(rows)
            context['message'] = 'All files were processed sucessfully.'
            context['color'] = 2
        except Exception:
            traceback.print_exc()
            context['message'] = 'An Error occured while processing the file, please check the logs'
            context['color'] = 4
        end = datetime.now()
        print(end - start)
        return render(request, 'home/compute.html', context)

    else:  
        result = GeneStorage.objects.all().values()
        df = pd.DataFrame(result)
        try:
            df = df[['chromosome', 'start_pos', 'end_pos', 'observed', 'zygosity',
                    'filename', 'count_hom', 'count_het', 'files_uploaded', 'New_allele_frequency']]

            df = df.sample(5)
            context['df_header'] = list(df.columns)
            context['df'] = df.to_dict('records')
        except Exception:
            traceback.print_exc()
        

        return render(request, 'home/compute.html', context)
