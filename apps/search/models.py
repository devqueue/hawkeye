from django.db import models

# Create your models here.


class GeneStorage(models.Model):
    id = models.AutoField(primary_key=True)
    chromosome = models.CharField(max_length=100, default=None)
    start_pos = models.CharField(max_length=100, default=None)
    end_pos = models.CharField(max_length=100, default=None)
    reference = models.CharField(max_length=100, default=None)
    observed = models.CharField(max_length=100, default=None, null=True, blank=True)
    zygosity = models.CharField(max_length=100, default=None)
    refGene_function = models.CharField(max_length=100, default=None, null=True, blank=True)
    refGene_gene = models.CharField(max_length=100, default=None)
    refGene_exonic_function = models.CharField(max_length=100, default=None, null=True, blank=True)
    AC = models.CharField(max_length=100, default=None, null=True, blank=True)
    AC_hom = models.CharField(max_length=100, default=None, null=True, blank=True)
    aug_all = models.CharField(max_length=100, default=None, null=True, blank=True)
    ExAC_ALL = models.CharField(max_length=100, default=None, null=True, blank=True)
    gnomAD_exome_AF = models.CharField(max_length=100, default=None, null=True, blank=True)
    Kaviar_AF = models.CharField(max_length=100, default=None, null=True, blank=True)
    SIFT_pred_41a = models.CharField(max_length=100, default=None, null=True, blank=True)
    SIFT4G_pred_41a = models.CharField(max_length=100, default=None, null=True, blank=True)
    Polyphen2_HDIV_pred_41a = models.CharField(max_length=100, default=None, null=True, blank=True)
    Polyphen2_HVAR_pred_41a = models.CharField(max_length=100, default=None, null=True, blank=True)
    CADD_phred_41a = models.CharField(max_length=100, default=None, null=True, blank=True)
    CLNSIG = models.CharField(max_length=100, default=None, null=True, blank=True)
    filename = models.CharField(max_length=100, default=None, null=True, blank=True)
    count_hom = models.CharField(max_length=100, default=None, null=True, blank=True)
    count_het = models.CharField(max_length=100, default=None, null=True, blank=True)
