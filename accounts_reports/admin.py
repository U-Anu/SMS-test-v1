from django.contrib import admin
from .models import *
# Register your models here.
class ReportmappingAdmin(admin.ModelAdmin):
    list_display = ['name','report_type','asset_catogery','asset_type','glline']
class PL_ReportmappingAdmin(admin.ModelAdmin):
    list_display = ['name','report_type','asset_catogery','glline']
admin.site.register(ReportType)
admin.site.register(PL_Catogary)
admin.site.register(Calculationmapping)
admin.site.register(PL_Calculationmapping)
admin.site.register(Reportmapping,ReportmappingAdmin)
admin.site.register(PL_Reportmapping,PL_ReportmappingAdmin)
