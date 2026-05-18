from rest_framework import serializers
from .models import DashboardReport, DashboardMetric


class DashboardReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = DashboardReport
        fields = ['id', 'name', 'report_type', 'description', 'filters', 'date_range', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class DashboardMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = DashboardMetric
        fields = ['id', 'metric_name', 'metric_value', 'metadata', 'date']
        read_only_fields = ['id']
