from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
from import_export import resources

# Register your models here.
class ReportmappingAdmin(admin.ModelAdmin):
    list_display = ['name','report_type','asset_catogery','asset_type','glline']
class PL_ReportmappingAdmin(admin.ModelAdmin):
    list_display = ['name','report_type','asset_catogery','glline']
# admin.site.register(ReportType)
admin.site.register(Calculationmapping)
admin.site.register(PL_Calculationmapping)
admin.site.register(Reportmapping,ReportmappingAdmin)

class PL_ReportmappingResource(resources.ModelResource):
    class Meta:
        model = PL_Reportmapping
        import_id_fields = ['name']

@admin.register(PL_Reportmapping)
class PL_ReportmappingAdmin(ImportExportModelAdmin):
    resource_class = PL_ReportmappingResource
    list_display = ( 'name', 'report_type', 'asset_catogery', 'glline')
    list_filter = ( 'name', 'report_type', 'asset_catogery')

class PL_CatogaryResource(resources.ModelResource):
    class Meta:
        model = PL_Catogary
        import_id_fields = ['name']

@admin.register(PL_Catogary)
class PL_CatogaryAdmin(ImportExportModelAdmin):
    resource_class = PL_CatogaryResource
    list_display = ( 'name','description' )

class ReportTypeResource(resources.ModelResource):
    class Meta:
        model = ReportType
        import_id_fields = ['name']

@admin.register(ReportType)
class ReportTypeAdmin(ImportExportModelAdmin):
    resource_class = ReportTypeResource
    list_display = ( 'name','description' )
