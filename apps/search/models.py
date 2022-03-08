from django.db import models

# Create your models here.


class GeneStorage(models.Model):
    id = models.AutoField(primary_key=True)
    chromosome = models.CharField(max_length=100)
    start_pos = models.CharField(max_length=100)
    end_pos = models.CharField(max_length=100)
    reference = models.CharField(max_length=100)
    observed = models.CharField(max_length=100)
    zygosity = models.CharField(max_length=100)
    refGene_function = models.CharField(max_length=100)
    refGene_gene = models.CharField(max_length=100)
    refGene_exonic_function = models.CharField(max_length=100)
    AC = models.CharField(max_length=100)
    AC_hom = models.CharField(max_length=100)
    aug_all = models.CharField(max_length=100)
    ExAC_ALL = models.CharField(max_length=100)
    gnomAD_exome_AF = models.CharField(max_length=100)
    Kaviar_AF = models.CharField(max_length=100)
    SIFT_pred_41a = models.CharField(max_length=100)
    SIFT4G_pred_41a = models.CharField(max_length=100)
    Polyphen2_HDIV_pred_41a = models.CharField(max_length=100)
    Polyphen2_HVAR_pred_41a = models.CharField(max_length=100)
    CADD_phred_41a = models.CharField(max_length=100)
    CLNSIG = models.CharField(max_length=100)
    count_hom = models.CharField(max_length=100)
    count_het = models.CharField(max_length=100)
