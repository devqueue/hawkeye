import numpy as np
from django.http import HttpResponse
from django.shortcuts import redirect, render


def unauthenticated_user(view_func):
	def wrapper_func(request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect('search')
		else:
			return view_func(request, *args, **kwargs)

	return wrapper_func


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            group = request.user.groups.all()
            
            if (any(item == str(gr) for gr in group for item in allowed_roles)) or request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            else:
                return render(request, 'home/page-403.html', )
        return wrapper_func
    return decorator



def count_het_hom(grouped):
    for index in grouped.index:
        if len(grouped.loc[index]['zygosity']) == 1:
            if grouped.loc[index]['zygosity'][0] == 'het':
                grouped.at[index, 'count_het'] = 1
            if grouped.loc[index]['zygosity'][0] == 'hom':
                grouped.at[index, 'count_hom'] = 1
        else:
            length = len(grouped.loc[index]['zygosity'])
            for i in range(length):
                if grouped.loc[index]['zygosity'][i] == 'hom':
                    grouped.at[index, 'count_hom'] = int(np.nan_to_num(
                        grouped.at[index, 'count_hom']) + 1)
                elif grouped.loc[index]['zygosity'][i] == 'het':
                    grouped.at[index, 'count_het'] = int(np.nan_to_num(
                        grouped.at[index, 'count_het']) + 1)
    return grouped


required = ["chromosome",
            "start pos",
            "end pos",
            "reference",
            "observed",
            "zygosity",
            "quality",
            "refGene function",
            "refGene gene",
            "refGene_exonic_function",
            "AC",
            "AC_hom",
            "1000g2015aug_all",
            "ExAC_ALL",
            "gnomAD_exome_AF",
            "Kaviar_AF",
            "SIFT_pred_41a",
            "SIFT4G_pred_41a",
            "Polyphen2_HDIV_pred_41a",
            "Polyphen2_HVAR_pred_41a",
            "CADD_phred_41a",
            "CLNSIG",
            "count hom",
            "count het"]
