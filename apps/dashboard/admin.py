from django.contrib import admin
from .models import DashboardReport, DashboardMetric


@admin.register(DashboardReport)
class DashboardReportAdmin(admin.ModelAdmin):
    list_display = ['name', 'report_type', 'account', 'date_range', 'created_at']
    search_fields = ['name']
    list_filter = ['report_type', 'account', 'created_at']


@admin.register(DashboardMetric)
class DashboardMetricAdmin(admin.ModelAdmin):
    list_display = ['metric_name', 'account', 'metric_value', 'date']
    search_fields = ['metric_name']
    list_filter = ['account', 'date']
    date_hierarchy = 'date'
