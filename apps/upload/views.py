from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import CsvModelForm
from .models import Csv
import pandas as pd
import numpy as np
from apps.utils import count_het_hom, required, allowed_users
from apps.search.models import GeneStorage
from datetime import datetime
import traceback
# Create your views here.


@login_required(login_url='/login')
@allowed_users(allowed_roles=['compute'])
def upload_file(request):
    form = CsvModelForm(request.POST or None, request.FILES or None)
    is_csv = False
    is_excel = False
    context = {
        'segment': 'upload',
        'form': form
    }
    start = datetime.now()
    if form.is_valid():
        context['post'] = True
        form.save()
        form = CsvModelForm()
        obj = Csv.objects.get(activated=False)

        if (obj.file_name.path).endswith('.csv'):
            is_csv = True
        if (obj.file_name.path).endswith('.xlsx') or (obj.file_name.path).endswith('.xls'):
            is_excel = True
        
        # populate the database
        
        try:
            if is_csv:
                df1 = pd.read_csv(obj.file_name.path, low_memory=False)
            elif is_excel:
                df1 = pd.read_excel(obj.file_name.path, low_memory=False)

            name = obj.file_name.path.split('/')[-1]
            df1.dropna(how='all', axis=1, inplace=True)
            df1.drop(df1.columns.difference(required), axis=1, inplace=True)
            df1.columns = df1.columns.str.replace(' ', '_')
            df1['filename'] = [name] * len(df1)


            # TODO: get all objects from the database
            gene_already = GeneStorage.objects.all().values()
            df_old = pd.DataFrame(gene_already)
            print(df_old)
            print(df1)
            df = pd.concat([df_old, df1])

            grouped = df.groupby(['chromosome', 'start_pos', 'end_pos',
                                  'observed']).agg(lambda x: x.tolist())

            df = count_het_hom(grouped)  # FIXME: slow and main bottleneck
            all_columns = list(df)  # Creates list of all column headers

            df[all_columns] = df[all_columns].astype(str)
            dff = df.replace("'", "", regex=True).replace("\[", "", regex=True).replace("\]", "", regex=True).replace("\,", ";", regex=True)
            print("After replace")
            print(dff)
            convert_dict = {'count_hom': float,
                            'count_het': float,
                            }
            dff = dff.astype(convert_dict)

            dff['count_het'].fillna(0, inplace=True)
            dff['count_hom'].fillna(0, inplace=True)
            dff['count_total'] = dff['count_hom'] + dff['count_het']


            dff['files_uploaded'] = [len(dff['filename'].unique())] * len(dff)
            dff['New_allele_frequency'] = (dff['count_het'] + 2*dff['count_hom']) / (dff['files_uploaded'] * 2)


            dff = dff.reset_index()
            print(dff)
            print(dff.info())
            # TODO: check if file name exists in database:

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
                refGene_exonic_function=record.get("refGene_exonic_function", None),
                AC=record.get("AC", None),
                AC_hom=record.get("AC_hom", None),
                aug_all=record.get("1000g2015aug_all", None),
                ExAC_ALL=record.get("ExAC_ALL", None),
                gnomAD_exome_AF=record.get("gnomAD_exome_AF", None),
                Kaviar_AF=record.get("Kaviar_AF", None),
                SIFT_pred_41a=record.get("SIFT_pred_41a", None),
                SIFT4G_pred_41a=record.get("SIFT4G_pred_41a", None),
                Polyphen2_HDIV_pred_41a=record.get("Polyphen2_HDIV_pred_41a", None),
                Polyphen2_HVAR_pred_41a=record.get("Polyphen2_HVAR_pred_41a", None),
                CADD_phred_41a=record.get("CADD_phred_41a", None),
                CLNSIG=record.get("CLNSIG", None),
                filename=record['filename'],
                count_hom=record["count_hom"],
                count_het=record["count_het"],
                count_total=record['count_total'],
                files_uploaded=record['files_uploaded'],
                New_allele_frequency=record['New_allele_frequency']
            ) for record in dff.to_dict('records')]

            GeneStorage.objects.all().delete()
            GeneStorage.objects.bulk_create(rows)
            
            # After sucessfully populating 
            context['message'] = 'File was uploaded sucessfully.'
            context['color'] = 2
        except Exception:
            traceback.print_exc()
            context['message'] = 'An Error occured while processing the file, please make sure the file format is correct and it contains all required columns.'
            context['color'] = 4
        obj.activated = True
        obj.save()
    end = datetime.now()
    print(end - start)
    return render(request, 'home/upload.html', context)


@login_required(login_url='/login')
@allowed_users(allowed_roles=['compute'])
def compute(request):
    context = {
        'segment': 'compute',
    }

    result = GeneStorage.objects.all().values()
    df = pd.DataFrame(result)
    try:
        df = df[['chromosome', 'start_pos', 'end_pos', 'observed', 'refGene_gene', 'zygosity',
                'filename', 'count_hom', 'count_het', 'files_uploaded', 'New_allele_frequency']]

        convert_dict = {'count_hom': int,
                    'count_het': int,
                    'files_uploaded': int,
                    'New_allele_frequency': int,
                    }

        df = df.astype(convert_dict)
        df = df.sample(8)
        context['df_header'] = list(df.columns)
        context['df'] = df.to_dict('records')
    except Exception:
        traceback.print_exc()
    

    return render(request, 'home/compute.html', context)
