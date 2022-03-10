from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import CsvModelForm
from .models import Csv
import pandas as pd
from apps.utils import count_het_hom, required
from apps.search.models import GeneStorage
# Create your views here.


@login_required(login_url='/login')
def upload_file(request):
    form = CsvModelForm(request.POST or None, request.FILES or None)
    is_csv = False
    is_excel = False
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

        if (obj.file_name.path).endswith('.csv'):
            is_csv = True
        if (obj.file_name.path).endswith('.xlsx') or (obj.file_name.path).endswith('.xls'):
            is_excel = True
        # populate the database
        try:
            if is_csv:
                df = pd.read_csv(obj.file_name.path, low_memory=False)
            elif is_excel:
                df = pd.read_excel(obj.file_name.path, low_memory=False)

            name = obj.file_name.path.split('/')[-1]
            df.dropna(how='all', axis=1, inplace=True)
            df.drop(df.columns.difference(required), axis=1, inplace=True)
            df['filename'] = [name] * len(df)
            grouped = df.groupby(['chromosome', 'start pos', 'end pos',
                                    'reference']).agg(lambda x: x.tolist())

            df = count_het_hom(grouped)  # FIXME: slow and main bottleneck
            all_columns = list(df)  # Creates list of all column headers
            df[all_columns] = df[all_columns].astype(str)
            dff = df[df.columns.difference(['count_hom', 'count_het'])].replace("'", "", regex=True).replace("\[", "", regex=True).replace("\]", "", regex=True)
            dff["count_hom"] = df['count_hom']
            dff["count_het"] = df['count_het']
            
            dff = dff.reset_index()

            rows = [GeneStorage(
                # id=record[" "],
                chromosome=record["chromosome"],
                start_pos=record["start pos"],
                end_pos=record["end pos"],
                reference=record["reference"],
                observed=record["observed"],
                zygosity=record["zygosity"],
                refGene_function=record.get("refGene function", None),
                refGene_gene=record["refGene gene"],
                refGene_exonic_function=record.get("refGene exonic function", None),
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
                count_het=record["count_het"]
            )for record in dff.to_dict('records')]
            try:
                GeneStorage.objects.bulk_create(rows)
            except:
                context['message'] = 'Could not populate the database, data already exists'
                context["color"] = 4
                return render(request, 'home/upload.html', context)

            # After sucessfully populating 
            context['message'] = 'File was uploaded sucessfully.'
            context['color'] = 2
        except:
            context['message'] = 'An Error occured while processing the file, please make sure the file format is correct and it contains all required columns.'
            context['color'] = 4
        obj.activated = True
        obj.save()
    return render(request, 'home/upload.html', context)
