from django.shortcuts import render
from .models import GeneStorage
import pandas as pd
# Create your views here.


# @login_required(login_url='accounts/login_user')
def search_gene(request):
    context = {
        'segment': 'search',
        'types': ['Chromosome', 'Gene'],
    }
    if request.method == 'POST':
        search = request.POST.get("search")
        select_type = request.POST.get("type")
        context['sel_type'] = select_type
        if select_type == 'Gene':
            result = GeneStorage.objects.filter(refGene_gene__contains=search).values()
        else:
            result = GeneStorage.objects.filter(chromosome=search).values()

        df = pd.DataFrame(list(result))
        df.dropna(how='all', axis=1, inplace=True)

        
        context['df'] = df.to_dict('records')
        context['df_header'] = list(df.columns)
        return render(request, 'home/search.html', context)
    else:
        context['sel_type'] = 'Chromosome'
        return render(request, 'home/search.html', context)
