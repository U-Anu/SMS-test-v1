from django.db import models
# from pesanile_accounting import models

# Create your models here.
class ReportType(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255)
    def __str__(self):
        return self.name
    
class PL_Catogary(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255)
    def __str__(self):
        return self.name
    
class Reportmapping(models.Model):
    name = models.CharField(max_length=255, unique=False,null=True,blank=True)
    report_type = models.ForeignKey(ReportType,on_delete=models.CASCADE, related_name='report_type_category')
    asset_catogery = models.ForeignKey('pesanile_accounting.AssetTypeCategory',on_delete=models.CASCADE,null=True,blank=True, related_name='AssetType_Category')
    asset_type= models.ForeignKey('pesanile_accounting.AssetType',on_delete=models.CASCADE,null=True,blank=True,related_name='assect_types')
    glline = models.ForeignKey('pesanile_accounting.GLLine',on_delete=models.CASCADE, related_name='gllines_name')
    
    def __str__(self):
        return str(self.report_type)
    
    
class PL_Reportmapping(models.Model):
    name = models.CharField(max_length=255, unique=False,null=True,blank=True)
    report_type = models.ForeignKey(ReportType,on_delete=models.CASCADE, related_name='report_type_categoryss')
    asset_catogery = models.ForeignKey(PL_Catogary,on_delete=models.CASCADE,null=True,blank=True, related_name='AssetType_Categoryss')
    glline = models.ForeignKey('pesanile_accounting.GLLine',on_delete=models.CASCADE, related_name='gllines_namess')
    
    def __str__(self):
        return str(self.report_type)
    
class Calculationmapping(models.Model):
    S_no = models.IntegerField(unique=False,null=True,blank=True)
    report_type = models.ForeignKey(ReportType,on_delete=models.CASCADE, related_name='report_type_categorys')
    assect_catogery = models.ManyToManyField('pesanile_accounting.AssetTypeCategory',null=True,blank=True, related_name='AssetType_Categorys')
    
    def __str__(self):
        return str(self.report_type)
    
class PL_Calculationmapping(models.Model):
    name = models.CharField(max_length=255, unique=False,null=True,blank=True)
    Sequences_no = models.IntegerField(unique=False,null=True,blank=True)
    report_type = models.ForeignKey(ReportType,on_delete=models.CASCADE, related_name='report_type_categorysspss')
    assect_catogery = models.ManyToManyField(PL_Catogary,null=True,blank=True, related_name='AssetTypes_Categoryspss')
    output_positions = models.ForeignKey(PL_Catogary,null=True,on_delete=models.CASCADE,blank=True, related_name='AssetTypess_Categoryspsss')
    
    def __str__(self):
        return str(self.report_type)