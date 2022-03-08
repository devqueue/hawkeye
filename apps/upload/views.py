from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import CsvModelForm
from .models import Csv
import pandas as pd
from apps.search.models import GeneStorage
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

        # TODO: populate the database
        try:
            df = pd.read_excel(obj.file_name.path)

            rows = [GeneStorage(
                # id=record[" "],
                chromosome=record["chromosome"],
                start_pos=record["start pos"],
                end_pos=record["end pos"],
                reference=record["reference"],
                observed=record["observed"],
                zygosity=record["zygosity"],
                refGene_function=record["refGene function"],
                refGene_gene=record["refGene gene"],
                refGene_exonic_function=record["refGene exonic function"],
                AC=record["AC"],
                AC_hom=record["AC_hom"],
                aug_all=record["1000g2015aug_all"],
                ExAC_ALL=record["ExAC_ALL"],
                gnomAD_exome_AF=record["gnomAD_exome_AF"],
                Kaviar_AF=record["Kaviar_AF"],
                SIFT_pred_41a=record["SIFT_pred_41a"],
                SIFT4G_pred_41a=record["SIFT4G_pred_41a"],
                Polyphen2_HDIV_pred_41a=record["Polyphen2_HDIV_pred_41a"],
                Polyphen2_HVAR_pred_41a=record["Polyphen2_HVAR_pred_41a"],
                CADD_phred_41a=record["CADD_phred_41a"],
                CLNSIG=record["CLNSIG"],
                count_hom=record["count hom"],
                count_het=record["count het"]
            )for record in df.to_dict('records')]
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
